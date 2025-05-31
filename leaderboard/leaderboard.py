# ************************************
#         LEADERBOARDS
# ************************************
import operator
import os

from display.display import print_message

# Define constants for the leaderboards
# Pipe '|' is used as delimiter for the leaderboards
# Like this: "name|score"
LEADERBOARD_FILE = "leaderboard/leaderboards.txt"
DELIMITER = "|"


def load_leaderboard(filename=LEADERBOARD_FILE):
    """Load, parse, and sort scores from the leaderboard file."""
    scores = []
    # Check if the file exists before attempting to open
    if not os.path.exists(filename):
        return scores

    try:
        # Open the file safely using 'with' statement
        with open(filename, encoding="utf-8") as f:
            # Enumerate lines for potential error reporting
            for line in f:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                # Split only on the first delimiter to handle names with '|'
                parts = line.split(DELIMITER, 1)

                # Ensure exactly two parts (name and score)
                if len(parts) != 2:
                    # Optional warning
                    # print( #
                    #     f"WARNING: Skipping wrong format line {line_num} in {filename}: {line}"
                    # )
                    continue

                name = parts[0].strip()
                try:
                    # Attempt to convert score part to integer
                    score = int(parts[1].strip())
                    # Ensure name is not empty after stripping
                    if name:
                        scores.append({"name": name, "score": score})
                    else:
                        # Optional warning
                        # print(
                        #     f"WARNING: Skipping line {line_num} in {filename} due to empty name"
                        # )
                        pass  # Silently skip lines with empty names
                except ValueError:
                    # Handle cases where score is not a valid integer
                    # Optional warning
                    # print(
                    #     f"WARNING: Skipping line {line_num} in {filename} due to invalid score: {parts[1]}"
                    # )
                    pass  # Silently skip lines with invalid scores

    except OSError as e:
        # Handle file reading errors (e.g., permissions)
        print_message(
            settings=None,  # Settings might not be available here
            message=f"ERROR: Could not read leaderboard file {filename}: {e}",
            border_style="red",
        )
    except Exception as e:
        # Handle any other unexpected errors during loading
        print_message(
            settings=None,
            message=f"ERROR: An unexpected error occurred loading leaderboard: {e}",
            border_style="red",
        )

    # Sort the collected scores by score in descending order
    scores.sort(key=operator.itemgetter("score"), reverse=True)
    return scores


def save_score(player_name, player_score, filename=LEADERBOARD_FILE) -> None:
    """Append a player's name and score to the leaderboard file."""
    try:
        # Use append mode 'a' to add to the end of the file
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{player_name}{DELIMITER}{player_score}\n")
    except OSError as e:
        # Handle file writing errors
        print_message(
            settings=None,
            message=f"ERROR: Could not save score to {filename}: {e}",
            border_style="red",
        )
    except Exception as e:
        # Handle any other unexpected errors during saving
        print_message(
            settings=None,
            message=f"ERROR: An unexpected error occurred saving score: {e}",
            border_style="red",
        )
