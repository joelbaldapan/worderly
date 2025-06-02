from data.settings_details import DifficultyData
from data.wizards_details import WizardData
from display.display_basic import (
    basic_display_menu_options,
    basic_display_wizard_art,
    basic_display_wizard_selection,
    basic_get_input,
    basic_print_grid,
    basic_print_message,
    basic_print_statistics,
    basic_print_streak_leaderboard,
)
from display.display_rich import (
    rich_display_menu_options,
    rich_display_wizard_art,
    rich_display_wizard_selection,
    rich_get_input,
    rich_print_grid,
    rich_print_message,
    rich_print_statistics,
    rich_print_streak_leaderboard,
)
from gameplay.game_state_handler import GameStateData, GameStatisticsData
from leaderboard.streak_handler import StreakEntry

DEFAULT_BORDER_STYLE = "bright_cyan"


def get_input(settings: DifficultyData | None, prompt_message: str = "Enter Guess") -> str:
    """Get user input using either rich or basic input based on settings."""
    if not settings or settings.heart_point_mode:
        return rich_get_input(prompt_message)
    else:
        return basic_get_input(prompt_message)


def print_streak_leaderboard(settings: DifficultyData | None, streaks: list[StreakEntry]) -> None:
    """Displays the winning streak leaderboard using rich or basic formatting.
    If settings are not provided (e.g. viewing from main menu before game mode select),
    or if heart_point_mode is True, it defaults to the rich display.
    """
    if not settings or settings.heart_point_mode:
        rich_print_streak_leaderboard(streaks)
    else:
        basic_print_streak_leaderboard(streaks)


def display_wizard_selection(
    settings: DifficultyData | None,
    wizard: WizardData,
    wizard_index: int,
) -> None:
    """Display wizard selection using either rich or basic formatting based on settings."""
    if not settings or settings.heart_point_mode:
        rich_display_wizard_selection(settings, wizard, wizard_index)
    else:
        basic_display_wizard_selection(settings, wizard, wizard_index)


def print_grid(  # noqa: PLR0913, PLR0917
    settings: DifficultyData | None,
    grid: list[list[str | None]] | None,
    highlighted_coords: set[tuple[int, int]] | list[tuple[int, int]] | None = None,
    highlight_color: str | None = None,
    letters_color: str = "black",
    hidden_color: str = "black",
    title: str = "THE WIZARDS OF WORDERLY PLACE",
    border_style: str = DEFAULT_BORDER_STYLE,
) -> None:
    """Print the game grid using either rich or basic formatting based on settings."""
    active_highlighted_coords = highlighted_coords if highlighted_coords is not None else []

    if not settings or settings.heart_point_mode:
        effective_highlight_color = highlight_color if highlight_color is not None else "yellow"
        rich_print_grid(
            grid,
            active_highlighted_coords,
            effective_highlight_color,
            letters_color,
            hidden_color,
            title,
            border_style,
        )
    else:
        basic_print_grid(grid)


def print_statistics(  # noqa: PLR0913, PLR0917
    settings: DifficultyData | None,
    statistics_obj: GameStatisticsData,
    border_style: str,
    grid: list[list[str | None]] | None,
    selected_wizard: WizardData,
    game_st: GameStateData,
) -> None:
    """Print game statistics using either rich or basic formatting based on settings."""
    if not settings or settings.heart_point_mode:
        rich_print_statistics(
            statistics_obj,
            border_style,
            grid,
            selected_wizard,
            game_st,
        )
    else:
        basic_print_statistics(statistics_obj)


def print_message(  # noqa: PLR0913, PLR0917
    settings: DifficultyData | None,
    message: str,
    style: str | None = None,
    border_style: str = DEFAULT_BORDER_STYLE,
    title: str | None = None,
    title_align: str = "left",
    *,
    expand: bool = False,
    width: int | None = None,
    justify: str = "left",
) -> None:
    """Print a message using either rich or basic formatting based on settings."""
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


def display_wizard_art(settings: DifficultyData | None, wizard: WizardData) -> None:
    """Display wizard art using either rich or basic formatting based on settings."""
    if not settings or settings.heart_point_mode:
        rich_display_wizard_art(settings, wizard)
    else:
        basic_display_wizard_art(settings, wizard)


def display_menu_options(
    settings: DifficultyData | None,
    options: list[str],
    current_index: int,
    title: str,
) -> None:
    """Display menu options using either rich or basic formatting based on settings."""
    if not settings or settings.heart_point_mode:
        rich_display_menu_options(settings, options, current_index, title)
    else:
        basic_display_menu_options(
            options,
            current_index,
            title,
        )
