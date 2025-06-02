# ************************************************
# Tests for: Board State and Grid Utilities
# ************************************************
import pytest
from unittest.mock import patch
from setup.grid_generator import board_state
from setup.grid_generator.board_state import PlacementDetail

@pytest.fixture
def empty_grid_3x4():
    """Creates a 3x4 empty grid. (Grid filled with None.)"""
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
def sample_grid_5x5():
    """Creates a 5x5 grid with a word placed for testing."""
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
def sample_state_data():
    """Creates sample data of coordinates used by imperative functions."""
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

# ************************************************
# Tests for: Creating Grid and Placing Letters
# ************************************************
def test_create_empty_grid():
    """Test creating an empty grid of specified dimensions."""
    height, width = 3, 5
    grid = board_state.create_empty_grid(height, width)
    assert len(grid) == height
    assert all(len(row) == width for row in grid)
    assert all(cell is None for row in grid for cell in row)

def test_place_letters_on_grid(empty_grid_3x4):
    """Test placing letters of a word onto specific coordinates."""
    # Grid:
    # R . . .
    # U . . .
    # N . . .
    grid = empty_grid_3x4
    word = "RUN"
    coords = [(0, 1), (1, 1), (2, 1)]
    board_state.place_letters_on_grid(grid, word, coords)
    assert grid[0][1] == "R"
    assert grid[1][1] == "U"
    assert grid[2][1] == "N"
    # Check other cells remain None
    assert grid[0][0] is None
    assert grid[1][2] is None


def test_calculate_straight_word_placement_coords():
    """Test calculating coordinates for horizontal/vertical placements."""
    # 1.) Horizontal
    placement_h = PlacementDetail("HORIZ", (2, 5), 2, "H")
    coords_h = board_state.calculate_straight_word_placement_coords(placement_h)
    assert coords_h == [(2, 3), (2, 4), (2, 5), (2, 6), (2, 7)]

    # 2.) Vertical
    placement_v = PlacementDetail("VERT", (3, 1), 1, "V")
    coords_v = board_state.calculate_straight_word_placement_coords(placement_v)
    assert coords_v == [(2, 1), (3, 1), (4, 1), (5, 1)]