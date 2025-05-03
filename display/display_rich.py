# ****************
# RICH DISPLAY
# ****************
from display.display_utils import clear_screen

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.console import Group

# For Wizards data
from data.wizards_details import WIZARDS_DATA

DEFAULT_BORDER_STYLE = "bright_cyan"
DETAILS_PANEL_WIDTH = 40  # For wizard details panel

console = Console()


def rich_print_grid(
    grid,
    highlighted_coords,
    highlight_color,
    letters_color,
    hidden_color,
    title,
    border_style,
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
        border_style=border_style,
        expand=False,
    )

    console.print(grid_panel)


def rich_print_statistics(statistics, border_style, grid, selected_wizard, game_state):
    wizard_color = selected_wizard["color"]
    # Assemble text
    player_stats_text = Text.assemble(
        ("Letters:      ", "bold cyan"),
        (f"{statistics.get('letters', 'N/A')}\n"),
        ("Lives left:   ", "bold green"),
        (f"{statistics.get('lives_left', 'N/A')}\n"),
        ("Points:       ", "bold yellow"),
        (f"{statistics.get('points', 'N/A')}\n"),
        ("Last Guess:   ", "bold magenta"),
        (f"{statistics.get('last_guess', 'None')}\n"),
    )

    powerup_stats_text = Text.assemble(
        ("Combo:        ", "bold cyan"),
        (f"{statistics.get('combo', 'None')}\n"),
        ("Power Points: ", "bold cyan"),
        (f"{statistics.get('power_points', 'None')}\n"),
        ("Shield Turns: ", "bold blue"),
        (f"{statistics.get('shield_turns', 'None')}"),
    )

    # TEXT
    PANELS_HEIGHT = 14
    STATS_HEIGHT = 6
    WIZARD_PANEL_WIDTH = 23  # 19 + 4: Art + Padding

    small_wizard_art = selected_wizard["small_art"].strip("\n")
    player_name = game_state["player_name"]

    # Create Text
    art_line = f"\n{small_wizard_art}"
    art_text = Text(art_line, style=wizard_color, justify="left")
    name_line = f"--- {player_name} ---"
    name_text = Text(name_line, style=wizard_color, justify="center")

    # Group
    wizard_panel_content = Group(art_text, name_text)

    # Calculate width, if grid is provided
    if grid:
        grid_row = grid[0]
        grid_width = len(grid_row) * 2 + 3
    else:
        # Default
        grid_width = None

    # PANELS
    wizard_panel_width = WIZARD_PANEL_WIDTH
    wizard_panel = Panel(
        wizard_panel_content,
        title="Your Wizard",
        border_style=border_style,
        style=wizard_color,
        padding=(0, 1),
        expand=False,
        width=wizard_panel_width,
        height=PANELS_HEIGHT,
    )

    stats_panel_width = grid_width - wizard_panel_width - 1
    player_stats_panel = Panel(
        player_stats_text,
        title="Game Stats",
        border_style=border_style,
        expand=True,
        width=stats_panel_width,
        height=STATS_HEIGHT,
    )

    powerup_stats_height = PANELS_HEIGHT - STATS_HEIGHT
    powerup_stats_panel = Panel(
        powerup_stats_text,
        title="Powerup Stats",
        border_style=border_style,
        expand=True,
        width=stats_panel_width,
        height=powerup_stats_height,
    )

    stats_group = Group(player_stats_panel, powerup_stats_panel)

    full_panel = Columns(
        [wizard_panel, stats_group],
        expand=False,
        equal=False,
    )

    # Create panel
    console.print(full_panel)


def rich_print_message(
    message,
    style=None,
    border_style=DEFAULT_BORDER_STYLE,
    title=None,
    title_align="left",
    expand=False,
    width=None,
    justify="left",
):
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


def rich_get_input(prompt_message):
    return input(prompt_message)


def rich_print_leaderboard(settings, leaderboard_data, max_entries=10):
    if not leaderboard_data:
        rich_print_message(
            "The leaderboard is empty!",
            title="Leaderboard",
            border_style="dim",
        )
        return

    table = Table(
        title="🏆 Leaderboard 🏆",
        border_style="bold yellow",
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


def rich_display_wizard_selection(settings, wizard_index):
    clear_screen()
    wizard = WIZARDS_DATA[wizard_index]

    # CALCULATE ART PANEL HEIGHT
    art_content_str = wizard["art"].strip("\n")
    num_art_lines = len(art_content_str.split("\n"))
    # KEEP IN MIND THAT:
    #   Panel height = content lines + top pad + bottom pad + top border + bottom border
    #   With padding=(1, 2), top/bottom padding is 1 each. Borders are 1 each.
    #   That means that the total added height = 1 + 1 + 1 + 1 = 4
    target_panel_height = num_art_lines + 4

    # CREATE PANELS
    # A. Wizard Art Panel
    art_text = Text(art_content_str, style=f"bold {wizard['color']}")
    art_panel = Panel(
        art_text,
        border_style=wizard["color"],
        title="Wizard",
        title_align="left",
        padding=(1, 2),
        height=target_panel_height,
    )

    # B. Wizard Info Panel
    info_text = Text.assemble(
        (f"{wizard['name']}\n", f"bold {wizard['color']} underline"),
        ("Starting Lives: ", "bold cyan"),
        (f"{wizard['starting_lives']}\n\n"),
        (f"Powerup: {wizard['powerup_name']}\n", "bold yellow"),
        (f"{wizard['powerup_desc']}\n\n", "yellow"),
        ("Powerup Combo Requirement: ", "bold yellow"),
        (f"{wizard['combo_requirement']}\n\n", "bold yellow"),
        ("Description:\n", "bold white"),
        (f"{wizard['description']}\n"),
        no_wrap=False,  # there should be wrapping
    )
    info_panel = Panel(
        info_text,
        border_style=wizard["color"],
        title="Details",
        title_align="left",
        padding=(1, 2),
        width=DETAILS_PANEL_WIDTH,
        height=target_panel_height,  # SET HEIGHT TO MATCH ART PANEL !
    )

    # CREATE COLUMNS SO THAT THEY'LL BE SIDE BY SIDE
    wizard_row = Columns(
        [art_panel, info_panel],
        expand=False,  # Do not expand vertically
        equal=False,  # Let panels have the width we set earlier
    )

    # PRINT COMPONENTS
    console.print(wizard_row)
    # Print instructions below
    rich_print_message(
        "Use (◀) Left / Right (▶) arrow keys to select. Press Enter to confirm.",
        title="Input",
        border_style=wizard["color"],
    )


def rich_display_wizard_art(wizard):
    art_content_str = wizard["art"].strip("\n")

    art_text = Text(art_content_str, style=f"bold {wizard['color']}")
    art_panel = Panel(
        art_text,
        border_style=wizard["color"],
        title="Wizard",
        title_align="left",
        padding=(1, 2),
        expand=False,
    )
    console.print(art_panel)


def rich_display_menu_options(options, current_index, title):
    options_list = []
    for i, option in enumerate(options):
        if i == current_index:
            # Selected
            prefix = "-> "
            line = f"[yellow]{prefix}{option}[/yellow]"
        else:
            # Not Selected
            prefix = "   "
            line = f"{prefix}{option}"
        options_list.append(line)
    # Join the list of lines with newlines
    options_str = "\n".join(options_list)

    rich_print_message(
        message=options_str,
        title=title,
        style="bright_white",
        border_style="bold magenta",
        width=71,
        expand=True,
    )
    rich_print_message(
        message="Use (▲) Up / Down (▼) arrow keys to select. Press Enter to confirm.",
        title="Input",
        border_style="magenta",
    )
