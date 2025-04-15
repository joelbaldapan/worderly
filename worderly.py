# ****************
# MAIN LOGIC
# ****************

from word_selector import generate_word_list
from grid_generator import generate_board
from gameplay import run_game


def main():
    # CREATE WORD LIST
    while True:
        middle_word, words_to_place = generate_word_list()

        if middle_word is None:
            print("Failed to set up word list!")
            continue

        # CREATE GRID
        final_grid, words_to_find = generate_board(middle_word, words_to_place)

        if final_grid is None:
            print("Failed to set up grid!")
            continue

        break

    # print_grid(final_grid)
    # print(words_to_find)

    # GAMEPLAY
    run_game(final_grid, words_to_find, middle_word)


if __name__ == "__main__":
    main()
