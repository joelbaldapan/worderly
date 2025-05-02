from getkey import getkey, keys
from display import clear_screen

MENU_OPTIONS = ["Start Game", "Check Leaderboards", "Tutorial", "Exit Game"]


def display_main_menu(current_index):
    clear_screen()
    print("=== Main Menu ===\n")
    for i, option in enumerate(MENU_OPTIONS):
        prefix = "-> " if i == current_index else "   "
        print(f"{prefix}{option}")


def option1():
    print("Game has started")


def main_menu_loop():
    current_index = 0
    while True:
        display_main_menu(current_index)
        key = getkey()

        if key == keys.UP:
            current_index = (current_index - 1) % len(MENU_OPTIONS)
        elif key == keys.DOWN:
            current_index = (current_index + 1) % len(MENU_OPTIONS)
        elif key == keys.ENTER or key == "\r" or key == "\n":
            selected = MENU_OPTIONS[current_index]
            clear_screen()
            if selected == "Start Game":
                option1()
            elif selected == "Check Leaderboards":
                print("These are the Leaderboards")
            elif selected == "Tutorial":
                print("Starting Tutorial Now")
            elif selected == "Exit Game":
                print("Excellent wandwork wizard!")
                break
            input("\n> Press Enter to return to menu...")


main_menu_loop()
