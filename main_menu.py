from getkey import getkey, keys
from display import clear_screen

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

HEART_POINTS_SETTINGS = {
    "Simple Scroll": {
        "grid": {"height": 15, "width": 25},
        "words_on_board_needed": {"minimum": 21, "maximum": 25},
        "max_word_length": 6,
        "min_subword_length": 3,
    },
    "Spellbook": {
        "grid": {"height": 15, "width": 35},
        "words_on_board_needed": {"minimum": 30, "maximum": 40},
        "max_word_length": 6,
        "min_subword_length": 3,
    },
    "Grand Tome": {
        "grid": {"height": 18, "width": 45},
        "words_on_board_needed": {"minimum": 50, "maximum": 60},
        "max_word_length": 7,
        "min_subword_length": 3,
    },
    "Arcane Codex": {
        "grid": {"height": 18, "width": 55},
        "words_on_board_needed": {"minimum": 100, "maximum": 110},
        "max_word_length": 7,
        "min_subword_length": 3,
    },
    "The Great Bibliotheca": {
        "grid": {"height": 25, "width": 75},
        "words_on_board_needed": {"minimum": 200, "maximum": 250},
        "max_word_length": 8,
        "min_subword_length": 3,
    },
    # Note: "Custom" is handled separately.
}

NO_HEART_POINTS_SETTINGS = {
    "grid": {"height": 15, "width": 25},
    "words_on_board_needed": {"minimum": 21, "maximum": 25},
    "lexicon_path": "corncob-lowercase.txt",
    "max_word_length": 6,
    "min_subword_length": 3,
    "design": False,
}


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
        settings["design"] = True

        print(f"Selected difficulty: {selected_option}")
        return settings

    elif selected_option == "Custom":
        ...


run_heart_points_menu()
