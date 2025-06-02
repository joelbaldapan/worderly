from typing import Any

from data.settings_details import DifficultyData
from data.wizards_details import WizardData
from display.display_utils import clear_screen
from gameplay.game_state_handler import GameStatisticsData
from leaderboard.streak_handler import StreakEntry


def basic_print_grid(grid: list[list[str | None]] | None) -> None:
    """Print a basic text representation of the game grid to the console.

    Args:
        grid (Optional[List[List[Optional[str]]]]):
            The 2D list representing the game grid. None represents empty cells.

    """
    if not grid:
        print("Grid is empty or not provided.")
        return
    for row in grid:
        print(" ".join(cell or "." for cell in row))


def basic_print_statistics(statistics: GameStatisticsData) -> None:
    """Print basic game statistics to the console.

    Args:
        statistics (GameStatisticsData):
            An object containing game stats like letters, lives_left,
            points, last_guess.

    """
    print(f"Letters:     {statistics.letters}")
    print(f"Lives left:  {statistics.lives_left}")
    print(f"Points:      {statistics.points}")
    last_guess_display = statistics.last_guess if statistics.last_guess is not None else "None"
    print(f"Last Guess:  {last_guess_display}")


def basic_print_message(message: str) -> None:
    """Print a simple message string to the console."""
    print(message)


def basic_get_input(prompt_message: str = "") -> str:
    """Get input from the user via the console."""
    return input(prompt_message)


def basic_print_leaderboard(leaderboard: list[dict[str, Any]]) -> None:
    """Print a basic text representation of the leaderboard.

    Args:
        leaderboard (List[Dict[str, Any]]):
            A list of score dictionaries, already sorted.
            Each dict should have 'name' and 'score' keys.

    """
    print("\n----------- Leaderboard -----------")
    if not leaderboard:
        print("Leaderboard is empty.")
        return

    num_entries = len(leaderboard)
    max_rank_width = len(str(num_entries)) if num_entries > 0 else 1

    for idx, entry in enumerate(leaderboard):
        rank = idx + 1
        formatted_rank = f"{rank:>{max_rank_width}}"
        name = str(entry.get("name", "N/A"))
        score = str(entry.get("score", "N/A"))
        print(f"{formatted_rank} | Name: {name}, {score} points")
    print("-----------------------------------\n")


def basic_display_wizard_selection(
    settings: DifficultyData | None,
    wizard: WizardData,
    wizard_index: int,
) -> None:
    """Display basic text information about the currently selected wizard.

    Args:
        settings (Optional[DifficultyData]): Game settings (passed by dispatcher, maybe unused).
        wizard (WizardData): The WizardData object to display.
        wizard_index (int): The index of the wizard (passed by dispatcher, maybe unused).

    """
    clear_screen()

    basic_display_wizard_art(settings, wizard)
    print("-----------------------------------------")
    print(f"Name: {wizard.name}")
    print(f"Starting Lives: {wizard.starting_lives}")
    print()
    print(f"Powerup: {wizard.powerup_name}")
    print(f"Powerup Description: {wizard.powerup_desc}")
    print()
    print(f"Wizard Description: {wizard.description}")
    print("-----------------------------------------")
    print()
    print("Use (◀) Left / Right (▶) arrow keys to select. Press Enter to confirm.")


def basic_display_wizard_art(
    settings: DifficultyData | None,
    wizard: WizardData,
) -> None:
    """Print the basic ASCII art for a given wizard.

    Args:
        settings (Optional[DifficultyData]): Game settings (passed by dispatcher, maybe unused).
        wizard (WizardData): The WizardData object containing the art.

    """
    print(wizard.art)


def basic_display_menu_options(options: list[str], current_index: int, title: str) -> None:
    """Display a basic text-based vertical menu with selection indicator.

    Args:
        options (List[str]): A list of strings representing the menu options.
        current_index (int): The index of the currently selected option.
        title (str): The title to display above the menu.

    """
    print(title)
    for i, option in enumerate(options):
        prefix = "-> " if i == current_index else "   "
        print(f"{prefix}{option}")
    print()
    print("Use (▲) Up / Down (▼) arrow keys to select. Press Enter to confirm.")


def basic_print_streak_leaderboard(streaks: list[StreakEntry]) -> None:
    """Prints a basic text representation of the winning streak leaderboard."""
    print("\n--- Winning Streaks Leaderboard ---")
    if not streaks:
        print("Leaderboard is empty.")
        print("---------------------------------")
        return

    max_name_len = 15  # Default/max width for player name
    if streaks:
        pass

    # Header
    header = f"{'Rank':<5} | {'Player Name':<{max_name_len}} | {'Streak':>7} | {'Total Points':>12}"
    print(header)
    print("-" * len(header))

    for index, entry in enumerate(streaks):
        rank = str(index + 1)
        name = entry.player_name
        streak = str(entry.streak_count)
        points = str(entry.total_points_in_streak)

        display_name = (name[: max_name_len - 3] + "...") if len(name) > max_name_len else name

        print(f"{rank:<5} | {display_name:<{max_name_len}} | {streak:>7} | {points:>12}")

    print("---------------------------------")
