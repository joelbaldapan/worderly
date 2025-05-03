# ************************************************
# Tests for: Grid Validation
# ************************************************
import pytest
from setup import grid_generator


def test_is_within_bounds():
    """Test the boundary checking function."""
    height, width = 10, 20

    # Within bounds
    assert grid_generator._is_within_bounds(0, 0, height, width) is True
    assert grid_generator._is_within_bounds(9, 19, height, width) is True
    assert grid_generator._is_within_bounds(5, 10, height, width) is True

    # Row too low
    assert grid_generator._is_within_bounds(-1, 5, height, width) is False
    # Col too low
    assert grid_generator._is_within_bounds(5, -1, height, width) is False

    # Row too high
    assert grid_generator._is_within_bounds(999, 5, height, width) is False
    # Col too high
    assert grid_generator._is_within_bounds(5, 999, height, width) is False

    # Row and Col a little too high
    assert grid_generator._is_within_bounds(10, 5, height, width) is False
    assert grid_generator._is_within_bounds(5, 20, height, width) is False


@pytest.fixture
def validation_grid():
    """Provides a grid for validation tests with TEST and SAIL placed."""
    grid = grid_generator.create_empty_grid(5, 5)
    # Place "TEST" H at (1,1)
    grid[1][1] = "T"
    grid[1][2] = "E"
    grid[1][3] = "S"
    grid[1][4] = "T"
    # Place "SAIL" V at (1,3) intersecting 'S'
    grid[2][3] = "A"
    grid[3][3] = "I"
    grid[4][3] = "L"

    # Resulting Grid:
    # . . . . . .
    # . T E S T .
    # . . . A . .
    # . . . I . .
    # . . . L . .
    # . . . . . .
    return grid


def test_check_parallel_cells(validation_grid):
    """Test _check_parallel_cells: checks parallel neighbors."""
    # PARAMETERS: grid, start_row, start_col, dr, dc
    # perp_dr, perp_dc = dc, dr

    grid = validation_grid

    # 1.) Perpedicular neighbors of dc -> -/+ 1 to column
    # Check parallel to 'T' in TEST (H placement, dr=0, dc=1) -> Neighbors (0,1), (2,1) are None
    assert grid_generator._check_parallel_cells(grid, 1, 1, 0, 1) is True

    # Place something parallel
    grid[0][2] = "A"
    grid[2][1] = "A"
    # Check parallel to 'T' in TEST (H placement, dr=0, dc=1) -> Neighbors (0,1), (2,1) occupied
    assert grid_generator._check_parallel_cells(grid, 1, 1, 0, 1) is False
    # Check parallel to 'E' in TEST (H placement, dr=0, dc=1) -> Neighbors (0,2), (2,2) occupied
    assert grid_generator._check_parallel_cells(grid, 1, 2, 0, 1) is False

    # Grid after placing new letters:
    # . . A . . .
    # . T E S T .
    # . A . A . .
    # . . . I . .
    # . . . L . .
    # . . . . . .

    # 2.) Perpedicular neighbors of dr -> -/+ 1 to row
    # Check parallel to 'I' in SAIL (V placement, dr=1, dc=0) -> Neighbors (3,2), (3,4) are None
    assert grid_generator._check_parallel_cells(grid, 3, 3, 1, 0) is True

    # Place something parallel
    grid[3][2] = "T"
    grid[4][4] = "A"
    # Check parallel to 'I' in SAIL (V placement, dr=1, dc=0) -> Neighbors (3,2), (3,4) occupied
    assert grid_generator._check_parallel_cells(grid, 3, 3, 1, 0) is False
    # Check parallel to 'L' in SAIL (V placement, dr=1, dc=0) -> Neighbors (3,2), (3,4) occupied
    assert grid_generator._check_parallel_cells(grid, 4, 3, 1, 0) is False

    # Grid after placing new letters:
    # . A . . . .
    # . T E S T .
    # . A . A . .
    # . . T I . .
    # . . . L A .
    # . . . . . .


def test_check_adjacent_before_start(validation_grid):
    """Test _check_adjacent_before_start: checks cell before word start."""
    # PARAMETERS: grid, start_row, start_col, dr, dc

    grid = validation_grid
    # Grid:
    # . . . . . .
    # . T E S T .
    # . . . A . .
    # . . . I . .
    # . . . L . .
    # . . . . . .

    # 1.) Out of bounds, but still valid
    # Try placing HORIZ starting at (1,0) -> cell before (1,-1) is OOB -> True
    assert grid_generator._check_adjacent_before_start(grid, 1, 0, 0, 1) is True
    # Try placing VERT starting at (0,3) -> cell before (-1,3) is OOB -> True
    assert grid_generator._check_adjacent_before_start(grid, 0, 3, 1, 0) is True

    # 2.) In bounds, free space
    # Try placing HORIZ starting at (4,1) -> cell before (4,0) empty -> True
    assert grid_generator._check_adjacent_before_start(grid, 4, 1, 0, 1) is True
    # Try placing VERT starting at (4,1) -> cell before (3,1) empty -> True
    assert grid_generator._check_adjacent_before_start(grid, 4, 1, 1, 0) is True

    # 3.) Conflicting with already placed letters
    # Try placing HORIZ starting at (1,2) -> cell before (1,1) is 'T' -> False
    assert grid_generator._check_adjacent_before_start(grid, 1, 2, 0, 1) is False
    # Try placing VERT starting at (2,3) -> cell before (1,3) is 'S' -> False
    assert grid_generator._check_adjacent_before_start(grid, 2, 3, 1, 0) is False


def test_check_adjacent_after_end(validation_grid):
    """Test _check_adjacent_after_end: checks cell after word end."""
    # PARAMETERS: grid, start_row, start_col, dr, dc
    # Grid:
    # . . . . . .
    # . T E S T .
    # . . . A . .
    # . . . I . .
    # . . . L . .
    # . . . . . .

    grid = validation_grid
    # Try placing HORIZ ending at (1,3) ('S') -> cell after (1,4) is 'T' -> False
    assert grid_generator._check_adjacent_after_end(grid, 1, 3, 0, 1) is False
    # Try placing VERT ending at (3,3) ('I') -> cell after (4,3) is 'L' -> False
    assert grid_generator._check_adjacent_after_end(grid, 3, 3, 1, 0) is False
    # Try placing HORIZ ending at (0,0) -> cell after (0,1) is None -> True
    assert grid_generator._check_adjacent_after_end(grid, 0, 0, 0, 1) is True
    # Try placing VERT ending at (4,4) -> cell after (5,4) is OOB -> True
    assert grid_generator._check_adjacent_after_end(grid, 4, 4, 1, 0) is True


def test_check_for_all_letters(validation_grid):
    """
    Test _check_for_all_letters: checks letter conflicts, parallel conflicts
    during placement, overwriting, and if any new letter was placed.
    """
    grid = validation_grid
    words_to_place = {"test", "sail"}
    # PARAMETERS: grid, word, words_to_place, word_len, start_row, start_col, dr, dc
    # Grid:
    # . . . . . .
    # . T E S T .
    # . . . A . .
    # . . . I . .
    # . . . L . .
    # . . . . . .

    # 1.) Placement intersecting 'E' (place 'ERA' V) conflicts on letter 'R' vs 'E'
    # Word: ERA, Start=(0,2), dr=1, dc=0. Path: (0,2)=N, (1,2)='E', (2,2)=N
    # Expect False due to letter conflict
    assert (
        grid_generator._check_for_all_letters(
            grid, "ERA", words_to_place, 3, 0, 2, 1, 0
        )
        is False
    )

    # 2.) Conflict with existing letter ('S')
    # Try placing 'SET' H starting at (1,2) -> Path (1,2)='E', (1,3)='S', (1,4)='T'
    # Checks S vs E -> Mismatch at first letter!
    assert (
        grid_generator._check_for_all_letters(
            grid, "SET", words_to_place, 3, 1, 2, 0, 1
        )
        is False
    )

    # 3.) Parallel conflict during placement
    # Try placing 'APE' H starting at (2,1). Path (2,1)=N, (2,2)=N, (2,3)='A'
    # Check parallel for (2,1): Neighbors (1,1)='T', (3,1)=N. Fails.
    assert (
        grid_generator._check_for_all_letters(
            grid, "APE", words_to_place, 3, 2, 1, 0, 1
        )
        is False
    )

    # 4.) Overwriting an existing word (place 'TEST' again)
    # Path (1,1)='T', (1,2)='E', (1,3)='S', (1,4)='T'
    # checked_letters becomes "TEST", which is in words_to_place -> False
    assert (
        grid_generator._check_for_all_letters(
            grid, "TEST", words_to_place, 4, 1, 1, 0, 1
        )
        is False
    )

    # 5.) Placing a word where no new letters are added ('AI')
    # Try placing 'AI' V starting at (2,3). Path (2,3)='A', (3,3)='I'.
    # Both cells occupied, matches word. placed_new_letter remains False.
    assert (
        grid_generator._check_for_all_letters(grid, "AI", words_to_place, 2, 2, 3, 1, 0)
        is False
    )


def test_is_valid_placement_scenarios(validation_grid):
    """
    Test is_valid_placement: Handles all of the previous checks. Does the following: bounds, adjacent, and letter checks.
    """
    # Parameters: grid, word, words_to_place, intersect_row, intersect_col, intersect_idx, orientation

    grid = validation_grid
    words_to_place = {"test", "sail"}

    # 1.) Place "ERA" V, intersecting "TEST" at E(1,2), idx 0
    # Word: ERA, Intersect: (1,2), Idx: 0, Orientation: V
    # Expect False because _check_for_all_letters returns False
    assert (
        grid_generator.is_valid_placement(grid, "ERA", words_to_place, 1, 2, 0, "V")
        is False
    )

    # 2.) Place "ASK" H, intersecting "SAIL" at A(2,3), idx 0 -> OOB
    # Expect False because Out of Bounds
    assert (
        grid_generator.is_valid_placement(grid, "ASK", words_to_place, 2, 3, 0, "H")
        is False
    )

    # 3.) Place "TALL" V, intersecting "TEST" at T(1,4), idx 0
    # Expect False because parallel check for 'A' at (2,4) fails
    assert (
        grid_generator.is_valid_placement(grid, "TALL", words_to_place, 1, 4, 0, "V")
        is False
    )

    # 4.) Place "SET" H, intersecting "TEST" at S(1,3), idx 0 -> OOB
    # Expect False because Out of Bounds
    assert (
        grid_generator.is_valid_placement(grid, "SET", words_to_place, 1, 3, 0, "H")
        is False
    )

    # 5.) Place "TIP" V, intersecting "TEST" at T(1,4), idx 0
    # Expect False because parallel check for 'I' at (2,4) fails
    assert (
        grid_generator.is_valid_placement(grid, "TIP", words_to_place, 1, 4, 0, "V")
        is False
    )
