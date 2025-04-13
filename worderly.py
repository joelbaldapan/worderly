# ****************
# MAIN LOGIC
# ****************

from word_utils import generate_word_list
from display_utils import print_grid
from grid_utils import generate_board


def main():
    # CREATE WORD LIST
    middle_word, words_to_place = generate_word_list()

    if middle_word is None:
        raise ValueError("Failed to set up word list!")

    # CREATE GRID
    final_grid, words_to_find = generate_board(middle_word, words_to_place)

    if final_grid is None:
        raise ValueError("failed to set up grid!")

    print_grid(final_grid)
    print(words_to_find)

    # GAMEPLAY
    ...


if __name__ == "__main__":
    main()
