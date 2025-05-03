# ****************
# BASIC DISPLAY
# ****************
from display.display_utils import clear_screen

# For Wizards data
from data.wizards_details import WIZARDS_DATA


def basic_print_grid(grid):
    for row in grid:
        print(" ".join(cell if cell else "." for cell in row))


def basic_print_statistics(statistics):
    print(f"Letters:     {statistics['letters']}")
    print(f"Lives left:  {statistics['lives_left']}")
    print(f"Points:      {statistics['points']}")
    print(f"Last Guess:  {statistics['last_guess']}")


def basic_print_message(message):
    print(message)


def basic_get_input(prompt_message=""):
    return input(prompt_message)


def basic_print_leaderboard(leaderboard):
    print("\n----------- Leaderboard -----------")
    if not leaderboard:
        print("Leaderboard is empty.")
        return

    # Calculate the width needed for the rank number
    num_entries = len(leaderboard)
    # Width is the number of digits in the largest rank number
    max_rank_width = len(str(num_entries))

    for idx, entry in enumerate(leaderboard):
        rank = idx + 1
        # Format the rank number with right-alignment and padding
        formatted_rank = f"{rank:>{max_rank_width}}"
        print(f"{formatted_rank} | Name: {entry['name']}, {entry['score']} points")
    print("-----------------------------------\n")


def basic_display_wizard_selection(wizard_index):
    clear_screen()

    wizard = WIZARDS_DATA[wizard_index]

    basic_display_wizard_art(wizard)
    print("-----------------------------------------")
    print(f"Name: {wizard['name']}")
    print(f"Starting Lives: {wizard['starting_lives']}")
    print()
    print(f"Powerup: {wizard['powerup_name']}")
    print(f"Powerup Description: {wizard['powerup_desc']}")
    print()
    print(f"Wizard Description: {wizard['description']}")
    print("-----------------------------------------")
    print()
    print("Use (◀) Left / Right (▶) arrow keys to select. Press Enter to confirm.")


def basic_display_wizard_art(wizard):
    print(wizard["art"])


def basic_display_menu_options(options, current_index, title):
    print(title)
    for i, option in enumerate(options):
        prefix = "-> " if i == current_index else "   "
        print(f"{prefix}{option}")
    print()
    print("Use (▲) Up / Down (▼) arrow keys to select. Press Enter to confirm.")
