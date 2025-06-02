# ************************************************
# Tests for: Board State and Grid Utilities
# ************************************************

import pytest

from setup.grid_generator import board_state


@pytest.fixture
def empty_grid_3x4() -> list[list[None]]:
    """Create a 3x4 empty grid (filled with None).

    Returns:
        list[list[None]]: A 3x4 grid filled with None.

    """
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
    """Create a 5x5 grid with a word placed for testing.

    Returns:
        list[list[str | None]]: A 5x5 grid with "TEST" placed horizontally at (1, 1).

    """
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
def sample_state_data() -> dict[str, object]:
    """Create sample data of coordinates used by imperative functions.

    Returns:
        dict[str, object]: Sample state data for testing.

    """
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
