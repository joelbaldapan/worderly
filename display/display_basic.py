# ****************
# BASIC DISPLAY
# ****************
# For Wizards data
from data.wizards_details import WIZARDS_DATA
from display.display_utils import clear_screen


def basic_print_grid(grid) -> None:
    """Prints a basic text representation of the game grid to the console.

    Args:
        grid (list[list[str | None]]):
            The 2D list representing the game grid.
            None represents empty cells.

    Returns:
        None: This function prints directly to the console and returns nothing.

    """
    for row in grid:
        # Print each cell, replacing None with '.' for visibility
        print(" ".join(cell or "." for cell in row))


def basic_print_statistics(statistics) -> None:
    """Prints basic game statistics to the console.

    Args:
        statistics (dict):
            A dictionary containing game stats: 'letters', 'lives_left',
            'points', 'last_guess'.

    Returns:
        None: This function prints directly to the console and returns nothing.

    """
    print(f"Letters:     {statistics.get('letters', 'N/A')}")
    print(f"Lives left:  {statistics.get('lives_left', 'N/A')}")
    print(f"Points:      {statistics.get('points', 'N/A')}")
    print(f"Last Guess:  {statistics.get('last_guess', 'None')}")


def basic_print_message(message) -> None:
    """Prints a simple message string to the console."""
    print(message)


def basic_get_input(prompt_message=""):
    """Gets input from the user via the console."""
    return input(prompt_message)


def basic_print_leaderboard(leaderboard) -> None:
    """Prints a basic text representation of the leaderboard.

    Formats the leaderboard data with rank numbers and prints it to the console.

    Args:
        leaderboard (list[dict]):
            A list of score dictionaries, which is already sorted.
            Each dict should have 'name' and 'score' keys.

    Returns:
        None: This function prints directly to the console and returns nothing.

    """
    print("\n----------- Leaderboard -----------")
    if not leaderboard:
        print("Leaderboard is empty.")
        return

    # Calculate the width needed for the rank number for alignment
    num_entries = len(leaderboard)
    # Width is the number of digits in the largest rank number
    max_rank_width = len(str(num_entries))

    for idx, entry in enumerate(leaderboard):
        rank = idx + 1
        # Format the rank number with right-alignment and padding
        formatted_rank = f"{rank:>{max_rank_width}}"
        name = entry.get("name", "N/A")  # Safely get name
        score = entry.get("score", "N/A")  # Safely get score
        print(f"{formatted_rank} | Name: {name}, {score} points")
    print("-----------------------------------\n")


def basic_display_wizard_selection(wizard_index) -> None:
    """Displays basic text information about the currently selected wizard.

    Clears the screen, prints the wizard's art and details based on the index.

    Args:
        wizard_index (int): The index of the wizard in WIZARDS_DATA to display.

    Returns:
        None: This function prints directly to the console and returns nothing.

    """
    clear_screen()

    # Handle potential index out of bounds
    if 0 <= wizard_index < len(WIZARDS_DATA):
        wizard = WIZARDS_DATA[wizard_index]
    else:
        print(f"Error: Invalid wizard index {wizard_index}")
        return  # Avoid crashing if index is bad

    basic_display_wizard_art(wizard)
    print("-----------------------------------------")
    print(f"Name: {wizard.get('name', 'N/A')}")
    print(f"Starting Lives: {wizard.get('starting_lives', 'N/A')}")
    print()
    print(f"Powerup: {wizard.get('powerup_name', 'N/A')}")
    print(f"Powerup Description: {wizard.get('powerup_desc', 'N/A')}")
    print()
    print(f"Wizard Description: {wizard.get('description', 'N/A')}")
    print("-----------------------------------------")
    print()
    print("Use (◀) Left / Right (▶) arrow keys to select. Press Enter to confirm.")


def basic_display_wizard_art(wizard) -> None:
    """Prints the basic ASCII art for a given wizard.

    Args:
        wizard (dict): The dictionary containing wizard data, including the 'art' key.

    Returns:
        None: This function prints directly to the console and returns nothing.

    """
    # Use .get() for safer access in case 'art' key is missing
    print(wizard.get("art", "No art available."))


def basic_display_menu_options(options, current_index, title) -> None:
    """Displays a basic text-based vertical menu with selection indicator.

    Args:
        options (list[str]): A list of strings representing the menu options.
        current_index (int): The index of the currently selected option.
        title (str): The title to display above the menu.

    Returns:
        None: This function prints directly to the console and returns nothing.

    """
    print(title)
    for i, option in enumerate(options):
        prefix = "-> " if i == current_index else "   "
        print(f"{prefix}{option}")
    print()
    print("Use (▲) Up / Down (▼) arrow keys to select. Press Enter to confirm.")
