# ****************
# DISPLAY
# ****************
from display.display_basic import (
    basic_print_grid,
    basic_print_statistics,
    basic_print_message,
    basic_get_input,
    basic_print_leaderboard,
    basic_display_wizard_selection,
    basic_display_wizard_art,
    basic_display_menu_options,
)
from display.display_rich import (
    rich_print_grid,
    rich_print_statistics,
    rich_print_message,
    rich_get_input,
    rich_print_leaderboard,
    rich_display_wizard_selection,
    rich_display_wizard_art,
    rich_display_menu_options,
)

import random


def shuffle_letters_statistic(middle_word):
    letters_list = list(str(middle_word).upper())
    random.shuffle(letters_list)
    return " ".join(letters_list)


# ************************************************
# DISPLAY HANDLERS
# If settings not provided, print rich as default
# ************************************************


DEFAULT_BORDER_STYLE = "bright_cyan"


def print_grid(
    settings,
    grid,
    highlighted_coords={},
    highlight_color=None,
    letters_color="black",  # black to debug if it's not working
    hidden_color="black",
    title="THE WIZARDS OF WORDERLY PLACE",
    border_style=DEFAULT_BORDER_STYLE,
):
    if not settings or settings["heart_point_mode"]:
        rich_print_grid(
            grid,
            highlighted_coords,
            highlight_color,
            letters_color,
            hidden_color,
            title,
            border_style,
        )
    else:
        basic_print_grid(grid)


def print_statistics(
    settings, statistics, border_style, grid, selected_wizard, game_state
):
    if not settings or settings["heart_point_mode"]:
        rich_print_statistics(
            statistics, border_style, grid, selected_wizard, game_state
        )
    else:
        basic_print_statistics(statistics)


def print_message(
    settings,
    message,
    style=None,
    border_style=DEFAULT_BORDER_STYLE,
    title=None,
    title_align="left",
    expand=False,
    width=None,
    justify="left",
):
    if not settings or settings["heart_point_mode"]:
        rich_print_message(
            message, style, border_style, title, title_align, expand, width, justify
        )
    else:
        basic_print_message(message)


def get_input(settings, prompt_message="Enter Guess"):
    if not settings or settings["heart_point_mode"]:
        return rich_get_input(prompt_message)
    else:
        return basic_get_input(prompt_message)


def print_leaderboard(settings, leaderboard):
    if not settings or settings["heart_point_mode"]:
        return rich_print_leaderboard(settings, leaderboard)
    else:
        return basic_print_leaderboard(leaderboard)


def display_wizard_selection(settings, wizard_index):
    if not settings or settings["heart_point_mode"]:
        return rich_display_wizard_selection(settings, wizard_index)
    else:
        return basic_display_wizard_selection(wizard_index)


def display_wizard_art(settings, wizard):
    if not settings or settings["heart_point_mode"]:
        rich_display_wizard_art(wizard)
    else:
        basic_display_wizard_art(wizard)


def display_menu_options(settings, options, current_index, title):
    if not settings or settings["heart_point_mode"]:
        rich_display_menu_options(options, current_index, title)
    else:
        basic_display_menu_options(options, current_index, title)
