# ****************
# MAIN LOGIC
# ****************
import sys

from data.settings_details import NO_HEART_POINTS_SETTINGS, DifficultyData  # Import NHP settings
from display.display_utils import clear_screen
from gameplay.gameplay import run_game  # Returns Tuple[str, int]
from leaderboard.streak_handler import StreakEntry, add_streak_entry
from setup.grid_generator.main_generator import generate_board
from setup.menus import (
    EXIT_GAME_SENTINEL,  # Import the sentinel
    initialize_player_info,
    run_heart_points_menu,
    run_main_menu,
)
from setup.word_selector import generate_word_list, read_word_file

MAX_SETUP_RETRIES = 5  # Maximum number of attempts to generate words and board
MAX_GRID_SETUP_RETRIES = 5  # Maximum number of attempts to generate board


def get_lexicon_file() -> str | None:
    """Retrieve and validates the lexicon file path from command-line arguments."""
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
    """Attempt to generate a valid word list and game board.

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


def _handle_fatal_setup_error(
    is_hp_session: bool,
    active_player_name: str | None,
    active_streak_count: int,
    active_streak_points_total: int,
) -> None:
    clear_screen()
    print("\n" + "=" * 50)
    print(f"FATAL ERROR: Failed to set up game after {MAX_SETUP_RETRIES} attempts.")
    print("This could be due to:")
    print("  - Very restrictive grid settings (Grid size, number of words needed, word lengths).")
    print("  - Lexicon file lacks suitable words (Must have enough subwords to satisfy grid creation).")
    print("Please check your settings, lexicon file, or try again.")
    print("Exiting program.")
    print("=" * 50 + "\n")
    if is_hp_session and active_streak_count > 0 and active_player_name:
        entry = StreakEntry(active_player_name, active_streak_count, active_streak_points_total)
        add_streak_entry(entry)


def _run_nhp_session(lexicon_file_p: str, nhp_difficulty_config: DifficultyData) -> None:
    """Runs the game in a persistent No Heart Points mode loop."""
    while True:
        player_name_for_this_game, selected_wizard = initialize_player_info(nhp_difficulty_config)

        setup_result = run_setup(nhp_difficulty_config, lexicon_file_p)
        if not setup_result:
            _handle_fatal_setup_error(False, None, 0, 0)  # NHP mode doesn't save streaks
            return  # Exit NHP session (and thus main) on fatal setup error

        middle_word, words_to_find, final_grid = setup_result

        # run_game will call simplified_end_game_interaction, which shows leaderboard
        # and the NHP-specific "Press Enter for next puzzle..." prompt.
        run_game(
            nhp_difficulty_config, final_grid, words_to_find,
            middle_word, player_name_for_this_game, selected_wizard,
        )
        # Loop continues for the next NHP game


def _run_hp_session(lexicon_file_p: str) -> None:
    """Runs the game in a persistent Heart Points mode loop with streak tracking."""
    active_player_name: str | None = None
    active_streak_count: int = 0
    active_streak_points_total: int = 0

    while True:
        game_specific_difficulty_config: DifficultyData
        menu_result = run_main_menu()
        if menu_result == EXIT_GAME_SENTINEL:
            if active_streak_count > 0 and active_player_name:
                entry = StreakEntry(active_player_name, active_streak_count, active_streak_points_total)
                add_streak_entry(entry)
            print("\nThanks for your bravery, Wizard! Exiting Worderly Place.")
            return
        game_specific_difficulty_config = menu_result

        player_name_for_this_game, selected_wizard = initialize_player_info(game_specific_difficulty_config)

        if active_player_name != player_name_for_this_game and active_player_name is not None:
            if active_streak_count > 0:
                entry = StreakEntry(active_player_name, active_streak_count, active_streak_points_total)
                add_streak_entry(entry)
            active_streak_count = 0
            active_streak_points_total = 0
        active_player_name = player_name_for_this_game

        setup_result = run_setup(game_specific_difficulty_config, lexicon_file_p)
        if not setup_result:
            _handle_fatal_setup_error(True, active_player_name, active_streak_count, active_streak_points_total)
            return

        middle_word, words_to_find, final_grid = setup_result

        game_outcome: str
        points_this_game: int
        game_outcome, points_this_game = run_game(
            game_specific_difficulty_config, final_grid, words_to_find,
            middle_word, active_player_name, selected_wizard,  # Pass active_player_name for streak
        )

        if active_player_name:
            if game_outcome == "win":
                active_streak_count += 1
                active_streak_points_total += points_this_game
            elif game_outcome == "loss":
                if active_streak_count > 0:
                    entry = StreakEntry(active_player_name, active_streak_count, active_streak_points_total)
                    add_streak_entry(entry)
                active_streak_count = 0
                active_streak_points_total = 0

        current_hp_round_difficulty_config = None  # Reset to show main menu for next HP game


def main() -> None:
    """Main function to run the Worderly game."""
    lexicon_file_p: str | None = get_lexicon_file()
    if not lexicon_file_p:
        return

    initial_mode_choice: DifficultyData | None = run_heart_points_menu()

    if initial_mode_choice is None:  # User selected Heart Points Mode path
        _run_hp_session(lexicon_file_p)
    elif not initial_mode_choice.heart_point_mode:  # User selected No Heart Points Mode
        _run_nhp_session(lexicon_file_p, NO_HEART_POINTS_SETTINGS)
    else:
        print("Exiting due to initial mode selection outcome.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\n" + "=" * 40)
        print("\nExiting game (Keyboard Interrupt)...")
        print("I bid you adieu, wandwork wizard!")
        print("\n" + "=" * 40)
