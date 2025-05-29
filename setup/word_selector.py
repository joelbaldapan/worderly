# setup/word_selector.py
import itertools
import random

from data.settings_details import DifficultyData
from display.display import print_message
from display.display_utils import clear_screen


def read_word_file(word_path: str) -> list[str]:
    """Reads a lexicon file, cleans words, and returns them as a list."""
    try:
        with open(word_path, encoding="utf-8") as file:
            return [word.strip().lower() for word in file if word.strip()]
    except FileNotFoundError:
        print(f"Error: File {word_path} not found.")
        return []
    except OSError as e:
        print(f"Error reading file {word_path}: {e}")
        return []


def filter_exact_length_words(words: list[str], exact_length: int) -> list[str]:
    """Filters a list of words to include only those of a specific exact length."""
    return [word for word in words if len(word) == exact_length]


def filter_words_up_to_max_length(words: list[str], max_length: int) -> set[str]:
    """Filters a word list to include only words up to a maximum length, returning a set."""
    return {word for word in words if len(word) <= max_length}


def get_valid_word_subwords(word: str, valid_words_set: set[str], min_length: int) -> list[str]:
    """Finds all valid subwords/anagrams of a given word from a valid set."""
    valid_subwords: set[str] = set()
    for length in range(min_length, len(word) + 1):
        for p in itertools.permutations(word, length):
            subword = "".join(p)
            if subword in valid_words_set and subword != word:
                valid_subwords.add(subword)
    return list(valid_subwords)


def find_valid_word_with_subwords(
    exact_max_length_words: list[str],
    min_subword_length: int,
    min_subwords_needed: int,
    valid_subword_set: set[str],
) -> tuple[str | None, list[str] | None]:
    """Searches for a word of a specific length that has enough valid subwords."""
    actual_subwords_needed = min_subwords_needed - 1

    for chosen_word in exact_max_length_words:
        subwords = get_valid_word_subwords(chosen_word, valid_subword_set, min_subword_length)
        if len(subwords) >= actual_subwords_needed:
            random.shuffle(subwords)
            return chosen_word, subwords

    print("Cannot create word list with given settings")
    return None, None


def generate_word_list(difficulty_conf: DifficultyData, lexicon_path: str) -> tuple[str | None, list[str] | None]:
    """Generates the middle word and the list of words to place on the board.

    Reads the lexicon, filters words based on settings, finds a suitable
    middle word with enough subwords, and returns them.

    Args:
        difficulty_conf (DifficultyData): The difficulty settings for the game.
        lexicon_path (str): Path to the word list file.

    Returns:
        Tuple[Optional[str], Optional[List[str]]]: A tuple containing:
            - The chosen middle word (str) or None if generation fails.
            - A list of shuffled subwords (List[str]) for placement or None.

    """
    max_len = difficulty_conf.max_word_length
    min_sub_len = difficulty_conf.min_subword_length
    min_words_needed = difficulty_conf.words_on_board_needed.minimum

    clear_screen()
    # The print_message function from display.display expects Optional[DifficultyData]
    # We pass difficulty_conf which is DifficultyData, matching this expectation.
    print_message(
        difficulty_conf,
        "↺ Building board... Hold on, wizard!",
        style="yellow",
        border_style="magenta",
    )

    all_words = read_word_file(lexicon_path)
    if not all_words:
        return None, None

    valid_subword_pool = filter_words_up_to_max_length(all_words, max_len)
    if not valid_subword_pool:
        return None, None

    potential_middle_words = filter_exact_length_words(list(valid_subword_pool), max_len)
    if not potential_middle_words:
        return None, None

    random.shuffle(potential_middle_words)

    middle_word, list_of_words_to_place = find_valid_word_with_subwords(
        potential_middle_words,
        min_sub_len,
        min_words_needed,
        valid_subword_pool,
    )

    return middle_word, list_of_words_to_place
