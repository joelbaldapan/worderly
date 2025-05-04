import pytest
from unittest.mock import patch

from gameplay import powerup_handler
from gameplay import game_constants


@pytest.fixture
def sample_statistics_fixture():
    """Creates a sample statistics dictionary."""
    return {
        "letters": "A B C",
        "lives_left": 3,
        "points": 10,
        "last_guess": None,
        "combo": 0,
        "power_points": 1,  # Start with 1 power point for easier testing of use_powerup
        "shield_turns": 0,
    }


@pytest.fixture
def sample_game_state_fixture(sample_statistics_fixture):
    """Creates a sample game state dictionary."""
    # Example coordinates for a simple grid
    hidden_coords = {(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)}
    found_coords = {(0, 0)}  # Simulate one letter found
    return {
        "player_name": "Power Tester",
        "statistics": sample_statistics_fixture,
        "hidden_grid": [["#"] * 2 for _ in range(3)],  # Dummy 3x2 grid
        "last_guess_coords": [],
        "correctly_guessed_words": set(),
        "hidden_letter_coords": hidden_coords
        - found_coords,  # {(0,1), (1,0), (1,1), (2,0), (2,1)}
        "found_letter_coords": found_coords.copy(),
        "next_message": "",
        "next_message_color": "white",
    }


@pytest.fixture(
    params=[
        # Wizard, initial_combo, expected_powerpoint_increment
        ({"combo_requirement": 3, "color": "red"}, 2, 0),  # Combo < req
        ({"combo_requirement": 3, "color": "red"}, 3, 1),  # Combo == req
        ({"combo_requirement": 3, "color": "red"}, 4, 0),  # Combo > req, not multiple
        ({"combo_requirement": 3, "color": "red"}, 6, 1),  # Combo multiple of req
        ({"combo_requirement": None, "color": "white"}, 5, 0),  # No req
        ({"combo_requirement": 4, "color": "green"}, 0, 0),  # Combo is 0
    ]
)
def power_point_update_data(request):
    """Creates data for testing update_power_points."""
    return request.param


@pytest.fixture(
    params=[
        # Wizard Color, Expected Action/Result
        ("red", "word_reveal"),
        ("green", "random_reveal"),
        ("magenta", "shield_increase"),
        ("blue", "life_increase"),
    ]
)
def use_powerup_data(request):
    """Creates data for testing use_powerup based on wizard color."""
    return request.param


@pytest.fixture
def sample_words_to_find_fixture():
    """Sample words_to_find for powerup tests."""
    return {
        "ONE": [(0, 0), (0, 1)],
        "TWO": [(1, 0), (1, 1)],
        "TEN": [(2, 0), (0, 0), (1, 0)],  # Shares letters with ONE and TWO
    }


@pytest.fixture
def sample_final_grid_fixture():
    """Sample final grid for powerup tests."""
    grid = [[None] * 2 for _ in range(3)]
    grid[0][0] = "O"
    grid[0][1] = "N"
    grid[1][0] = "T"
    grid[1][1] = "W"
    grid[2][0] = "E"
    # grid[2][1] = None # Example setup
    return grid


# ************************************************
# Tests for: Power Points Updating
# ************************************************


def test_check_power_point_increment():
    """Test the logic for checking if power points should increment."""
    # 1.) Meets requirement
    stats1 = {"combo": 3}
    assert powerup_handler.check_power_point_increment(3, stats1) is True

    # 2.) Combo is multiple of requirement
    stats2 = {"combo": 6}
    assert powerup_handler.check_power_point_increment(3, stats2) is True

    # 3.) Combo less than requirement
    stats3 = {"combo": 2}
    assert powerup_handler.check_power_point_increment(3, stats3) is False

    # 4.) Combo greater but not multiple
    stats4 = {"combo": 4}
    assert powerup_handler.check_power_point_increment(3, stats4) is False

    # 5.) Combo is zero
    stats5 = {"combo": 0}
    assert powerup_handler.check_power_point_increment(3, stats5) is False

    # 6.) No combo requirement
    stats6 = {"combo": 5}
    assert powerup_handler.check_power_point_increment(None, stats6) is False


def test_update_power_points(power_point_update_data, sample_game_state_fixture):
    """Test updating power points based on combo and wizard requirement."""
    wizard, initial_combo, expected_increment = power_point_update_data
    game_state = sample_game_state_fixture
    game_state["statistics"]["combo"] = initial_combo
    init_powerpoints = game_state["statistics"]["power_points"]

    powerup_handler.update_power_points(game_state, wizard)

    assert (
        game_state["statistics"]["power_points"]
        == init_powerpoints + expected_increment
    )


# ************************************************
# Tests for: Power Up Logic
# ************************************************


@patch("random.randint")
@patch("random.sample")
def test_get_coords_for_random_reveal(mock_sample, mock_randint):
    """Test selecting random coordinates to reveal."""
    hidden_coords_set = {
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
    }
    min_r, max_r = 5, 8

    # Simulate randint choosing 0 and sample choosing specific coords
    mock_randint.return_value = 6
    expected_coords = [(1, 1), (3, 3), (5, 5), (7, 7), (0, 0), (2, 2)]
    mock_sample.return_value = expected_coords

    result = powerup_handler.get_coords_for_random_reveal(
        hidden_coords_set, min_r, max_r
    )

    # Check if mock functions were called
    mock_randint.assert_called_once_with(min_r, max_r)
    mock_sample.assert_called_once()

    # Check if received result is the same
    assert result == expected_coords


@patch("random.randint")
@patch("random.sample")
def test_get_coords_for_random_reveal_less_available(mock_sample, mock_randint):
    """Test random reveal when fewer coords are available than max_reveal."""
    hidden_coords_set = {(0, 0), (1, 1), (2, 2)}  # Only 3 available
    min_r, max_r = 5, 8

    # Simulate randint choosing 7 (but only 3 available)
    mock_randint.return_value = 7
    expected_coords = [(1, 1), (0, 0), (2, 2)]  # Sample will return all 3
    mock_sample.return_value = expected_coords

    result = powerup_handler.get_coords_for_random_reveal(
        hidden_coords_set, min_r, max_r
    )

    # Check if mock functions were called
    mock_randint.assert_called_once_with(min_r, max_r)
    mock_sample.assert_called_once()

    # Check if received result is the same
    assert result == expected_coords


@patch("random.choice")
def test_get_coords_for_word_reveal(mock_choice, sample_words_to_find_fixture):
    """Test selecting coordinates for a random unrevealed word."""
    words_to_find = sample_words_to_find_fixture
    # Simulate "HELLO" is already guessed
    correct_guesses = {"ONE"}

    # Simulate random.choice picking "TEN"
    mock_choice.return_value = "TEN"
    expected_coords = words_to_find["TEN"]

    result = powerup_handler.get_coords_for_word_reveal(words_to_find, correct_guesses)

    # Check results
    mock_choice.assert_called_once()
    assert result == expected_coords


# ************************************************
# Tests for: Main Powerup Function
# ************************************************


@patch("gameplay.powerup_handler.get_coords_for_word_reveal")
@patch("gameplay.powerup_handler.apply_coordinate_reveal")
@patch("gameplay.powerup_handler.check_for_completed_words")
def test_use_powerup_reveal_completes_words(
    mock_check_completed,
    mock_apply_reveal,
    mock_word_reveal,
    sample_game_state_fixture,
    sample_words_to_find_fixture,
    sample_final_grid_fixture,
):
    """Test reveal powerup message when words are implicitly completed."""
    wizard_color = "red"  # Example: Random word reveal powerup
    game_state = sample_game_state_fixture
    selected_wizard = {"color": wizard_color, "combo_requirement": 3}
    initial_guessed_words = game_state["correctly_guessed_words"].copy()

    # Mock Functionss
    coords_revealed = [(1, 0), (1, 1)]  # Coords for "TWO"
    mock_word_reveal.return_value = coords_revealed
    completed = ["TWO"]  # Simulate "TWO" being completed by the reveal
    mock_check_completed.return_value = completed

    powerup_handler.use_powerup(
        game_state,
        selected_wizard,
        sample_words_to_find_fixture,
        sample_final_grid_fixture,
    )

    # Check if mock functions were run
    mock_word_reveal.assert_called_once()
    mock_apply_reveal.assert_called_once_with(
        game_state, sample_final_grid_fixture, coords_revealed
    )
    mock_check_completed.assert_called_once_with(
        game_state, sample_words_to_find_fixture
    )

    # Check message indicates completed words and correctly_guessed_words set was updated
    assert game_state["next_message"] == game_constants.POWERUP_REVEAL_WORDS_MSG.format(
        ", ".join(completed)
    )
    assert game_state["correctly_guessed_words"] == initial_guessed_words.union(
        set(completed)
    )
