# ****************
# MAIN LOGIC
# ****************

from word_selector import generate_word_list
from grid_generator import generate_board
from player_info_initializer import initialize_player_info
from gameplay import run_game
from config import settings


def main():
    while True:
        # CREATE WORD LIST
        middle_word, words_to_place = generate_word_list(settings)

        if middle_word is None:
            print("Failed to set up word list!")
            continue

        # CREATE GRID
        final_grid, words_to_find = generate_board(
            settings, middle_word, words_to_place
        )

        if final_grid is None:
            print("Failed to set up grid!")
            continue

        break

    # INITALIZE GAME
    player_name, selected_wizard = initialize_player_info()

    # GAMEPLAY
    run_game(final_grid, words_to_find, middle_word, player_name, selected_wizard)


if __name__ == "__main__":
    main()
