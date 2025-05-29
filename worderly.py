# ****************
# MAIN LOGIC
# ****************
import sys

from display.display_utils import clear_screen
from gameplay.gameplay import run_game
from setup.grid_generator import generate_board
from setup.menus import initialize_player_info, run_heart_points_menu, run_main_menu
from setup.word_selector import generate_word_list, read_word_file

MAX_SETUP_RETRIES = 5  # Maximum number of attempts to generate words and board
MAX_GRID_SETUP_RETRIES = 5  # Maximum number of attempts to generate board


def get_lexicon_file():
    """Retrieves and validates the lexicon file path from command-line arguments."""
    if len(sys.argv) < 2:
        print("The game requires a lexicon file to start!", file=sys.stderr)
        print("Please input the correct format.", file=sys.stderr)
        return None

    lexicon_file = sys.argv[1]
    # Use read_word_file for validation (checks existence and non-emptiness)
    if not read_word_file(lexicon_file):
        print("Lexicon file reading failed, or file is empty!", file=sys.stderr)
        print("Please recheck your file.", file=sys.stderr)
        return None
    else:
        return lexicon_file


def run_setup(settings):
    """Attempts to generate a valid word list and game board based on settings.

    Retries word list generation and grid generation up to a maximum number
    of attempts defined by MAX_SETUP_RETRIES and MAX_GRID_SETUP_RETRIES.

    Args:
        settings (dict):
            A dictionary containing game settings like grid size,
            word length constraints, and minimum words needed.

    Returns:
        tuple or None: A tuple containing (middle_word, words_to_find, final_grid)
                      if setup is successful. Returns None if setup fails after
                      all retry attempts.
                      - middle_word (str): The central word for the puzzle.
                      - words_to_find (dict): Dictionary mapping placed words
                        to their coordinates.
                      - final_grid (list[list[str|None]]): The generated game grid.

    """
    setup_attempts = 0

    # ATTEMPT TO GENERATE VALID WORD LIST AND BOARD
    while setup_attempts < MAX_SETUP_RETRIES:
        setup_attempts += 1  # Increment attempt counter at the start
        grid_setup_attempts = 0

        # CREATE WORD LIST
        middle_word, words_to_place = generate_word_list(settings)
        if middle_word is None:
            # FAILED word list generation for this attempt
            continue  # Go to the next setup attempt

        # CREATE GRID
        while grid_setup_attempts < MAX_GRID_SETUP_RETRIES:
            grid_setup_attempts += 1  # Increment grid attempt counter
            final_grid, words_to_find = generate_board(
                settings,
                middle_word,
                words_to_place,
            )
            if final_grid is None:
                # FAILED grid generation for this attempt
                continue  # Go to the next grid attempt
            # Both word list and grid succeeded!
            return middle_word, words_to_find, final_grid

    return None  # Return None if all setup attempts failed


def main() -> None:
    """Main function to run the Worderly game.

    Handles command-line validation, menu navigation, game setup,
    and the main game loop.
    """
    # VALIDATE LEXICON FILE
    lexicon_file = get_lexicon_file()
    if not lexicon_file:
        return  # Exit out of program if lexicon is invalid

    # RUN SET-UP MENUS
    # run_heart_points_menu determines initial mode or returns None to go to main menu
    settings = run_heart_points_menu()

    # LOOP UNTIL THE USER EXITS (Outer loop for Heart Point Mode or single game)
    while True:
        # If run_heart_points_menu returned None (meaning user chose HP mode initially
        # or finished a non-HP game), run the main menu to get settings.
        if settings is None:
            settings = run_main_menu()

        # Ensure lexicon path is always set for the current game round
        settings["lexicon_path"] = lexicon_file

        # SET UP WORD LIST AND GRID LAYOUT
        result = run_setup(settings)

        # Check if setup failed after all retries
        if not result:
            clear_screen()
            print("\n" + "=" * 50)
            print(
                f"FATAL ERROR: Failed to set up the game after {MAX_SETUP_RETRIES} attempts.",
            )
            print("This could be due to:")
            print(
                "  - Very restrictive grid settings (Grid size, number of words needed, word lengths).",
            )
            print(
                "  - Lexicon file lacks suitable words (Must have enough subwords to satisfy grid creation).",
            )
            print("Please check your settings, lexicon file, or try again.")
            print("Exiting program.")
            print("=" * 50 + "\n")
            return  # Exit the entire application

        # UNPACK RESULT
        middle_word, words_to_find, final_grid = result

        # INITALIZE PLAYER INFO (only relevant for HP mode, returns defaults otherwise)
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

        # Check if we should break the outer loop
        if not settings.get("heart_point_mode", False):  # Check if heart_point_mode
            break  # Exit the outer loop if not on heart point mode
        # In HP mode, reset settings to None to force main menu on next loop iteration
        settings = None


if __name__ == "__main__":
    # Entry point when the script is executed directly
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\n" + "=" * 40)
        print("\nExiting game...")
        print("I bid you adieu, wandwork wizard!")
        print("\n" + "=" * 40)
