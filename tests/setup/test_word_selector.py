# ************************************************
# Tests for: Word Selector
# ************************************************
import itertools
from unittest.mock import mock_open, patch

import pytest

from data.settings_details import DifficultyData, GridConfigData, WordsNeededData
from setup import word_selector


@pytest.fixture
def sample_settings():
    """Creates a sample DifficultyData object for tests."""
    # The lexicon_path is not part of DifficultyData, so we pass it separately in tests.
    return DifficultyData(
        grid=GridConfigData(height=10, width=10),
        words_on_board_needed=WordsNeededData(minimum=5, maximum=50),
        max_word_length=6,
        min_subword_length=3,
        heart_point_mode=True,
    )


@pytest.fixture
def simple_word_list():
    """Creates a simple list of words for filtering tests."""
    return ["a", "be", "cat", "nap", "ohhh", "nooo", "wahhh", "streak"]


@pytest.fixture
def streak_word_set():
    """Creates the specific set of words related to 'streak'. From the CS11 specs."""
    words_streak = "STREAK rat stare arks rate stark ear rest steak east sat take era sear takes erst seat tar est skate tears eta stake teas treks"
    return set(words_streak.lower().split())


# Tests for: read_word_file
def test_read_word_file_not_found():
    """Test read_word_file when the target file doesn't exist."""
    with (
        patch("setup.word_selector.open", side_effect=FileNotFoundError) as mock_open_func,
        patch("builtins.print") as mock_print,
    ):
        result = word_selector.read_word_file("non_existent_file.txt")
        assert result == []
        mock_open_func.assert_called_once_with("non_existent_file.txt", encoding="utf-8")
        mock_print.assert_called_once()
        assert "Error: File non_existent_file.txt not found." in mock_print.call_args[0][0]


def test_read_word_file_io_error():
    """Test read_word_file when an IOError occurs during reading."""
    with (
        patch("setup.word_selector.open", side_effect=OSError("Permission denied")) as mock_open_func,
        patch("builtins.print") as mock_print,
    ):
        result = word_selector.read_word_file("some_file.txt")
        assert result == []
        mock_open_func.assert_called_once_with("some_file.txt", encoding="utf-8")
        mock_print.assert_called_once()
        assert "Error reading file some_file.txt: Permission denied" in mock_print.call_args[0][0]


def test_read_word_file_empty():
    """Test read_word_file correctly handles an empty file."""
    with patch("builtins.open", mock_open(read_data="")) as mock_file:
        result = word_selector.read_word_file("empty.txt")
        assert result == []
        mock_file.assert_called_once_with("empty.txt", encoding="utf-8")


def test_read_word_file_valid():
    """Test read_word_file cleans and processes valid file content."""
    file_content = " Apple \nbanana\n\nCherry\n   \ndate "
    expected_result = ["apple", "banana", "cherry", "date"]
    with patch("builtins.open", mock_open(read_data=file_content)) as mock_file:
        result = word_selector.read_word_file("valid.txt")
        assert result == expected_result
        mock_file.assert_called_once_with("valid.txt", encoding="utf-8")


# Tests for: filter_exact_length_words
def test_filter_exact_length_words(simple_word_list):
    """Test filtering words to find only those of an exact length."""
    words = simple_word_list
    assert word_selector.filter_exact_length_words(words, 3) == ["cat", "nap"]
    assert word_selector.filter_exact_length_words(words, 5) == ["wahhh"]
    assert word_selector.filter_exact_length_words(words, 6) == ["streak"]
    assert word_selector.filter_exact_length_words(words, 7) == []


# Tests for: filter_words_up_to_max_length (Pure Function)
def test_filter_words_up_to_max_length(simple_word_list):
    """Test filtering words to find those up to a maximum length."""
    words = simple_word_list
    expected_max_3 = {"a", "be", "cat", "nap"}
    assert word_selector.filter_words_up_to_max_length(words, 3) == expected_max_3
    expected_max_5 = {"a", "be", "cat", "nap", "ohhh", "nooo", "wahhh"}
    assert word_selector.filter_words_up_to_max_length(words, 5) == expected_max_5
    expected_max_10 = {"a", "be", "cat", "nap", "ohhh", "nooo", "wahhh", "streak"}
    assert word_selector.filter_words_up_to_max_length(words, 10) == expected_max_10


# Tests for: get_valid_word_subwords
def test_get_valid_word_subwords_found(streak_word_set):
    """Test finding valid subwords from a given word and valid set."""
    word_to_check = "streak"
    valid_set = streak_word_set
    min_len = 3

    expected_subwords = set()
    for k in range(min_len, len(word_to_check)):
        for p in itertools.permutations(word_to_check, k):
            sub = "".join(p)
            if sub in valid_set:
                expected_subwords.add(sub)

    actual_subwords = word_selector.get_valid_word_subwords(
        word_to_check, valid_set, min_len,
    )

    assert set(actual_subwords) == expected_subwords
    assert word_to_check not in actual_subwords


def test_get_valid_word_subwords_none_found(streak_word_set):
    """Test case where no valid subwords are found."""
    word_to_check = "lmnop"
    valid_set = streak_word_set
    min_len = 3
    actual_subwords = word_selector.get_valid_word_subwords(
        word_to_check, valid_set, min_len,
    )
    assert actual_subwords == []


# Tests for: find_valid_word_with_subwords
@patch("setup.word_selector.get_valid_word_subwords")
@patch("setup.word_selector.random.shuffle")
def test_find_valid_word_with_subwords_success(
    mock_shuffle, mock_get_subwords, streak_word_set, sample_settings,
):
    """Test finding a middle word that meets the subword count requirement."""
    candidate_middle_words = ["helloo", "streak", "other"]
    valid_subword_set = streak_word_set
    min_subword_len = sample_settings.min_subword_length
    min_subwords_needed = sample_settings.words_on_board_needed.minimum

    def get_subwords_side_effect(word, valid_set, min_len):
        if word == "streak":
            return [
                "rat",
                "stare",
                "rate",
                "stark",
                "ear",
                "rest",
            ]
        elif word == "helloo":
            return ["only", "two"]
        else:
            return []

    mock_get_subwords.side_effect = get_subwords_side_effect

    middle_word, words_to_place = word_selector.find_valid_word_with_subwords(
        candidate_middle_words, min_subword_len, min_subwords_needed, valid_subword_set,
    )

    assert middle_word == "streak"
    assert len(words_to_place) >= (min_subwords_needed - 1)
    assert set(words_to_place) == {"rat", "stare", "rate", "stark", "ear", "rest"}
    mock_shuffle.assert_called_once_with(
        ["rat", "stare", "rate", "stark", "ear", "rest"],
    )


@patch("setup.word_selector.get_valid_word_subwords")
@patch("setup.word_selector.random.shuffle")
def test_find_valid_word_with_subwords_fail(
    mock_shuffle, mock_get_subwords, streak_word_set, sample_settings,
):
    """Test when no candidate middle word yields enough subwords."""
    candidate_middle_words = ["please", "letme", "sleepp"]
    valid_subword_set = streak_word_set
    min_subword_len = sample_settings.min_subword_length
    min_subwords_needed = sample_settings.words_on_board_needed.minimum

    mock_get_subwords.return_value = ["sub1", "sub2"]

    middle_word, words_to_place = word_selector.find_valid_word_with_subwords(
        candidate_middle_words, min_subword_len, min_subwords_needed, valid_subword_set,
    )

    assert middle_word is None
    assert words_to_place is None
    mock_shuffle.assert_not_called()


# Tests for: generate_word_list
# we'll check if the logic holds when running this function
@patch("setup.word_selector.read_word_file")
@patch("setup.word_selector.find_valid_word_with_subwords")
@patch("setup.word_selector.clear_screen")
@patch("setup.word_selector.print_message")
@patch("setup.word_selector.random.shuffle")
def test_generate_word_list_success(
    mock_rnd_shuffle_exact,
    mock_print,
    mock_clear,
    mock_find,
    mock_read,
    sample_settings,
    streak_word_set,
):
    """Test the main generate_word_list function successfully finds words."""
    settings = sample_settings  # DifficultyData
    lexicon_path = "dummy_lexicon.txt"

    mock_read.return_value = list(streak_word_set)
    expected_middle = "streak"
    expected_subs = ["rat", "stare", "rate", "stark", "ear"]
    mock_find.return_value = (expected_middle, expected_subs)

    actual_middle, actual_subs = word_selector.generate_word_list(settings, lexicon_path)

    assert actual_middle == expected_middle
    assert actual_subs == expected_subs

    mock_clear.assert_called_once()
    mock_print.assert_called_once()
    mock_read.assert_called_once_with(lexicon_path)
    mock_find.assert_called_once()

    args_find, _ = mock_find.call_args
    assert args_find[0] == ["streak"]
    assert args_find[1] == settings.min_subword_length
    assert args_find[2] == settings.words_on_board_needed.minimum
    expected_valid_set = word_selector.filter_words_up_to_max_length(
        streak_word_set, settings.max_word_length,
    )
    assert args_find[3] == expected_valid_set

    mock_rnd_shuffle_exact.assert_called_once_with(["streak"])


@patch("setup.word_selector.read_word_file")
@patch("setup.word_selector.clear_screen")
@patch("setup.word_selector.print_message")
def test_generate_word_list_read_fail(
    mock_print, mock_clear, mock_read, sample_settings,
):
    """Test generate_word_list when reading the lexicon fails."""
    settings = sample_settings
    lexicon_path = "dummy_lexicon.txt"
    mock_read.return_value = []

    actual_middle, actual_subs = word_selector.generate_word_list(settings, lexicon_path)

    assert actual_middle is None
    assert actual_subs is None
    mock_clear.assert_called_once()
    mock_print.assert_called_once()


@patch("setup.word_selector.read_word_file")
@patch("setup.word_selector.find_valid_word_with_subwords")
@patch("setup.word_selector.clear_screen")
@patch("setup.word_selector.print_message")
@patch("setup.word_selector.random.shuffle")
def test_generate_word_list_find_fail(
    mock_rnd_shuffle,
    mock_print,
    mock_clear,
    mock_find,
    mock_read,
    sample_settings,
    streak_word_set,
):
    """Test generate_word_list when finding a suitable middle word fails."""
    settings = sample_settings
    lexicon_path = "dummy_lexicon.txt"
    mock_read.return_value = list(streak_word_set)
    mock_find.return_value = (None, None)

    actual_middle, actual_subs = word_selector.generate_word_list(settings, lexicon_path)

    assert actual_middle is None
    assert actual_subs is None
    mock_clear.assert_called_once()
    mock_print.assert_called_once()
    mock_read.assert_called_once()
    mock_find.assert_called_once()
    mock_rnd_shuffle.assert_called_once()
