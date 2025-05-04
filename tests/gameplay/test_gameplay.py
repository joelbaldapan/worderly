import pytest
from unittest.mock import patch
import copy

from gameplay import gameplay
from gameplay import game_constants


@pytest.fixture
def sample_settings():
    """Creates sample settings."""
    return {
        "heart_point_mode": True,
    }


@pytest.fixture
def sample_settings_no_hp():
    """Creates sample settings with heart_point_mode False."""
    return {
        "heart_point_mode": False,
    }


@pytest.fixture
def sample_wizard():
    """Creates sample wizard data."""
    # Using data similar to WIZARDS_DATA
    # Though didn't include some that aren't needed here
    return {
        "name": "Mock Wizard",
        "color": "cyan",
        "starting_lives": 3,
        "combo_requirement": 3,
        "small_art": "artplaceholdere",
    }


@pytest.fixture
def sample_game_state(sample_wizard):
    """Creates a basic game state dictionary."""
    return {
        "player_name": "Tester",
        "statistics": {
            "letters": "A B C",
            "lives_left": 3,
            "points": 0,
            "last_guess": None,
            "combo": 0,
            "power_points": 1,  # Start with 1 point for testing
            "shield_turns": 0,
        },
        "hidden_grid": [["#"]],
        "last_guess_coords": [],
        "correctly_guessed_words": set(),
        "hidden_letter_coords": {(0, 0)},
        "found_letter_coords": set(),
        "next_message": "Welcome",
        "next_message_color": sample_wizard["color"],
    }


@pytest.fixture
def sample_final_grid():
    """Sample minimal final grid."""
    return [["A"]]


@pytest.fixture
def sample_words_to_find():
    """Sample minimal words_to_find."""
    return {"A": [(0, 0)]}


PATCH_PRINT_GRID = "gameplay.gameplay.print_grid"
PATCH_PRINT_STATS = "gameplay.gameplay.print_statistics"
PATCH_PRINT_MSG = "gameplay.gameplay.print_message"
PATCH_PRINT_LB = "gameplay.gameplay.print_leaderboard"
PATCH_GET_INPUT = "gameplay.gameplay.get_input"
PATCH_GET_GUESS = "gameplay.gameplay.get_guess"
PATCH_CLEAR_SCREEN = "gameplay.gameplay.clear_screen"
PATCH_INIT_STATE = "gameplay.gameplay.initialize_game_state"
PATCH_PROC_GUESS = "gameplay.gameplay.process_guess"
PATCH_CHECK_GO = "gameplay.gameplay.check_game_over"
PATCH_UPDATE_PP = "gameplay.gameplay.update_power_points"
PATCH_USE_PU = "gameplay.gameplay.use_powerup"
PATCH_LOAD_LB = "gameplay.gameplay.load_leaderboard"
PATCH_SAVE_SCORE = "gameplay.gameplay.save_score"
PATCH_UPDATE_DISPLAY = "gameplay.gameplay.update_display"
PATCH_UPDATE_GO_DISPLAY = "gameplay.gameplay.update_game_over_display"
PATCH_UPDATE_END_DISPLAY = "gameplay.gameplay.update_end_game_display"


# ************************************************
# Tests for: Update Displays
# ************************************************


@patch(PATCH_CLEAR_SCREEN)
@patch(PATCH_PRINT_GRID)
@patch(PATCH_PRINT_STATS)
@patch(PATCH_PRINT_MSG)
def test_update_display(
    mock_print_msg,
    mock_print_stats,
    mock_print_grid,
    mock_clear,
    sample_settings,
    sample_game_state,
    sample_wizard,
):
    """Test that update_display calls all the necessary display functions."""
    gameplay.update_display(sample_settings, sample_game_state, sample_wizard)

    # Check if all necessary functions called
    mock_clear.assert_called_once()
    mock_print_grid.assert_called_once()
    mock_print_stats.assert_called_once()
    mock_print_msg.assert_called_once()


@patch(PATCH_GET_INPUT)
@patch(PATCH_CLEAR_SCREEN)
@patch(PATCH_SAVE_SCORE)
@patch(PATCH_LOAD_LB)
@patch(PATCH_PRINT_LB)
@patch(PATCH_PRINT_MSG)
def test_update_end_game_display(
    mock_print_msg,
    mock_print_lb,
    mock_load_lb,
    mock_save,
    mock_clear,
    mock_get_input,
    sample_settings,
):
    """Test the sequence of actions in the end game display."""
    player_name = "WINNAHHH"
    final_score = 100
    mock_leaderboard_data = [{"name": "WINNAHHH", "score": 100}]
    mock_load_lb.return_value = mock_leaderboard_data

    gameplay.update_end_game_display(sample_settings, player_name, final_score)

    # Check if all necessary functions called
    mock_get_input.assert_any_call(
        sample_settings, "  > Press Enter to continue... "
    )
    mock_clear.assert_called_once()
    mock_save.assert_called_once_with(player_name, final_score)
    mock_load_lb.assert_called_once()
    mock_print_lb.assert_called_once_with(sample_settings, mock_leaderboard_data)
    mock_print_msg.assert_called_once()


# ************************************************
# Tests for: Getting Guesses
# ************************************************


@patch(PATCH_GET_INPUT)
@patch(PATCH_UPDATE_DISPLAY)
def test_get_guess_valid_word(
    mock_update_disp, mock_get_input, sample_settings, sample_game_state, sample_wizard
):
    """Test get_guess returns a valid word input."""
    mock_get_input.return_value = "  VALID  "  # Input with whitespace/caps
    expected_guess = "valid"

    guess = gameplay.get_guess(sample_settings, sample_game_state, sample_wizard)

    assert guess == expected_guess
    mock_get_input.assert_called_once()
    mock_update_disp.assert_not_called()  # Should not be called for first valid input


@patch(PATCH_GET_INPUT)
@patch(PATCH_UPDATE_DISPLAY)  # Mock the whole update_display here
def test_get_guess_invalid_then_valid(
    mock_update_disp, mock_get_input, sample_settings, sample_game_state, sample_wizard
):
    """Test get_guess handles invalid input then accepts valid input."""
    # Simulate empty, then non-alpha, then valid input
    mock_get_input.side_effect = ["", "123", "GOOD"]
    expected_guess = "good"

    guess = gameplay.get_guess(sample_settings, sample_game_state, sample_wizard)

    assert guess == expected_guess


@patch(PATCH_GET_INPUT)
@patch(PATCH_UPDATE_DISPLAY)
def test_get_guess_powerup_command_valid(
    mock_update_disp, mock_get_input, sample_settings, sample_game_state, sample_wizard
):
    """Test get_guess returns the powerup command when valid."""
    # Ensure wizard is not white and has power points
    wizard = sample_wizard
    wizard["color"] = "red"  # Not white
    state = copy.deepcopy(sample_game_state)
    state["statistics"]["power_points"] = 1  # Has points

    mock_get_input.return_value = game_constants.POWERUP_COMMAND

    guess = gameplay.get_guess(sample_settings, state, wizard)

    assert guess == game_constants.POWERUP_COMMAND
    mock_get_input.assert_called_once()
    mock_update_disp.assert_not_called()  # No errors displayed


@patch(PATCH_GET_INPUT)
@patch(PATCH_UPDATE_DISPLAY)
def test_get_guess_powerup_command_invalid_wizard(
    mock_update_disp, mock_get_input, sample_settings, sample_game_state, sample_wizard
):
    """Test get_guess handles powerup attempt with white wizard."""
    # White wizard cannot use powerups
    wizard_white = sample_wizard
    wizard_white["color"] = "bright_white"
    state = copy.deepcopy(sample_game_state)
    state["statistics"]["power_points"] = 1
    mock_get_input.side_effect = [
        game_constants.POWERUP_COMMAND,
        "valid",
    ]  # Try powerup, then give valid
    
    guess = gameplay.get_guess(sample_settings, state, wizard_white)
    assert guess == "valid"
    assert mock_update_disp.call_count == 1  # Error message displayed


@patch(PATCH_GET_INPUT)
@patch(PATCH_UPDATE_DISPLAY)
def test_get_guess_powerup_command_invalid_points(
    mock_update_disp, mock_get_input, sample_settings, sample_game_state, sample_wizard
):
    """Test get_guess handles powerup attempt with insufficient points."""
    # Non-white wizard can use powerups
    wizard_red = sample_wizard
    wizard_red["color"] = "red"  
    state = copy.deepcopy(sample_game_state)
    state["statistics"]["power_points"] = 0  # No points
    mock_get_input.side_effect = [
        game_constants.POWERUP_COMMAND,
        "valid",
    ]  # Try powerup, then give valid

    guess = gameplay.get_guess(sample_settings, state, wizard_red)
    assert guess == "valid"
    assert mock_update_disp.call_count == 1  # Error message displayed


# ************************************************
# Tests for: Running Game
# We will see if the flow is accurate
# ************************************************


@patch(PATCH_INIT_STATE)
@patch(PATCH_UPDATE_DISPLAY)
@patch(PATCH_GET_GUESS)
@patch(PATCH_PROC_GUESS)
@patch(PATCH_UPDATE_PP)
@patch(PATCH_USE_PU)
@patch(PATCH_CHECK_GO)
@patch(PATCH_UPDATE_GO_DISPLAY)
@patch(PATCH_UPDATE_END_DISPLAY)
def test_run_game_win_hp_mode(
    mock_end_disp,
    mock_go_disp,
    mock_check_go,
    mock_use_pu,
    mock_update_pp,
    mock_proc_guess,
    mock_get_guess_func,
    mock_update_disp,
    mock_init_state,
    sample_settings,
    sample_final_grid,
    sample_words_to_find,
    sample_wizard,
):
    """Test a winning game flow in Heart Point mode."""
    # Initial state
    player_name = "Player1"
    middle_word = "MIDDLE"

    mock_init_state.return_value = {
        "statistics": {"points": 50},
        "player_name": player_name,
    }  # Simplified state
    
    # Game flow: valid guess -> win
    mock_get_guess_func.return_value = "goodguess"  # Make get_guess return the word
    mock_check_go.side_effect = [
        "continue",
        "win",
    ]  # First check continue, second check win

    gameplay.run_game(
        sample_settings,
        sample_final_grid,
        sample_words_to_find,
        middle_word,
        player_name,
        sample_wizard,
    )

    # Check initialization
    mock_init_state.assert_called_once_with(
        sample_final_grid, middle_word, sample_wizard, player_name
    )
    
    # Check if all functions in the flow are called
    mock_update_disp.assert_called()
    mock_get_guess_func.assert_called()
    mock_proc_guess.assert_called()
    mock_update_pp.assert_called()
    
    mock_use_pu.assert_not_called()  # Powerup not used
    
    # Check game over check calls
    mock_go_disp.assert_called_once()  # Show game over screen
    mock_end_disp.assert_called_once()  # Show end display (HP mode)


@patch(PATCH_INIT_STATE)
@patch(PATCH_UPDATE_DISPLAY)
@patch(PATCH_GET_GUESS)
@patch(PATCH_PROC_GUESS)
@patch(PATCH_UPDATE_PP)
@patch(PATCH_USE_PU)
@patch(PATCH_CHECK_GO)
@patch(PATCH_UPDATE_GO_DISPLAY)
@patch(PATCH_UPDATE_END_DISPLAY)
def test_run_game_loss_no_hp_mode(
    mock_end_disp,
    mock_go_disp,
    mock_check_go,
    mock_use_pu,
    mock_update_pp,
    mock_proc_guess,
    mock_get_guess_func,
    mock_update_disp,
    mock_init_state,
    sample_settings_no_hp,
    sample_final_grid,
    sample_words_to_find,
    sample_wizard,
):
    """Test a losing game flow NOT in Heart Point mode."""
    # No name needed if not HP mode
    player_name = None  
    middle_word = "MIDDLE"
    mock_init_state.return_value = {
        "statistics": {"points": 10},
        "player_name": player_name,
    }

    # Game flow: wrong guess -> loss
    mock_get_guess_func.return_value = "badguess"
    mock_check_go.side_effect = [
        "continue",
        "loss",
    ]  # First check continue, second check loss

    gameplay.run_game(
        sample_settings_no_hp,
        sample_final_grid,
        sample_words_to_find,
        middle_word,
        player_name,
        sample_wizard,
    )

    # Check initialization
    mock_init_state.assert_called_once_with(
        sample_final_grid, middle_word, sample_wizard, player_name
    )

    # Check if all functions in the flow are called
    mock_update_disp.assert_called()
    mock_get_guess_func.assert_called()
    mock_proc_guess.assert_called()
    mock_update_pp.assert_called()

    mock_use_pu.assert_not_called() # Powerup not used

    mock_go_disp.assert_called_once()
    mock_end_disp.assert_not_called()  # NOT called (no HP mode)


@patch(PATCH_INIT_STATE)
@patch(PATCH_UPDATE_DISPLAY)
@patch("gameplay.gameplay.get_guess")
@patch(PATCH_PROC_GUESS)
@patch(PATCH_UPDATE_PP)
@patch(PATCH_USE_PU)
@patch(PATCH_CHECK_GO)
@patch(PATCH_UPDATE_GO_DISPLAY)
@patch(PATCH_UPDATE_END_DISPLAY)
def test_run_game_uses_powerup(
    mock_end_disp,
    mock_go_disp,
    mock_check_go,
    mock_use_pu,
    mock_update_pp,
    mock_proc_guess,
    mock_get_guess_func,
    mock_update_disp,
    mock_init_state,
    sample_settings,
    sample_final_grid,
    sample_words_to_find,
    sample_wizard,
):
    """Test game flow when a powerup is used."""
    player_name = "PlayerPU"
    middle_word = "MIDDLE"
    mock_init_state.return_value = {
        "statistics": {"points": 0},
        "player_name": player_name,
    }

    # Game flow: use powerup -> win
    mock_get_guess_func.return_value = (
        game_constants.POWERUP_COMMAND
    )  # Simulate powerup command
    mock_check_go.side_effect = ["continue", "win"]  # Game ends after powerup

    gameplay.run_game(
        sample_settings,
        sample_final_grid,
        sample_words_to_find,
        middle_word,
        player_name,
        sample_wizard,
    )

    # Check initialization
    mock_init_state.assert_called_once()
    mock_update_disp.assert_called()
    mock_get_guess_func.assert_called()
    mock_use_pu.assert_called()

    # Process guess skipped
    # Check update_power_points NOT called after powerup
    mock_proc_guess.assert_not_called()  
    mock_update_pp.assert_not_called()

    # Check game over check and final displays
    mock_go_disp.assert_called_once()
    mock_end_disp.assert_called_once()
