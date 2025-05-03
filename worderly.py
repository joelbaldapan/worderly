# ****************
# MAIN LOGIC
# ****************
import sys
from display.display_utils import clear_screen
from display.menus import run_heart_points_menu, initialize_player_info
from setup.word_selector import generate_word_list, read_word_file
from setup.grid_generator import generate_board
from gameplay.gameplay import run_game

MAX_SETUP_RETRIES = 5  # Maximum number of attempts to generate words and board
MAX_GRID_SETUP_RETRIES = 5  # Maximum number of attempts to generate board


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


def run_setup(
    settings,
):
    setup_attempts = 0

    # ATTEMPT TO GENERATE VALID WORD LIST AND BOARD
    while setup_attempts < MAX_SETUP_RETRIES:
        grid_setup_attempts = 0

        # CREATE WORD LIST
        middle_word, words_to_place = generate_word_list(settings)
        if middle_word is None:
            # FAILED
            setup_attempts += 1
            continue  # Go to the next attempt

        # CREATE GRID
        while grid_setup_attempts < MAX_GRID_SETUP_RETRIES:
            final_grid, words_to_find = generate_board(
                settings, middle_word, words_to_place
            )
            if final_grid is None:
                # FAILED
                grid_setup_attempts += 1
                continue  # Go to the next attempt
            else:
                # Both word list and grid succeeded!
                return middle_word, words_to_find, final_grid


def main():
    # VALIDATE LEXICON FILE
    lexicon_file = get_lexicon_file()
    if not lexicon_file:
        return  # Exit out of program

    # RUN SET-UP MENUS
    settings = run_heart_points_menu()
    settings["lexicon_path"] = lexicon_file

    # LOOP UNTIL THE USER EXITS (Outer loop for Heart Point Mode or single game)
    while True:
        # SET UP WORD LIST AND GRID LAYOUT
        result = run_setup(settings)
        # Check if setup failed after all retries
        if not result:
            clear_screen()
            print("\n" + "=" * 50)
            print(
                f"FATAL ERROR: Failed to set up the game after {MAX_SETUP_RETRIES} attempts."
            )
            print("This could be due to:")
            print(
                "  - Very restrictive grid settings (Grid size, number of words needed, word lengths)."
            )
            print(
                "  - Lexicon file lacks suitable words (Must have enough subwords to satisfy grid creation)."
            )
            print("Please check your settings, lexicon file, or try again.")
            print("Exiting program.")
            print("=" * 50 + "\n")
            return  # Exit the entire application

        # UNPACK RESULT
        middle_word, words_to_find, final_grid = result

        # INITALIZE GAME
        player_name, selected_wizard = initialize_player_info(settings)

        # GAMEPLAY
        run_game(
            settings,
            final_grid,
            words_to_find,
            middle_word,
            player_name,
            selected_wizard,
        )

        if not settings["heart_point_mode"]:
            break  # Exit the game if not on heart point mode


if __name__ == "__main__":
    main()
