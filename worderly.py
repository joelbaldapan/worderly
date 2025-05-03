# ****************
# MAIN LOGIC
# ****************
import sys
from display.menus import run_heart_points_menu, initialize_player_info
from setup.word_selector import generate_word_list, read_word_file
from setup.grid_generator import generate_board
from gameplay.gameplay import run_game


def get_lexicon_file():
    if len(sys.argv) < 2:
        print("The game requires a lexicon file to start!", file=sys.stderr)
        print("Please input the correct format.", file=sys.stderr)
        return None

    lexicon_file = sys.argv[1]
    if not read_word_file(lexicon_file):
        print("Lexicon file reading failed, or file is empty!", file=sys.stderr)
        print("Please recheck your file.", file=sys.stderr)
        return None
    else:
        return lexicon_file


def main():
    # VALIDATE LEXICON FILE
    lexicon_file = get_lexicon_file() 
    if not lexicon_file:
        return # Exit out of program

    # RUN SET-UP MENUS
    settings = run_heart_points_menu()
    settings["lexicon_path"] = lexicon_file

    # LOOP UNTIL THE USER EXITS (If on Heart Point Mode)
    while True:
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

        if not settings["heart_point_mode"]:
            break # Exit the game if not on heart point mode


if __name__ == "__main__":
    main()
