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

from .menu_constants import (
    EXIT_GAME_MARKER,
    MAIN_TITLE,
    MENU1_OPTIONS,
    MENU2_OPTIONS,
    MENU3_OPTIONS,
)

MAX_NAME_LENGTH = 10


def select_from_menu(
    options: list[str],
    title: str = "+.+.+.+ Menu +.+.+.+",
    *,
    show_main_title: bool = False,
) -> str:
    """Display a vertical text-based menu and handle user navigation and selection.

    Args:
        options (list[str]): List of menu option strings.
        title (str, optional): Title to display above the menu. Defaults to "+.+.+.+ Menu +.+.+.+".
        show_main_title (bool, optional): Whether to display the main game title. Defaults to False.

    Returns:
        str: The selected menu option.

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
    """Display the character selection menu and handle user navigation and selection.

    Args:
        settings (DifficultyData | None): Game settings, possibly None or DifficultyData.

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
        except KeyboardInterrupt as e:
            clear_screen()
            print_message(
                settings,
                f"An error occurred during character selection. Normal class will be chosen:\n{e}",
                border_style="red",
            )
            get_input(settings, "  > Press Enter to continue... ")
            return WIZARDS_DATA[0]


def get_player_name(settings: DifficultyData | None, selected_wizard: WizardData) -> str:
    """Prompt the player to enter their name and validate the input.

    Args:
        settings (DifficultyData | None): Game settings, used for display mode.
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
    """Initialize player name and selected wizard based on game mode.

    In Heart Points mode, allows wizard selection.
    In No Heart Points mode, uses a default wizard.

    Args:
        settings (DifficultyData): Game settings.
        current_session_player_name (str | None): Player name from current session, if any.

    Returns:
        tuple[str, WizardData]: Player name and selected wizard.

    """
    player_name_to_use: str
    selected_wizard_for_game: WizardData

    clear_screen()
    if settings.heart_point_mode:
        selected_wizard_for_game = select_character_menu(settings)
        clear_screen()
        display_wizard_art(settings, selected_wizard_for_game)
    else:
        selected_wizard_for_game = WIZARDS_DATA[0]

    if current_session_player_name:
        player_name_to_use = current_session_player_name
        print_message(
            settings,
            f"Continuing streak as {player_name_to_use}!",
            border_style="green",
        )
        get_input(settings, "  > Press Enter to begin...")
    else:
        player_name_to_use = get_player_name(settings, selected_wizard_for_game)

    return player_name_to_use, selected_wizard_for_game


def run_heart_points_menu() -> DifficultyData | None:
    """Display the initial menu to select the game mode (Heart Points or No Heart Points).

    Returns:
        DifficultyData | None: DifficultyData for No Heart Points mode, or None for HP mode.

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
    """Run the main menu loop for Heart Points mode.

    Returns:
        DifficultyData | str: DifficultyData if "Start Game" is chosen,
        EXIT_GAME_MARKER if "Exit Game", otherwise loops for leaderboards.

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
            return EXIT_GAME_MARKER


def run_difficulty_menu() -> DifficultyData:
    """Display the difficulty selection menu and return the chosen difficulty settings.

    Returns:
        DifficultyData: A DifficultyData object for the chosen difficulty.

    """
    title = "+.+.+.+ Select Difficulty / Book +.+.+.+"
    selected_option: str = select_from_menu(MENU3_OPTIONS, title=title, show_main_title=True)

    return HEART_POINTS_SETTINGS[selected_option]
