# ****************
# PLAYER INFO INITIALIZERR
# ****************
from getkey import getkey, keys
from display import (
    clear_screen,
    display_selection,
    print_message,
    get_input,
    display_wizard_art,
)

from wizards_details import WIZARDS_DATA
from leaderboard import DELIMITER

MAX_NAME_LENGTH = 10


def get_player_name(selected_wizard):
    clear_screen()

    display_wizard_art(selected_wizard)
    print_message(
        "Mighty wizard, please enter your name!",
        border_style=selected_wizard["color"], title="Input"
    )
    
    while True:
        name = get_input("  > Name: ").strip()
        clear_screen()
        display_wizard_art(selected_wizard)
        if not name:
            print_message("Name cannot be empty. Please try again.", border_style="red", title="Input")
        elif DELIMITER in name:
            print_message(
                f"Name cannot contain the character '{DELIMITER}'. Please try again.",
                border_style="red", title="Input"
            )
        elif len(name) > MAX_NAME_LENGTH:
            print_message(
                f"Name cannot be longer than {MAX_NAME_LENGTH} characters. Please try again.",
                border_style="red", title="Input"
            )
        else:
            return name


def select_character():
    current_index = 0
    num_wizards = len(WIZARDS_DATA)

    while True:
        try:
            display_selection(current_index)

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
                f"An error occurred during character selection. Normal class will be chosen:\n{e}",
                border_style="red",
            )
            get_input("  > Press Enter to continue... ")
            return WIZARDS_DATA[0]


def initialize_player_info():
    # GET PLAYER NAME
    selected_wizard = select_character()

    player_name = get_player_name(selected_wizard)
    return player_name, selected_wizard
