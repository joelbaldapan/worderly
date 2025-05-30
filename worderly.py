# ****************
# MAIN LOGIC
# ****************
import sys
from typing import TYPE_CHECKING

# Import dataclasses from other modules
from data.settings_details import DifficultyData
from display.display_utils import clear_screen
from gameplay.gameplay import run_game
from setup.grid_generator.main_generator import generate_board
from setup.menus import initialize_player_info, run_heart_points_menu, run_main_menu
from setup.word_selector import generate_word_list, read_word_file

if TYPE_CHECKING:
    from data.wizards_details import WizardData

MAX_SETUP_RETRIES = 5  # Maximum number of attempts to generate words and board
MAX_GRID_SETUP_RETRIES = 5  # Maximum number of attempts to generate board


def get_lexicon_file() -> str | None:
    """Retrieves and validates the lexicon file path from command-line arguments."""
    if len(sys.argv) < 2:
        print("The game requires a lexicon file to start!", file=sys.stderr)
        print("Please input the correct format.", file=sys.stderr)
        return None

    lexicon_file_path = sys.argv[1]
    if not read_word_file(lexicon_file_path):
        print("Lexicon file reading failed, or file is empty!", file=sys.stderr)
        print("Please recheck your file.", file=sys.stderr)
        return None
    else:
        return lexicon_file_path


def run_setup(difficulty_config: DifficultyData, lexicon_file_path: str):
    """Attempts to generate a valid word list and game board.

    Args:
        difficulty_config (DifficultyData): The difficulty settings for the game.
        lexicon_file_path (str): The path to the lexicon file.

    Returns:
        Optional[Tuple[str, Dict[str, List[Tuple[int, int]]], List[List[Optional[str]]]]]:
            (middle_word, words_to_find, final_grid) on success, None on failure.

    """
    setup_attempts = 0
    while setup_attempts < MAX_SETUP_RETRIES:
        setup_attempts += 1
        grid_setup_attempts = 0

        middle_word, words_to_place = generate_word_list(difficulty_config, lexicon_file_path)
        if middle_word is None:
            continue

        while grid_setup_attempts < MAX_GRID_SETUP_RETRIES:
            grid_setup_attempts += 1
            final_grid, words_to_find = generate_board(
                difficulty_config,
                middle_word,
                words_to_place,
            )
            if final_grid is None:
                continue
            return middle_word, words_to_find, final_grid
    return None


def main() -> None:
    """Main function to run the Worderly game."""
    lexicon_file_p: str | None = get_lexicon_file()
    if not lexicon_file_p:
        return

    current_difficulty_setting: DifficultyData | None = run_heart_points_menu()

    while True:
        if current_difficulty_setting is None:
            current_difficulty_setting = run_main_menu()

        setup_result = run_setup(current_difficulty_setting, lexicon_file_p)

        if not setup_result:
            clear_screen()
            print("\n" + "=" * 50)
            print(f"FATAL ERROR: Failed to set up the game after {MAX_SETUP_RETRIES} attempts.")
            print("This could be due to:")
            print("  - Very restrictive grid settings (Grid size, number of words needed, word lengths).")
            print("  - Lexicon file lacks suitable words (Must have enough subwords to satisfy grid creation).")
            print("Please check your settings, lexicon file, or try again.")
            print("Exiting program.")
            print("=" * 50 + "\n")
            return

        middle_word: str
        words_to_find: dict[str, list[tuple[int, int]]]
        final_grid: list[list[str | None]]
        middle_word, words_to_find, final_grid = setup_result

        player_name: str | None
        selected_wizard: WizardData  # initialize_player_info returns WizardData
        player_name, selected_wizard = initialize_player_info(current_difficulty_setting)

        run_game(
            current_difficulty_setting,  # Pass DifficultyData
            final_grid,
            words_to_find,
            middle_word,
            player_name,
            selected_wizard,
        )

        if not current_difficulty_setting.heart_point_mode:
            break

        current_difficulty_setting = None


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\n" + "=" * 40)
        print("\nExiting game...")
        print("I bid you adieu, wandwork wizard!")
        print("\n" + "=" * 40)
