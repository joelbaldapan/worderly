# ****************
# DISPLAY
# ****************
from config import settings

import random
import os
import subprocess
import sys


# ****************
# UTILS
# ****************
def clear_screen():
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = "cls" if os.name == "nt" else "clear"
        subprocess.run([clear_cmd])


def shuffle_letters_statistic(middle_word):
    letters_list = list(str(middle_word).upper())
    random.shuffle(letters_list)
    return " ".join(letters_list)


# ****************
# DISPLAY HANDLERS
# ****************


def print_grid(grid):
    if settings["design"]:
        normal_print_grid(grid)
    else:
        rich_print_grid(grid)


def print_statistics(statistics):
    if settings["design"]:
        normal_print_statistics(statistics)
    else:
        rich_print_statistics(statistics)


def print_message(message):
    if settings["design"]:
        normal_print_message(message)
    else:
        rich_print_message(message)


def get_input(prompt_message="Enter Guess: "):
    if settings["design"]:
        normal_get_input(prompt_message)
    else:
        rich_get_input(prompt_message)


# ****************
# BASIC DISPLAY
# ****************


def normal_print_grid(grid):
    for row in grid:
        print(" ".join(cell if cell else "." for cell in row))


def normal_print_statistics(statistics):
    print(f"Letters:     {statistics['letters']}")
    print(f"Lives left:  {statistics['lives_left']}")
    print(f"Points:      {statistics['points']}")
    print(f"Last Guess:  {statistics['last_guess']}")


def normal_print_message(message):
    # This function will be used for formatting printing
    print(message)


def normal_get_input(prompt_message="Enter Guess: "):
    # This function will be used for formatting user input
    return input(prompt_message)


# ****************
# RICH DISPLAY
# ****************


def rich_print_grid(grid): ...


def rich_clear_screen(): ...


def rich_shuffle_letters_statistic(middle_word): ...


def rich_print_statistics(statistics): ...


def rich_print_message(message):
    # This function will be used for formatting printing
    ...


def rich_get_input(prompt_message="Enter Guess: "):
    # This function will be used for formatting user input
    ...
