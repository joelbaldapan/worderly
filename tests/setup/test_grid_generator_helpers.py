import pytest
from unittest.mock import patch
from setup import grid_generator


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
    grid = grid_generator.create_empty_grid(5, 5)
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


# Tests for: Creating Grid and Placing Letters
def test_create_empty_grid():
    """Test creating an empty grid of specified dimensions."""
    height, width = 3, 5
    grid = grid_generator.create_empty_grid(height, width)
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
    grid_generator.place_letters_on_grid(grid, word, coords)
    assert grid[0][1] == "R"
    assert grid[1][1] == "U"
    assert grid[2][1] == "N"
    # Check other cells remain None
    assert grid[0][0] is None
    assert grid[1][2] is None


# Tests for: State Update Logic
# For: update_placed_word_coords
def test_update_placed_word_coords(sample_state_data):
    """Test updating the dictionary tracking placed words and their coords."""
    placed_words_coords = sample_state_data["placed_words_coords"].copy()
    middle_coords = sample_state_data["middle_word_coords"]
    used_middle_coords = sample_state_data["used_middle_word_coords"].copy()

    # Grid, Drawn out:
    # E X . . . .
    # . E . . . .
    # . . . . . .
    # . . . W E .
    # . . . . . .
    # . . . . . E

    # For the next tests, these are defined:
    # chosen_placement
    #   - dict {"word": ..., "coord" ...}
    #       - "word" is a str to be placed
    #       - "coord" is the coord that intersects with a letter on grid
    # coords_to_place
    #   - list of (i, j) pairs for coordinates to be placed at
    # We are testing if:
    #   - placed_word_coords[word] is updated
    #   - used_middle_coords is updated or not

    # 1.) Placement doesn't intersect an unused middle coord
    # Grid, Drawn out:
    # E X . . . .
    # . E . . . .
    # . . . . Y .
    # . . . W E .
    # . . . . . .
    # . . . . . E

    chosen_placement_1 = {
        "word": "YE",
        "coord": (4, 2),
    }  # Intersects 'e' (not in middle word coords)
    coords_to_place_1 = [(3, 2), (4, 2)]
    grid_generator.update_placed_word_coords(
        chosen_placement_1,
        coords_to_place_1,
        placed_words_coords,
        middle_coords,
        used_middle_coords,
    )
    assert placed_words_coords["YE"] == coords_to_place_1
    assert len(used_middle_coords) == 2  # Should not increase

    # 2.) Placement intersects an unused middle coord
    # Grid, Drawn out (Middle word is CAPITALIZED):
    # E X . . . .
    # . E . . . .
    # . . . . Y .
    # . . . W E .
    # . . . . . .
    # . . . J O E

    chosen_placement_2 = {
        "word": "JOE",
        "coord": (5, 5),
    }  # Intersects unused middle coord
    coords_to_place_2 = [(5, 3), (5, 4), (5, 5)]
    grid_generator.update_placed_word_coords(
        chosen_placement_2,
        coords_to_place_2,
        placed_words_coords,
        middle_coords,
        used_middle_coords,
    )
    assert placed_words_coords["JOE"] == coords_to_place_2
    assert len(used_middle_coords) == 3  # Should increase
    assert (5, 5) in used_middle_coords  # (5, 5) was used

    # 3.) Placement intersects an already used middle coord
    # E X . . . .
    # . E . . . .
    # . . . . Y .
    # . . . W E .
    # . . . . . T
    # . . . J O E

    chosen_placement_3 = {
        "word": "TE",
        "coord": (5, 5),
    }  # Intersects used middle coord
    coords_to_place_3 = [(4, 5), (5, 5)]
    grid_generator.update_placed_word_coords(
        chosen_placement_3,
        coords_to_place_3,
        placed_words_coords,
        middle_coords,
        used_middle_coords,
    )
    assert placed_words_coords["TE"] == coords_to_place_3
    assert len(used_middle_coords) == 3  # Should not increase further
    assert (5, 5) in used_middle_coords


# For: update_placed_letter_coords
def test_update_placed_letter_coords(sample_state_data):
    """Test updating the dictionary tracking letters and their coordinates."""
    # Starting:
    #     "placed_letter_coords": {
    #     "E": [(0, 0), (1, 1), (5, 5), (3, 4)],
    #     "X": [(0, 1)],
    #     "W": [(3, 3)],
    # },
    placed_letter_coords = sample_state_data["placed_letter_coords"].copy()

    # 1.) New word with new (A) and existing letters (X, E)
    word1 = "AXE"
    coords1 = [(5, 5), (0, 1), (0, 0)]  # A->(5,5), X->(0,1), E->(0,0)
    grid_generator.update_placed_letter_coords(placed_letter_coords, word1, coords1)

    assert placed_letter_coords["A"] == [(5, 5)]  # NEW LETTER (A)
    assert (0, 1) in placed_letter_coords["X"]  # Already there
    assert len(placed_letter_coords["X"]) == 1  # Length unchanged for X
    assert (0, 0) in placed_letter_coords["E"]  # Already there
    assert len(placed_letter_coords["E"]) == 4  # Length unchanged for E

    # 2.) Word adds new coords for existing letters only (E, X, E)
    word2 = "EXE"
    coords2 = [(10, 10), (20, 20), (30, 30)]  # E->(10,10), X->(20,20), E->(30,30)
    grid_generator.update_placed_letter_coords(placed_letter_coords, word2, coords2)

    # Check if all original letters are still there
    assert (10, 10) in placed_letter_coords["E"]
    assert (30, 30) in placed_letter_coords["E"]
    assert (0, 0) in placed_letter_coords["E"]
    assert (1, 1) in placed_letter_coords["E"]
    assert (5, 5) in placed_letter_coords["E"]
    assert len(placed_letter_coords["E"]) == 6
    assert (20, 20) in placed_letter_coords["X"]
    assert (0, 1) in placed_letter_coords["X"]
    # Length for X is correct (1 initial + 1 new = 2)
    assert len(placed_letter_coords["X"]) == 2


# Tests for: Coordinate Calculations
# For: calculate_middle_word_placement_coords
def test_calculate_middle_word_placement_coords():
    """Test calculating diagonal coordinates for the middle word."""
    # PARAMETERS: height, width, middle_word

    # 1.) Just fits, barely
    coords = grid_generator.calculate_middle_word_placement_coords(5, 5, "FIT")
    assert coords == [(0, 0), (2, 2), (4, 4)]

    # 2.) Fits in the middle
    coords = grid_generator.calculate_middle_word_placement_coords(20, 20, "WORD")
    assert coords == [(6, 6), (8, 8), (10, 10), (12, 12)]

    # 3.) Word too long for grid (height)
    coords = grid_generator.calculate_middle_word_placement_coords(4, 10, "LONG")
    assert coords is None

    # 4.) Word too long for grid (width)
    coords = grid_generator.calculate_middle_word_placement_coords(10, 4, "LONG")
    assert coords is None

    # 5.) Word too long for grid (width and height)
    coords = grid_generator.calculate_middle_word_placement_coords(
        10, 4, "PNEUMONOULTRAMICROSCOPICSILICOVOLCANOCONIOSIS"
    )
    assert coords is None


# For: calculate_straight_word_placement
def test_calculate_straight_word_placement_coords():
    """Test calculating coordinates for horizontal/vertical placements."""
    # 1.) Horizontal
    placement_h = {"word": "HORIZ", "coord": (2, 5), "idx": 2, "orientation": "H"}
    coords_h = grid_generator.calculate_straight_word_placement_coords(placement_h)
    assert coords_h == [(2, 3), (2, 4), (2, 5), (2, 6), (2, 7)]

    # 2.) Vertical
    placement_v = {"word": "VERT", "coord": (3, 1), "idx": 1, "orientation": "V"}
    coords_v = grid_generator.calculate_straight_word_placement_coords(placement_v)
    assert coords_v == [(2, 1), (3, 1), (4, 1), (5, 1)]


# Tests for: Placement Finding and Selection
# For: find_possible_placements
@patch("setup.grid_generator.is_valid_placement")
def test_find_possible_placements(mock_is_valid):
    """Test finding potential placements by checking intersections."""
    grid = []
    word = "NEW"
    words_to_place = {"OLD"}
    # Simulate 'E' is already placed at (1,1) and (3,3)
    placed_letter_coords = {
        "O": [(0, 0)],
        "L": [(0, 1)],
        "D": [(0, 2)],
        "E": [(1, 1), (3, 3)],
    }

    # Configure mock_is_valid to return True only for specific calls
    # This simulates how there are some spots where you can't place a given word
    def valid_side_effect(g, w, wtps, r, c, i, o):
        # Simulate only placing 'NEW' vertically at E(1,1) idx 1 is valid
        if w == "NEW" and r == 1 and c == 1 and i == 1 and o == "V":
            return True
        # Simulate only placing 'NEW' horizontally at E(3,3) idx 1 is valid
        if w == "NEW" and r == 3 and c == 3 and i == 1 and o == "H":
            return True
        return False

    mock_is_valid.side_effect = valid_side_effect

    placements = grid_generator.find_possible_placements(
        grid, word, words_to_place, placed_letter_coords
    )

    expected_placements = [
        {"word": "NEW", "coord": (1, 1), "idx": 1, "orientation": "V"},
        {"word": "NEW", "coord": (3, 3), "idx": 1, "orientation": "H"},
    ]

    assert len(placements) == len(expected_placements)
    assert set(tuple((p.items())) for p in placements) == set(
        tuple((p.items())) for p in expected_placements
    )


# For: categorize_placement
def test_categorize_placement():
    """Test categorizing placements based on middle word intersection."""
    placements = [
        {"word": "WA", "coord": (1, 1)},  # Is middle, unused
        {"word": "WB", "coord": (2, 2)},  # Not middle
        {"word": "WC", "coord": (3, 3)},  # Is middle, used
        {"word": "WD", "coord": (4, 4)},  # Is middle, unused
        {"word": "WE", "coord": (5, 5)},  # Not middle
    ]
    middle_coords = {(1, 1), (3, 3), (4, 4)}
    used_middle_coords = {(3, 3)}

    priority, other = grid_generator.categorize_placement(
        placements, middle_coords, used_middle_coords
    )

    # Check priority placements
    assert len(priority) == 2
    assert priority[0] == {"word": "WA", "coord": (1, 1)}  # Is middle, unused
    assert priority[1] == {"word": "WD", "coord": (4, 4)}  # Is middle, unused

    # Check other placements
    assert len(other) == 3
    assert other[0] == {"word": "WB", "coord": (2, 2)}  # Not middle
    assert other[1] == {"word": "WC", "coord": (3, 3)}  # Is middle, but used
    assert other[2] == {"word": "WE", "coord": (5, 5)}  # Not middle


# For: select_random_placement
@patch("setup.grid_generator.random.choice")
def test_select_random_placement(mock_random_choice):
    """Test selecting a placement, prioritizing unused middle coords."""
    priority = [{"p": (1, 1)}, {"p": (2, 2)}]
    other = [{"o": (10, 10)}, {"o": (20, 20)}]

    # 1.) Priority list has items
    # Selected should be priority
    mock_random_choice.return_value = {"p": (1, 1)}
    selected = grid_generator.select_random_placement(priority, other)
    assert selected == {"p": (1, 1)}
    mock_random_choice.assert_called_once_with(priority)

    # 2.) Priority list empty, other list has items
    # Selected should be others
    mock_random_choice.reset_mock()
    mock_random_choice.return_value = {"o": (20, 20)}
    selected = grid_generator.select_random_placement([], other)
    assert selected == {"o": (20, 20)}
    mock_random_choice.assert_called_once_with(other)

    # 3.) Both lists empty
    # Selected should be None
    mock_random_choice.reset_mock()
    selected = grid_generator.select_random_placement([], [])
    assert selected is None
    mock_random_choice.assert_not_called()


# For: apply_placement
# Test apply_placement by mocking its dependencies
@patch("setup.grid_generator.calculate_straight_word_placement_coords")
@patch("setup.grid_generator.update_placed_letter_coords")
@patch("setup.grid_generator.update_placed_word_coords")
@patch("setup.grid_generator.place_letters_on_grid")
def test_apply_placement(
    mock_place_letters, mock_update_word, mock_update_letter, mock_calc_coords
):
    """Test that apply_placement calls its helper functions correctly."""
    grid = []
    chosen = {"word": "APPLY", "coord": (1, 1), "idx": 1, "orientation": "H"}
    placed_letters = {}
    placed_words = {}
    middle_coords = set()
    used_middle = set()
    calculated_coords = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]
    mock_calc_coords.return_value = calculated_coords

    grid_generator.apply_placement(
        grid, chosen, placed_letters, placed_words, middle_coords, used_middle
    )

    # Check if all functions called
    mock_calc_coords.assert_called_once_with(chosen)
    mock_update_letter.assert_called_once_with(
        placed_letters, "APPLY", calculated_coords
    )
    mock_update_word.assert_called_once_with(
        chosen, calculated_coords, placed_words, middle_coords, used_middle
    )
    mock_place_letters.assert_called_once_with(grid, "APPLY", calculated_coords)
