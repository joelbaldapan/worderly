from getkey import getkey, keys

from data.settings_details import HEART_POINTS_SETTINGS, NO_HEART_POINTS_SETTINGS, DifficultyData
from data.wizards_details import WIZARDS_DATA, WizardData
from display.display import (
    display_menu_options,
    display_wizard_art,
    display_wizard_selection,
    get_input,
    print_message,
    print_streak_leaderboard,
)
from display.display_utils import clear_screen
from leaderboard.streak_handler import load_streaks

EXIT_GAME_SENTINEL = "##EXIT_GAME_SENTINEL##"

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


def select_from_menu(options: list[str], title: str = "+.+.+.+ Menu +.+.+.+", show_main_title: bool = False) -> str:
    """Handle navigation and selection for vertical text-based menus.
    Assume options is not empty and a selection will always be made.

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


def select_character_menu(settings: DifficultyData | None) -> WizardData:
    """Handle the character selection menu interface.

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


def get_player_name(settings: DifficultyData | None, selected_wizard: WizardData) -> str:
    """Prompts the player to enter their name and validates it.

    Args:
        settings (Optional[DifficultyData]): Game settings, used for display mode.
        selected_wizard (WizardData): The data object for the selected wizard.

    Returns:
        str: The validated player name.

    """
    clear_screen()

    if settings.heart_point_mode:
        display_wizard_art(settings, selected_wizard)

    print_message(
        settings,
        "Mighty wizard, please enter your name!",
        border_style=selected_wizard.color,
        title="Input",
    )

    while True:
        name = get_input(settings, "  > Name: ").strip()
        clear_screen()
        if settings.heart_point_mode:
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


def initialize_player_info(
    settings: DifficultyData,
    current_session_player_name: str | None,
) -> tuple[str, WizardData]:
    """Initializes player name and selected wizard based on game mode.
    - HP Mode: Skips name prompt if current_session_player_name (from active streak) is provided. Allows wizard selection.
    - NHP Mode: Skips name prompt if current_session_player_name (from NHP session) is provided. Uses a default wizard.
    """
    player_name_to_use: str
    selected_wizard_for_game: WizardData

    clear_screen()
    # Get wizard
    if settings.heart_point_mode:
        # Heart Points Mode
        selected_wizard_for_game = select_character_menu(settings)  # Player chooses wizard
        display_wizard_art(settings, selected_wizard_for_game)
    else:
        # No Heart Points Mode
        selected_wizard_for_game = WIZARDS_DATA[0]  # Default wizard

    # Re-use name if in a current streak session
    if current_session_player_name:
        clear_screen()
        player_name_to_use = current_session_player_name
        print_message(settings, f"Continuing streak as {player_name_to_use}!", border_style="green")
        get_input(settings, "  > Press Enter to begin...")
    else:
        player_name_to_use = get_player_name(settings, selected_wizard_for_game)

    return player_name_to_use, selected_wizard_for_game


MENU1_OPTIONS: list[str] = [
    "</3 No Heart Points",
    "♥♥♥ Heart Points",
]

MENU2_OPTIONS: list[str] = [
    "Start Game",
    "Check Leaderboards",
    "Exit Game",
]

MENU3_OPTIONS: list[str] = [
    "Simple Scroll",
    "Spellbook",
    "Grand Tome",
    "Arcane Codex",
    "The Great Bibliotheca",
]


def run_heart_points_menu() -> DifficultyData | None:
    """Run the initial menu to select the game mode.

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
    return None


def run_main_menu() -> DifficultyData | str:
    """Runs the main menu loop for Heart Points mode.
    Returns DifficultyData if "Start Game" is chosen,
    EXIT_GAME_SENTINEL if "Exit Game", otherwise loops for leaderboards.
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
            streaks = load_streaks()
            print_streak_leaderboard(settings=None, streaks=streaks)
            get_input(
                settings=None,
                prompt_message="  > Press Enter to continue... ",
            )
        elif selected_option == "Exit Game":
            return EXIT_GAME_SENTINEL


def run_difficulty_menu() -> DifficultyData:
    """Run the difficulty selection menu.
    Assumes the user always makes a valid selection.

    Returns:
        DifficultyData: A DifficultyData object for the chosen difficulty.

    """
    title = "+.+.+.+ Select Difficulty / Book +.+.+.+"
    selected_option: str = select_from_menu(MENU3_OPTIONS, title=title, show_main_title=True)

    return HEART_POINTS_SETTINGS[selected_option]
