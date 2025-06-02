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
    """Get user input using either rich or basic input based on settings.

    Args:
        settings (DifficultyData | None): The current difficulty settings, or None.
        prompt_message (str): The prompt message to display to the user.

    Returns:
        str: The user's input.

    """
    if not settings or settings.heart_point_mode:
        return rich_get_input(prompt_message)
    return basic_get_input(prompt_message)


def print_streak_leaderboard(settings: DifficultyData | None, streaks: list[StreakEntry]) -> None:
    """Display the winning streak leaderboard using rich or basic formatting.

    If settings are not provided or if heart_point_mode is True, it defaults to the rich display.

    Args:
        settings (DifficultyData | None): The current difficulty settings, or None.
        streaks (list[StreakEntry]): List of streak entries to display.

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
    """Display wizard selection using either rich or basic formatting based on settings.

    Args:
        settings (DifficultyData | None): The current difficulty settings, or None.
        wizard (WizardData): The wizard data to display.
        wizard_index (int): The index of the wizard.

    """
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
    """Print the game grid using either rich or basic formatting based on settings.

    Args:
        settings (DifficultyData | None): The current difficulty settings, or None.
        grid (list[list[str | None]] | None): The grid to display.
        highlighted_coords (set[tuple[int, int]] | list[tuple[int, int]] | None): Coordinates to highlight.
        highlight_color (str | None): Color for highlights.
        letters_color (str): Color for letters.
        hidden_color (str): Color for hidden cells.
        title (str): Title for the grid display.
        border_style (str): Style for the border.

    """
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
    """Print game statistics using either rich or basic formatting based on settings.

    Args:
        settings (DifficultyData | None): The current difficulty settings, or None.
        statistics_obj (GameStatisticsData): The statistics object to display.
        border_style (str): Style for the border.
        grid (list[list[str | None]] | None): The grid to display.
        selected_wizard (WizardData): The selected wizard.
        game_st (GameStateData): The current game state.

    """
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
    """Print a message using either rich or basic formatting based on settings.

    Args:
        settings (DifficultyData | None): The current difficulty settings, or None.
        message (str): The message to display.
        style (str | None): The style to apply to the message.
        border_style (str): Style for the border.
        title (str | None): Title for the message box.
        title_align (str): Alignment for the title.
        expand (bool): Whether to expand the message box.
        width (int | None): Width of the message box.
        justify (str): Justification for the message text.

    """
    if not settings or settings.heart_point_mode:
        rich_print_message(
            message=message,
            style=style,
            border_style=border_style,
            title=title,
            title_align=title_align,
            expand=expand,
            width=width,
            justify=justify,
        )
    else:
        basic_print_message(message)


def display_wizard_art(settings: DifficultyData | None, wizard: WizardData) -> None:
    """Display wizard art using either rich or basic formatting based on settings.

    Args:
        settings (DifficultyData | None): The current difficulty settings, or None.
        wizard (WizardData): The wizard data to display.

    """
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
    """Display menu options using either rich or basic formatting based on settings.

    Args:
        settings (DifficultyData | None): The current difficulty settings, or None.
        options (list[str]): List of menu options.
        current_index (int): The index of the currently selected option.
        title (str): Title for the menu.

    """
    if not settings or settings.heart_point_mode:
        rich_display_menu_options(settings, options, current_index, title)
    else:
        basic_display_menu_options(
            options,
            current_index,
            title,
        )
