# ****************
# MAIN LOGIC
# ****************
import sys
from display.menus import run_heart_points_menu, initialize_player_info
from setup.word_selector import generate_word_list, read_word_file
from setup.grid_generator import generate_board
from gameplay.gameplay import run_game


def check_lexicon_file():
    if len(sys.argv) < 2:
        print("The game requires a lexicon file to start!", file=sys.stderr)
        print("Please input the correct format.", file=sys.stderr)
        return False

    lexicon_file = sys.argv[1]
    if not read_word_file(lexicon_file):
        print("Lexicon file reading failed, or file is empty!", file=sys.stderr)
        print("Please recheck your file.", file=sys.stderr)
        return False
    else:
        return True


def main():
    if not check_lexicon_file():
        return

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
    run_game(
        settings, final_grid, words_to_find, middle_word, player_name, selected_wizard
    )


if __name__ == "__main__":
    main()
