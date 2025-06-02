import json
import pytest

from leaderboard import streak_handler

# ************************************************
# Fixtures
# ************************************************

@pytest.fixture
def sample_streak_entries():
    """Creates a sample list of StreakEntry objects."""
    return [
        streak_handler.StreakEntry(player_name="Joel", streak_count=5, total_points_in_streak=100),
        streak_handler.StreakEntry(player_name="Angelo", streak_count=3, total_points_in_streak=50),
        streak_handler.StreakEntry(player_name="Baldapan", streak_count=7, total_points_in_streak=150),
    ]


@pytest.fixture
def sample_streak_dicts():
    """Creates a sample list of dicts representing streak entries."""
    return [
        {"player_name": "Joel", "streak_count": 5, "total_points_in_streak": 100},
        {"player_name": "Angelo", "streak_count": 3, "total_points_in_streak": 50},
        {"player_name": "Baldapan", "streak_count": 7, "total_points_in_streak": 150},
    ]


@pytest.fixture
def streak_file_path(tmp_path):
    """Provides a temporary file path for streaks."""
    return tmp_path / "winning_streaks.json"


# ************************************************
# Tests for: load_streaks
# ************************************************

def test_load_streaks_file_not_exist(monkeypatch, tmp_path):
    """Test loading streaks when file does not exist."""

    # Make Path.exists to always return False
    monkeypatch.setattr("pathlib.Path.exists", lambda self: False)
    result = streak_handler.load_streaks(tmp_path / "i_do_not_exist_mwahahaha.json")
    assert result == []


def test_load_streaks_empty_file(tmp_path):
    """Test loading streaks from an empty file."""
    file_path = tmp_path / "empty.json"
    file_path.write_text("")
    result = streak_handler.load_streaks(file_path)
    assert result == []


def test_load_streaks_valid_data(tmp_path, sample_streak_dicts):
    """Test loading valid streak data from file."""
    file_path = tmp_path / "valid.json"
    file_path.write_text(json.dumps(sample_streak_dicts))
    result = streak_handler.load_streaks(file_path)

    # Should return list of StreakEntry objects
    assert all(isinstance(entry, streak_handler.StreakEntry) for entry in result)
    assert {e.player_name for e in result} == {"Joel", "Angelo", "Baldapan"}


def test_load_streaks_invalid_json(tmp_path):
    """Test loading streaks with invalid JSON in file."""
    file_path = tmp_path / "bad.json"
    file_path.write_text("{not valid json")
    result = streak_handler.load_streaks(file_path)
    assert result == []


def test_load_streaks_invalid_entries(tmp_path):
    """Test loading streaks with some invalid entries in file."""
    file_path = tmp_path / "malformed.json"
    # One valid, one missing keys, one not a dict
    data = [
        {"player_name": "Joel", "streak_count": 5, "total_points_in_streak": 100},
        {"player_name": "Bad"},  # Missing keys
        "notadict"
    ]
    file_path.write_text(json.dumps(data))
    result = streak_handler.load_streaks(file_path)

    # Only valid and extra (extra keys are ignored)
    assert any(e.player_name == "Joel" for e in result)
    assert len(result) == 1  # Only Joel should be loaded


def test_load_streaks_io_error(monkeypatch, tmp_path):
    """Test loading streaks with IOError."""
    def raise_ioerror(*args, **kwargs):
        raise IOError()
    monkeypatch.setattr("pathlib.Path.open", lambda self, *a, **k: raise_ioerror())
    file_path = tmp_path / "ioerror.json"
    result = streak_handler.load_streaks(file_path)
    assert result == []


# ************************************************
# Tests for: _save_streaks_to_file
# ************************************************

def test_save_streaks_to_file(tmp_path, sample_streak_entries):
    """Test saving streaks to file."""
    file_path = tmp_path / "save.json"
    streak_handler._save_streaks_to_file(file_path, sample_streak_entries)

    # File should exist and contain valid JSON
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert any(d["player_name"] == "Joel" for d in data)


def test_save_streaks_to_file_io_error(monkeypatch, sample_streak_entries, tmp_path):
    """Test IOError during saving streaks to file."""
    def raise_ioerror(*args, **kwargs):
        raise IOError()
    monkeypatch.setattr("pathlib.Path.open", lambda self, *a, **k: raise_ioerror())
    file_path = tmp_path / "ioerror_save.json"
    # Should not raise
    streak_handler._save_streaks_to_file(file_path, sample_streak_entries)


# ************************************************
# Tests for: add_streak_entry
# ************************************************

def test_add_streak_entry_new_file(tmp_path):
    """Test adding a streak entry to a new file."""
    file_path = tmp_path / "add.json"
    entry = streak_handler.StreakEntry("Joel", 5, 100)
    streak_handler.add_streak_entry(entry, file_path, max_entries=5)
    loaded = streak_handler.load_streaks(file_path)
    assert any(e.player_name == "Joel" for e in loaded)


def test_add_streak_entry_limit(tmp_path, sample_streak_entries):
    """Test that add_streak_entry enforces max_entries limit and sorts."""
    file_path = tmp_path / "limit.json"

    # Save initial entries
    streak_handler._save_streaks_to_file(file_path, sample_streak_entries)

    # Add a new entry with high streak/points
    new_entry = streak_handler.StreakEntry("Top", 10, 999)
    streak_handler.add_streak_entry(new_entry, file_path, max_entries=3)
    loaded = streak_handler.load_streaks(file_path)

    # Should only keep 3, and "Top" should be first
    assert len(loaded) == 3
    assert loaded[0].player_name == "Top"


def test_add_streak_entry_sorting(tmp_path):
    """Test that add_streak_entry sorts by streak_count then total_points_in_streak."""
    file_path = tmp_path / "sort.json"
    entries = [
        streak_handler.StreakEntry("A", 2, 100),
        streak_handler.StreakEntry("B", 5, 50),
        streak_handler.StreakEntry("C", 5, 200),
    ]
    for e in entries:
        streak_handler.add_streak_entry(e, file_path, max_entries=10)
    loaded = streak_handler.load_streaks(file_path)

    # C (5,200) > B (5,50) > A (2,100)
    assert loaded[0].player_name == "C"
    assert loaded[1].player_name == "B"
    assert loaded[2].player_name == "A"