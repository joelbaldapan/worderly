# ****************
# WORD CREATION
# ****************
import itertools
import random

from display.display import (
    print_message,
)
from display.display_utils import clear_screen


def read_word_file(word_path):
    """Reads a lexicon file, cleans words, and returns them as a list."""
    try:
        with open(word_path) as file:
            return [word.strip().lower() for word in file if word.strip()]
    except FileNotFoundError:
        print(f"Error: File {word_path} not found.")
        return []
    except OSError as e:
        print(f"Error reading file {word_path}: {e}")
        return []


def filter_exact_length_words(words, exact_length):
    """Filters a list of words to include only those of a specific exact length."""
    return [word for word in words if len(word) == exact_length]


def filter_words_up_to_max_length(words, max_length):
    """Filters a word collection to include only words up to a maximum length, returning a set."""
    return {word for word in words if len(word) <= max_length}


def get_valid_word_subwords(word, valid_words_set, min_length):
    """Finds all valid subwords/anagrams of a given word from a valid set."""
    valid_subwords = set()
    # Iterate through possible lengths for permutations
    for length in range(min_length, len(word) + 1):
        # Generate all permutations of the specified length
        for p in itertools.permutations(word, length):
            subword = "".join(p)
            # Check if the permutation is a valid word and not the original word itself
            if subword in valid_words_set and subword != word:
                valid_subwords.add(subword)
        # print("DONE", length) # Debug print
    # Return the found subwords as a list
    return list(valid_subwords)


def find_valid_word_with_subwords(
    exact_max_length_words, min_subword_length, min_subwords_needed, valid_subword_set,
):
    """Searches for a word of a specific length that has enough valid subwords."""
    # middle word counts as 1 word already
    # so we need min_words - 1 additional words
    actual_subwords_needed = min_subwords_needed - 1

    # Iterate through potential middle words
    for chosen_word in exact_max_length_words:
        # Find subwords for the current candidate
        subwords = get_valid_word_subwords(
            chosen_word, valid_subword_set, min_subword_length,
        )

        # Check if enough subwords were found
        if len(subwords) >= actual_subwords_needed:
            random.shuffle(subwords)  # Shuffle the list for variety
            # Return the chosen middle word and the list of other words to place
            return chosen_word, subwords
        else:
            # Debug print
            # print(
            #     f"Could not find enough subwords for {chosen_word}. "
            #     f"Needed: {actual_subwords_needed}, Found: {len(subwords)}"
            # )
            pass  # Continue to the next candidate word

    # If no suitable middle word is found after checking all candidates
    print("Cannot create word list with given settings")
    return None, None


def generate_word_list(settings):
    """Generates the middle word and the list of words to place on the board.

    Reads the lexicon, filters words based on settings, finds a suitable
    middle word with enough subwords, and returns them. Handles file reading
    errors and cases where no suitable words can be found according to settings.

    Args:
        settings (dict): The game settings dictionary. Expected keys include:
            - "lexicon_path" (str): Path to the word list file.
            - "max_word_length" (int): The required length for the middle word
              and the maximum length for subwords.
            - "min_subword_length" (int): The minimum length for subwords.
            - "words_on_board_needed" (dict): Dictionary with word count info:
                - "minimum" (int): The minimum total words (middle + subwords)
                  required for a valid setup.
            - Other keys like "grid", "heart_point_mode" exist but are
              not directly used by this function.

    Returns:
        tuple[str | None, list[str] | None]: A tuple containing:
            - The chosen middle word (str) or None if generation fails.
            - A list of shuffled subwords (list[str]) for placement or None.

    """
    # Extract settings for clarity
    lexicon_path = settings["lexicon_path"]
    max_len = settings["max_word_length"]
    min_subword_length = settings["min_subword_length"]
    min_subwords_needed = settings["words_on_board_needed"]["minimum"]

    # Display status message (requires mocking in tests)
    clear_screen()
    print_message(
        settings,
        "↺ Building board... Hold on, wizard!",
        style="yellow",
        border_style="magenta",
    )

    # Read all words from the lexicon file
    all_words = read_word_file(lexicon_path)
    if not all_words:
        # Handle file read failure or empty file
        # print("ERROR: Lexicon file reading failed or file is empty") # Debug Message
        return None, None

    # Create a set of valid words up to the maximum length for efficient lookup
    valid_subword_set = filter_words_up_to_max_length(all_words, max_len)
    if not valid_subword_set:
        # Handle case where no words meet the max length criteria
        # print(f"ERROR: No words found with length up to {max_len}") # Debug Message
        return None, None

    # Create a list of potential middle words (exactly max_len)
    # Filter from the valid_subword_set for efficiency
    exact_length_words = filter_exact_length_words(valid_subword_set, max_len)
    if not exact_length_words:
        # Handle case where no words of the exact max length exist
        # print(f"ERROR: No words found with exact length {max_len}") # Debug Message
        return None, None

    # Shuffle potential middle words for variety between game plays
    random.shuffle(exact_length_words)

    # Find a suitable middle word and its accompanying subwords
    middle_word, list_of_words_to_place = find_valid_word_with_subwords(
        exact_length_words, min_subword_length, min_subwords_needed, valid_subword_set,
    )

    # Return the result
    # Ccould be (None, None) if find_valid_word_with_subwords failed
    return middle_word, list_of_words_to_place
