import json
import os
from dataclasses import asdict, dataclass


@dataclass
class StreakEntry:
    player_name: str
    streak_count: int
    total_points_in_streak: int


LEADERBOARD_DIR = "leaderboard"
STREAK_LEADERBOARD_FILENAME = "winning_streaks.json"
STREAK_LEADERBOARD_FILEPATH = os.path.join(LEADERBOARD_DIR, STREAK_LEADERBOARD_FILENAME)
MAX_STREAK_ENTRIES = 10


def load_streaks(filepath: str = STREAK_LEADERBOARD_FILEPATH) -> list[StreakEntry]:
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            loaded_streaks: list[StreakEntry] = []
            if isinstance(data, list):
                for entry_dict in data:
                    if isinstance(entry_dict, dict):
                        try:
                            loaded_streaks.append(StreakEntry(**entry_dict))
                        except TypeError:  # Mismatched keys or extra keys
                            pass
            return loaded_streaks
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    except Exception:
        return []


def _save_streaks_to_file(filepath: str, streaks: list[StreakEntry]) -> None:
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data_to_save = [asdict(entry) for entry in streaks]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4)
    except OSError:
        print(f"Error: Could not save streaks to {filepath}.")
    except Exception:
        print("An unexpected error occurred while saving streaks.")


def add_streak_entry(
    new_entry: StreakEntry,
    filepath: str = STREAK_LEADERBOARD_FILEPATH,
    max_entries: int = MAX_STREAK_ENTRIES,
) -> None:
    current_streaks = load_streaks(filepath)
    current_streaks.append(new_entry)
    current_streaks.sort(key=lambda x: (x.streak_count, x.total_points_in_streak), reverse=True)
    updated_streaks = current_streaks[:max_entries]
    _save_streaks_to_file(filepath, updated_streaks)
