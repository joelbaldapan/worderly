# ****************
# MAIN LOGIC
# ****************

from word_selector import generate_word_list
from grid_generator import generate_board
from gameplay import run_game

from menus import run_heart_points_menu, initialize_player_info


def main():
    settings = run_heart_points_menu()

    # TODO: Add lexicon path to terminal
    settings["lexicon_path"] = "corncob-lowercase.txt"

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
    player_name, selected_wizard = initialize_player_info(settings)

    # GAMEPLAY
    run_game(settings, final_grid, words_to_find, middle_word, player_name, selected_wizard)


if __name__ == "__main__":
    main()
