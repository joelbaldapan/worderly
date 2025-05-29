# display/display.py

from typing import List, Optional, Dict, Set, Tuple, Any, Union  # Added Union

# Import dataclasses
from data.settings_details import DifficultyData
from data.wizards_details import WizardData

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

DEFAULT_BORDER_STYLE = "bright_cyan"


def print_grid(
    settings: Optional[DifficultyData],
    grid: Optional[List[List[Optional[str]]]],
    highlighted_coords: Optional[Union[Set[Tuple[int, int]], List[Tuple[int, int]]]] = None,
    highlight_color: Optional[str] = None,  # Made Optional, rich version needs it
    letters_color: str = "black",
    hidden_color: str = "black",  # Consistency with rich version
    title: str = "THE WIZARDS OF WORDERLY PLACE",
    border_style: str = DEFAULT_BORDER_STYLE,
) -> None:
    """Prints the game grid using either rich or basic formatting based on settings."""
    active_highlighted_coords = highlighted_coords if highlighted_coords is not None else []  # Default to empty list

    if not settings or settings.heart_point_mode:
        # Ensure highlight_color is provided if None, or handle in rich_print_grid
        effective_highlight_color = highlight_color if highlight_color is not None else "yellow"  # Default for rich
        rich_print_grid(
            grid,
            active_highlighted_coords,
            effective_highlight_color,
            letters_color,
            hidden_color,  # Pass hidden_color
            title,
            border_style,
        )
    else:
        # basic_print_grid typically doesn't handle highlights or complex coloring
        basic_print_grid(grid)


def print_statistics(
    settings: Optional[DifficultyData],
    statistics: Dict[str, Any],
    border_style: str,  # Used by rich version
    grid: Optional[List[List[Optional[str]]]],  # Used by rich version for layout
    selected_wizard: WizardData,  # Now WizardData
    game_state: Dict[str, Any],  # Used by rich version
) -> None:
    """Prints game statistics using either rich or basic formatting based on settings."""
    if not settings or settings.heart_point_mode:
        rich_print_statistics(
            statistics,
            border_style,
            grid,
            selected_wizard,  # Pass WizardData
            game_state,
        )
    else:
        # basic_print_statistics only takes 'statistics'
        basic_print_statistics(statistics)


def print_message(
    settings: Optional[DifficultyData],
    message: str,
    style: Optional[str] = None,
    border_style: str = DEFAULT_BORDER_STYLE,
    title: Optional[str] = None,
    title_align: str = "left",
    expand: bool = False,
    width: Optional[int] = None,
    justify: str = "left",
) -> None:
    """Prints a message using either rich or basic formatting based on settings."""
    if not settings or settings.heart_point_mode:
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


def get_input(settings: Optional[DifficultyData], prompt_message: str = "Enter Guess") -> str:
    """Gets user input using either rich or basic input based on settings."""
    if not settings or settings.heart_point_mode:
        return rich_get_input(prompt_message)
    else:
        return basic_get_input(prompt_message)


def print_leaderboard(settings: Optional[DifficultyData], leaderboard: List[Dict[str, Any]]) -> None:
    """Prints the leaderboard using either rich or basic formatting based on settings."""
    if not settings or settings.heart_point_mode:
        rich_print_leaderboard(leaderboard)
    else:
        basic_print_leaderboard(leaderboard)


# Signature changed to match call from menus.py
def display_wizard_selection(
    settings: Optional[DifficultyData],
    wizard: WizardData,  # Changed from wizard_index to WizardData object
    wizard_index: int,  # Kept wizard_index if basic version or rich version still needs it
) -> None:
    """Displays wizard selection using either rich or basic formatting based on settings."""
    if not settings or settings.heart_point_mode:
        # rich_display_wizard_selection expects (settings, wizard_object, wizard_index)
        rich_display_wizard_selection(settings, wizard, wizard_index)
    else:
        # basic_display_wizard_selection will need to be updated to accept similar args
        # or adapt. For now, let's assume it can take the wizard object.
        # If it strictly needs only index, this call needs adjustment or basic_display_wizard_selection needs to lookup.
        basic_display_wizard_selection(settings, wizard, wizard_index)


# Signature changed to accept WizardData
def display_wizard_art(settings: Optional[DifficultyData], wizard: WizardData) -> None:
    """Displays wizard art using either rich or basic formatting based on settings."""
    if not settings or settings.heart_point_mode:
        # rich_display_wizard_art expects (settings, wizard_object)
        rich_display_wizard_art(settings, wizard)
    else:
        # basic_display_wizard_art will need to be updated to accept WizardData
        basic_display_wizard_art(settings, wizard)


def display_menu_options(
    settings: Optional[DifficultyData], options: List[str], current_index: int, title: str
) -> None:
    """Displays menu options using either rich or basic formatting based on settings."""
    if not settings or settings.heart_point_mode:
        # rich_display_menu_options expects (settings, options, current_index, title)
        rich_display_menu_options(settings, options, current_index, title)
    else:
        basic_display_menu_options(
            options, current_index, title
        )  # basic doesn't need settings if it doesn't use HEART_POINTS_SETTINGS
