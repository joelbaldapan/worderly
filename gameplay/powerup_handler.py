from gameplay.game_constants import *
from gameplay.game_state_handler import apply_coordinate_reveal, check_for_completed_words


# **********************
# POWER POINTS UPDATING
# **********************
def check_power_point_increment(combo_req, statistics):
    return (
        combo_req is not None
        and statistics["combo"] > 0
        and statistics["combo"] % combo_req == 0
    )


def update_power_points(game_state, selected_wizard):
    combo_req = selected_wizard["combo_requirement"]
    statistics = game_state["statistics"]

    if statistics["combo"] == 0:
        return

    if check_power_point_increment(combo_req, statistics):
        statistics["power_points"] += 1


# ****************
# POWER-UP LOGIC
# ****************
import random


def get_coords_for_random_reveal(hidden_letter_coords_set, min_reveal, max_reveal):
    hidden_letter_coords_list = list(hidden_letter_coords_set)

    # total number of available hidden letters
    available_to_reveal_count = len(hidden_letter_coords_list)

    # Choose a random number of letters to reveal within the specified range
    # and make suree that chosen number doesn't exceed the available hidden letters
    if available_to_reveal_count == 0:
        num_to_reveal = 0
    else:
        chosen_number = random.randint(min_reveal, max_reveal)
        num_to_reveal = min(chosen_number, available_to_reveal_count)

    # Randomly select the coordinates to reveal directly from the list of hidden coords
    # random.sample handles the case where num_to_reveal is 0 or the list is empty
    return random.sample(hidden_letter_coords_list, num_to_reveal)


def get_coords_for_word_reveal(words_to_find, correct_guesses_set):
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
    stats = game_state["statistics"]
    wizard_color = selected_wizard["color"]
    hidden_letter_coords = game_state["hidden_letter_coords"]
    correctly_guessed_words = game_state["correctly_guessed_words"]

    coords_to_reveal = []
    powerup_message = ""

    stats["power_points"] -= 1  # Consume the power point

    if wizard_color == "red":
        coords_to_reveal = get_coords_for_word_reveal(
            words_to_find, correctly_guessed_words
        )
    elif wizard_color == "green":
        coords_to_reveal = get_coords_for_random_reveal(
            hidden_letter_coords, MIN_RANDOM_REVEAL, MAX_RANDOM_REVEAL
        )
    elif wizard_color == "magenta":
        stats["shield_turns"] += SHIELD_INCREMENT
        powerup_message = SHIELD_ACTIVATED_MSG
    elif wizard_color == "blue":
        stats["lives_left"] += 1
        powerup_message = LIFE_GAINED_MSG

    game_state["next_message_color"] = wizard_color

    # Note: RED and GREEN reveals letters on the board,
    if wizard_color == "red" or wizard_color == "green":
        apply_coordinate_reveal(game_state, final_grid, coords_to_reveal)

        # Check if revealing coordinates completed any words
        completed_words = check_for_completed_words(game_state, words_to_find)

        if completed_words:
            # Update the set of correctly guessed words explicitly here
            # because apply_coordinate_reveal doesn't know about words
            correctly_guessed_words.update(completed_words)
            powerup_message = POWERUP_REVEAL_WORDS_MSG.format(
                ", ".join(completed_words)
            )
        else:
            powerup_message = POWERUP_REVEAL_LETTERS_MSG

    game_state["next_message"] = powerup_message
