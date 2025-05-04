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
from rich.progress import Progress, BarColumn

# For Settings and Wizards data
from data.wizards_details import WIZARDS_DATA
from data.settings_details import HEART_POINTS_SETTINGS

DEFAULT_BORDER_STYLE = "bright_cyan"
DETAILS_PANEL_WIDTH = 40  # For wizard details panel

# Initialize Rich Console
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
    """Prints the game grid using Rich library for prettier formatting.

    Creates a Rich Table within a Rich Panel to display the grid, applying
    specified colors for letters, hidden cells, and highlights.

    Args:
        grid (list[list[str | None]] | None):
            The 2D list representing the game grid. None represents empty cells.
        highlighted_coords (set[tuple[int, int]] | list[tuple[int, int]]):
            A set or list of (row, col) tuples to highlight.
        highlight_color (str): The Rich color string for highlighted letters.
        letters_color (str): The Rich color string for revealed letters.
        hidden_color (str): The Rich color string for hidden letters ('#').
        title (str): The title to display on the Panel border.
        border_style (str): The Rich style string for the Panel border.

    Returns:
        None: This function prints directly to the console and returns nothing.
    """
    # Check for completely empty grid or grid with only empty rows
    if not grid or not any(grid):
        message = "[yellow]Empty grid provided.[/yellow]"
        # Check specifically for [[]] case
        if grid == [[]]:
            message = "[yellow]Grid contains an empty row.[/yellow]"
        console.print(Panel(message, title=title, border_style="red"))
        return

    # Create table for the grid layout
    table = Table(
        show_header=False,
        box=None,  # No internal grid lines
        padding=(0, 0),  # No padding between cells
    )

    # Determine number of columns based on the longest row
    num_cols = 0
    if grid:  # Make sure grid is not empty before checking rows
        try:
            num_cols = max(
                len(row) for row in grid if row
            )  # Handle potential empty rows
        except ValueError:  # Handles case where grid only contains empty lists
            num_cols = 0

    # Handle grid with rows but no columns
    if num_cols == 0 and grid:
        console.print(
            Panel(
                "[yellow]Grid has rows but no columns.[/yellow]",
                title=title,
                border_style="yellow",
            )
        )
        return
    elif num_cols == 0:  # Handles grid = [[]] or grid = [] after initial checks
        console.print(
            Panel(
                "[yellow]Empty grid provided (no columns).[/yellow]",
                title=title,
                border_style="red",
            )
        )
        return

    # Add columns to the Rich Table
    for _ in range(num_cols):
        # Add empty column; content will be added row by row with spacing
        table.add_column(justify="left", no_wrap=True)

    # Add rows to the Rich Table with styled content
    for row_idx, row in enumerate(grid):
        styled_row = []
        # Make sure row processing matches num_cols, padding shorter rows if necessary
        for col_idx in range(num_cols):
            content = "."  # Default for empty cells
            style = "dim"  # Default style for empty cells
            try:
                cell = row[col_idx] if row and col_idx < len(row) else None
            except IndexError:
                cell = None  # Handle rows shorter than num_cols

            # If the cell is not None
            if cell:
                content = cell
                coord = (row_idx, col_idx)
                if coord in highlighted_coords:  # Highlighted letter
                    style = f"bold {highlight_color}"
                elif cell == "#":  # Hidden letter
                    style = f"dim {hidden_color}"
                else:  # Revealed letter
                    style = f"bold {letters_color}"

            # Add space separator between cells, except for the last column
            separator = " " if col_idx < num_cols - 1 else ""
            # Append styled Text object for the cell content + separator
            styled_row.append(Text(content + separator, style=style))

        # Add the complete styled row to the table
        table.add_row(*styled_row)

    # Wrap the table in a Panel for the outer border and title
    grid_panel = Panel(
        table,
        title=title,
        border_style=border_style,
        expand=False,  # Prevent panel from expanding unnecessarily
    )

    # Print the final Panel to the console
    console.print(grid_panel)


def _append_combo_stats(statistics, selected_wizard, powerup_parts):
    """Appends combo meter Text and Progress bar to the powerup_parts list.

    Calculates the current combo progress relative to the wizard's requirement
    and adds formatted text and a Rich Progress bar if applicable.

    Args:
        statistics (dict): The game statistics dictionary.
        selected_wizard (dict): The selected wizard's data dictionary.
        powerup_parts (list): The list to which Rich renderables are appended.

    Returns:
        None: Modifies powerup_parts list in place.
    """
    wizard_color = selected_wizard.get("color", "white")  # Default color
    combo = statistics.get("combo", 0)
    combo_req = selected_wizard.get("combo_requirement")

    # Only display combo meter if there's a requirement
    if combo_req is not None and combo_req > 0:
        # Calculate current progress for the bar, handling full bar correctly
        curr_combo = combo % combo_req
        if combo > 0 and curr_combo == 0:
            # Show full bar if combo is a non-zero multiple of requirement
            curr_combo = combo_req

        # Add the "Combo Meter: CURR / REQ" text
        powerup_parts.append(
            Text.assemble(
                ("Combo Meter:  ", "bold cyan"),
                (f"{curr_combo} / {combo_req}\n"),  # Show current / required
            )
        )

        # Create and configure the progress bar
        combo_progress = Progress(
            BarColumn(
                bar_width=27,  # Fixed width for consistent layout
                style="dim white",  # Style for the empty part
                complete_style="bright_white",  # Style for the filled part
                finished_style=f"bold {wizard_color}",  # Style when bar is full
            ),
            expand=False,  # Prevent progress bar from expanding
        )
        # Add the task to the progress bar
        # Make sure 'completed' doesn't exceed 'total'
        combo_progress.add_task(
            "combo", total=combo_req, completed=min(curr_combo, combo_req)
        )
        powerup_parts.append(combo_progress)
        powerup_parts.append(Text("\n"))  # Add spacing after the bar


def rich_print_statistics(statistics, border_style, grid, selected_wizard, game_state):
    """Prints the formatted statistics panel using Rich Columns and Panels.

    Displays game stats (letters, lives, points, guess) and powerup stats
    (combo, power points, meter, shield) alongside wizard art and name.

    Args:
        statistics (dict): The game statistics dictionary.
        border_style (str): The Rich style string for Panel borders.
        grid (list[list[str or None]]): The current game grid (used for width calculation).
        selected_wizard (dict): The dictionary containing data for the selected wizard.
        game_state (dict): The main game state dictionary (used for player name).

    Returns:
        None: This function prints directly to the console and returns nothing.
    """
    wizard_color = selected_wizard.get("color", "white")

    # Setup Panel Contents
    # A. Player Stats Panel Content
    player_stats_content = Text.assemble(
        ("Letters:    ", "bold cyan"),
        (f"{statistics.get('letters', 'N/A')}\n"),
        ("Lives left: ", "bold green"),
        (f"{statistics.get('lives_left', 'N/A')}\n"),
        ("Points:     ", "bold yellow"),
        (f"{statistics.get('points', 'N/A')}\n"),
        ("Last Guess: ", "bold magenta"),
        (f"{statistics.get('last_guess', 'None')}"),
    )

    # B. Powerup Stats Panel Content
    powerup_parts = []  # Build content as a list of Rich renderables
    powerup_parts.append(
        Text.assemble(
            ("Combo:        ", "bold cyan"), (f"{statistics.get('combo', 0)}")
        )
    )

    # Add Shield Turns if active
    shield_turns = statistics.get("shield_turns", 0)
    if shield_turns > 0:
        # Add newline for shield turns
        if wizard_color != "bright_white" and selected_wizard.get("combo_requirement"):
            powerup_parts.append(
                Text.assemble(("Shield Turns: ", "bold blue"), (f"{shield_turns}"))
            )

    # Add Power Points and Combo Meter if applicable
    if wizard_color != "bright_white":
        powerup_parts.append(
            Text.assemble(
                ("Power Points: ", "bold cyan"),
                (f"{statistics.get('power_points', 0)}"),
            )
        )
        # Call helper to add the combo meter bar
        _append_combo_stats(statistics, selected_wizard, powerup_parts)
    else:
        powerup_parts.append(
            Text("\nNote: White wizards have no powerups!", style="bright_white")
        )


    # Group all powerup parts together
    powerup_stats_content = Group(*powerup_parts)

    # C. Wizard Panel Content
    small_wizard_art = selected_wizard.get("small_art", "").strip("\n")
    player_name = game_state.get("player_name", "Player")
    art_text = Text(f"\n{small_wizard_art}", style=wizard_color, justify="left")
    name_text = Text(f"--- {player_name} ---", style=wizard_color, justify="center")
    wizard_panel_content = Group(art_text, name_text)

    # Layout Calculations
    # (Make sure widths of grid and stats are the same)
    PANELS_HEIGHT = 15  # Target height for consistent layout
    STATS_HEIGHT = 6  # Height for the top stats panel
    WIZARD_PANEL_WIDTH = 23  # Fixed width for wizard art panel

    grid_width = None
    # Calculate required width based on grid if possible
    if grid and grid[0]:  # Check grid and first row exist
        grid_width = len(grid[0]) * 2 + 3  # (cols * 2 chars/col) + padding/border
    else:
        # Fallback width if grid is invalid or empty
        grid_width = WIZARD_PANEL_WIDTH + 30  # Estimate a reasonable width

    # Make sure calculated width is enough
    stats_panel_width = max(10, grid_width - WIZARD_PANEL_WIDTH - 1)  # Min width of 10

    # Create Panels
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
    powerup_stats_height = PANELS_HEIGHT - STATS_HEIGHT  # Calculate remaining height
    powerup_stats_panel = Panel(
        powerup_stats_content,
        title="Powerup Stats",
        title_align="left",
        border_style=border_style,
        expand=True,
        width=stats_panel_width,
        height=max(1, powerup_stats_height),  # Make sure height is at least 1
    )

    # Combine everything and Print
    stats_group = Group(player_stats_panel, powerup_stats_panel)
    full_panel = Columns([wizard_panel, stats_group], expand=False, equal=False)
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
    """Prints a message string wrapped in a Rich Panel.

    Args:
        message (str):
            The message content. Can include Rich markup.
        style (str, optional):
            Rich style for the message text. Defaults to None.
        border_style (str, optional):
            Rich style for the panel border.
            Defaults to DEFAULT_BORDER_STYLE.
        title (str, optional):
            Text to display in the panel border. Defaults to None.
        title_align (str, optional):
            Alignment for the title ('left', 'center', 'right').
            Defaults to "left".
        expand (bool, optional):
            Whether the panel should expand to fill available width.
            Defaults to False.
        width (int, optional): Fixed width for the panel. Defaults to None (auto).
        justify (str, optional):
            Text justification ('left', 'center', 'right'). Defaults to "left".

    Returns:
        None
    """
    # Create styled text content
    text_content = Text.from_markup(message, style=style, justify=justify)
    # Create the panel with specified options
    panel = Panel(
        text_content,
        border_style=border_style,
        title=title,
        title_align=title_align,
        expand=expand,
        width=width,
    )
    # Print the panel to the console
    console.print(panel)


def rich_get_input(prompt_message):
    """Gets user input using the standard input() function (for Rich compatibility).

    Args:
        prompt_message (str): The message to display before waiting for input.

    Returns:
        str: The string entered by the user.
    """
    # Rich generally works well with standard input()
    return input(prompt_message)


def rich_print_leaderboard(leaderboard_data, max_entries=10):
    """Prints the leaderboard data in a formatted Rich Table.

    Args:
        leaderboard_data (list[dict]):
            List of score dictionaries sorted by score.
            Each dict needs 'name' and 'score'.
        max_entries (int, optional):
            Maximum number of entries to display. Defaults to 10.

    Returns:
        None: This function prints directly to the console and returns nothing.
    """
    # Handle empty leaderboard case
    if not leaderboard_data:
        rich_print_message(
            "The leaderboard is empty!",
            title="Leaderboard",
            border_style="dim",
        )
        return

    # Create the table
    table = Table(
        title="🏆 Leaderboard 🏆",
        border_style="bold yellow",
        show_header=True,
        header_style="bold yellow",
    )
    # Define columns
    table.add_column("Rank", width=6, justify="center")
    table.add_column("Name", min_width=15)
    table.add_column("Score", justify="right", min_width=8)

    # Add rows for top entries
    for index, entry in enumerate(leaderboard_data[:max_entries]):
        rank = str(index + 1)
        name = entry.get("name", "N/A")
        score = str(entry.get("score", "N/A"))
        table.add_row(rank, name, score)

    # Print the table
    console.print(table)


def rich_display_wizard_selection(wizard_index):
    """Displays the wizard selection interface using Rich Panels and Columns.

    Shows wizard art, details, and navigation instructions.

    Args:
        wizard_index (int): The index of the wizard to display from WIZARDS_DATA.

    Returns:
        None: This function prints directly to the console and returns nothing.
    """
    clear_screen()  # Clear screen before displaying

    # Safely get wizard data
    try:
        wizard = WIZARDS_DATA[wizard_index]
    except IndexError:
        print(f"Error: Invalid wizard index {wizard_index}")
        return

    # Calculate Panel Height (Which takes account for the paddings)
    art_content_str = wizard.get("art", "").strip("\n")
    num_art_lines = len(art_content_str.split("\n"))
    target_panel_height = num_art_lines + 4

    # Create Panels
    # A. Wizard Art Panel
    art_text = Text(art_content_str, style=f"bold {wizard.get('color', 'white')}")
    art_panel = Panel(
        art_text,
        border_style=wizard.get("color", "white"),
        title="Wizard",
        title_align="left",
        padding=(1, 2),
        height=target_panel_height,
    )

    # B. Wizard Info Panel
    info_text = Text.assemble(
        (
            f"{wizard.get('name', 'N/A')}\n",
            f"bold {wizard.get('color', 'white')} underline",
        ),
        ("Starting Lives: ", "bold cyan"),
        (f"{wizard.get('starting_lives', 'N/A')}\n\n"),
        (f"Powerup: {wizard.get('powerup_name', 'N/A')}\n", "bold yellow"),
        (f"{wizard.get('powerup_desc', 'N/A')}\n\n", "yellow"),
        ("Powerup Combo Requirement: ", "bold yellow"),
        (f"{wizard.get('combo_requirement', 'N/A')}\n\n", "bold yellow"),
        ("Description:\n", "bold white"),
        (f"{wizard.get('description', 'N/A')}\n"),
        no_wrap=False,  # Allow wrapping for description
    )
    info_panel = Panel(
        info_text,
        border_style=wizard.get("color", "white"),
        title="Details",
        title_align="left",
        padding=(1, 2),
        width=DETAILS_PANEL_WIDTH,
        height=target_panel_height,  # Match height with art panel
    )

    # Combine Panels
    wizard_row = Columns(
        [art_panel, info_panel],
        expand=False,  # Do not expand vertically
        equal=False,  # Let panels determine width
    )

    # Print Components, then print instructions below
    console.print(wizard_row)
    rich_print_message(
        "Use (◀) Left / Right (▶) arrow keys to select. Press Enter to confirm.",
        title="Input",
        border_style=wizard.get("color", "white"),
    )


def rich_display_wizard_art(wizard):
    """Displays only the ASCII art for a given wizard in a Rich Panel.

    Args:
        wizard (dict):
            The dictionary containing wizard data, including 'art' and 'color' keys.

    Returns:
        None: This function prints directly to the console and returns nothing.
    """
    art_content_str = wizard.get("art", "No Art").strip("\n")
    wizard_color = wizard.get("color", "white")

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


def rich_display_menu_options(options, current_index, title):
    """Displays vertical menu options using Rich, highlighting the current selection.

    Args:
        options (list[str]): The list of menu option strings.
        current_index (int): The index of the currently selected option.
        title (str): The title for the menu panel.

    Returns:
        None: This function prints directly to the console and returns nothing.
    """

    options_list = []
    for i, option in enumerate(options):
        detailed_prefix = ""
        if option in HEART_POINTS_SETTINGS:
            details = HEART_POINTS_SETTINGS[option]

            height = details["grid"]["height"]
            width = details["grid"]["width"]
            min_words_needed = details["words_on_board_needed"]["minimum"]
            max_words_needed = details["words_on_board_needed"]["maximum"]
            detailed_prefix = (
                f"{height}x{width}, {min_words_needed}-{max_words_needed} words"
            )
            detailed_prefix = detailed_prefix.ljust(22)

        if i == current_index:
            # Apply yellow style and arrow prefix to the selected option
            prefix = "-> "
            line = f"[yellow]{prefix}{detailed_prefix} {option}[/yellow]"
        else:
            # Add padding prefix to non-selected options
            # 3 spaces to align with "-> "
            prefix = "   "
            line = f"{prefix}{detailed_prefix} {option}"
        options_list.append(line)

    # Join the list of lines with newlines for the message content
    options_str = "\n".join(options_list)

    # Print the options panel
    # then print the instructions panel
    rich_print_message(
        message=options_str,
        title=title,
        style="bright_white",  # Default style for non-selected options
        border_style="bold magenta",
        width=71,  # Fixed width for consistent appearance
        expand=False,  # Don't expand horizontally
    )
    rich_print_message(
        message="Use (▲) Up / Down (▼) arrow keys to select. Press Enter to confirm.",
        title="Input",
        border_style="magenta",
    )
