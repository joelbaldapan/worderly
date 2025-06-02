from unittest.mock import patch

import pytest

# Import the module to be tested
import worderly


@pytest.fixture
def sample_settings() -> dict:
    """Provide a basic settings dictionary for tests.

    Returns:
        dict: A dictionary with sample settings.

    """
    return {"key": "value", "heart_point_mode": True}  # Added hp mode for consistency


# ************************************************
# Paths For Convenience
# ************************************************


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

# ************************************************
# Tests For: Getting lexicon file
# ************************************************


@patch("sys.argv", ["worderly.py"])  # Simulate no command-line argument
@patch(PATCH_PRINT)
def test_get_lexicon_file_no_arg(mock_print: object) -> None:
    """Test get_lexicon_file when no filename argument is provided.

    Ensure function returns None and prints error messages.
    """
    result = worderly.get_lexicon_file()
    assert result is None
    # Check that error messages were printed (to stderr, implicitly checked by print mock)
    assert mock_print.call_count == 2
    assert "requires a lexicon file" in mock_print.call_args_list[0][0][0]


@patch("sys.argv", ["worderly.py", "my_lexicon.txt"])
@patch(
    PATCH_READ_WORD_FILE, return_value=[],
)  # Simulate read returning empty list (failure)
@patch(PATCH_PRINT)
def test_get_lexicon_file_read_fail(mock_print: object, mock_read: object) -> None:
    """Test get_lexicon_file when read_word_file fails.

    Ensure function returns None and prints error messages.
    """
    lexicon_path = "my_lexicon.txt"
    result = worderly.get_lexicon_file()
    assert result is None
    mock_read.assert_called_once_with(lexicon_path)
    # Check that error messages were printed
    assert mock_print.call_count == 2
    assert "Lexicon file reading failed" in mock_print.call_args_list[0][0][0]


@patch("sys.argv", ["worderly.py", "my_lexicon.txt"])
@patch(
    PATCH_READ_WORD_FILE, return_value=["word1", "word2"],
)  # Simulate successful read
@patch(PATCH_PRINT)
def test_get_lexicon_file_success(mock_print: object, mock_read: object) -> None:
    """Test get_lexicon_file successful execution.

    Ensure function returns the lexicon path and does not print errors.
    """
    lexicon_path = "my_lexicon.txt"
    result = worderly.get_lexicon_file()
    assert result == lexicon_path
    mock_read.assert_called_once_with(lexicon_path)
    mock_print.assert_not_called()  # No errors printed


# Remove patch for print
@patch(PATCH_GET_LEXICON, return_value=None)  # Simulate lexicon failure
@patch(PATCH_RUN_HP_MENU)
def test_main_exits_if_no_lexicon(mock_run_menu: object, mock_get_lex: object) -> None:
    """Test that main returns if get_lexicon_file returns None.

    Ensure main does not proceed to run_heart_points_menu.
    """
    worderly.main()  # Call main directly

    mock_get_lex.assert_called_once()
    mock_run_menu.assert_not_called()  # Should return before menu
