# ************************************************
# Tests for: Main Board Setup Helper Functions
# ************************************************
import pytest
from unittest.mock import patch
from setup.grid_generator import main_generator
from setup.grid_generator.board_state import BoardGenerationState

@pytest.fixture
def initial_board_state_fixture():
    """Creates a clean initial board state object."""
    # Note: We mock create_empty_grid when testing initialize_board_state,
    # but provide a concrete example state here for other tests.
    return BoardGenerationState(
        grid=[[None] * 5 for _ in range(5)],  # Example 5x5 grid
        placed_words_coords={},
        placed_letter_coords={},
        used_middle_word_coords=set(),
        middle_word_coords=set(),
    )

@patch("setup.grid_generator.board_state.create_empty_grid")
def test_initialize_board_state(mock_create_empty):
    """Test initialization of the board state dictionary."""
    height, width = 7, 9
    mock_grid = [[None] * width for _ in range(height)]  # Mock return value of grid
    mock_create_empty.return_value = mock_grid

    state = main_generator.initialize_board_state(height, width)

    mock_create_empty.assert_called_once_with(height, width)
    assert state.grid == mock_grid
    assert state.placed_words_coords == {}
    assert state.placed_letter_coords == {}
    assert state.used_middle_word_coords == set()
    assert state.middle_word_coords == set()

@patch("setup.grid_generator.main_generator.calculate_middle_word_placement_coords")
@patch("setup.grid_generator.main_generator.place_letters_on_grid")
@patch("setup.grid_generator.main_generator.update_placed_letter_coords")
def test_place_middle_word_success(
    mock_update_letters,
    mock_place_letters,
    mock_calc_placement,
    initial_board_state_fixture,
):
    """Test placing middle word successfully."""
    state = initial_board_state_fixture
    middle_word = "START"
    # Simulate successful coords calculation
    calculated_coords = [
        (1, 1),
        (3, 3),
        (5, 5),
        (7, 7),
        (9, 9),
    ]  # Example coords for word of len 5
    mock_calc_placement.return_value = calculated_coords

    result = main_generator.place_middle_word(state, middle_word)

    assert result is True  # Should return True on success

    # Check if all functions were called correctly
    mock_calc_placement.assert_called_once_with(
        len(state.grid), len(state.grid[0]), middle_word
    )
    mock_place_letters.assert_called_once_with(
        state.grid, middle_word, calculated_coords
    )
    # update_placed_letter_coords now expects (state, word, coords)
    mock_update_letters.assert_called_once_with(
        state, middle_word, calculated_coords
    )

    # Check state updates
    assert state.placed_words_coords[middle_word] == calculated_coords
    assert state.middle_word_coords == set(calculated_coords)

@patch("setup.grid_generator.main_generator.calculate_middle_word_placement_coords")
@patch("setup.grid_generator.main_generator.place_letters_on_grid")
@patch("setup.grid_generator.main_generator.update_placed_letter_coords")
def test_place_middle_word_fail_no_coords(
    mock_update_letters,
    mock_place_letters,
    mock_calc_placement,
    initial_board_state_fixture,
):
    """Test placing middle word when coordinate calculation fails."""
    state = initial_board_state_fixture
    middle_word = "TOOLONG"

    # Simulate coordinate calculation failure
    mock_calc_placement.return_value = None

    result = main_generator.place_middle_word(state, middle_word)

    assert result is False  # Should return False on failure
    mock_calc_placement.assert_called_once_with(len(state.grid), len(state.grid[0]), middle_word)

    # Check if other functions were NOT called
    mock_place_letters.assert_not_called()
    mock_update_letters.assert_not_called()

    # Check if state has NOT changed
    assert middle_word not in state.placed_words_coords
    assert state.middle_word_coords == set()

@patch("setup.grid_generator.main_generator.random.shuffle")
@patch("setup.grid_generator.main_generator.find_possible_placements")
@patch("setup.grid_generator.main_generator.select_random_placement")
@patch("setup.grid_generator.main_generator.apply_placement")
def test_place_other_words_success(
    mock_apply, mock_select, mock_find, mock_shuffle, initial_board_state_fixture
):
    """Test the basic loop and placement attempt logic."""
    state = initial_board_state_fixture

    # Add pre-placed middle word for context
    state.placed_words_coords["MIDDLE"] = [(1, 1)]
    state.placed_letter_coords["M"] = [(1, 1)]
    state.middle_word_coords = {(1, 1)}

    words_to_place = ["ONE", "TWO", "THREE"]
    max_total_words = 999  # Allow placing all words

    # Mock shuffle and find possible placement
    def apply_mock_shuffle_side_effect(placements):
        return placements

    mock_shuffle.side_effect = apply_mock_shuffle_side_effect

    # Define a PlacementDetail-like class for mocking
    class Placement:
        def __init__(self, word, coord, idx, orientation):
            self.word = word
            self.coord = coord
            self.idx = idx
            self.orientation = orientation

    # Return Placement objects, not dicts
    mock_find.return_value = [
        Placement("mock", (0, 0), 0, "H")
    ]

    chosen_placement_1 = Placement("ONE", (2, 2), 0, "H")
    chosen_placement_2 = Placement("TWO", (3, 3), 0, "V")
    mock_select.side_effect = [chosen_placement_1, chosen_placement_2, None]

    main_generator.place_other_words(state, words_to_place, max_total_words)

    # Check:
    #   - shuffle was called once
    #   - find_possible_placements was called for each word
    #   - Check select_random_placement was called for each word where find returned placements
    #   - Check apply_placement was called only when select_random_placement returned a value
    mock_shuffle.assert_called_once()
    assert mock_find.call_count == 3
    assert mock_select.call_count == 3
    assert mock_apply.call_count == 2

    # Check if apply placement was called on the two placements
    mock_apply.assert_any_call(
        state, chosen_placement_1
    )
    mock_apply.assert_any_call(
        state, chosen_placement_2
    )

@patch("setup.grid_generator.main_generator.random.shuffle")
@patch("setup.grid_generator.main_generator.find_possible_placements")
@patch("setup.grid_generator.main_generator.select_random_placement")
@patch("setup.grid_generator.main_generator.apply_placement")
def test_place_other_words_reach_max(
    mock_apply, mock_select, mock_find, mock_shuffle, initial_board_state_fixture
):
    """Test the basic loop and placement attempt logic reaching the max words limit."""
    state = initial_board_state_fixture

    # Add pre-placed middle word for context
    state.placed_words_coords["MIDDLE"] = [(1, 1)]
    state.placed_letter_coords["M"] = [(1, 1)]
    state.middle_word_coords = {(1, 1)}
    state.used_middle_word_coords = {(1, 1)}

    words_to_place = ["ONE", "TWO", "THREE"]
    # Allow placing only 2 (so 1 other placement, since we have 1 middle already)
    max_total_words = 2

    # Mock shuffle and find possible placement functions
    def apply_mock_shuffle_side_effect(placements):
        return placements

    mock_shuffle.side_effect = apply_mock_shuffle_side_effect

    # Define a PlacementDetail-like class for mocking
    class Placement:
        def __init__(self, word, coord, idx, orientation):
            self.word = word
            self.coord = coord
            self.idx = idx
            self.orientation = orientation

    mock_find.return_value = [
        Placement("mock", (0, 0), 0, "H")
    ]

    # mock_apply side effect to simulate adding the word and updating the states
    def apply_side_effect(state, chosen_placement):
        word = getattr(chosen_placement, "word", "mock_word")
        if word not in state.placed_words_coords:
            state.placed_words_coords[f"{word}_{len(state.placed_words_coords)}"] = []

    mock_apply.side_effect = apply_side_effect

    # Simulate select_random_placement returning a chosen placement for the first two words,
    # and None for the third
    chosen_placement_1 = Placement("ONE", (2, 2), 0, "H")
    chosen_placement_2 = Placement("TWO", (3, 3), 0, "V")
    chosen_placement_3 = Placement("THREE", (4, 4), 0, "V")
    mock_select.side_effect = [
        chosen_placement_1,
        chosen_placement_2,
        chosen_placement_3,
    ]

    main_generator.place_other_words(state, words_to_place, max_total_words)

    # Check:
    #   - shuffle was called once
    #   - find_possible_placements was called for each word
    #   - Check select_random_placement was called for each word where find returned placements
    #   - Check apply_placement was called only when select_random_placement returned a value
    mock_shuffle.assert_called_once()
    assert mock_find.call_count == 1
    assert mock_select.call_count == 1
    assert mock_apply.call_count == 1

    # Check if apply placement was called on the first chosen placement
    mock_apply.assert_any_call(
        state, chosen_placement_1
    )
    
def test_validate_final_grid():
    """Test the final grid validation logic."""
    min_words = 3

    # 1.) Enough words placed on the grid, all middle coords used
    # Expected to be Valid
    state_valid = BoardGenerationState(
        grid=[],
        placed_words_coords={"M": [], "W1": [], "W2": []},  # 3 words >= min_words
        placed_letter_coords={},
        middle_word_coords={(1, 1), (2, 2)},
        used_middle_word_coords={(1, 1), (2, 2)},
    )
    assert main_generator.validate_final_grid(state_valid, min_words) is True

    # 2.) Not enough words placed on the grid, but all middle coords used
    # Expected to be Invalid
    state_few_words = BoardGenerationState(
        grid=[],
        placed_words_coords={"M": [], "W1": []},  # 2 words < min_words
        placed_letter_coords={},
        middle_word_coords={(1, 1), (2, 2)},
        used_middle_word_coords={(1, 1), (2, 2)},
    )
    assert main_generator.validate_final_grid(state_few_words, min_words) is False

    # 3.) Middle coords not fully used, but enough words on grid
    # Expected to be Invalid
    state_unused_middle = BoardGenerationState(
        grid=[],
        placed_words_coords={"M": [], "W1": [], "W2": []},  # 3 words >= min_words
        placed_letter_coords={},
        middle_word_coords={(1, 1), (2, 2), (3, 3)},  # Has (3,3)
        used_middle_word_coords={(1, 1), (2, 2)},  # Missing (3,3)
    )
    assert main_generator.validate_final_grid(state_unused_middle, min_words) is False

@patch("setup.grid_generator.main_generator.place_letters_on_grid")
def test_capitalize_middle_word_appearance(mock_place_letters):
    """Test capitalizing the middle word on the grid."""
    middle_word = "angelo"
    middle_coords = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
    state = BoardGenerationState(
        grid=[],
        placed_words_coords={middle_word: middle_coords, "other": []},
        placed_letter_coords={},
        middle_word_coords=set(middle_coords),
        used_middle_word_coords=set(),
    )

    main_generator.capitalize_middle_word_appearance(state, middle_word)

    # Check that place_letters_on_grid was called with uppercase word and correct coords
    mock_place_letters.assert_called_once_with(
        state.grid,
        "ANGELO",  # Should be uppercase
        middle_coords,
    )