# ****************
# DISPLAY
# ****************
from config import settings

import random
import os
import subprocess
import sys

# For rich
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


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


DEFAULT_BORDER_STYLE = "bright_cyan"


def print_grid(
    grid,
    highlighted_coords={},
    highlight_color=None,
    letters_color="cyan",
    hidden_color="bright_blue",
    title="THE WIZARDS OF WORDERLY PLACE",
):
    if settings["design"]:
        rich_print_grid(
            grid,
            highlighted_coords,
            highlight_color,
            letters_color,
            hidden_color,
            title,
        )
    else:
        basic_print_grid(grid)


def print_statistics(statistics):
    if settings["design"]:
        rich_print_statistics(statistics)
    else:
        basic_print_statistics(statistics)


def print_message(
    message, style="", border_style=DEFAULT_BORDER_STYLE, title=None, expand=False
):
    if settings["design"]:
        rich_print_message(message, style, border_style, title, expand)
    else:
        basic_print_message(message)


def get_input(prompt_message="Enter Guess"):
    if settings["design"]:
        return rich_get_input(prompt_message)
    else:
        return basic_get_input(prompt_message)


def print_leaderboard(leaderboard):
    if settings["design"]:
        return rich_print_leaderboard(leaderboard)
    else:
        return basic_print_leaderboard(leaderboard)


# ****************
# BASIC DISPLAY
# ****************


def basic_print_grid(grid):
    for row in grid:
        print(" ".join(cell if cell else "." for cell in row))


def basic_print_statistics(statistics):
    print(f"Letters:     {statistics['letters']}")
    print(f"Lives left:  {statistics['lives_left']}")
    print(f"Points:      {statistics['points']}")
    print(f"Last Guess:  {statistics['last_guess']}")


def basic_print_message(message):
    print(message)


def basic_get_input(prompt_message=""):
    return input(prompt_message)


def basic_print_leaderboard(leaderboard): ...


# ****************
# RICH DISPLAY
# ****************


console = Console()


def rich_print_grid(
    grid, highlighted_coords, highlight_color, letters_color, hidden_color, title
):
    if grid is None:
        grid = []

    if not grid or not any(grid):
        message = "[yellow]Empty grid provided.[/yellow]"
        if grid == [[]]:
            message = "[yellow]Grid contains an empty row.[/yellow]"
        console.print(Panel(message, title=title, border_style="red"))
        return

    # Create table
    table = Table(
        show_header=False,
        box=None,
        padding=(0, 0),
    )

    num_cols = max(len(row) for row in grid if row)

    if num_cols == 0:
        console.print(
            Panel(
                "[yellow]Grid has rows but no columns.[/yellow]",
                title=title,
                border_style="yellow",
            )
        )
        return

    # COLUMNS
    for _ in range(num_cols):
        # Mnually adding space, so column width is 2 chars
        table.add_column(justify="left", no_wrap=True)

    # ROWS
    for row_idx in range(len(grid)):
        styled_row = []
        for col_idx in range(num_cols):
            # CONTENT
            content = "."
            style = "dim"
            cell = grid[row_idx][col_idx]
            if cell:
                content = cell

                if (row_idx, col_idx) in highlighted_coords:
                    style = f"bold {highlight_color}"
                elif cell == "#":
                    style = f"dim {hidden_color}"
                else:
                    style = f"bold {letters_color}"

            # Add a space ONLY if it's NOT the last column
            separator = " " if col_idx < num_cols - 1 else ""

            # Append the content + separator as styled Text
            styled_row.append(Text(content + separator, style=style))

        table.add_row(*styled_row)

    # Wrap the table in a Panel for the outer border
    grid_panel = Panel(
        table,
        title=title,
        border_style=DEFAULT_BORDER_STYLE,
        expand=False,
    )

    console.print(grid_panel)


def rich_print_statistics(statistics):
    # Assemble text
    stats_text = Text.assemble(
        ("Letters:    ", "bold cyan"),
        (f"{statistics.get('letters', 'N/A')}\n"),
        ("Lives left: ", "bold green"),
        (f"{statistics.get('lives_left', 'N/A')}\n"),
        ("Points:     ", "bold yellow"),
        (f"{statistics.get('points', 'N/A')}\n"),
        ("Last Guess: ", "bold magenta"),
        (f"{statistics.get('last_guess', 'None')}"),
    )
    # Create panel
    panel = Panel(
        stats_text, title="Game Stats", border_style=DEFAULT_BORDER_STYLE, expand=False
    )
    console.print(panel)


def rich_print_message(message, style, border_style, title, expand):
    panel = Panel(
        Text(message, style=style),
        border_style=border_style,
        title=title,
        expand=expand,
    )
    console.print(panel)


def rich_get_input(prompt_message):
    return input(prompt_message)


def rich_print_leaderboard(leaderboard_data, max_entries=10):
    if not leaderboard_data:
        print_message(
            "The leaderboard is empty!", title="Leaderboard", border_style="dim"
        )
        return

    table = Table(
        title="🏆 Leaderboard 🏆",
        border_style=DEFAULT_BORDER_STYLE,
        show_header=True,
        header_style="bold yellow",
    )
    table.add_column("Rank", width=6, justify="center")
    table.add_column("Name", min_width=15)
    table.add_column("Score", justify="right", min_width=8)

    for index, entry in enumerate(leaderboard_data[:max_entries]):
        rank = str(index + 1)
        name = entry.get("name", "N/A")
        score = str(entry.get("score", "N/A"))
        table.add_row(rank, name, score)

    console.print(table)
