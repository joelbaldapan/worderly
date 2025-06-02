from typing import Any

from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import BarColumn, Progress
from rich.table import Table
from rich.text import Text

from data.settings_details import HEART_POINTS_SETTINGS, DifficultyData
from data.wizards_details import WizardData
from gameplay.game_state_handler import GameStateData, GameStatisticsData
from leaderboard.streak_handler import StreakEntry

from .display_utils import clear_screen

DEFAULT_BORDER_STYLE = "bright_cyan"
DETAILS_PANEL_WIDTH = 40

console = Console()


def _print_empty_grid_message(grid: list[list[str | None]], title: str) -> None:
    message = "[yellow]Empty grid provided.[/yellow]"
    if grid == [[]]:
        message = "[yellow]Grid contains an empty row.[/yellow]"
    console.print(Panel(Text.from_markup(message), title=title, border_style="red"))


def _print_no_columns_message(grid: list[list[str | None]], title: str) -> None:
    if grid:
        console.print(
            Panel(
                Text.from_markup("[yellow]Grid has rows but no columns.[/yellow]"),
                title=title,
                border_style="yellow",
            ),
        )
    else:
        console.print(
            Panel(
                Text.from_markup("[yellow]Empty grid provided (no columns).[/yellow]"),
                title=title,
                border_style="red",
            ),
        )


def _get_num_cols(grid: list[list[str | None]]) -> int:
    if not grid:
        return 0
    try:
        return max(len(row) for row in grid if row)
    except ValueError:
        return 0


def _append_combo_stats(statistics: GameStatisticsData, selected_wizard: WizardData, powerup_parts: list[Any]) -> None:
    """Append combo meter Text and Progress bar to the powerup_parts list."""
    wizard_color = selected_wizard.color
    combo = statistics.combo
    combo_req = selected_wizard.combo_requirement

    if combo_req is not None and combo_req > 0:
        curr_combo = combo % combo_req
        if combo > 0 and curr_combo == 0:
            curr_combo = combo_req

        powerup_parts.append(
            Text.assemble(
                ("Combo Meter:  ", "bold cyan"),
                (f"{curr_combo} / {combo_req}\n"),
            ),
        )
        combo_progress = Progress(
            BarColumn(
                bar_width=27,
                style="dim white",
                complete_style="bright_white",
                finished_style=f"bold {wizard_color}",
            ),
            expand=False,
        )
        combo_progress.add_task("combo", total=combo_req, completed=min(curr_combo, combo_req))
        powerup_parts.extend((combo_progress, Text("\n")))


def _make_wizard_panel(
    selected_wizard: WizardData,
    game_st: GameStateData,
    border_style: str,
    wizard_panel_width: int,
    panels_height: int,
) -> Panel:
    wizard_color = selected_wizard.color
    small_wizard_art = selected_wizard.small_art.strip("\n")
    player_name_display = game_st.player_name if game_st.player_name is not None else "Player"
    art_text = Text(f"\n{small_wizard_art}", style=wizard_color, justify="left")
    name_text = Text(f"--- {player_name_display} ---", style=wizard_color, justify="center")
    wizard_panel_content = Group(art_text, name_text)
    return Panel(
        wizard_panel_content,
        title="Your Wizard",
        border_style=border_style,
        style=wizard_color,
        padding=(0, 1),
        expand=False,
        width=wizard_panel_width,
        height=panels_height,
    )


def _make_player_stats_panel(
    statistics: GameStatisticsData,
    border_style: str,
    stats_panel_width: int,
    stats_height: int,
) -> Panel:
    player_stats_content = Text.assemble(
        ("Letters:    ", "bold cyan"),
        (f"{statistics.letters}\n"),
        ("Lives left: ", "bold green"),
        (f"{statistics.lives_left}\n"),
        ("Points:     ", "bold yellow"),
        (f"{statistics.points}\n"),
        ("Last Guess: ", "bold magenta"),
        (f"{statistics.last_guess if statistics.last_guess is not None else 'None'}"),
    )
    return Panel(
        player_stats_content,
        title="Game Stats",
        title_align="left",
        border_style=border_style,
        expand=True,
        width=stats_panel_width,
        height=stats_height,
    )


def _make_powerup_stats_panel(
    statistics: GameStatisticsData,
    selected_wizard: WizardData,
    border_style: str,
    stats_panel_width: int,
    powerup_stats_height: int,
) -> Panel:
    wizard_color = selected_wizard.color
    powerup_parts: list[Any] = []
    powerup_parts.append(Text.assemble(("Combo:        ", "bold cyan"), (f"{statistics.combo}")))

    shield_turns = statistics.shield_turns
    if shield_turns > 0 and wizard_color != "bright_white" and selected_wizard.combo_requirement is not None:
        powerup_parts.append(Text.assemble(("Shield Turns: ", "bold blue"), (f"{shield_turns}")))

    if wizard_color != "bright_white":
        powerup_parts.append(Text.assemble(("Power Points: ", "bold cyan"), (f"{statistics.power_points}")))
        _append_combo_stats(statistics, selected_wizard, powerup_parts)
    else:
        powerup_parts.append(Text("\nNote: White wizards have no powerups!", style="bright_white"))

    powerup_stats_content = Group(*powerup_parts)
    return Panel(
        powerup_stats_content,
        title="Powerup Stats",
        title_align="left",
        border_style=border_style,
        expand=True,
        width=stats_panel_width,
        height=max(1, powerup_stats_height),
    )


def rich_print_statistics(
    statistics: GameStatisticsData,
    border_style: str,
    grid: list[list[str | None]] | None,
    selected_wizard: WizardData,
    game_st: GameStateData,
) -> None:
    """Print the formatted statistics panel using Rich Columns and Panels."""
    wizard_panel_width = 23
    panels_height = 15
    stats_height = 6

    grid_actual_width = wizard_panel_width + 30
    if grid and grid[0]:
        grid_actual_width = len(grid[0]) * 2 + 3

    stats_panel_width = max(10, grid_actual_width - wizard_panel_width - 1)
    powerup_stats_height = panels_height - stats_height

    wizard_panel = _make_wizard_panel(selected_wizard, game_st, border_style, wizard_panel_width, panels_height)
    player_stats_panel = _make_player_stats_panel(statistics, border_style, stats_panel_width, stats_height)
    powerup_stats_panel = _make_powerup_stats_panel(
        statistics,
        selected_wizard,
        border_style,
        stats_panel_width,
        powerup_stats_height,
    )

    stats_group = Group(player_stats_panel, powerup_stats_panel)
    full_panel = Columns([wizard_panel, stats_group], expand=False, equal=False)
    console.print(full_panel)


def _get_styled_row_items(  # noqa: PLR0913, PLR0917
    row_idx: int,
    row_data: list[str | None],
    num_cols: int,
    highlighted_coords: set[tuple[int, int]] | list[tuple[int, int]],
    highlight_color: str,
    letters_color: str,
    hidden_color: str,
) -> list[Text]:
    styled_row_items: list[Text] = []
    for col_idx in range(num_cols):
        content = "."
        current_style = "dim"
        cell_value = None
        if row_data and col_idx < len(row_data):
            cell_value = row_data[col_idx]

        if cell_value is not None:
            content = cell_value
            coord = (row_idx, col_idx)
            if coord in highlighted_coords:
                current_style = f"bold {highlight_color}"
            elif cell_value == "#":
                current_style = f"dim {hidden_color}"
            else:
                current_style = f"bold {letters_color}"

        separator = " " if col_idx < num_cols - 1 else ""
        styled_row_items.append(Text(content + separator, style=current_style))
    return styled_row_items


def rich_print_grid(  # noqa: PLR0913, PLR0917
    grid: list[list[str | None]] | None,
    highlighted_coords: set[tuple[int, int]] | list[tuple[int, int]],
    highlight_color: str,
    letters_color: str,
    hidden_color: str,
    title: str,
    border_style: str,
) -> None:
    """Print the game grid using Rich library for prettier formatting."""
    if not grid or not any(grid):
        _print_empty_grid_message(grid, title)
        return

    table = Table(show_header=False, box=None, padding=(0, 0))
    num_cols = _get_num_cols(grid)

    if num_cols == 0:
        _print_no_columns_message(grid, title)
        return

    for _ in range(num_cols):
        table.add_column(justify="left", no_wrap=True)

    for row_idx, row_data in enumerate(grid):
        styled_row_items = _get_styled_row_items(
            row_idx,
            row_data,
            num_cols,
            highlighted_coords,
            highlight_color,
            letters_color,
            hidden_color,
        )
        table.add_row(*styled_row_items)

    grid_panel = Panel(table, title=title, border_style=border_style, expand=False)
    console.print(grid_panel)


def rich_print_message(  # noqa: PLR0913
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
    """Print a message string wrapped in a Rich Panel."""
    text_content = Text.from_markup(message, style=style, justify=justify)
    panel = Panel(
        text_content,
        border_style=border_style,
        title=title,
        title_align=title_align,
        expand=expand,
        width=width,
    )
    console.print(panel)


def rich_get_input(prompt_message: str) -> str:
    """Get user input using the standard input() function."""
    return input(prompt_message)


def rich_print_leaderboard(leaderboard_data: list[dict[str, Any]], max_entries: int = 10) -> None:
    """Print the leaderboard data in a formatted Rich Table."""
    if not leaderboard_data:
        rich_print_message("The leaderboard is empty!", title="Leaderboard", border_style="dim")
        return

    table = Table(title="🏆 Leaderboard 🏆", border_style="bold yellow", show_header=True, header_style="bold yellow")
    table.add_column("Rank", width=6, justify="center")
    table.add_column("Name", min_width=15)
    table.add_column("Score", justify="right", min_width=8)

    for index, entry in enumerate(leaderboard_data[:max_entries]):
        rank = str(index + 1)
        name = str(entry.get("name", "N/A"))
        score = str(entry.get("score", "N/A"))
        table.add_row(rank, name, score)
    console.print(table)


def rich_display_wizard_selection(settings: DifficultyData | None, wizard: WizardData, wizard_index: int) -> None:
    """Display the wizard selection interface using Rich Panels and Columns."""
    clear_screen()

    art_content_str = wizard.art.strip("\n")
    num_art_lines = len(art_content_str.split("\n"))
    target_panel_height = num_art_lines + 4

    art_text = Text(art_content_str, style=f"bold {wizard.color}")
    art_panel = Panel(
        art_text,
        border_style=wizard.color,
        title="Wizard",
        title_align="left",
        padding=(1, 2),
        height=target_panel_height,
    )

    info_text = Text.assemble(
        (f"{wizard.name}\n", f"bold {wizard.color} underline"),
        ("Starting Lives: ", "bold cyan"),
        (f"{wizard.starting_lives}\n\n"),
        (f"Powerup: {wizard.powerup_name}\n", "bold yellow"),
        (f"{wizard.powerup_desc}\n\n", "yellow"),
        ("Powerup Combo Requirement: ", "bold yellow"),
        (f"{wizard.combo_requirement if wizard.combo_requirement is not None else 'N/A'}\n\n", "bold yellow"),
        ("Description:\n", "bold white"),
        (f"{wizard.description}\n"),
        no_wrap=False,
    )
    info_panel = Panel(
        info_text,
        border_style=wizard.color,
        title="Details",
        title_align="left",
        padding=(1, 2),
        width=DETAILS_PANEL_WIDTH,
        height=target_panel_height,
    )

    wizard_row = Columns([art_panel, info_panel], expand=False, equal=False)
    console.print(wizard_row)
    rich_print_message(
        "Use (◀) Left / Right (▶) arrow keys to select. Press Enter to confirm.",
        title="Input",
        border_style=wizard.color,
    )


def rich_display_wizard_art(
    settings: DifficultyData | None,
    wizard: WizardData,
) -> None:
    """Display only the ASCII art for a given wizard in a Rich Panel."""
    art_content_str = wizard.art.strip("\n")
    wizard_color = wizard.color

    art_text = Text(art_content_str, style=f"bold {wizard_color}")
    art_panel = Panel(
        art_text,
        border_style=wizard_color,
        title="Wizard",
        title_align="left",
        padding=(1, 2),
        expand=False,
    )
    console.print(art_panel)


def rich_display_menu_options(
    settings: DifficultyData | None,
    options: list[str],
    current_index: int,
    title: str,
) -> None:
    """Display vertical menu options using Rich, highlighting the current selection."""
    options_texts: list[str] = []
    for i, option_name in enumerate(options):
        detailed_prefix = ""
        if option_name in HEART_POINTS_SETTINGS:
            difficulty_details: DifficultyData = HEART_POINTS_SETTINGS[option_name]

            height = difficulty_details.grid.height
            width = difficulty_details.grid.width
            min_words_needed = difficulty_details.words_on_board_needed.minimum
            max_words_needed = difficulty_details.words_on_board_needed.maximum
            detailed_prefix = f"{height}x{width}, {min_words_needed}-{max_words_needed} words"
            detailed_prefix = detailed_prefix.ljust(22)

        prefix = "-> " if i == current_index else "   "
        line_style = "[yellow]" if i == current_index else ""
        end_line_style = "[/yellow]" if i == current_index else ""

        options_texts.append(f"{line_style}{prefix}{detailed_prefix} {option_name}{end_line_style}")

    options_str = "\n".join(options_texts)
    rich_print_message(
        message=options_str,
        title=title,
        style="bright_white",
        border_style="bold magenta",
        width=71,
        expand=False,
    )
    rich_print_message(
        message="Use (▲) Up / Down (▼) arrow keys to select. Press Enter to confirm.",
        title="Input",
        border_style="magenta",
    )


def rich_print_streak_leaderboard(streaks: list[StreakEntry]) -> None:
    """Prints the winning streak leaderboard data in a formatted Rich Table.
    Uses styling similar to the old high score leaderboard.
    """
    if not streaks:
        rich_print_message(
            "Winning streak leaderboard is empty!",
            title="🏆 Winning Streaks 🏆",
            border_style="dim",
            justify="center",
        )
        return

    table = Table(
        title="🏆 Winning Streaks Leaderboard 🏆",
        border_style="bold yellow",
        show_header=True,
        header_style="bold yellow",
        min_width=50,
    )

    table.add_column("Rank", style="cyan", width=6, justify="center")
    table.add_column("Player Name", style="magenta", min_width=15, overflow="ellipsis")
    table.add_column("Streak", style="green", justify="right", min_width=8)
    table.add_column("Total Points", style="blue", justify="right", min_width=12)

    for index, entry in enumerate(streaks):
        rank = str(index + 1)
        player_name = entry.player_name
        streak_count = str(entry.streak_count)
        total_points = str(entry.total_points_in_streak)

        table.add_row(rank, player_name, streak_count, total_points)

    console.print(table)
