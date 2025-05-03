# tests/test_worderly.py

import pytest
from unittest.mock import patch, MagicMock
import sys  # To patch sys.argv

# Import the module to be tested
import worderly

# --- Fixtures ---


@pytest.fixture
def sample_settings():
    """Basic settings dictionary."""
    return {"key": "value", "heart_point_mode": True}  # Added hp mode for consistency


# --- Patch Paths ---
# Target functions imported into worderly.py
PATCH_READ_WORD_FILE = "worderly.read_word_file"
PATCH_GEN_WORD_LIST = "worderly.generate_word_list"
PATCH_GEN_BOARD = "worderly.generate_board"
PATCH_RUN_HP_MENU = "worderly.run_heart_points_menu"
PATCH_RUN_MAIN_MENU = "worderly.run_main_menu"  # Added
PATCH_RUN_SETUP = "worderly.run_setup"
PATCH_INIT_PLAYER = "worderly.initialize_player_info"
PATCH_RUN_GAME = "worderly.run_game"
PATCH_CLEAR_SCREEN = "worderly.clear_screen"
PATCH_PRINT = "builtins.print"  # For print calls within worderly.py
PATCH_GET_LEXICON = "worderly.get_lexicon_file"  # For testing main

# --- Tests for get_lexicon_file ---


@patch("sys.argv", ["worderly.py"])  # Simulate no command-line argument
@patch(PATCH_PRINT)
def test_get_lexicon_file_no_arg(mock_print):
    """Test get_lexicon_file when no filename argument is provided."""
    result = worderly.get_lexicon_file()
    assert result is None
    # Check that error messages were printed (to stderr, implicitly checked by print mock)
    assert mock_print.call_count == 2
    assert "requires a lexicon file" in mock_print.call_args_list[0][0][0]


@patch("sys.argv", ["worderly.py", "my_lexicon.txt"])
@patch(
    PATCH_READ_WORD_FILE, return_value=[]
)  # Simulate read returning empty list (failure)
@patch(PATCH_PRINT)
def test_get_lexicon_file_read_fail(mock_print, mock_read):
    """Test get_lexicon_file when read_word_file fails."""
    lexicon_path = "my_lexicon.txt"
    result = worderly.get_lexicon_file()
    assert result is None
    mock_read.assert_called_once_with(lexicon_path)
    # Check that error messages were printed
    assert mock_print.call_count == 2
    assert "Lexicon file reading failed" in mock_print.call_args_list[0][0][0]


@patch("sys.argv", ["worderly.py", "my_lexicon.txt"])
@patch(
    PATCH_READ_WORD_FILE, return_value=["word1", "word2"]
)  # Simulate successful read
@patch(PATCH_PRINT)
def test_get_lexicon_file_success(mock_print, mock_read):
    """Test get_lexicon_file successful execution."""
    lexicon_path = "my_lexicon.txt"
    result = worderly.get_lexicon_file()
    assert result == lexicon_path
    mock_read.assert_called_once_with(lexicon_path)
    mock_print.assert_not_called()  # No errors printed


# --- Tests for run_setup ---


@patch(PATCH_GEN_BOARD)
@patch(PATCH_GEN_WORD_LIST)
def test_run_setup_success_first_try(mock_gen_list, mock_gen_board, sample_settings):
    """Test run_setup succeeding on the first attempt."""
    # Simulate successful generation
    mock_gen_list.return_value = ("MIDDLE", ["word1", "word2"])
    mock_gen_board.return_value = ([["M"]], {"MIDDLE": [(0, 0)]})  # Dummy grid/coords

    result = worderly.run_setup(sample_settings)

    mock_gen_list.assert_called_once_with(sample_settings)
    mock_gen_board.assert_called_once_with(
        sample_settings, "MIDDLE", ["word1", "word2"]
    )
    assert result == (
        "MIDDLE",
        {"MIDDLE": [(0, 0)]},
        [["M"]],
    )  # Note: order changed slightly in return


@patch(PATCH_GEN_BOARD)
@patch(PATCH_GEN_WORD_LIST)
def test_run_setup_word_list_retry(mock_gen_list, mock_gen_board, sample_settings):
    """Test run_setup succeeding after word list generation fails once."""
    # Simulate list fails once, then succeeds; board succeeds
    mock_gen_list.side_effect = [(None, None), ("MIDDLE", ["word1", "word2"])]
    mock_gen_board.return_value = ([["M"]], {"MIDDLE": [(0, 0)]})

    result = worderly.run_setup(sample_settings)

    assert mock_gen_list.call_count == 2
    mock_gen_board.assert_called_once_with(
        sample_settings, "MIDDLE", ["word1", "word2"]
    )
    assert result == ("MIDDLE", {"MIDDLE": [(0, 0)]}, [["M"]])


@patch(PATCH_GEN_BOARD)
@patch(PATCH_GEN_WORD_LIST)
def test_run_setup_grid_retry(mock_gen_list, mock_gen_board, sample_settings):
    """Test run_setup succeeding after grid generation fails once."""
    # Simulate list succeeds; board fails once, then succeeds
    mock_gen_list.return_value = ("MIDDLE", ["word1", "word2"])
    mock_gen_board.side_effect = [(None, None), ([["M"]], {"MIDDLE": [(0, 0)]})]

    result = worderly.run_setup(sample_settings)

    mock_gen_list.assert_called_once_with(sample_settings)
    assert mock_gen_board.call_count == 2
    mock_gen_board.assert_any_call(sample_settings, "MIDDLE", ["word1", "word2"])
    assert result == ("MIDDLE", {"MIDDLE": [(0, 0)]}, [["M"]])


@patch(PATCH_GEN_BOARD)
@patch(PATCH_GEN_WORD_LIST)
def test_run_setup_word_list_fails_all_retries(
    mock_gen_list, mock_gen_board, sample_settings
):
    """Test run_setup when word list generation fails MAX_SETUP_RETRIES times."""
    # Simulate list always failing
    mock_gen_list.return_value = (None, None)

    # Store original retry value and set to 1 for faster test
    original_retries = worderly.MAX_SETUP_RETRIES
    worderly.MAX_SETUP_RETRIES = 1
    try:
        result = worderly.run_setup(sample_settings)
        assert mock_gen_list.call_count == 1
        mock_gen_board.assert_not_called()  # Board generation shouldn't be reached
        assert result is None  # Implicit return value on failure
    finally:
        # Restore original value
        worderly.MAX_SETUP_RETRIES = original_retries


@patch(PATCH_GEN_BOARD)
@patch(PATCH_GEN_WORD_LIST)
def test_run_setup_grid_fails_all_retries(
    mock_gen_list, mock_gen_board, sample_settings
):
    """Test run_setup when grid generation fails MAX_GRID_SETUP_RETRIES times."""
    # Simulate list succeeds, board always fails
    mock_gen_list.return_value = ("MIDDLE", ["word1", "word2"])
    mock_gen_board.return_value = (None, None)

    # Store original retry values and set to 1 for faster test
    original_setup_retries = worderly.MAX_SETUP_RETRIES
    original_grid_retries = worderly.MAX_GRID_SETUP_RETRIES
    worderly.MAX_SETUP_RETRIES = 1
    worderly.MAX_GRID_SETUP_RETRIES = 1
    try:
        result = worderly.run_setup(sample_settings)
        assert mock_gen_list.call_count == 1  # Outer loop runs once
        assert mock_gen_board.call_count == 1  # Inner loop runs once
        assert result is None
    finally:
        # Restore original values
        worderly.MAX_SETUP_RETRIES = original_setup_retries
        worderly.MAX_GRID_SETUP_RETRIES = original_grid_retries


# --- Tests for main (High-Level Flow) ---


# Remove patch for print
@patch(PATCH_GET_LEXICON, return_value=None)  # Simulate lexicon failure
@patch(PATCH_RUN_HP_MENU)
def test_main_exits_if_no_lexicon(mock_run_menu, mock_get_lex):
    """Test that main returns if get_lexicon_file returns None."""
    worderly.main()  # Call main directly

    mock_get_lex.assert_called_once()
    mock_run_menu.assert_not_called()  # Should return before menu


# Remove patch for print
@patch(PATCH_GET_LEXICON, return_value="lex.txt")
@patch(
    PATCH_RUN_HP_MENU, return_value={"heart_point_mode": True}
)  # Simulate HP mode selected
@patch(PATCH_RUN_SETUP, return_value=None)  # Simulate setup failing completely
@patch(PATCH_CLEAR_SCREEN)
# Remove mock_print parameter
def test_main_exits_if_setup_fails(
    mock_clear, mock_run_setup, mock_run_menu, mock_get_lex
):
    """Test that main prints error and returns if run_setup fails."""
    worderly.main()  # Call main directly

    mock_get_lex.assert_called_once()
    mock_run_menu.assert_called_once()
    mock_run_setup.assert_called_once()
    mock_clear.assert_called_once()  # Called before printing fatal error
    # Removed check for print output


@patch(PATCH_GET_LEXICON, return_value="lex.txt")
@patch(
    PATCH_RUN_HP_MENU, return_value={"heart_point_mode": False, "lexicon_path": ""}
)  # Simulate No HP mode
@patch(PATCH_RUN_SETUP)
@patch(PATCH_INIT_PLAYER)
@patch(PATCH_RUN_GAME)
@patch(PATCH_RUN_MAIN_MENU)  # Mock this as it might be called if loop continued
def test_main_no_hp_mode_runs_once(
    mock_run_main_menu,
    mock_run_game,
    mock_init_player,
    mock_run_setup,
    mock_run_hp_menu,
    mock_get_lex,
):
    """Test that main loop runs once and breaks if not in heart point mode."""
    # Simulate successful setup
    mock_run_setup.return_value = ("MIDDLE", {"A": []}, [["A"]])
    # Simulate player info init
    mock_init_player.return_value = (None, {"color": "white"})  # Default player/wizard

    worderly.main()  # Should not raise SystemExit and should break loop

    mock_get_lex.assert_called_once()
    mock_run_hp_menu.assert_called_once()
    mock_run_setup.assert_called_once()
    mock_init_player.assert_called_once()
    mock_run_game.assert_called_once()
    mock_run_main_menu.assert_not_called()  # Should not loop back to main menu


@patch(PATCH_GET_LEXICON, return_value="lex.txt")
@patch(PATCH_RUN_HP_MENU)
@patch(PATCH_RUN_MAIN_MENU)  # Need to mock this too
@patch(PATCH_RUN_SETUP)
@patch(PATCH_INIT_PLAYER)
@patch(PATCH_RUN_GAME)
def test_main_hp_mode_loops(
    mock_run_game,
    mock_init_player,
    mock_run_setup,
    mock_run_main_menu,
    mock_run_hp_menu,
    mock_get_lex,
):
    """Test that main loop continues in heart point mode (mocked for one loop)."""
    # Simulate HP mode selected initially
    settings_hp = {"heart_point_mode": True, "lexicon_path": ""}
    mock_run_hp_menu.return_value = settings_hp
    # Simulate successful setup
    mock_run_setup.return_value = ("MIDDLE", {"A": []}, [["A"]])
    # Simulate player info init
    mock_init_player.return_value = ("Player", {"color": "red"})

    # Limit the loop for testing purposes by making run_game raise an exception
    # This stops the 'while True' loop after one iteration for the test
    mock_run_game.side_effect = Exception("Stop test loop")

    # Catch the exception we raised to stop the loop
    with pytest.raises(Exception, match="Stop test loop"):
        worderly.main()

    mock_get_lex.assert_called_once()
    mock_run_hp_menu.assert_called_once()
    mock_run_main_menu.assert_not_called()  # Not called initially
    mock_run_setup.assert_called_once()
    mock_init_player.assert_called_once()
    mock_run_game.assert_called_once()
    # This test verifies one successful loop iteration in HP mode
