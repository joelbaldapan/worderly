# ****************
# DISPLAY
# ****************
from display.display_basic import (
    basic_display_menu_options,
    basic_display_wizard_art,
    basic_display_wizard_selection,
    basic_get_input,
    basic_print_grid,
    basic_print_leaderboard,
    basic_print_message,
    basic_print_statistics,
)
from display.display_rich import (
    rich_display_menu_options,
    rich_display_wizard_art,
    rich_display_wizard_selection,
    rich_get_input,
    rich_print_grid,
    rich_print_leaderboard,
    rich_print_message,
    rich_print_statistics,
)

# ************************************************
# DISPLAY HANDLERS
# If settings not provided, print rich as default
# ************************************************


DEFAULT_BORDER_STYLE = "bright_cyan"


def print_grid(
    settings,
    grid,
    highlighted_coords=None,
    highlight_color=None,
    letters_color="black",  # black to debug if it's not working
    hidden_color="black",
    title="THE WIZARDS OF WORDERLY PLACE",
    border_style=DEFAULT_BORDER_STYLE,
) -> None:
    """Prints the game grid using either rich or basic formatting based on settings."""
    if highlighted_coords is None:
        highlighted_coords = {}
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
    settings,
    statistics,
    border_style,
    grid,
    selected_wizard,
    game_state,
) -> None:
    """Prints game statistics using either rich or basic formatting based on settings."""
    if not settings or settings["heart_point_mode"]:
        rich_print_statistics(
            statistics,
            border_style,
            grid,
            selected_wizard,
            game_state,
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
) -> None:
    """Prints a message using either rich or basic formatting based on settings."""
    if not settings or settings["heart_point_mode"]:
        rich_print_message(
            message,
            style,
            border_style,
            title,
            title_align,
            expand,
            width,
            justify,
        )
    else:
        basic_print_message(message)


def get_input(settings, prompt_message="Enter Guess"):
    """Gets user input using either rich or basic input based on settings."""
    if not settings or settings["heart_point_mode"]:
        return rich_get_input(prompt_message)
    else:
        return basic_get_input(prompt_message)


def print_leaderboard(settings, leaderboard) -> None:
    """Prints the leaderboard using either rich or basic formatting based on settings."""
    if not settings or settings["heart_point_mode"]:
        rich_print_leaderboard(leaderboard)
    else:
        basic_print_leaderboard(leaderboard)


def display_wizard_selection(settings, wizard_index) -> None:
    """Displays wizard selection using either rich or basic formatting based on settings."""
    if not settings or settings["heart_point_mode"]:
        rich_display_wizard_selection(wizard_index)
    else:
        basic_display_wizard_selection(wizard_index)


def display_wizard_art(settings, wizard) -> None:
    """Displays wizard art using either rich or basic formatting based on settings."""
    if not settings or settings["heart_point_mode"]:
        rich_display_wizard_art(wizard)
    else:
        basic_display_wizard_art(wizard)


def display_menu_options(settings, options, current_index, title) -> None:
    """Displays menu options using either rich or basic formatting based on settings."""
    if not settings or settings["heart_point_mode"]:
        rich_display_menu_options(options, current_index, title)
    else:
        basic_display_menu_options(options, current_index, title)
