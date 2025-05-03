# ************************************
#            LEADERBOARDS
# ************************************
import os
from display.display import print_message


# Define constants for the leaderboards
# Pipe '|' is used as delimiter for the leaderboards
# Like this: "name|score"
LEADERBOARD_FILE = "leaderboard/leaderboards.txt"
DELIMITER = "|"


def load_leaderboard(filename=LEADERBOARD_FILE):
    scores = []
    if not os.path.exists(filename):
        return scores

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                # Split only on the first delimiter
                parts = line.split(DELIMITER, 1)

                if len(parts) != 2:
                    # print(
                    #     f"WARNING: Skipping wrong format line {line_num} in {filename}: {line}"
                    # )
                    continue

                name = parts[0].strip()
                try:
                    score = int(parts[1].strip())
                    if name:
                        scores.append({"name": name, "score": score})
                    else:
                        # print(
                        #     f"WARNING: Skipping line {line_num} in {filename} due to empty name"
                        # )
                        ...
                except ValueError:
                    # print(
                    #     f"WARNING: Skipping line {line_num} in {filename} due to invalid score: {parts[1]}"
                    # )
                    ...

    except IOError as e:
        print_message(
            f"ERROR: Could not read leaderboard file {filename}: {e}",
            border_style="red",
        )
    except Exception as e:
        print_message(
            f"ERROR: An unexpected error occurred loading leaderboard: {e}",
            border_style="red",
        )

    # Sort by score DESCENDING ORDER
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores


def save_score(player_name, player_score, filename=LEADERBOARD_FILE):
    if DELIMITER in player_name:
        print_message(
            f"WARNING: Player name '{player_name}' contains the delimiter '{DELIMITER}'. Replacing it with '_'.",
            border_style="red",
        )
        player_name = player_name.replace(DELIMITER, "_")

    try:
        # Use append mode 'a' because we'll add onto the leaderboards
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{player_name}{DELIMITER}{player_score}\n")
    except IOError as e:
        print_message(
            f"ERROR: Could not save score to {filename}: {e}", border_style="red"
        )
    except Exception as e:
        print_message(
            f"ERROR: An unexpected error occurred saving score: {e}", border_style="red"
        )
