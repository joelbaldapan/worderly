import sys
from typing import List, Optional, Tuple

from getkey import getkey, keys

# Import the new dataclasses and the data constants
from data.settings_details import HEART_POINTS_SETTINGS, NO_HEART_POINTS_SETTINGS, DifficultyData
from data.wizards_details import WIZARDS_DATA, WizardData

from display.display import (
    display_menu_options,
    display_wizard_art,
    display_wizard_selection,
    get_input,
    print_leaderboard,
    print_message,
)
from display.display_utils import clear_screen
from leaderboard.leaderboard import load_leaderboard

MAX_NAME_LENGTH = 10
MAIN_TITLE = """
 .+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.
(                                                                                 )
 )                                                                               (
(    ██╗    ██╗██╗███████╗ █████╗ ██████╗ ██████╗ ███████╗     ██████╗ ███████╗   )
 )   ██║    ██║██║╚══███╔╝██╔══██╗██╔══██╗██╔══██╗██╔════╝    ██╔═══██╗██╔════╝  (
(    ██║ █╗ ██║██║  ███╔╝ ███████║██████╔╝██║  ██║███████╗    ██║   ██║█████╗     )
 )   ██║███╗██║██║ ███╔╝  ██╔══██║██╔══██╗██║  ██║╚════██║    ██║   ██║██╔══╝    (
(    ╚███╔███╔╝██║███████╗██║  ██║██║  ██║██████╔╝███████║    ╚██████╔╝██║        )
 )    ╚══╝╚══╝ ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝     ╚═════╝ ╚═╝       (
(        ██╗    ██╗ ██████╗ ██████╗ ██████╗ ███████╗██████╗ ██╗  ██╗   ██╗        )
 )       ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██║  ╚██╗ ██╔╝       (
(        ██║ █╗ ██║██║   ██║██████╔╝██║  ██║█████╗  ██████╔╝██║   ╚████╔╝         )
 )       ██║███╗██║██║   ██║██╔══██╗██║  ██║██╔══╝  ██╔══██╗██║    ╚██╔╝         (
(        ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║███████╗██║           )
 )        ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝          (
(                   ██████╗ ██╗      █████╗  ██████╗███████╗██╗                   )
 )                  ██╔══██╗██║     ██╔══██╗██╔════╝██╔════╝██║                  (
(                   ██████╔╝██║     ███████║██║     █████╗  ██║                   )
 )                  ██╔═══╝ ██║     ██╔══██║██║     ██╔══╝  ╚═╝                  (
(                   ██║     ███████╗██║  ██║╚██████╗███████╗██╗                   )
 )                  ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝                  (
(                                                                                 )
 "+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"
"""


def select_from_menu(options: List[str], title: str = "+.+.+.+ Menu +.+.+.+", show_main_title: bool = False) -> str:
    """Handles navigation and selection for vertical text-based menus.
    Assumes options is not empty and a selection will always be made.

    Args:
        options (List[str]): A list of strings representing the menu choices.
        title (str, optional): The title to display above the menu.
        show_main_title (bool, optional): Whether to display the main game title.

    Returns:
        str: The string of the selected option.
    """
    current_index = 0
    while True:
        clear_screen()
        if show_main_title:
            print_message(
                settings=None,
                message=MAIN_TITLE,
                style="magenta",
                border_style="black",
            )

        display_menu_options(
            settings=None,
            options=options,
            current_index=current_index,
            title=title,
        )

        key = getkey()

        if key == keys.UP:
            current_index = (current_index - 1) % len(options)
        elif key == keys.DOWN:
            current_index = (current_index + 1) % len(options)
        elif key in {keys.ENTER, "\r", "\n"}:
            return options[current_index]


def select_character_menu(settings: Optional[DifficultyData]) -> WizardData:
    """Handles the character selection menu interface.

    Args:
        settings (Optional[DifficultyData]): Game settings, possibly None or DifficultyData.
                                            Used by display functions for mode.

    Returns:
        WizardData: The selected wizard's data object.
    """
    current_index = 0
    num_wizards = len(WIZARDS_DATA)

    while True:
        try:
            # Assuming display_wizard_selection is updated to take WizardData and current_index
            display_wizard_selection(settings, WIZARDS_DATA[current_index], current_index)
            key = getkey()

            if key == keys.LEFT:
                current_index = (current_index - 1) % num_wizards
            elif key == keys.RIGHT:
                current_index = (current_index + 1) % num_wizards
            elif key in {keys.ENTER, "\r", "\n"}:
                return WIZARDS_DATA[current_index]
        except Exception as e:
            clear_screen()
            print_message(
                settings,
                f"An error occurred during character selection. Normal class will be chosen:\n{e}",
                border_style="red",
            )
            get_input(settings, "  > Press Enter to continue... ")
            return WIZARDS_DATA[0]


def get_player_name(settings: Optional[DifficultyData], selected_wizard: WizardData) -> str:
    """Prompts the player to enter their name and validates it.

    Args:
        settings (Optional[DifficultyData]): Game settings, used for display mode.
        selected_wizard (WizardData): The data object for the selected wizard.

    Returns:
        str: The validated player name.
    """
    clear_screen()
    # Assuming display_wizard_art is updated to take WizardData
    display_wizard_art(settings, selected_wizard)
    print_message(
        settings,
        "Mighty wizard, please enter your name!",
        border_style=selected_wizard.color,  # Direct attribute access
        title="Input",
    )

    while True:
        name = get_input(settings, "  > Name: ").strip()
        clear_screen()
        display_wizard_art(settings, selected_wizard)
        if not name:
            print_message(
                settings,
                "Name cannot be empty. Please try again.",
                border_style="red",
                title="Input",
            )
        elif not name.isalpha():
            print_message(
                settings,
                "Name must only contain letters! Please try again.",
                border_style="red",
                title="Input",
            )
        elif len(name) > MAX_NAME_LENGTH:
            print_message(
                settings,
                f"Name cannot be longer than {MAX_NAME_LENGTH} characters. Please try again.",
                border_style="red",
                title="Input",
            )
        else:
            return name


def initialize_player_info(settings: DifficultyData) -> Tuple[Optional[str], WizardData]:
    """Initializes player name and selected wizard based on game mode.

    Args:
        settings (DifficultyData): The game settings object.

    Returns:
        Tuple[Optional[str], WizardData]: Player name (or None) and wizard data object.
    """
    if settings.heart_point_mode:  # Direct attribute access
        selected_wizard = select_character_menu(settings)
        player_name = get_player_name(settings, selected_wizard)
        return player_name, selected_wizard
    else:
        return None, WIZARDS_DATA[0]


MENU1_OPTIONS: List[str] = [
    "</3 No Heart Points",
    "♥♥♥ Heart Points",
]

MENU2_OPTIONS: List[str] = [
    "Start Game",
    "Check Leaderboards",
    "Exit Game",
]

MENU3_OPTIONS: List[str] = [
    "Simple Scroll",
    "Spellbook",
    "Grand Tome",
    "Arcane Codex",
    "The Great Bibliotheca",
]


def run_heart_points_menu() -> Optional[DifficultyData]:
    """Runs the initial menu to select the game mode.

    Returns:
        Optional[DifficultyData]: DifficultyData for No Heart Points mode, or None for HP mode.
    """
    selected_option = select_from_menu(
        MENU1_OPTIONS,
        title="+.+.+.+ Select Heart Points Mode +.+.+.+",
    )
    if selected_option == "</3 No Heart Points":
        return NO_HEART_POINTS_SETTINGS
    elif selected_option == "♥♥♥ Heart Points":
        return None
    # This path should ideally not be reached if select_from_menu guarantees a return from options
    return None


def run_main_menu() -> DifficultyData:
    """Runs the main menu loop for Heart Points mode.

    Returns:
        DifficultyData: DifficultyData object if "Start Game" is chosen, otherwise exits.
    """
    title = "+.+.+.+ Main Menu +.+.+.+"

    while True:
        selected_option = select_from_menu(
            MENU2_OPTIONS,
            title=title,
            show_main_title=True,
        )
        if selected_option == "Start Game":
            return run_difficulty_menu()
        elif selected_option == "Check Leaderboards":
            clear_screen()
            leaderboard = load_leaderboard()
            print_leaderboard(settings=None, leaderboard=leaderboard)
            get_input(
                settings=None,
                prompt_message="  > Press Enter to continue... ",
            )
        elif selected_option == "Exit Game":
            print_message(
                settings=None,
                message="Farewell, wizard! May you venture back on this journey.",
                border_style="magenta",
                title="Input",
            )
            sys.exit()
        # No 'else' needed if select_from_menu always returns a valid option


def run_difficulty_menu() -> DifficultyData:
    """Runs the difficulty selection menu.
    Assumes the user always makes a valid selection.

    Returns:
        DifficultyData: A DifficultyData object for the chosen difficulty.
    """
    title = "+.+.+.+ Select Difficulty / Book +.+.+.+"
    selected_option: str = select_from_menu(MENU3_OPTIONS, title=title, show_main_title=True)

    print(f"Selected Option (DEBUG): {selected_option}")  # Kept debug print

    difficulty_config = HEART_POINTS_SETTINGS[selected_option]
    return difficulty_config
