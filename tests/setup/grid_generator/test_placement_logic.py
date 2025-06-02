import pytest
from unittest.mock import patch
from setup.grid_generator import placement_logic
from setup.grid_generator.board_state import PlacementDetail, BoardGenerationState

# ************************************************
# Tests for: Placement Finding and Selection
# ************************************************
@patch("setup.grid_generator.placement_logic.is_valid_placement")
def test_find_possible_placements(mock_is_valid):
    """Test finding potential placements by checking intersections."""
    grid = []
    word = "NEW"
    words_to_place = {"OLD"}
    placed_letter_coords = {
        "O": [(0, 0)],
        "L": [(0, 1)],
        "D": [(0, 2)],
        "E": [(1, 1), (3, 3)],
    }

    # for is_valid_placement
    def valid_side_effect(grid, word, words_to_place_set, intersection_info, orientation):
        r = intersection_info["row"]
        c = intersection_info["col"]
        i = intersection_info["idx"]
        # Simulate only placing 'NEW' vertically at E(1,1) idx 1 is valid
        if word == "NEW" and r == 1 and c == 1 and i == 1 and orientation == "V":
            return True
        # Simulate only placing 'NEW' horizontally at E(3,3) idx 1 is valid
        if word == "NEW" and r == 3 and c == 3 and i == 1 and orientation == "H":
            return True
        return False

    mock_is_valid.side_effect = valid_side_effect

    placements = placement_logic.find_possible_placements(
        grid, word, words_to_place, placed_letter_coords
    )

    expected_placements = [
        PlacementDetail("NEW", (1, 1), 1, "V"),
        PlacementDetail("NEW", (3, 3), 1, "H"),
    ]

    assert len(placements) == len(expected_placements)
    for p in expected_placements:
        assert any(
            (pl.word, pl.coord, pl.idx, pl.orientation) == (p.word, p.coord, p.idx, p.orientation)
            for pl in placements
        )

def test_categorize_placement():
    """Test categorizing placements based on middle word intersection."""
    placements = [
        PlacementDetail("WA", (1, 1), 0, "H"),  # Is middle, unused
        PlacementDetail("WB", (2, 2), 0, "H"),  # Not middle
        PlacementDetail("WC", (3, 3), 0, "H"),  # Is middle, used
        PlacementDetail("WD", (4, 4), 0, "H"),  # Is middle, unused
        PlacementDetail("WE", (5, 5), 0, "H"),  # Not middle
    ]
    middle_coords = {(1, 1), (3, 3), (4, 4)}
    used_middle_coords = {(3, 3)}

    priority, other = placement_logic.categorize_placement(
        placements, middle_coords, used_middle_coords
    )

    # Check priority placements
    assert len(priority) == 2
    assert priority[0].word == "WA" and priority[0].coord == (1, 1)
    assert priority[1].word == "WD" and priority[1].coord == (4, 4)

    # Check other placements
    assert len(other) == 3
    assert other[0].word == "WB" and other[0].coord == (2, 2)
    assert other[1].word == "WC" and other[1].coord == (3, 3)
    assert other[2].word == "WE" and other[2].coord == (5, 5)

@patch("setup.grid_generator.placement_logic.random.choice")
def test_select_random_placement(mock_random_choice):
    """Test selecting a placement, prioritizing unused middle coords."""
    # Use PlacementDetail objects for consistency
    p1 = PlacementDetail("P", (1, 1), 0, "H")
    p2 = PlacementDetail("P", (2, 2), 0, "H")
    o1 = PlacementDetail("O", (10, 10), 0, "H")
    o2 = PlacementDetail("O", (20, 20), 0, "H")
    priority = [p1, p2]
    other = [o1, o2]

    # 1.) Priority list has items
    mock_random_choice.return_value = p1
    selected = placement_logic.select_random_placement(priority, other)
    assert selected == p1
    mock_random_choice.assert_called_once_with(priority)

    # 2.) Priority list empty, other list has items
    mock_random_choice.reset_mock()
    mock_random_choice.return_value = o2
    selected = placement_logic.select_random_placement([], other)
    assert selected == o2
    mock_random_choice.assert_called_once_with(other)

    # 3.) Both lists empty
    mock_random_choice.reset_mock()
    selected = placement_logic.select_random_placement([], [])
    assert selected is None
    mock_random_choice.assert_not_called()

@patch("setup.grid_generator.placement_logic.calculate_straight_word_placement_coords")
@patch("setup.grid_generator.placement_logic.update_placed_letter_coords")
@patch("setup.grid_generator.placement_logic.update_placed_word_coords")
@patch("setup.grid_generator.placement_logic.place_letters_on_grid")
def test_apply_placement(
    mock_place_letters, mock_update_word, mock_update_letter, mock_calc_coords
):
    """Test that apply_placement calls its helper functions correctly."""
    # Create a fake BoardGenerationState
    state = BoardGenerationState(
        grid=[],
        placed_words_coords={},
        placed_letter_coords={},
        used_middle_word_coords=set(),
        middle_word_coords=set(),
    )
    chosen = PlacementDetail("APPLY", (1, 1), 1, "H")
    calculated_coords = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]
    mock_calc_coords.return_value = calculated_coords

    placement_logic.apply_placement(
        state, chosen
    )

    # Check if all functions called
    mock_calc_coords.assert_called_once_with(chosen)
    mock_update_letter.assert_called_once_with(
        state, "APPLY", calculated_coords
    )
    mock_update_word.assert_called_once_with(
        chosen, calculated_coords, state
    )
    mock_place_letters.assert_called_once_with(state.grid, "APPLY", calculated_coords)