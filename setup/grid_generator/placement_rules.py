def _is_within_bounds(r: int, c: int, height: int, width: int) -> bool:
    """Check if a given coordinate (r, c) is within the grid boundaries."""
    return 0 <= r < height and 0 <= c < width


def _check_parallel_cells(grid: list[list[str | None]], r: int, c: int, dr: int, dc: int) -> bool:
    """Check if cells perpendicular to a given cell along a direction are empty."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    perp_dr, perp_dc = dc, dr

    check_r1, check_c1 = r - perp_dr, c - perp_dc
    neighbor1_occupied = _is_within_bounds(check_r1, check_c1, height, width) and grid[check_r1][check_c1] is not None

    check_r2, check_c2 = r + perp_dr, c + perp_dc
    neighbor2_occupied = _is_within_bounds(check_r2, check_c2, height, width) and grid[check_r2][check_c2] is not None
    return not (neighbor1_occupied or neighbor2_occupied)


def _check_adjacent_before_start(
    grid: list[list[str | None]],
    start_row: int,
    start_col: int,
    dr: int,
    dc: int,
) -> bool:
    """Check if the cell immediately before the start of a word path is empty."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    before_r, before_c = start_row - dr, start_col - dc

    cell_occupied = _is_within_bounds(before_r, before_c, height, width) and grid[before_r][before_c] is not None
    return not cell_occupied


def _check_adjacent_after_end(grid: list[list[str | None]], end_row: int, end_col: int, dr: int, dc: int) -> bool:
    """Check if the cell immediately after the end of a word path is empty."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    after_r, after_c = end_row + dr, end_col + dc

    cell_occupied = _is_within_bounds(after_r, after_c, height, width) and grid[after_r][after_c] is not None
    return not cell_occupied


def _check_for_all_letters(
    grid: list[list[str | None]],
    word: str,
    words_to_place_set: set[str],
    word_len: int,
    start_row: int,
    start_col: int,
    dr: int,
    dc: int,
) -> bool:
    """Check conditions along the entire path of a potential word placement."""
    placed_new_letter = False
    checked_letters = ""
    grid_height = len(grid)
    grid_width = len(grid[0]) if grid_height > 0 else 0

    for i in range(word_len):
        current_row = start_row + i * dr
        current_col = start_col + i * dc

        if not _is_within_bounds(current_row, current_col, grid_height, grid_width):
            return False

        current_cell = grid[current_row][current_col]

        if current_cell:
            checked_letters += current_cell
            if current_cell.lower() != word[i].lower():
                return False  # Letter conflict
        else:
            placed_new_letter = True
            if not _check_parallel_cells(grid, current_row, current_col, dr, dc):
                return False  # Parallel conflict

        # Prevents placing a word that forms an existing word by only using already placed letters
        # Trying to place "ABC" over "ABC"
        if len(checked_letters) > 1 and checked_letters.lower() in words_to_place_set:
            if len(checked_letters) == word_len and not placed_new_letter:
                return False

    return placed_new_letter  # Must place at least one new letter


def is_valid_placement(
    grid: list[list[str | None]],
    word: str,
    words_to_place_set: set[str],  # All words that could be on the board
    intersect_row: int,
    intersect_col: int,
    intersect_idx: int,
    orientation: str,  # "V" or "H"
) -> bool:
    """Determine if placing a word at a specific intersection is valid."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    word_len = len(word)

    dr, dc = (1, 0) if orientation == "V" else (0, 1)
    start_row = intersect_row - intersect_idx * dr
    start_col = intersect_col - intersect_idx * dc
    end_row = start_row + (word_len - 1) * dr
    end_col = start_col + (word_len - 1) * dc

    if not (
        _is_within_bounds(start_row, start_col, height, width) and _is_within_bounds(end_row, end_col, height, width)
    ):
        return False

    if not (
        _check_adjacent_before_start(grid, start_row, start_col, dr, dc)
        and _check_adjacent_after_end(grid, end_row, end_col, dr, dc)
    ):
        return False

    return _check_for_all_letters(grid, word, words_to_place_set, word_len, start_row, start_col, dr, dc)
