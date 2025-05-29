from typing import List, Optional, Dict, Set, Tuple, Any  # Added common types

from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import BarColumn, Progress
from rich.table import Table
from rich.text import Text

from data.settings_details import DifficultyData, HEART_POINTS_SETTINGS
from data.wizards_details import WizardData
from gameplay.game_state_handler import GameStateData, GameStatisticsData

from .display_utils import clear_screen

DEFAULT_BORDER_STYLE = "bright_cyan"
DETAILS_PANEL_WIDTH = 40

console = Console()


def rich_print_grid(
    grid: Optional[List[List[Optional[str]]]],
    highlighted_coords: Set[Tuple[int, int]] | List[Tuple[int, int]],  # Can be set or list
    highlight_color: str,
    letters_color: str,
    hidden_color: str,
    title: str,
    border_style: str,
) -> None:
    """Prints the game grid using Rich library for prettier formatting."""
    if not grid or not any(grid):  # Check for empty grid or grid with only empty rows
        message = "[yellow]Empty grid provided.[/yellow]"
        if grid == [[]]:  # Check specifically for [[]] case
            message = "[yellow]Grid contains an empty row.[/yellow]"
        console.print(Panel(Text.from_markup(message), title=title, border_style="red"))
        return

    table = Table(show_header=False, box=None, padding=(0, 0))
    num_cols = 0
    if grid:
        try:
            num_cols = max(len(row) for row in grid if row)
        except ValueError:
            num_cols = 0

    if num_cols == 0 and grid:
        console.print(
            Panel(
                Text.from_markup("[yellow]Grid has rows but no columns.[/yellow]"), title=title, border_style="yellow"
            )
        )
        return
    elif num_cols == 0:
        console.print(
            Panel(
                Text.from_markup("[yellow]Empty grid provided (no columns).[/yellow]"), title=title, border_style="red"
            )
        )
        return

    for _ in range(num_cols):
        table.add_column(justify="left", no_wrap=True)

    for row_idx, row_data in enumerate(grid):
        styled_row_items: List[Text] = []
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
        table.add_row(*styled_row_items)

    grid_panel = Panel(table, title=title, border_style=border_style, expand=False)
    console.print(grid_panel)


def _append_combo_stats(statistics: GameStatisticsData, selected_wizard: WizardData, powerup_parts: List[Any]) -> None:
    """Appends combo meter Text and Progress bar to the powerup_parts list."""
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
        powerup_parts.append(combo_progress)
        powerup_parts.append(Text("\n"))


def rich_print_statistics(
    statistics: GameStatisticsData,
    border_style: str,
    grid: Optional[List[List[Optional[str]]]],
    selected_wizard: WizardData,
    game_st: GameStateData,
) -> None:
    """Prints the formatted statistics panel using Rich Columns and Panels."""
    wizard_color = selected_wizard.color

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

    powerup_parts: List[Any] = []
    powerup_parts.append(Text.assemble(("Combo:        ", "bold cyan"), (f"{statistics.combo}")))

    shield_turns = statistics.shield_turns
    if shield_turns > 0:
        if wizard_color != "bright_white" and selected_wizard.combo_requirement is not None:
            powerup_parts.append(Text.assemble(("Shield Turns: ", "bold blue"), (f"{shield_turns}")))

    if wizard_color != "bright_white":
        powerup_parts.append(Text.assemble(("Power Points: ", "bold cyan"), (f"{statistics.power_points}")))
        _append_combo_stats(statistics, selected_wizard, powerup_parts)
    else:
        powerup_parts.append(Text("\nNote: White wizards have no powerups!", style="bright_white"))

    powerup_stats_content = Group(*powerup_parts)

    small_wizard_art = selected_wizard.small_art.strip("\n")
    # Access player_name from GameStateData, provide default if None
    player_name_display = game_st.player_name if game_st.player_name is not None else "Player"
    art_text = Text(f"\n{small_wizard_art}", style=wizard_color, justify="left")
    name_text = Text(f"--- {player_name_display} ---", style=wizard_color, justify="center")
    wizard_panel_content = Group(art_text, name_text)

    PANELS_HEIGHT = 15
    STATS_HEIGHT = 6
    WIZARD_PANEL_WIDTH = 23

    grid_actual_width = WIZARD_PANEL_WIDTH + 30
    if grid and grid[0]:
        grid_actual_width = len(grid[0]) * 2 + 3

    stats_panel_width = max(10, grid_actual_width - WIZARD_PANEL_WIDTH - 1)

    wizard_panel = Panel(
        wizard_panel_content,
        title="Your Wizard",
        border_style=border_style,
        style=wizard_color,
        padding=(0, 1),
        expand=False,
        width=WIZARD_PANEL_WIDTH,
        height=PANELS_HEIGHT,
    )
    player_stats_panel = Panel(
        player_stats_content,
        title="Game Stats",
        title_align="left",
        border_style=border_style,
        expand=True,
        width=stats_panel_width,
        height=STATS_HEIGHT,
    )
    powerup_stats_height = PANELS_HEIGHT - STATS_HEIGHT
    powerup_stats_panel = Panel(
        powerup_stats_content,
        title="Powerup Stats",
        title_align="left",
        border_style=border_style,
        expand=True,
        width=stats_panel_width,
        height=max(1, powerup_stats_height),
    )

    stats_group = Group(player_stats_panel, powerup_stats_panel)
    full_panel = Columns([wizard_panel, stats_group], expand=False, equal=False)
    console.print(full_panel)


def rich_print_message(
    message: str,
    style: Optional[str] = None,
    border_style: str = DEFAULT_BORDER_STYLE,
    title: Optional[str] = None,
    title_align: str = "left",
    expand: bool = False,
    width: Optional[int] = None,
    justify: str = "left",
) -> None:
    """Prints a message string wrapped in a Rich Panel."""
    text_content = Text.from_markup(message, style=style, justify=justify)
    panel = Panel(
        text_content, border_style=border_style, title=title, title_align=title_align, expand=expand, width=width
    )
    console.print(panel)


def rich_get_input(prompt_message: str) -> str:
    """Gets user input using the standard input() function."""
    return input(prompt_message)


def rich_print_leaderboard(leaderboard_data: List[Dict[str, Any]], max_entries: int = 10) -> None:
    """Prints the leaderboard data in a formatted Rich Table."""
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


def rich_display_wizard_selection(settings: Optional[DifficultyData], wizard: WizardData, wizard_index: int) -> None:
    """Displays the wizard selection interface using Rich Panels and Columns."""
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
    settings: Optional[DifficultyData],  # Added settings for consistency if display.py passes it
    wizard: WizardData,  # Changed from dict
) -> None:
    """Displays only the ASCII art for a given wizard in a Rich Panel."""
    art_content_str = wizard.art.strip("\n")
    wizard_color = wizard.color

    art_text = Text(art_content_str, style=f"bold {wizard_color}")
    art_panel = Panel(
        art_text, border_style=wizard_color, title="Wizard", title_align="left", padding=(1, 2), expand=False
    )
    console.print(art_panel)


def rich_display_menu_options(
    settings: Optional[DifficultyData],  # Added settings for consistency
    options: List[str],
    current_index: int,
    title: str,
) -> None:
    """Displays vertical menu options using Rich, highlighting the current selection."""
    options_texts: List[str] = []
    for i, option_name in enumerate(options):
        detailed_prefix = ""
        # HEART_POINTS_SETTINGS now stores DifficultyData objects
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
        message=options_str, title=title, style="bright_white", border_style="bold magenta", width=71, expand=False
    )
    rich_print_message(
        message="Use (▲) Up / Down (▼) arrow keys to select. Press Enter to confirm.",
        title="Input",
        border_style="magenta",
    )
