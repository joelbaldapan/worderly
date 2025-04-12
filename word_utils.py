# ****************
# WORD CREATION
# ****************
from config import settings
import itertools
import random


def read_word_file(word_path):
    try:
        with open(word_path, "r") as file:
            return [word.strip().lower() for word in file if word.strip()]
    except FileNotFoundError:
        print(f"Error: File {word_path} not found.")
        return []
    except IOError as e:
        print(f"Error reading file {word_path}: {e}")
        return []


def filter_exact_length_words(words, exact_length):
    return [word for word in words if len(word) == exact_length]


def filter_words_up_to_max_length(words, max_length):
    return {word for word in words if len(word) <= max_length}


def get_valid_word_subwords(word, valid_words_set, min_length):
    valid_subwords = set()
    for length in range(min_length, len(word) + 1):
        for p in itertools.permutations(word, length):
            subword = "".join(p)
            if subword in valid_words_set and subword != word:
                valid_subwords.add(subword)
        print("DONE", length)
    return list(valid_subwords)


def find_valid_word_with_subwords(exact_max_length_words, valid_subword_set):
    # middle word counts as 1 word already
    # so we need min_words - 1 additional words
    min_subwords_needed = settings["words_on_board"]["minimum"] - 1

    for chosen_word in exact_max_length_words:
        subwords = get_valid_word_subwords(
            chosen_word, valid_subword_set, min_length=settings["min_subword_length"]
        )

        if len(subwords) >= min_subwords_needed:
            random.shuffle(subwords)
            # Return the chosen middle word and the list of other words to place
            return chosen_word, subwords
        else:
            print(
                f"Could not find enough subwords for {chosen_word}. Subwords: {len(subwords)}"
            )

    print("Cannot create word list with given settings")
    return None


def generate_word_list():
    lexicon_path = settings["lexicon_path"]
    max_len = settings["max_word_length"]

    all_words = read_word_file(lexicon_path)
    if not all_words:
        print("ERROR: Lexicon file reading failed or file is empty")
        return None

    # Create a set of valid words <= max_len
    valid_subword_set = filter_words_up_to_max_length(all_words, max_len)
    if not valid_subword_set:
        print(f"ERROR: No words found with length up to {max_len}")
        return None

    # Create a list of valid words == max_len
    exact_length_words = filter_exact_length_words(valid_subword_set, max_len)

    if not exact_length_words:
        print(f"ERROR: No words found with exact length {max_len}")
        return None

    # Shuffle to try different middle words each playthrough
    random.shuffle(exact_length_words)

    # Find a middle word and its subwords
    result = find_valid_word_with_subwords(exact_length_words, valid_subword_set)

    if result is None:
        return None

    # (middle_word, list_of_words_to_place)
    return result
