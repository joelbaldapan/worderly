# gameplay/powerup_handler.py

import gameplay.game_constants as game_constants
from gameplay.game_state_handler import (
    apply_coordinate_reveal,
    check_for_completed_words,
)
import random


# **********************
# POWER POINTS UPDATING
# **********************
def check_power_point_increment(combo_req, statistics):
    """
    Checks if conditions are met to increment power points.

    Args:
        combo_req (int or None):
            The combo count required to gain a power point. None if the
            wizard has no requirement.
        statistics (dict): The game state's statistics dictionary.

    Returns:
        bool: True if power points should be incremented, False otherwise.
    """
    return (
        combo_req is not None  # Requirement must exist
        and statistics["combo"] > 0  # Combo must be active
        and statistics["combo"] % combo_req == 0  # Combo must be a multiple of req
    )


def update_power_points(game_state, selected_wizard):
    """
    Increments power points in the game state if the combo requirement is met.

    Args:
        game_state (dict): The main game state dictionary.
        selected_wizard (dict): The dictionary containing data for the
                                selected wizard, including 'combo_requirement'.

    Returns:
        None: Modifies game_state in place.
    """
    combo_req = selected_wizard["combo_requirement"]
    statistics = game_state["statistics"]

    # Don't increment if combo is broken
    if statistics["combo"] == 0:
        return

    # Check and increment if conditions met
    if check_power_point_increment(combo_req, statistics):
        statistics["power_points"] += 1


# ****************
# POWER-UP LOGIC
# ****************


def get_coords_for_random_reveal(hidden_letter_coords_set, min_reveal, max_reveal):
    """
    Determines a random subset of hidden coordinates to reveal.

    Selects a random number of coordinates between min_reveal and max_reveal,
    ensuring not to exceed the number of available hidden coordinates.

    Args:
        hidden_letter_coords_set (set[tuple[int, int]]):
            A set of coordinates currently hidden.
        min_reveal (int): The minimum number of coordinates to potentially reveal.
        max_reveal (int): The maximum number of coordinates to potentially reveal.

    Returns:
        list[tuple[int, int]]:
            A list of randomly selected coordinates to reveal. Returns an empty
            list if no hidden coordinates are available.
    """

    hidden_letter_coords_list = list(hidden_letter_coords_set)
    available_to_reveal_count = len(hidden_letter_coords_list)

    if available_to_reveal_count == 0:
        num_to_reveal = 0
    else:
        # Choose a random number within the range
        chosen_number = random.randint(min_reveal, max_reveal)
        # Clamp the number to the available count
        num_to_reveal = min(chosen_number, available_to_reveal_count)

    # Select the sample (handles k=0 correctly)
    return random.sample(hidden_letter_coords_list, num_to_reveal)


def get_coords_for_word_reveal(words_to_find, correct_guesses_set):
    """
    Selects the coordinates of a random, not-yet-guessed word.

    Args:
        words_to_find (dict):
            Dictionary mapping words (str) to their
            coordinate lists (list[tuple[int, int]]).
        correct_guesses_set (set[str]): A set of words already guessed correctly.

    Returns:
        list[tuple[int, int]]:
            The list of coordinates for the randomly chosen unrevealed word.
            Returns an empty list if all words have been guessed.
    """

    # Find all words that haven't been guessed yet
    unrevealed_words = [
        word for word in words_to_find.keys() if word not in correct_guesses_set
    ]

    if not unrevealed_words:
        return []

    # Randomly select one word from the unrevealed list
    chosen_word = random.choice(unrevealed_words)
    return words_to_find[chosen_word]


# ************************
# MAIN POWERUP FUNCTION
# ************************


def use_powerup(game_state, selected_wizard, words_to_find, final_grid):
    """
    Activates the selected wizard's power-up and updates the game state.

    Consumes one power point, determines the power-up effect based on the
    wizard's color, calls appropriate helper functions (reveals, state updates),
    and sets the next message and color in the game state.

    Args:
        game_state (dict): The main game state dictionary.
        selected_wizard (dict): Dictionary containing the selected wizard's data.
        words_to_find (dict): Dictionary mapping words to their coordinates.
        final_grid (list[list[strorNone]]): The complete game grid.

    Returns:
        None: Modifies game_state in place.
    """
    stats = game_state["statistics"]
    wizard_color = selected_wizard["color"]
    hidden_letter_coords = game_state["hidden_letter_coords"]
    correctly_guessed_words = game_state["correctly_guessed_words"]

    coords_to_reveal = []
    powerup_message = ""  # Default message
    stats["power_points"] -= 1  # Consume the power point

    # Determine power-up based on wizard color
    if wizard_color == "red":
        coords_to_reveal = get_coords_for_word_reveal(
            words_to_find, correctly_guessed_words
        )
        # Message set below based on reveal outcome
    elif wizard_color == "green":
        coords_to_reveal = get_coords_for_random_reveal(
            hidden_letter_coords,
            game_constants.MIN_RANDOM_REVEAL,
            game_constants.MAX_RANDOM_REVEAL,
        )
        # Message set below based on reveal outcome
    elif wizard_color == "magenta":
        stats["shield_turns"] += game_constants.SHIELD_INCREMENT
        powerup_message = game_constants.SHIELD_ACTIVATED_MSG
    elif wizard_color == "blue":
        stats["lives_left"] += 1
        powerup_message = game_constants.LIFE_GAINED_MSG

    # Set message color to wizard's color
    game_state["next_message_color"] = wizard_color

    # Apply reveal logic for Red and Green wizards
    if wizard_color == "red" or wizard_color == "green":
        if not coords_to_reveal:
            # Handle case where no coords could be revealed (All words found for red)
            powerup_message = game_constants.POWERUP_NO_REVEAL_MSG
        else:
            apply_coordinate_reveal(game_state, final_grid, coords_to_reveal)
            # Check if the reveal completed any words
            completed_words = check_for_completed_words(game_state, words_to_find)

            if completed_words:
                # Update the set of correctly guessed words explicitly
                correctly_guessed_words.update(completed_words)
                powerup_message = game_constants.POWERUP_REVEAL_WORDS_MSG.format(
                    ", ".join(completed_words)
                )
            else:
                # If reveal happened but no words completed
                powerup_message = game_constants.POWERUP_REVEAL_LETTERS_MSG

    # Update the game state message
    game_state["next_message"] = powerup_message
