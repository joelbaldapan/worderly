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


menu1_options = [  # Heart Points Mode
    "No Heart Points",
    "Heart Points",
]

menu2_options = [  # Main Menu
    "Start Game",
    "Check Leaderboards",
    "Exit Game",
]

menu3_options = [  # Difficulty / Book Selection
    "Simple Scroll",
    "Spellbook",
    "Grand Tome",
    "Arcane Codex",
    "The Great Bibliotheca",
    "Custom",
]


def run_heart_points_menu():
    selected_option = select_from_menu(
        menu1_options, title="+.+.+.+ Select Heart Points Mode +.+.+.+"
    )
    if selected_option is not None:
        if selected_option == "No Heart Points":
            print("Chosen: 0")
        elif selected_option == "Heart Points":
            print("Chosen: 1")
    else:
        print("No option selected from Heart Points menu.")


def run_main_menu():
    title = MAIN_TITLE + "\n+.+.+.+ Main Menu +.+.+.+"
    selected_option = select_from_menu(menu2_options, title=title)
    if selected_option is not None:
        if selected_option == "Start Game":
            print("Chosen: 0")
        elif selected_option == "Check Leaderboards":
            print("Chosen: 1")
        elif selected_option == "Exit Game":
            print("Chosen: 2")
    else:
        print("No option selected from Main menu.")


def run_difficulty_menu():
    title = MAIN_TITLE + "\n+.+.+.+ Select Difficulty / Book +.+.+.+"
    selected_option = select_from_menu(
        menu3_options, title=title
    )
    if selected_option is not None:
        if selected_option == "Simple Scroll":
            print("Chosen: 0")
        elif selected_option == "Spellbook":
            print("Chosen: 1")
        elif selected_option == "Grand Tome":
            print("Chosen: 2")
        elif selected_option == "Arcane Codex":
            print("Chosen: 3")
        elif selected_option == "The Great Bibliotheca":
            print("Chosen: 4")
        elif selected_option == "Custom":
            print("Chosen: 5")
    else:
        print("No option selected from Difficulty menu.")


run_heart_points_menu()
run_main_menu()
run_difficulty_menu()
