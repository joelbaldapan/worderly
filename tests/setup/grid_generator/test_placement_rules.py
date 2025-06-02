# ************************************************
# Tests for: Grid Validation
# ************************************************

import pytest

from setup.grid_generator import board_state, placement_rules
from setup.grid_generator.board_state import PlacementDetail
from setup.grid_generator.placement_logic import (
    update_placed_letter_coords,
    update_placed_word_coords,
)


@pytest.fixture
def empty_grid_3x4() -> list[list[None]]:
    """Create a 3x4 empty grid filled with None."""
    # Grid:
    # . . . .
    # . . . .
    # . . . .
    return [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]


@pytest.fixture
def sample_grid_5x5() -> list[list[str | None]]:
    """Create a 5x5 grid with a word placed for testing."""
    grid = board_state.create_empty_grid(5, 5)
    # Place "TEST" horizontally at (1, 1)
    # Grid:
    # . . . . .
    # . T E S T
    # . . . . .
    # . . . . .
    # . . . . .
    grid[1][1] = "T"
    grid[1][2] = "E"
    grid[1][3] = "S"
    grid[1][4] = "T"
    return grid


@pytest.fixture
def sample_state_data() -> dict:
    """Create sample data of coordinates used by imperative functions."""
    # Grid: (EWE is the middle word)
    # E X . . . .
    # . E . . . .
    # . . . . . .
    # . . . W E .
    # . . . . . .
    # . . . . . E
    return {
        "placed_words_coords": {
            "EX": [(0, 0), (0, 1)],
            "XE": [(0, 1), (1, 1)],
            "EWE": [(1, 1), (3, 3), (5, 5)],
            "WE": [(3, 3), (3, 4)],
        },
        "placed_letter_coords": {
            "E": [(0, 0), (1, 1), (5, 5), (3, 4)],
            "X": [(0, 1)],
            "W": [(3, 3)],
        },
        "middle_word_coords": {
            (1, 1),
            (3, 3),
            (5, 5),
        },
        "used_middle_word_coords": {(1, 1), (3, 3)},  # Occupied by xE and We
    }


def testis_within_bounds() -> None:
    """Test boundary checking function."""
    height, width = 10, 20

    # Within bounds
    assert placement_rules.is_within_bounds(0, 0, height, width) is True
    assert placement_rules.is_within_bounds(9, 19, height, width) is True
    assert placement_rules.is_within_bounds(5, 10, height, width) is True

    # Row too low
    assert placement_rules.is_within_bounds(-1, 5, height, width) is False
    # Col too low
    assert placement_rules.is_within_bounds(5, -1, height, width) is False

    # Row too high
    assert placement_rules.is_within_bounds(999, 5, height, width) is False
    # Col too high
    assert placement_rules.is_within_bounds(5, 999, height, width) is False

    # Row and Col a little too high
    assert placement_rules.is_within_bounds(10, 5, height, width) is False
    assert placement_rules.is_within_bounds(5, 20, height, width) is False


@pytest.fixture
def validation_grid() -> list[list[str | None]]:
    """Provide a grid for validation tests with TEST and SAIL placed."""
    grid = board_state.create_empty_grid(6, 6)
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


def testcheck_parallel_cells(validation_grid: list[list[str | None]]) -> None:
    """Test check_parallel_cells to check parallel neighbors."""
    # PARAMETERS: grid, start_row, start_col, dr, dc
    # perp_dr, perp_dc = dc, dr

    grid = validation_grid

    # 1.) Perpedicular neighbors of dc -> -/+ 1 to column
    # Check parallel to 'T' in TEST (H placement, dr=0, dc=1) -> Neighbors (0,1), (2,1) are None
    assert placement_rules.check_parallel_cells(grid, 1, 1, 0, 1) is True

    # Place something parallel
    grid[0][2] = "A"
    grid[2][1] = "A"
    # Check parallel to 'T' in TEST (H placement, dr=0, dc=1) -> Neighbors (0,1), (2,1) occupied
    assert placement_rules.check_parallel_cells(grid, 1, 1, 0, 1) is False
    # Check parallel to 'E' in TEST (H placement, dr=0, dc=1) -> Neighbors (0,2), (2,2) occupied
    assert placement_rules.check_parallel_cells(grid, 1, 2, 0, 1) is False

    # Grid after placing new letters:
    # . . A . . .
    # . T E S T .
    # . A . A . .
    # . . . I . .
    # . . . L . .
    # . . . . . .

    # 2.) Perpedicular neighbors of dr -> -/+ 1 to row
    # Check parallel to 'I' in SAIL (V placement, dr=1, dc=0) -> Neighbors (3,2), (3,4) are None
    assert placement_rules.check_parallel_cells(grid, 3, 3, 1, 0) is True

    # Place something parallel
    grid[3][2] = "T"
    grid[4][4] = "A"
    # Check parallel to 'I' in SAIL (V placement, dr=1, dc=0) -> Neighbors (3,2), (3,4) occupied
    assert placement_rules.check_parallel_cells(grid, 3, 3, 1, 0) is False
    # Check parallel to 'L' in SAIL (V placement, dr=1, dc=0) -> Neighbors (3,2), (3,4) occupied
    assert placement_rules.check_parallel_cells(grid, 4, 3, 1, 0) is False

    # Grid after placing new letters:
    # . . A . . .
    # . T E S T .
    # . A . A . .
    # . . T I . .
    # . . . L A .
    # . . . . . .


def testcheck_adjacent_before_start(validation_grid: list[list[str | None]]) -> None:
    """Test check_adjacent_before_start to check cell before word start."""
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
    assert placement_rules.check_adjacent_before_start(grid, 1, 0, 0, 1) is True
    # Try placing VERT starting at (0,3) -> cell before (-1,3) is OOB -> True
    assert placement_rules.check_adjacent_before_start(grid, 0, 3, 1, 0) is True

    # 2.) In bounds, free space
    # Try placing HORIZ starting at (4,1) -> cell before (4,0) empty -> True
    assert placement_rules.check_adjacent_before_start(grid, 4, 1, 0, 1) is True
    # Try placing VERT starting at (4,1) -> cell before (3,1) empty -> True
    assert placement_rules.check_adjacent_before_start(grid, 4, 1, 1, 0) is True

    # 3.) Conflicting with already placed letters
    # Try placing HORIZ starting at (1,2) -> cell before (1,1) is 'T' -> False
    assert placement_rules.check_adjacent_before_start(grid, 1, 2, 0, 1) is False
    # Try placing VERT starting at (2,3) -> cell before (1,3) is 'S' -> False
    assert placement_rules.check_adjacent_before_start(grid, 2, 3, 1, 0) is False


def testcheck_adjacent_after_end(validation_grid: list[list[str | None]]) -> None:
    """Test check_adjacent_after_end to check cell after word end."""
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
    assert placement_rules.check_adjacent_after_end(grid, 1, 3, 0, 1) is False
    # Try placing VERT ending at (3,3) ('I') -> cell after (4,3) is 'L' -> False
    assert placement_rules.check_adjacent_after_end(grid, 3, 3, 1, 0) is False
    # Try placing HORIZ ending at (0,0) -> cell after (0,1) is None -> True
    assert placement_rules.check_adjacent_after_end(grid, 0, 0, 0, 1) is True
    # Try placing VERT ending at (4,4) -> cell after (5,4) is OOB -> True
    assert placement_rules.check_adjacent_after_end(grid, 4, 4, 1, 0) is True


def testcheck_for_all_letters(validation_grid: list[list[str | None]]) -> None:
    """Test check_for_all_letters for letter conflicts and placement rules."""
    grid = validation_grid
    words_to_place = {"test", "sail"}

    # 1.) Placement intersecting 'E' (place 'ERA' V) conflicts on letter 'R' vs 'E'
    assert (
        placement_rules.check_for_all_letters(
            grid, "ERA", words_to_place, (0, 2), (1, 0),
        )
        is False
    )

    # 2.) Conflict with existing letter ('S')
    assert (
        placement_rules.check_for_all_letters(
            grid, "SET", words_to_place, (1, 2), (0, 1),
        )
        is False
    )

    # 3.) Parallel conflict during placement
    assert (
        placement_rules.check_for_all_letters(
            grid, "APE", words_to_place, (2, 1), (0, 1),
        )
        is False
    )

    # 4.) Overwriting an existing word (place 'TEST' again)
    assert (
        placement_rules.check_for_all_letters(
            grid, "TEST", words_to_place, (1, 1), (0, 1),
        )
        is False
    )

    # 5.) Placing a word where no new letters are added ('AI')
    assert (
        placement_rules.check_for_all_letters(
            grid, "AI", words_to_place, (2, 3), (1, 0),
        )
        is False
    )


def test_is_valid_placement_scenarios(validation_grid: list[list[str | None]]) -> None:
    """Test is_valid_placement for bounds, adjacent, and letter checks."""
    # Parameters: grid, word, words_to_place, intersect_row, intersect_col, intersect_idx, orientation

    grid = validation_grid
    words_to_place = {"test", "sail"}

    # 1.) Place "ERA" V, intersecting "TEST" at E(1,2), idx 0
    # Word: ERA, Intersect: (1,2), Idx: 0, Orientation: V
    # Expect False because check_for_all_letters returns False
    assert (
        placement_rules.is_valid_placement(
            grid, "ERA", words_to_place,
            {"row": 1, "col": 2, "idx": 0}, "V",
        )
        is False
    )

    # 2.) Place "ASK" H, intersecting "SAIL" at A(2,3), idx 0 -> OOB
    # Expect False because Out of Bounds
    assert (
        placement_rules.is_valid_placement(
            grid, "ASK", words_to_place,
            {"row": 2, "col": 3, "idx": 0}, "H",
        )
        is False
    )

    # 3.) Place "TALL" V, intersecting "TEST" at T(1,4), idx 0
    # Expect False because parallel check for 'A' at (2,4) fails
    assert (
        placement_rules.is_valid_placement(
            grid, "TALL", words_to_place,
            {"row": 1, "col": 4, "idx": 0}, "V",
        )
        is False
    )

    # 4.) Place "SET" H, intersecting "TEST" at S(1,3), idx 0 -> OOB
    # Expect False because Out of Bounds
    assert (
        placement_rules.is_valid_placement(
            grid, "SET", words_to_place,
            {"row": 1, "col": 3, "idx": 0}, "H",
        )
        is False
    )

    # 5.) Place "TIP" V, intersecting "TEST" at T(1,4), idx 0
    # Expect False because parallel check for 'I' at (2,4) fails
    assert (
        placement_rules.is_valid_placement(
            grid, "TIP", words_to_place,
            {"row": 1, "col": 4, "idx": 0}, "V",
        )
        is False
    )


# ************************************************
# Tests for: State Update Logic
# ************************************************
def test_update_placed_word_coords(sample_state_data: dict) -> None:
    """Test updating the dictionary tracking placed words and their coords."""
    placed_words_coords = sample_state_data["placed_words_coords"].copy()
    middle_coords = sample_state_data["middle_word_coords"]
    used_middle_coords = sample_state_data["used_middle_word_coords"].copy()

    # 1.) Placement doesn't intersect an unused middle coord
    chosen_placement_1 = PlacementDetail("YE", (4, 2), 0, "H")
    coords_to_place_1 = [(3, 2), (4, 2)]
    update_placed_word_coords(
        chosen_placement_1,
        coords_to_place_1,
        # Simulate a BoardGenerationState-like object for this test
        type("FakeState", (), {
            "placed_words_coords": placed_words_coords,
            "middle_word_coords": middle_coords,
            "used_middle_word_coords": used_middle_coords,
        })(),
    )
    assert placed_words_coords["YE"] == coords_to_place_1
    assert len(used_middle_coords) == 2  # Should not increase

    # 2.) Placement intersects an unused middle coord
    chosen_placement_2 = PlacementDetail("JOE", (5, 5), 2, "H")
    coords_to_place_2 = [(5, 3), (5, 4), (5, 5)]
    update_placed_word_coords(
        chosen_placement_2,
        coords_to_place_2,
        type("FakeState", (), {
            "placed_words_coords": placed_words_coords,
            "middle_word_coords": middle_coords,
            "used_middle_word_coords": used_middle_coords,
        })(),
    )
    assert placed_words_coords["JOE"] == coords_to_place_2
    assert len(used_middle_coords) == 3  # Should increase
    assert (5, 5) in used_middle_coords

    # 3.) Placement intersects an already used middle coord
    chosen_placement_3 = PlacementDetail("TE", (5, 5), 1, "H")
    coords_to_place_3 = [(4, 5), (5, 5)]
    update_placed_word_coords(
        chosen_placement_3,
        coords_to_place_3,
        type("FakeState", (), {
            "placed_words_coords": placed_words_coords,
            "middle_word_coords": middle_coords,
            "used_middle_word_coords": used_middle_coords,
        })(),
    )
    assert placed_words_coords["TE"] == coords_to_place_3
    assert len(used_middle_coords) == 3  # Should not increase further
    assert (5, 5) in used_middle_coords


def test_update_placed_letter_coords(sample_state_data: dict) -> None:
    """Test updating the dictionary tracking letters and their coordinates."""
    placed_letter_coords = sample_state_data["placed_letter_coords"].copy()

    # 1.) New word with new (A) and existing letters (X, E)
    word1 = "AXE"
    coords1 = [(5, 5), (0, 1), (0, 0)]  # A->(5,5), X->(0,1), E->(0,0)
    # Simulate a BoardGenerationState-like object for this test
    fake_state = type("FakeState", (), {"placed_letter_coords": placed_letter_coords})()
    update_placed_letter_coords(fake_state, word1, coords1)

    assert placed_letter_coords["A"] == [(5, 5)]  # NEW LETTER (A)
    assert (0, 1) in placed_letter_coords["X"]  # Already there
    assert len(placed_letter_coords["X"]) == 1  # Length unchanged for X
    assert (0, 0) in placed_letter_coords["E"]  # Already there
    assert len(placed_letter_coords["E"]) == 4  # Length unchanged for E

    # 2.) Word adds new coords for existing letters only (E, X, E)
    word2 = "EXE"
    coords2 = [(10, 10), (20, 20), (30, 30)]  # E->(10,10), X->(20,20), E->(30,30)
    update_placed_letter_coords(fake_state, word2, coords2)

    assert (10, 10) in placed_letter_coords["E"]
    assert (30, 30) in placed_letter_coords["E"]
    assert (0, 0) in placed_letter_coords["E"]
    assert (1, 1) in placed_letter_coords["E"]
    assert (5, 5) in placed_letter_coords["E"]
    assert len(placed_letter_coords["E"]) == 6
    assert (20, 20) in placed_letter_coords["X"]
    assert (0, 1) in placed_letter_coords["X"]
    assert len(placed_letter_coords["X"]) == 2


# ************************************************
# Tests for: Coordinate Calculations
# ************************************************
def test_calculate_middle_word_placement_coords() -> None:
    """Test calculating diagonal coordinates for the middle word.

    Returns:
        list[tuple[int, int]] | None: List of coordinates or None if not possible.

    """
    coords = board_state.calculate_middle_word_placement_coords(5, 5, "FIT")
    assert coords == [(0, 0), (2, 2), (4, 4)]

    coords = board_state.calculate_middle_word_placement_coords(20, 20, "WORD")
    assert coords == [(6, 6), (8, 8), (10, 10), (12, 12)]

    coords = board_state.calculate_middle_word_placement_coords(4, 10, "LONG")
    assert coords is None

    coords = board_state.calculate_middle_word_placement_coords(10, 4, "LONG")
    assert coords is None

    coords = board_state.calculate_middle_word_placement_coords(
        10, 4, "PNEUMONOULTRAMICROSCOPICSILICOVOLCANOCONIOSIS",
    )
    assert coords is None
