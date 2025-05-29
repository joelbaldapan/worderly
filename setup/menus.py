import sys

from getkey import getkey, keys

from data.settings_details import HEART_POINTS_SETTINGS, NO_HEART_POINTS_SETTINGS
from data.wizards_details import WIZARDS_DATA
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


# ************************************
# MENU SELECTION LOGIC
# ************************************


def select_from_menu(options, title="+.+.+.+ Menu +.+.+.+", show_main_title=False):
    """Handles navigation and selection for vertical text-based menus.

    Displays options, allows navigation with UP/DOWN keys, and returns the
    selected option when ENTER is pressed.

    Args:
        options (list[str]): A list of strings representing the menu choices.
        title (str, optional):
            The title to display above the menu. Defaults to "+.+.+.+ Menu +.+.+.+".
        show_main_title (bool, optional):
            Indicates whether to display the large ASCII art title (MAIN_TITLE).
            Defaults to False.

    Returns:
        str | None: The string of the selected option, or None if the options
                    list was empty.

    """
    if not options:
        # Handle empty options
        print("Warning: No options provided for the menu.")
        return None

    current_index = 0
    while True:
        # DISPLAY
        clear_screen()
        if show_main_title:
            print_message(
                settings=None,
                message=MAIN_TITLE,
                style="magenta",
                border_style="black",
            )

        display_menu_options(
            settings=None, options=options, current_index=current_index, title=title,
        )

        # GET INPUT
        key = getkey()

        if key == keys.UP:
            current_index = (current_index - 1) % len(options)
        elif key == keys.DOWN:
            current_index = (current_index + 1) % len(options)
        elif key in {keys.ENTER, "\r", "\n"}:
            return options[current_index]


def select_character_menu(settings):
    """Handles the character selection menu interface.

    Displays wizard art and details, allows navigation with LEFT/RIGHT keys,
    and returns the selected wizard's data dictionary upon pressing ENTER.
    Includes basic error handling.

    Args:
        settings (dict | None):
            The game settings dictionary. Has the key 'heart_point_mode' (bool)
            which decides whether to print in basic text or Rich mode.

    Returns:
        dict:
            The dictionary containing the selected wizard's data from
            WIZARDS_DATA. Returns the default wizard (index 0) if an
            exception occurs during selection.

    """
    current_index = 0
    num_wizards = len(WIZARDS_DATA)

    while True:
        try:
            display_wizard_selection(settings, current_index)

            key = getkey()

            if key == keys.LEFT:
                current_index = (current_index - 1) % num_wizards
            elif key == keys.RIGHT:
                current_index = (current_index + 1) % num_wizards
            elif key in {keys.ENTER, "\r", "\n"}:
                # CONFIRM
                return WIZARDS_DATA[current_index]
        except Exception as e:
            # Fallback on error
            clear_screen()
            print_message(
                settings,
                f"An error occurred during character selection. Normal class will be chosen:\n{e}",
                border_style="red",
            )
            get_input(settings, "  > Press Enter to continue... ")
            return WIZARDS_DATA[0]  # Return default wizard


def get_player_name(settings, selected_wizard):
    """Prompts the player to enter their name and validates it.

    Displays the selected wizard's art and a prompt. Loops until a valid name
    (non-empty, alphabetic, within MAX_NAME_LENGTH) is entered. Displays error
    messages for invalid input.

    Args:
        settings (dict | None): The game settings dictionary.
        selected_wizard (dict):
            The dictionary containing data for the wizard (used for display).

    Returns:
        str: The validated player name entered by the user.

    """
    clear_screen()

    display_wizard_art(settings, selected_wizard)
    print_message(
        settings,
        "Mighty wizard, please enter your name!",
        border_style=selected_wizard.get("color", "white"),
        title="Input",
    )

    while True:
        name = get_input(settings, "  > Name: ").strip()
        clear_screen()  # Clear after input, before potential error message
        display_wizard_art(settings, selected_wizard)  # Redisplay art
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
            return name  # Return valid name


def initialize_player_info(settings):
    """Initializes player name and selected wizard based on game mode.

    If 'heart_point_mode' is True in settings, runs the character selection
    and name input menus. Otherwise, returns None for name and the default
    wizard data.

    Args:
        settings (dict):
            The game settings dictionary. Must contain the key
            'heart_point_mode' (bool).

    Returns:
        tuple[str | None, dict]: A tuple containing:
            - The player's name (str) or None.
            - The selected wizard's data dictionary (dict).

    """
    if settings["heart_point_mode"]:
        # GET PLAYER NAME AND WIZARD IN HP MODE
        selected_wizard = select_character_menu(settings)
        player_name = get_player_name(settings, selected_wizard)
        return player_name, selected_wizard
    else:
        # NO HEART POINTS MODE - Use defaults
        return None, WIZARDS_DATA[0]  # Send white wizard as default


# ************************************
# MENUS
# ************************************


MENU1_OPTIONS = [  # Heart Points Mode
    "</3 No Heart Points",
    "♥♥♥ Heart Points",
]

MENU2_OPTIONS = [  # Main Menu
    "Start Game",
    "Check Leaderboards",
    "Exit Game",
]

MENU3_OPTIONS = [  # Difficulty Menu
    "Simple Scroll",
    "Spellbook",
    "Grand Tome",
    "Arcane Codex",
    "The Great Bibliotheca",
]


def run_heart_points_menu():
    """Runs the initial menu to select the game mode (Heart Points vs No).

    Based on the selection, returns either the specific settings dictionary
    for No Heart Points mode, or None to indicate that Heart Points mode
    was chosen and the main menu should run next.

    Args:
        None

    Returns:
        dict: The settings dictionary for No Heart Points mode.

    """
    selected_option = select_from_menu(
        MENU1_OPTIONS, title="+.+.+.+ Select Heart Points Mode +.+.+.+",
    )
    if selected_option is not None:
        if selected_option == "</3 No Heart Points":
            return NO_HEART_POINTS_SETTINGS
        elif selected_option == "♥♥♥ Heart Points":
            # Indicate HP mode selected, main menu should follow
            return None
    else:
        # Handle case where user might somehow exit selection
        # Fallback to choosingn Heart Points mode
        return None
    return None


def run_main_menu():
    """Runs the main menu loop for Heart Points mode.

    Displays options (Start, Leaderboards, Exit). Handles leaderboard display
    or proceeds to the difficulty menu if "Start Game" is chosen. The loop
    continues until "Start Game" or "Exit Game" (or None selection) occurs.

    Args:
        None

    Returns:
        dict:
            The settings dictionary returned by run_difficulty_menu if
            "Start Game" is selected. If the user selects "Exit Game",
            then the program closes

    """
    title = "+.+.+.+ Main Menu +.+.+.+"

    # Keep running until Start Game/Exit Game is chosen by the user
    while True:
        selected_option = select_from_menu(
            MENU2_OPTIONS, title=title, show_main_title=True,
        )
        if selected_option is not None:
            if selected_option == "Start Game":
                # Run Difficulty Menu and return its result
                return run_difficulty_menu()
            elif selected_option == "Check Leaderboards":
                # Display leaderboard and loop back to main menu
                clear_screen()
                leaderboard = load_leaderboard()
                print_leaderboard(settings=None, leaderboard=leaderboard)
                get_input(
                    settings=None, prompt_message="  > Press Enter to continue... ",
                )
                # Continue loop to show main menu again
            elif selected_option == "Exit Game":
                # Exit program
                print_message(
                    settings=None,
                    message="Farewell, wizard! May you venture back on this journey.",
                    border_style="magenta",
                    title="Input",
                )
                sys.exit()
        else:
            # Handle case where user might somehow exit selection
            # Fall back to running difficulty menu
            return run_difficulty_menu()


def run_difficulty_menu():
    """Runs the difficulty selection menu.

    Allows the user to choose a predefined difficulty or a custom board setup.
    Returns the corresponding settings dictionary.

    Args:
        None

    Returns:
        dict:
            A dictionary containing the game settings for the chosen
            difficulty, or None if the selection process fails.

    """
    title = "+.+.+.+ Select Difficulty / Book +.+.+.+"
    selected_option = select_from_menu(MENU3_OPTIONS, title=title, show_main_title=True)
    print(f"Selected Option: {selected_option}")  # Keep for debugging

    settings = None
    if selected_option in HEART_POINTS_SETTINGS:
        # Get the base settings dictionary
        base_settings = HEART_POINTS_SETTINGS[selected_option]

        # Create copy of settings and have `heart_point_mode` to be True
        settings = base_settings.copy()
        settings["heart_point_mode"] = True

        return settings
    else:
        # If somehow the user chooses a different setting,
        # then fallback to first choice
        return HEART_POINTS_SETTINGS[MENU3_OPTIONS[0]]
