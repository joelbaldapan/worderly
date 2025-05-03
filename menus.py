from getkey import getkey, keys
from display import (
    clear_screen,
    display_selection,
    print_message,
    get_input,
    display_wizard_art,
)

from settings_details import HEART_POINTS_SETTINGS, NO_HEART_POINTS_SETTINGS
from wizards_details import WIZARDS_DATA

MAX_NAME_LENGTH = 10
MAIN_TITLE = """
 .+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+. 
(                                                                                     )
 )                                                                                   ( 
(     ██╗    ██╗██╗███████╗ █████╗ ██████╗ ██████╗ ███████╗     ██████╗ ███████╗      )
 )    ██║    ██║██║╚══███╔╝██╔══██╗██╔══██╗██╔══██╗██╔════╝    ██╔═══██╗██╔════╝     ( 
(     ██║ █╗ ██║██║  ███╔╝ ███████║██████╔╝██║  ██║███████╗    ██║   ██║█████╗        )
 )    ██║███╗██║██║ ███╔╝  ██╔══██║██╔══██╗██║  ██║╚════██║    ██║   ██║██╔══╝       ( 
(     ╚███╔███╔╝██║███████╗██║  ██║██║  ██║██████╔╝███████║    ╚██████╔╝██║           )
 )     ╚══╝╚══╝ ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝     ╚═════╝ ╚═╝          ( 
(                                                                                     )
 )        ██╗    ██╗ ██████╗ ██████╗ ██████╗ ███████╗██████╗ ██╗  ██╗   ██╗          ( 
(         ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██║  ╚██╗ ██╔╝           )
 )        ██║ █╗ ██║██║   ██║██████╔╝██║  ██║█████╗  ██████╔╝██║   ╚████╔╝           ( 
(         ██║███╗██║██║   ██║██╔══██╗██║  ██║██╔══╝  ██╔══██╗██║    ╚██╔╝             )
 )        ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║███████╗██║             ( 
(          ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝              )
 )                                                                                   ( 
(                   ██████╗ ██╗      █████╗  ██████╗███████╗██╗                       )
 )                  ██╔══██╗██║     ██╔══██╗██╔════╝██╔════╝██║                      ( 
(                   ██████╔╝██║     ███████║██║     █████╗  ██║                       )
 )                  ██╔═══╝ ██║     ██╔══██║██║     ██╔══╝  ╚═╝                      ( 
(                   ██║     ███████╗██║  ██║╚██████╗███████╗██╗                       )
 )                  ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝                      ( 
(                                                                                     )
 "+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+" 
"""


def select_from_menu(options, title="+.+.+.+ Menu +.+.+.+"):
    if not options:
        # Handle empty options list gracefully
        print("Warning: No options provided for the menu.")
        return None

    current_index = 0
    while True:
        # DISPLAY
        clear_screen()
        print(f"{title}\n")
        for i, option in enumerate(options):
            prefix = "-> " if i == current_index else "   "
            print(f"{prefix}{option}")

        # GET INPUT
        key = getkey()

        if key == keys.UP:
            current_index = (current_index - 1) % len(options)
        elif key == keys.DOWN:
            current_index = (current_index + 1) % len(options)
        elif key == keys.ENTER or key == "\r" or key == "\n":
            selected_option = options[current_index]
            return selected_option  # Return the chosen option string


def select_character_menu(settings):
    current_index = 0
    num_wizards = len(WIZARDS_DATA)

    while True:
        try:
            display_selection(settings, current_index)

            key = getkey()

            if key == keys.LEFT:
                current_index = (current_index - 1) % num_wizards
            elif key == keys.RIGHT:
                current_index = (current_index + 1) % num_wizards
            elif key == keys.ENTER or key == "\r" or key == "\n":
                # CONFIRM
                selected_wizard = WIZARDS_DATA[current_index]
                return selected_wizard
        except Exception as e:
            clear_screen()
            print_message(
                settings,
                f"An error occurred during character selection. Normal class will be chosen:\n{e}",
                border_style="red",
            )
            get_input(settings, "  > Press Enter to continue... ")
            return WIZARDS_DATA[0]
        


def get_player_name(settings, selected_wizard):
    clear_screen()

    display_wizard_art(settings, selected_wizard)
    print_message(
        settings,
        "Mighty wizard, please enter your name!",
        border_style=selected_wizard["color"],
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



def initialize_player_info(settings):
    if settings["heart_point_mode"]:
        # GET PLAYER NAME
        selected_wizard = select_character_menu(settings)
        player_name = get_player_name(settings, selected_wizard)
        return player_name, selected_wizard
    else:
        # NO HEART POINTS. Don't ask for details.
        return None, WIZARDS_DATA[0]  # Send white wizard as default (no powerups)


# ************************************
# MENUS
# ************************************


MENU1_OPTIONS = [  # Heart Points Mode
    "No Heart Points",
    "Heart Points",
]

MENU2_OPTIONS = [  # Main Menu
    "Start Game",
    "Check Leaderboards",
    "Exit Game",
]

MENU3_OPTIONS = [
    "Simple Scroll",
    "Spellbook",
    "Grand Tome",
    "Arcane Codex",
    "The Great Bibliotheca"
]


def run_heart_points_menu():
    selected_option = select_from_menu(
        MENU1_OPTIONS, title="+.+.+.+ Select Heart Points Mode +.+.+.+"
    )
    if selected_option is not None:
        if selected_option == "No Heart Points":
            return NO_HEART_POINTS_SETTINGS
        elif selected_option == "Heart Points":
            # Run Main Menu
            return run_main_menu()
    else:
        print("No option selected from Heart Points menu.")


def run_main_menu():
    title = MAIN_TITLE + "\n+.+.+.+ Main Menu +.+.+.+"
    selected_option = select_from_menu(MENU2_OPTIONS, title=title)
    if selected_option is not None:
        if selected_option == "Start Game":
            # Run Difficulty Menu
            return run_difficulty_menu()
        elif selected_option == "Check Leaderboards":
            print("Chosen: 1")
        elif selected_option == "Exit Game":
            print("Chosen: 2")
    else:
        print("No option selected from Main menu.")


def run_difficulty_menu():
    title = MAIN_TITLE + "\n+.+.+.+ Select Difficulty / Book +.+.+.+"
    selected_option = select_from_menu(MENU3_OPTIONS, title=title)
    print(selected_option)

    settings = None
    if selected_option in HEART_POINTS_SETTINGS:
        # Get the base settings dictionary
        base_settings = HEART_POINTS_SETTINGS[selected_option]

        # Create copy of settings, and have design=True
        settings = base_settings.copy()
        settings["heart_point_mode"] = True

        print(f"Selected difficulty: {selected_option}")
        return settings

    elif selected_option == "Custom":
        ...
