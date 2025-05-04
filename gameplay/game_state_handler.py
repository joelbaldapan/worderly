# gameplay/game_state_handler.py
import gameplay.game_constants as game_constants
import random


# ****************
# UTILS
# ****************


def shuffle_letters_statistic(middle_word):
    """Shuffles the letters of the middle word for display in statistics.

    Args:
        middle_word (str): The central word of the puzzle.

    Returns:
        str:
            A string of the shuffled uppercase letters of the middle word,
            separated by spaces.
    """
    letters_list = list(str(middle_word).upper())
    random.shuffle(letters_list)
    return " ".join(letters_list)


# ******************
# GRID RELATED
# ******************


def create_hidden_grid(final_grid):
    """Creates the initial hidden grid for the player."""
    return [["#" if col else None for col in row] for row in final_grid]


def reveal_coords_in_hidden_grid(final_grid, hidden_grid, coords):
    """Reveals specific coordinates on the hidden grid.

    Updates the `hidden_grid` in place by copying the characters from the
    `final_grid` at the locations specified in `coords`.

    Args:
        final_grid (list[list]):
            The complete game grid containing the actual letters (str or None).
        hidden_grid (list[list]):
            The player-visible grid, potentially containing '#' characters (str or None).
            This grid is modified in place.
        coords (iterable):
            An iterable (like list or set) of (row, col) tuples (tuple[int, int])
            indicating which cells to reveal.

    Returns:
        None: The `hidden_grid` is modified directly.
    """
    for i, j in coords:
        # Basic bounds check for safety, although coords should be valid
        if 0 <= i < len(hidden_grid) and 0 <= j < len(hidden_grid[0]):
            hidden_grid[i][j] = final_grid[i][j]


def get_all_letter_coords(final_grid):
    """Gets the set of all coordinates containing letters on the final grid."""
    all_coords = set()
    height = len(final_grid)
    width = len(final_grid[0]) if height > 0 else 0
    for r in range(height):
        for c in range(width):
            if final_grid[r][c] is not None:
                all_coords.add((r, c))
    return all_coords


def apply_coordinate_reveal(game_state, final_grid, coords_to_reveal):
    """Applies the effects of revealing coordinates to the game state.

    Updates the hidden grid display, calculates points gained from newly revealed
    letters, updates the sets tracking found and hidden coordinates, and stores
    the revealed coordinates for highlighting in the next display update.

    Args:
        game_state (dict):
            The main dictionary holding the current game status,
            including 'statistics', 'hidden_grid', 'found_letter_coords',
            'hidden_letter_coords', and 'last_guess_coords'. Modified in place.
        final_grid (list[list]):
            The complete game grid with correct letters (str or None).
        coords_to_reveal (iterable):
            An iterable of (row, col) coordinates (tuple[int, int]) that
            should be revealed.

    Returns:
        None: The `game_state` dictionary is modified directly.
    """
    stats = game_state["statistics"]
    coords_set = set(coords_to_reveal)

    # Update the visual hidden grid
    reveal_coords_in_hidden_grid(final_grid, game_state["hidden_grid"], coords_set)

    # Calculate points gained only for newly revealed unique letters
    newly_revealed_coords = coords_set - game_state["found_letter_coords"]
    stats["points"] += len(newly_revealed_coords)

    # Update coord tracking sets
    game_state["found_letter_coords"].update(coords_set)  # Add all revealed coords
    game_state["last_guess_coords"] = list(coords_set)  # Store for highlighting
    # Remove revealed coords from the set of hidden coords
    for coord in coords_set:
        game_state["hidden_letter_coords"].discard(coord)


# ******************
# GAMEPLAY RELATED
# ******************


def initialize_game_state(final_grid, middle_word, selected_wizard, player_name):
    """Initializes the game state dictionary for a new game round.

    Sets up the player's view (hidden grid), initial statistics (lives, points,
    combo, etc.), tracking sets for letters and words, and the initial welcome
    message based on the provided parameters.

    Args:
        final_grid (list[list]):
            The fully generated solution grid containing strings or None values.
        middle_word (str):
            The central word used for generating the puzzle, used here for the
            shuffled letters statistic.
        selected_wizard (dict):
            A dictionary containing the chosen wizard's attributes
            (like 'starting_lives', 'color').
        player_name (str | None):
            The name of the player, or None if not in Heart Point mode.

    Returns:
        dict:
            The initialized game state dictionary containing all necessary
            information to start tracking the game's progress.
    """
    hidden_grid = create_hidden_grid(final_grid)
    statistics = {
        "letters": shuffle_letters_statistic(middle_word),
        "lives_left": selected_wizard["starting_lives"],
        "points": 0,
        "last_guess": None,
        "combo": 0,
        "power_points": 0,
        "shield_turns": 0,
    }
    game_state = {
        "player_name": player_name,
        "statistics": statistics,
        "hidden_grid": hidden_grid,
        "last_guess_coords": [],
        "correctly_guessed_words": set(),
        "hidden_letter_coords": get_all_letter_coords(final_grid),
        "found_letter_coords": set(),
        "next_message": game_constants.WELCOME_MSG,
        "next_message_color": selected_wizard["color"],
    }
    return game_state


def process_guess(guess, game_state, words_to_find, final_grid, wizard_color):
    """Processes a player's word guess and updates the game state accordingly.

    Checks if the guess is correct, incorrect, or already found. Updates
    statistics (combo, lives, points), reveals letters on the grid for correct
    guesses, checks for words completed implicitly by the reveal, applies damage
    if the guess is invalid and shields are down, decrements shield duration,
    and sets the feedback message for the next display update.

    Args:
        guess (str): The lowercase, stripped word guessed by the player.
        game_state (dict): The main game state dictionary. Modified in place.
        words_to_find (dict): A dictionary mapping all valid words (str) in the
            puzzle to their coordinate lists (list[tuple[int, int]]).
        final_grid (list[list]): The complete solution grid containing strings
            or None values.
        wizard_color (str): The Rich color string associated with the player's
            selected wizard, used for styling success messages.

    Returns:
        None: The `game_state` dictionary is modified directly.
    """
    stats = game_state["statistics"]
    correctly_guessed_words = game_state["correctly_guessed_words"]

    stats["last_guess"] = guess
    game_state["last_guess_coords"] = []  # Reset highlight from previous turn/powerup
    took_damage = False

    if guess in correctly_guessed_words:
        # DUPLICATE GUESS
        stats["combo"] = 0
        game_state["next_message"] = game_constants.ALREADY_FOUND_MSG.format(guess)
        game_state["next_message_color"] = game_constants.ERROR_COLOR
        took_damage = True

    elif guess not in words_to_find:
        # WRONG GUESS
        stats["combo"] = 0
        game_state["next_message"] = game_constants.NOT_A_WORD_MSG.format(guess)
        game_state["next_message_color"] = game_constants.ERROR_COLOR
        took_damage = True

    else:
        # CORRECT GUESS
        game_state["next_message"] = game_constants.CORRECT_GUESS_MSG.format(guess)
        game_state["next_message_color"] = wizard_color  # Use wizard color for success
        stats["combo"] += 1
        correctly_guessed_words.add(guess)  # Add the correctly guessed word

        word_coords = words_to_find[guess]
        apply_coordinate_reveal(game_state, final_grid, word_coords)

        # Check if revealing this word implicitly completed others
        completed_words = check_for_completed_words(game_state, words_to_find)
        if completed_words:
            # Update the set of correctly guessed words for implicitly found ones
            correctly_guessed_words.update(completed_words)
            game_state["next_message"] += (
                f" (Also completed: {', '.join(completed_words)})"
            )

    # Apply damage if guess was wrong/duplicate AND shield is down
    if took_damage and stats["shield_turns"] <= 0:
        stats["lives_left"] -= 1

    # Decrement shield turns regardless of guess outcome, if active
    if stats["shield_turns"] > 0:
        stats["shield_turns"] -= 1


def check_for_completed_words(game_state, words_to_find):
    """Checks if any words were implicitly completed by the last reveal.

    Iterates through all words in the puzzle that haven't been correctly guessed yet.
    For each word, it checks if all of its constituent letters are now visible
    (i.e., their coordinates are no longer in the `hidden_letter_coords` set).

    Args:
        game_state (dict):
            The current game state dictionary, containing the sets
            `correctly_guessed_words` and `hidden_letter_coords`.
        words_to_find (dict):
            Dictionary mapping all valid puzzle words (str) to their coordinate
            lists (list[tuple[int, int]]).

    Returns:
        list[str]:
            A list of words that were found to be implicitly completed
            during this check. Can be empty.
    """
    newly_found_words = []
    correctly_guessed_words = game_state["correctly_guessed_words"]
    hidden_letter_coords_set = game_state["hidden_letter_coords"]

    # Iterate through all words that haven't been guessed yet
    for word, coords in words_to_find.items():
        # Only check words that are not already marked as correctly guessed
        if word not in correctly_guessed_words:
            # Check if ALL coordinates for this word are NOT in the hidden_letter_coords set
            # If a coordinate is NOT in hidden_letter_coords_set, it means it HAS been revealed
            all_letters_revealed = all(
                coord not in hidden_letter_coords_set for coord in coords
            )

            if all_letters_revealed:
                newly_found_words.append(word)

    return newly_found_words


def check_game_over(game_state, words_to_find):
    """Checks if the game has reached a win or loss condition.

    Args:
        game_state (dict):
            The current game state dictionary, particularly containing
            `correctly_guessed_words` set and `statistics['lives_left']`.
        words_to_find (dict):
            Dictionary mapping all valid puzzle words (str) to their coordinates
            (list[tuple[int, int]]), used to determine the total number of words needed.

    Returns:
        str:
            "win" if all words have been found, "loss" if lives are zero or less,
            "continue" otherwise.
    """
    if len(game_state["correctly_guessed_words"]) == len(words_to_find):
        return "win"
    elif game_state["statistics"]["lives_left"] <= 0:
        return "loss"
    else:
        return "continue"
