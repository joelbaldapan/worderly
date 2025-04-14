# ****************
# DISPLAY
# ****************
import random
import os
import subprocess
import sys


def print_grid(grid):
    for row in grid:
        print(" ".join(cell if cell else "." for cell in row))


def clear_screen():
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = "cls" if os.name == "nt" else "clear"
        subprocess.run([clear_cmd])

def shuffle_letters_statistic(middle_word):
    letters_list = list(str(middle_word).upper())
    random.shuffle(letters_list)
    return " ".join(letters_list)


def print_statistics(statistics):
    print(f"Letters:     {statistics['letters']}")
    print(f"Lives left:  {statistics['lives_left']}")
    print(f"Points:      {statistics['points']}")
    print(f"Last Guess:  {statistics['last_guess']}")


def print_message(message):
    # This function will be used for formatting printing
    print(message)


def get_input(prompt_message="Enter Guess: "):
    # This function will be used for formatting user input
    return input(prompt_message)

