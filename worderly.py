# ****************
# MAIN LOGIC
# ****************
import sys
from dataclasses import dataclass

from data.settings_details import NO_HEART_POINTS_SETTINGS, DifficultyData
from display.display_utils import clear_screen
from gameplay.gameplay import run_game
from leaderboard.streak_handler import StreakEntry, add_streak_entry
from setup.grid_generator.main_generator import generate_board
from setup.menus import (
    EXIT_GAME_SENTINEL,
    initialize_player_info,
    run_heart_points_menu,
    run_main_menu,
)
from setup.word_selector import generate_word_list, read_word_file


@dataclass
class SessionStreakState:
    player_name: str | None = None
    count: int = 0
    points_total: int = 0

    def reset_streak_counters(self) -> None:
        """Reset count and points, keeps player name for the session."""
        self.count = 0
        self.points_total = 0

    def full_reset(self) -> None:
        """Reset all streak information, including player name."""
        self.player_name = None
        self.count = 0
        self.points_total = 0


CURRENT_SESSION_STREAK = SessionStreakState()
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


def _handle_fatal_setup_error() -> None:
    """Handle fatal setup error, prints message, and saves active streak."""
    clear_screen()
    print("\n" + "=" * 50)
    print(f"FATAL ERROR: Failed to set up game after {MAX_SETUP_RETRIES} attempts.")
    print("This could be due to:")
    print("  - Very restrictive grid settings (Grid size, number of words needed, word lengths).")
    print("  - Lexicon file lacks suitable words (Must have enough subwords to satisfy grid creation).")
    print("Please check your settings, lexicon file, or try again.")
    print("Exiting program.")
    print("=" * 50 + "\n")
    if CURRENT_SESSION_STREAK.count > 0 and CURRENT_SESSION_STREAK.player_name:
        entry = StreakEntry(
            CURRENT_SESSION_STREAK.player_name,
            CURRENT_SESSION_STREAK.count,
            CURRENT_SESSION_STREAK.points_total,
        )
        add_streak_entry(entry)
        print(f"Saved active streak for {CURRENT_SESSION_STREAK.player_name} due to setup error.")


def _save_streak():
    """Save the current streak if it exists and player name is set."""
    if CURRENT_SESSION_STREAK.count > 0 and CURRENT_SESSION_STREAK.player_name:
        entry = StreakEntry(
            CURRENT_SESSION_STREAK.player_name,
            CURRENT_SESSION_STREAK.count,
            CURRENT_SESSION_STREAK.points_total,
        )
        add_streak_entry(entry)


def _update_player_name(player_name_from_init: str | None):
    """Update the player name in the streak state, saving old streak if needed."""
    if CURRENT_SESSION_STREAK.player_name != player_name_from_init:
        if CURRENT_SESSION_STREAK.player_name is not None and CURRENT_SESSION_STREAK.count > 0:
            _save_streak()
        CURRENT_SESSION_STREAK.player_name = player_name_from_init
        CURRENT_SESSION_STREAK.reset_streak_counters()
    elif CURRENT_SESSION_STREAK.player_name is None and player_name_from_init:
        CURRENT_SESSION_STREAK.player_name = player_name_from_init
        CURRENT_SESSION_STREAK.reset_streak_counters()


def _run_game_session(
    lexicon_file_p: str,
    initial_difficulty_config_for_nhp: DifficultyData | None,
    is_hp_mode_session: bool,
) -> None:
    """Run the game session loop for either HP or NHP mode, using global streak state."""
    while True:
        # Select difficulty config for this round
        if is_hp_mode_session:
            menu_result = run_main_menu()
            if menu_result == EXIT_GAME_SENTINEL:
                _save_streak()
                print("\nThanks for your bravery, Wizard! Exiting Worderly Place.")
                return
            difficulty_config_this_round = menu_result
        else:
            if initial_difficulty_config_for_nhp is None:
                print("Error: NHP settings missing.")
                return
            difficulty_config_this_round = initial_difficulty_config_for_nhp

        # Determine player name to pass to init
        name_to_pass_to_init: str | None = (
            CURRENT_SESSION_STREAK.player_name
            if (CURRENT_SESSION_STREAK.count > 0 and CURRENT_SESSION_STREAK.player_name)
            or (not is_hp_mode_session and CURRENT_SESSION_STREAK.player_name)
            else None
        )

        player_name_from_init, selected_wizard = initialize_player_info(
            difficulty_config_this_round,
            name_to_pass_to_init,
        )

        _update_player_name(player_name_from_init)

        setup_result = run_setup(difficulty_config_this_round, lexicon_file_p)
        if not setup_result:
            _handle_fatal_setup_error()
            return

        middle_word, words_to_find, final_grid = setup_result

        game_outcome, points_this_game = run_game(
            difficulty_config_this_round,
            final_grid,
            words_to_find,
            middle_word,
            CURRENT_SESSION_STREAK.player_name,
            selected_wizard,
        )

        if CURRENT_SESSION_STREAK.player_name:
            if game_outcome == "win":
                CURRENT_SESSION_STREAK.count += 1
                CURRENT_SESSION_STREAK.points_total += points_this_game
            elif game_outcome == "loss":
                _save_streak()
                CURRENT_SESSION_STREAK.reset_streak_counters()


def main() -> None:
    """Run the Worderly game."""
    lexicon_file_p: str | None = get_lexicon_file()
    if not lexicon_file_p:
        return

    initial_mode_choice: DifficultyData | None = run_heart_points_menu()

    CURRENT_SESSION_STREAK.full_reset()

    if initial_mode_choice is None:
        _run_game_session(lexicon_file_p, None, is_hp_mode_session=True)
    elif not initial_mode_choice.heart_point_mode:
        _run_game_session(lexicon_file_p, NO_HEART_POINTS_SETTINGS, is_hp_mode_session=False)
    else:
        print("Exiting due to an unexpected initial mode selection outcome.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        if CURRENT_SESSION_STREAK.count > 0 and CURRENT_SESSION_STREAK.player_name:
            print("\nInterrupt detected. Saving current streak...")
            _save_streak()
            print(
                f"Streak for {CURRENT_SESSION_STREAK.player_name} saved: "
                f"{CURRENT_SESSION_STREAK.count} wins, {CURRENT_SESSION_STREAK.points_total} pts.",
            )
        else:
            print("\nInterrupt detected. No active streak to save or player name not set.")

        print("\n" + "=" * 40)
        print("Exiting game (Keyboard Interrupt)...")
        print("I bid you adieu, wandwork wizard!")
        print("=" * 40)
