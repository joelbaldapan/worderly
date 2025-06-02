# ************************************************
# Tests for: Word Selector
# ************************************************
import itertools
from unittest.mock import mock_open, patch

import pytest

from data.settings_details import DifficultyData, GridConfigData, WordsNeededData
from setup import word_selector


@pytest.fixture
def sample_settings() -> DifficultyData:
    """Create a sample DifficultyData object for tests.

    Returns:
        DifficultyData: A sample settings object for testing.

    """
    return DifficultyData(
        grid=GridConfigData(height=10, width=10),
        words_on_board_needed=WordsNeededData(minimum=5, maximum=50),
        max_word_length=6,
        min_subword_length=3,
        heart_point_mode=True,
    )


@pytest.fixture
def simple_word_list() -> list[str]:
    """Create a simple list of words for filtering tests.

    Returns:
        list[str]: A list of sample words.

    """
    return ["a", "be", "cat", "nap", "ohhh", "nooo", "wahhh", "streak"]


@pytest.fixture
def streak_word_set() -> set[str]:
    """Create the specific set of words related to 'streak' from the CS11 specs.

    Returns:
        set[str]: Set of valid subwords for 'streak'.

    """
    words_streak = "STREAK rat stare arks rate stark ear rest steak east sat " \
    "take era sear takes erst seat tar est skate tears eta stake teas treks"
    return set(words_streak.lower().split())


def test_read_word_file_not_found() -> None:
    """Test that read_word_file returns [] and prints error when file is missing."""
    with (
        patch("setup.word_selector.open", side_effect=FileNotFoundError) as mock_open_func,
        patch("builtins.print") as mock_print,
    ):
        result = word_selector.read_word_file("non_existent_file.txt")
        assert result == []
        mock_open_func.assert_called_once_with("non_existent_file.txt", encoding="utf-8")
        mock_print.assert_called_once()
        assert "Error: File non_existent_file.txt not found." in mock_print.call_args[0][0]


def test_read_word_file_io_error() -> None:
    """Test that read_word_file returns [] and prints error on IOError."""
    with (
        patch("setup.word_selector.open", side_effect=OSError("Permission denied")) as mock_open_func,
        patch("builtins.print") as mock_print,
    ):
        result = word_selector.read_word_file("some_file.txt")
        assert result == []
        mock_open_func.assert_called_once_with("some_file.txt", encoding="utf-8")
        mock_print.assert_called_once()
        assert "Error reading file some_file.txt: Permission denied" in mock_print.call_args[0][0]


def test_read_word_file_empty() -> None:
    """Test that read_word_file returns [] for an empty file."""
    with patch("builtins.open", mock_open(read_data="")) as mock_file:
        result = word_selector.read_word_file("empty.txt")
        assert result == []
        mock_file.assert_called_once_with("empty.txt", encoding="utf-8")


def test_read_word_file_valid() -> None:
    """Test that read_word_file cleans and processes valid file content."""
    file_content = " Apple \nbanana\n\nCherry\n   \ndate "
    expected_result = ["apple", "banana", "cherry", "date"]
    with patch("builtins.open", mock_open(read_data=file_content)) as mock_file:
        result = word_selector.read_word_file("valid.txt")
        assert result == expected_result
        mock_file.assert_called_once_with("valid.txt", encoding="utf-8")


def test_filter_exact_length_words(simple_word_list: list[str]) -> None:
    """Filter words to find only those of an exact length."""
    words = simple_word_list
    assert word_selector.filter_exact_length_words(words, 3) == ["cat", "nap"]
    assert word_selector.filter_exact_length_words(words, 5) == ["wahhh"]
    assert word_selector.filter_exact_length_words(words, 6) == ["streak"]
    assert word_selector.filter_exact_length_words(words, 7) == []


def test_filter_words_up_to_max_length(simple_word_list: list[str]) -> None:
    """Filter words to find those up to a maximum length."""
    words = simple_word_list
    expected_max_3 = {"a", "be", "cat", "nap"}
    assert word_selector.filter_words_up_to_max_length(words, 3) == expected_max_3
    expected_max_5 = {"a", "be", "cat", "nap", "ohhh", "nooo", "wahhh"}
    assert word_selector.filter_words_up_to_max_length(words, 5) == expected_max_5
    expected_max_10 = {"a", "be", "cat", "nap", "ohhh", "nooo", "wahhh", "streak"}
    assert word_selector.filter_words_up_to_max_length(words, 10) == expected_max_10


def test_get_valid_word_subwords_found(
    streak_word_set: set[str],
) -> None:
    """Find valid subwords from a given word and valid set."""
    word_to_check = "streak"
    valid_set = streak_word_set
    min_len = 3

    expected_subwords: set[str] = set()
    for k in range(min_len, len(word_to_check)):
        for p in itertools.permutations(word_to_check, k):
            sub = "".join(p)
            if sub in valid_set:
                expected_subwords.add(sub)

    actual_subwords = word_selector.get_valid_word_subwords(
        word_to_check,
        valid_set,
        min_len,
    )

    assert set(actual_subwords) == expected_subwords
    assert word_to_check not in actual_subwords


def test_get_valid_word_subwords_none_found(
    streak_word_set: set[str],
) -> None:
    """Test that no valid subwords are found when none exist."""
    word_to_check = "lmnop"
    valid_set = streak_word_set
    min_len = 3
    actual_subwords = word_selector.get_valid_word_subwords(
        word_to_check,
        valid_set,
        min_len,
    )
    assert actual_subwords == []


@patch("setup.word_selector.get_valid_word_subwords")
@patch("setup.word_selector.random.shuffle")
def test_find_valid_word_with_subwords_success(
    mock_shuffle: object,
    mock_get_subwords: object,
    streak_word_set: set[str],
    sample_settings: DifficultyData,
) -> None:
    """Find a middle word that meets the subword count requirement."""
    candidate_middle_words: list[str] = ["helloo", "streak", "other"]
    valid_subword_set: set[str] = streak_word_set
    min_subword_len: int = sample_settings.min_subword_length
    min_subwords_needed: int = sample_settings.words_on_board_needed.minimum

    def get_subwords_side_effect(
        word: str,
        valid_set: set[str],
        min_len: int,
    ) -> list[str]:
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
        candidate_middle_words,
        min_subword_len,
        min_subwords_needed,
        valid_subword_set,
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
    mock_shuffle: object,
    mock_get_subwords: object,
    streak_word_set: set[str],
    sample_settings: DifficultyData,
) -> None:
    """Test that no candidate middle word yields enough subwords."""
    candidate_middle_words: list[str] = ["please", "letme", "sleepp"]
    valid_subword_set: set[str] = streak_word_set
    min_subword_len: int = sample_settings.min_subword_length
    min_subwords_needed: int = sample_settings.words_on_board_needed.minimum

    mock_get_subwords.return_value = ["sub1", "sub2"]

    middle_word, words_to_place = word_selector.find_valid_word_with_subwords(
        candidate_middle_words,
        min_subword_len,
        min_subwords_needed,
        valid_subword_set,
    )

    assert middle_word is None
    assert words_to_place is None
    mock_shuffle.assert_not_called()


@patch("setup.word_selector.read_word_file")
@patch("setup.word_selector.find_valid_word_with_subwords")
@patch("setup.word_selector.clear_screen")
@patch("setup.word_selector.print_message")
@patch("setup.word_selector.random.shuffle")
def test_generate_word_list_success(
    mock_rnd_shuffle_exact: object,
    mock_print: object,
    mock_clear: object,
    mock_find: object,
    mock_read: object,
    sample_settings: DifficultyData,
    streak_word_set: set[str],
) -> None:
    """Test that generate_word_list successfully finds words."""
    settings: DifficultyData = sample_settings
    lexicon_path: str = "dummy_lexicon.txt"

    mock_read.return_value = list(streak_word_set)
    expected_middle: str = "streak"
    expected_subs: list[str] = ["rat", "stare", "rate", "stark", "ear"]
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
        streak_word_set,
        settings.max_word_length,
    )
    assert args_find[3] == expected_valid_set

    mock_rnd_shuffle_exact.assert_called_once_with(["streak"])


@patch("setup.word_selector.read_word_file")
@patch("setup.word_selector.clear_screen")
@patch("setup.word_selector.print_message")
def test_generate_word_list_read_fail(
    mock_print: object,
    mock_clear: object,
    mock_read: object,
    sample_settings: DifficultyData,
) -> None:
    """Test that generate_word_list returns None when reading the lexicon fails."""
    settings: DifficultyData = sample_settings
    lexicon_path: str = "dummy_lexicon.txt"
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
    mock_rnd_shuffle: object,
    mock_print: object,
    mock_clear: object,
    mock_find: object,
    mock_read: object,
    sample_settings: DifficultyData,
    streak_word_set: set[str],
) -> None:
    """Test that generate_word_list returns None when finding a suitable middle word fails."""
    settings: DifficultyData = sample_settings
    lexicon_path: str = "dummy_lexicon.txt"
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
