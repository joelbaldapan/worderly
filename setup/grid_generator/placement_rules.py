def is_within_bounds(r: int, c: int, height: int, width: int) -> bool:
    """Check if the coordinate (r, c) is within the grid boundaries.

    Args:
        r (int): Row index of the cell to check.
        c (int): Column index of the cell to check.
        height (int): Number of rows in the grid.
        width (int): Number of columns in the grid.

    Returns:
        bool: True if (r, c) is within bounds, False otherwise.

    """
    return 0 <= r < height and 0 <= c < width


def check_parallel_cells(
    grid: list[list[str | None]],
    r: int,
    c: int,
    dr: int,
    dc: int,
) -> bool:
    """Check if the cells perpendicular to (r, c) along the given direction are empty.

    Args:
        grid (list[list[str | None]]): 2D list representing the grid.
        r (int): Row index of the cell to check.
        c (int): Column index of the cell to check.
        dr (int): Row direction of the word (1 for vertical, 0 for horizontal).
        dc (int): Column direction of the word (1 for horizontal, 0 for vertical).

    Returns:
        bool: True if both perpendicular neighbor cells are empty or out of bounds, False otherwise.

    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    perp_dr, perp_dc = dc, dr

    check_r1, check_c1 = r - perp_dr, c - perp_dc
    neighbor1_occupied = is_within_bounds(check_r1, check_c1, height, width) and grid[check_r1][check_c1] is not None

    check_r2, check_c2 = r + perp_dr, c + perp_dc
    neighbor2_occupied = is_within_bounds(check_r2, check_c2, height, width) and grid[check_r2][check_c2] is not None
    return not (neighbor1_occupied or neighbor2_occupied)


def check_adjacent_before_start(
    grid: list[list[str | None]],
    start_row: int,
    start_col: int,
    dr: int,
    dc: int,
) -> bool:
    """Check if the cell immediately before the start of a word path is empty or out of bounds.

    Args:
        grid (list[list[str | None]]): 2D list representing the grid.
        start_row (int): Row index of the word's starting cell.
        start_col (int): Column index of the word's starting cell.
        dr (int): Row direction of the word.
        dc (int): Column direction of the word.

    Returns:
        bool: True if the cell before the start is empty or out of bounds, False otherwise.

    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    before_r, before_c = start_row - dr, start_col - dc

    cell_occupied = is_within_bounds(before_r, before_c, height, width) and grid[before_r][before_c] is not None
    return not cell_occupied


def check_adjacent_after_end(
    grid: list[list[str | None]],
    end_row: int,
    end_col: int,
    dr: int,
    dc: int,
) -> bool:
    """Check if the cell immediately after the end of a word path is empty or out of bounds.

    Args:
        grid (list[list[str | None]]): 2D list representing the grid.
        end_row (int): Row index of the word's ending cell.
        end_col (int): Column index of the word's ending cell.
        dr (int): Row direction of the word.
        dc (int): Column direction of the word.

    Returns:
        bool: True if the cell after the end is empty or out of bounds, False otherwise.

    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    after_r, after_c = end_row + dr, end_col + dc

    cell_occupied = is_within_bounds(after_r, after_c, height, width) and grid[after_r][after_c] is not None
    return not cell_occupied


def check_for_all_letters(
    grid: list[list[str | None]],
    word: str,
    words_to_place_set: set[str],
    start: tuple[int, int],
    direction: tuple[int, int],
) -> bool:
    """Check if all placement rules are satisfied for the word along the given path.

    Args:
        grid (list[list[str | None]]): 2D list representing the grid.
        word (str): The word to place.
        words_to_place_set (set[str]): Set of all words that could be on the board.
        start (tuple[int, int]): Tuple (row, col) for the starting cell.
        direction (tuple[int, int]): Tuple (dr, dc) for the direction (vertical or horizontal).

    Returns:
        bool: True if placement is valid and at least one new letter is placed, False otherwise.

    """
    placed_new_letter = False
    checked_letters = ""
    grid_height = len(grid)
    grid_width = len(grid[0]) if grid_height > 0 else 0
    word_len = len(word)
    start_row, start_col = start
    dr, dc = direction

    for i in range(word_len):
        current_row = start_row + i * dr
        current_col = start_col + i * dc

        if not is_within_bounds(current_row, current_col, grid_height, grid_width):
            return False

        current_cell = grid[current_row][current_col]

        if current_cell:
            checked_letters += current_cell
            if current_cell.lower() != word[i].lower():
                return False
        else:
            placed_new_letter = True
            if not check_parallel_cells(grid, current_row, current_col, dr, dc):
                return False

        if (len(checked_letters) > 1 and checked_letters.lower() in words_to_place_set) and (
            len(checked_letters) == word_len and not placed_new_letter
        ):
            return False

    return placed_new_letter


def is_valid_placement(
    grid: list[list[str | None]],
    word: str,
    words_to_place_set: set[str],
    intersection_info: dict,
    orientation: str,
) -> bool:
    """Check if placing the word at the specified intersection and orientation is valid.

    Args:
        grid (list[list[str | None]]): 2D list representing the grid.
        word (str): The word to place.
        words_to_place_set (set[str]): Set of all words that could be on the board.
        intersection_info (dict): Dict with keys 'row', 'col', 'idx' for intersection details.
        orientation (str): "V" for vertical or "H" for horizontal.

    Returns:
        bool: True if the placement is valid, False otherwise.

    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    word_len = len(word)

    intersect_row = intersection_info["row"]
    intersect_col = intersection_info["col"]
    intersect_idx = intersection_info["idx"]

    dr, dc = (1, 0) if orientation == "V" else (0, 1)
    start_row = intersect_row - intersect_idx * dr
    start_col = intersect_col - intersect_idx * dc
    end_row = start_row + (word_len - 1) * dr
    end_col = start_col + (word_len - 1) * dc

    if not (
        is_within_bounds(start_row, start_col, height, width) and is_within_bounds(end_row, end_col, height, width)
    ):
        return False

    if not (
        check_adjacent_before_start(grid, start_row, start_col, dr, dc)
        and check_adjacent_after_end(grid, end_row, end_col, dr, dc)
    ):
        return False

    return check_for_all_letters(grid, word, words_to_place_set, (start_row, start_col), (dr, dc))
