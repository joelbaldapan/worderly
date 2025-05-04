import pytest
from unittest.mock import mock_open, patch

from leaderboard import leaderboard

# Define constants used in the module
LEADERBOARD_FILE = leaderboard.LEADERBOARD_FILE
DELIMITER = leaderboard.DELIMITER


# ************************************************
# Tests for: Leaderboards
# ************************************************


@pytest.fixture
def mock_leaderboard_file(mocker):
    """Fixture to mock os.path.exists and builtins.open"""
    mock_exists = mocker.patch("os.path.exists")
    mock_file_open = mocker.patch("builtins.open", new_callable=mock_open)
    return mock_exists, mock_file_open


# TESTS FOR: load_leaderboard
def test_load_leaderboard_file_not_found(mock_leaderboard_file):
    """Test loading when the leaderboard file does not exist."""
    mock_exists, _ = mock_leaderboard_file
    mock_exists.return_value = False

    scores = leaderboard.load_leaderboard(LEADERBOARD_FILE)

    assert scores == []
    mock_exists.assert_called_once_with(LEADERBOARD_FILE)


def test_load_leaderboard_empty_file(mock_leaderboard_file):
    """Test loading from an empty leaderboard file."""
    mock_exists, mock_file = mock_leaderboard_file
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = ""  # nothing inside

    scores = leaderboard.load_leaderboard(LEADERBOARD_FILE)

    assert scores == []
    mock_exists.assert_called_once_with(LEADERBOARD_FILE)
    mock_file.assert_called_once_with(LEADERBOARD_FILE, "r", encoding="utf-8")


def test_load_leaderboard_valid_data(mocker):
    """Test loading valid data. The function is expected to correctly parse and sort."""

    mock_exists = mocker.patch("os.path.exists")
    mock_exists.return_value = True

    file_content = f"JOEL{DELIMITER}100\nAngelO{DELIMITER}50\nbaldapan{DELIMITER}150\n"

    with patch("builtins.open", mock_open(read_data=file_content)) as mocked_open_func:
        scores = leaderboard.load_leaderboard(LEADERBOARD_FILE)

        expected_scores = [
            {"name": "baldapan", "score": 150},
            {"name": "JOEL", "score": 100},
            {"name": "AngelO", "score": 50},
        ]

        assert scores == expected_scores

    mock_exists.assert_called_once_with(LEADERBOARD_FILE)
    mocked_open_func.assert_called_once_with(LEADERBOARD_FILE, "r", encoding="utf-8")


def test_load_leaderboard_invalid_data(mocker):
    """Test loading data with invalid lines. The function is expected to skip them."""

    mock_exists = mocker.patch("os.path.exists")
    mock_exists.return_value = True

    file_content = (
        f"ALVIN{DELIMITER}10000000\n"
        f"TooManyDelimiters{DELIMITER}score{DELIMITER}Extra\n"  # Skip, 2 delimiters
        f"DE{DELIMITER}420420\n"
        f"\n"  # Skip, Empty
        f"NoDelimiter\n"  # Skip, No delimiter
        f"ScoreIsNotInt{DELIMITER}abc\n"  # Skip, Score is not a number
        f"{DELIMITER}120\n"  # Skip
        f"LA{DELIMITER}77\n"
        f"  FUENTE  {DELIMITER} 25   \n"  # Strip
    )

    with patch("builtins.open", mock_open(read_data=file_content)) as mocked_open_func:
        scores = leaderboard.load_leaderboard(LEADERBOARD_FILE)
        expected_scores = [
            {"name": "ALVIN", "score": 10000000},
            {"name": "DE", "score": 420420},
            {"name": "LA", "score": 77},
            {"name": "FUENTE", "score": 25},
        ]
        assert scores == expected_scores

    mock_exists.assert_called_once_with(LEADERBOARD_FILE)
    mocked_open_func.assert_called_once_with(LEADERBOARD_FILE, "r", encoding="utf-8")


def test_load_leaderboard_io_error(mock_leaderboard_file, capsys):
    """Test handling of IOError during file reading."""
    mock_exists, mock_file = mock_leaderboard_file
    mock_exists.return_value = True
    mock_file.side_effect = IOError()

    scores = leaderboard.load_leaderboard(LEADERBOARD_FILE)

    assert scores == []
    # Check if an error message was printed (uses capsys fixture)
    captured = capsys.readouterr()
    assert (
        "ERROR: Could not read leaderboard file" in captured.out
        or "ERROR: Could not read leaderboard file" in captured.err
    )


# TESTS FOR: save_score
def test_save_score(mock_leaderboard_file):
    """Test saving a score to the file."""
    _, mock_file = mock_leaderboard_file
    mock_handle = mock_file.return_value

    player_name = "Tester"
    player_score = 999

    leaderboard.save_score(player_name, player_score, LEADERBOARD_FILE)

    # Assert file was opened in append mode and called with the correct formatted string
    mock_file.assert_called_once_with(LEADERBOARD_FILE, "a", encoding="utf-8")
    mock_handle.write.assert_called_once_with(
        f"{player_name}{DELIMITER}{player_score}\n"
    )


def test_save_score_io_error(mock_leaderboard_file, capsys):
    """Test handling of IOError during file writing."""
    _, mock_file = mock_leaderboard_file
    mock_file.side_effect = IOError()

    leaderboard.save_score("H4cKerMan", 500, LEADERBOARD_FILE)

    # Check if an error message was printed
    captured = capsys.readouterr()
    assert (
        f"ERROR: Could not save score to {LEADERBOARD_FILE}" in captured.out
        or f"ERROR: Could not save score to {LEADERBOARD_FILE}" in captured.err
    )
