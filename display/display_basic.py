# display/display_basic.py

from typing import List, Optional, Dict, Any, Tuple  # Added necessary types

# Import WizardData for type hinting and WIZARDS_DATA for direct access if still needed (though ideally pass objects)
from data.wizards_details import WizardData, WIZARDS_DATA  # WIZARDS_DATA for basic_display_wizard_selection
from data.settings_details import DifficultyData  # For type hinting 'settings' parameter

from display.display_utils import clear_screen


def basic_print_grid(grid: Optional[List[List[Optional[str]]]]) -> None:
    """Prints a basic text representation of the game grid to the console.

    Args:
        grid (Optional[List[List[Optional[str]]]]):
            The 2D list representing the game grid. None represents empty cells.
    """
    if not grid:
        print("Grid is empty or not provided.")
        return
    for row in grid:
        print(" ".join(cell or "." for cell in row))


def basic_print_statistics(statistics: Dict[str, Any]) -> None:
    """Prints basic game statistics to the console.

    Args:
        statistics (Dict[str, Any]):
            A dictionary containing game stats like 'letters', 'lives_left',
            'points', 'last_guess'.
    """
    print(f"Letters:     {statistics.get('letters', 'N/A')}")
    print(f"Lives left:  {statistics.get('lives_left', 'N/A')}")
    print(f"Points:      {statistics.get('points', 'N/A')}")
    print(f"Last Guess:  {statistics.get('last_guess', 'None')}")


def basic_print_message(message: str) -> None:
    """Prints a simple message string to the console."""
    print(message)


def basic_get_input(prompt_message: str = "") -> str:
    """Gets input from the user via the console."""
    return input(prompt_message)


def basic_print_leaderboard(leaderboard: List[Dict[str, Any]]) -> None:
    """Prints a basic text representation of the leaderboard.

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


# Updated signature to match how it's called from display.py
# The 'settings' and 'wizard_index' parameters might be ignored if 'wizard' object is sufficient.
def basic_display_wizard_selection(
    settings: Optional[DifficultyData],  # Passed by display.py, may be unused here
    wizard: WizardData,  # The actual WizardData object
    wizard_index: int,  # Passed by display.py, may be unused here
) -> None:
    """Displays basic text information about the currently selected wizard.

    Args:
        settings (Optional[DifficultyData]): Game settings (passed by dispatcher, maybe unused).
        wizard (WizardData): The WizardData object to display.
        wizard_index (int): The index of the wizard (passed by dispatcher, maybe unused).
    """
    clear_screen()

    # Use the passed 'wizard' object directly
    basic_display_wizard_art(settings, wizard)  # Pass settings and wizard object
    print("-----------------------------------------")
    print(f"Name: {wizard.name}")  # Attribute access
    print(f"Starting Lives: {wizard.starting_lives}")  # Attribute access
    print()
    print(f"Powerup: {wizard.powerup_name}")  # Attribute access
    print(f"Powerup Description: {wizard.powerup_desc}")  # Attribute access
    print()
    print(f"Wizard Description: {wizard.description}")  # Attribute access
    print("-----------------------------------------")
    print()
    print("Use (◀) Left / Right (▶) arrow keys to select. Press Enter to confirm.")


# Updated signature to accept WizardData and settings (for consistency)
def basic_display_wizard_art(
    settings: Optional[DifficultyData],  # Passed by display.py, may be unused here
    wizard: WizardData,  # Changed to WizardData object
) -> None:
    """Prints the basic ASCII art for a given wizard.

    Args:
        settings (Optional[DifficultyData]): Game settings (passed by dispatcher, maybe unused).
        wizard (WizardData): The WizardData object containing the art.
    """
    print(wizard.art)  # Direct attribute access


def basic_display_menu_options(options: List[str], current_index: int, title: str) -> None:
    """Displays a basic text-based vertical menu with selection indicator.

    Args:
        options (List[str]): A list of strings representing the menu options.
        current_index (int): The index of the currently selected option.
        title (str): The title to display above the menu.
    """
    print(title)
    for i, option in enumerate(options):
        prefix = "-> " if i == current_index else "   "  # Corrected spacing for alignment
        print(f"{prefix}{option}")
    print()
    print("Use (▲) Up / Down (▼) arrow keys to select. Press Enter to confirm.")
