import itertools
import random

from data.settings_details import DifficultyData
from display.display import print_message
from display.display_utils import clear_screen


def read_word_file(word_path: str) -> list[str]:
    """Read a lexicon file and return a list of cleaned, lowercase words.

    Args:
        word_path (str): The path to the word file.

    Returns:
        list[str]: A list of words from the file, cleaned and lowercased.

    """
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
    """Return a list of words with exactly the specified length.

    Args:
        words (list[str]): The list of words to filter.
        exact_length (int): The required word length.

    Returns:
        list[str]: Words with the exact specified length.

    """
    return [word for word in words if len(word) == exact_length]


def filter_words_up_to_max_length(words: list[str], max_length: int) -> set[str]:
    """Return a set of words with length less than or equal to max_length.

    Args:
        words (list[str]): The list of words to filter.
        max_length (int): The maximum allowed word length.

    Returns:
        set[str]: Words with length up to max_length.

    """
    return {word for word in words if len(word) <= max_length}


def get_valid_word_subwords(word: str, valid_words_set: set[str], min_length: int) -> list[str]:
    """Find all valid subwords/anagrams of a word from a set, with minimum length.

    Args:
        word (str): The word to find subwords for.
        valid_words_set (set[str]): Set of valid words to check against.
        min_length (int): Minimum length for subwords.

    Returns:
        list[str]: List of valid subwords (excluding the original word).

    """
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
    """Find a word of a specific length with enough valid subwords.

    Args:
        exact_max_length_words (list[str]): Words of the required length.
        min_subword_length (int): Minimum length for subwords.
        min_subwords_needed (int): Minimum number of subwords required (including the word itself).
        valid_subword_set (set[str]): Set of valid words for subword checking.

    Returns:
        tuple[str | None, list[str] | None]: The chosen word and its subwords, or (None, None) if not found.

    """
    actual_subwords_needed = min_subwords_needed - 1

    for chosen_word in exact_max_length_words:
        subwords = get_valid_word_subwords(chosen_word, valid_subword_set, min_subword_length)
        if len(subwords) >= actual_subwords_needed:
            random.shuffle(subwords)
            return chosen_word, subwords

    print("Cannot create word list with given settings")
    return None, None


def generate_word_list(difficulty_conf: DifficultyData, lexicon_path: str) -> tuple[str | None, list[str] | None]:
    """Generate a middle word and a list of subwords for the game board.

    Reads the lexicon, filters words based on settings, finds a suitable
    middle word with enough subwords, and returns them.

    Args:
        difficulty_conf (DifficultyData): The difficulty settings for the game.
        lexicon_path (str): Path to the word list file.

    Returns:
        tuple[str | None, list[str] | None]: The chosen middle word and a list of subwords, or (None, None) if failed.

    """
    max_len = difficulty_conf.max_word_length
    min_sub_len = difficulty_conf.min_subword_length
    min_words_needed = difficulty_conf.words_on_board_needed.minimum

    clear_screen()
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
