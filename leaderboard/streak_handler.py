import contextlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class StreakEntry:
    player_name: str
    streak_count: int
    total_points_in_streak: int


LEADERBOARD_DIR = Path("leaderboard")
STREAK_LEADERBOARD_FILENAME = "winning_streaks.json"
STREAK_LEADERBOARD_FILEPATH = LEADERBOARD_DIR / STREAK_LEADERBOARD_FILENAME
MAX_STREAK_ENTRIES = 10


def load_streaks(filepath: Path = STREAK_LEADERBOARD_FILEPATH) -> list[StreakEntry]:
    if not filepath.exists():
        return []
    try:
        with filepath.open(encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    else:
        if not isinstance(data, list):
            return []
        loaded_streaks: list[StreakEntry] = []
        for entry_dict in data:
            if not isinstance(entry_dict, dict):
                continue
            with contextlib.suppress(TypeError):
                loaded_streaks.append(StreakEntry(**entry_dict))
        return loaded_streaks


def _save_streaks_to_file(filepath: Path, streaks: list[StreakEntry]) -> None:
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        data_to_save = [asdict(entry) for entry in streaks]
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4)
    except OSError:
        print(f"Error: Could not save streaks to {filepath}.")


def add_streak_entry(
    new_entry: StreakEntry,
    filepath: Path = STREAK_LEADERBOARD_FILEPATH,
    max_entries: int = MAX_STREAK_ENTRIES,
) -> None:
    current_streaks = load_streaks(filepath)
    current_streaks.append(new_entry)
    current_streaks.sort(key=lambda x: (x.streak_count, x.total_points_in_streak), reverse=True)
    updated_streaks = current_streaks[:max_entries]
    _save_streaks_to_file(filepath, updated_streaks)
