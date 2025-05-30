import random

from data.wizards_details import WizardData
from gameplay import game_constants
from gameplay.game_state_handler import (
    GameStateData,
    GameStatisticsData,
    apply_coordinate_reveal,
    check_for_completed_words,
)


def check_power_point_increment(combo_req: int | None, statistics: GameStatisticsData) -> bool:
    """Checks if conditions are met to increment power points."""
    return combo_req is not None and statistics.combo > 0 and statistics.combo % combo_req == 0


def update_power_points(game_st: GameStateData, current_selected_wizard: WizardData) -> None:
    """Increments power points in the game state if the combo requirement is met."""
    combo_req = current_selected_wizard.combo_requirement
    stats = game_st.statistics  # stats is GameStatisticsData

    if stats.combo == 0:
        return

    if check_power_point_increment(combo_req, stats):
        stats.power_points += 1
        game_st.next_message += " Combo requirement reached, +1 Power Point!"


def get_coords_for_random_reveal(
    hidden_letter_coords_set: set[tuple[int, int]],
    min_reveal: int,
    max_reveal: int,
) -> list[tuple[int, int]]:
    """Determines a random subset of hidden coordinates to reveal."""
    hidden_letter_coords_list = list(hidden_letter_coords_set)
    available_to_reveal_count = len(hidden_letter_coords_list)

    num_to_reveal = 0
    if available_to_reveal_count > 0:
        chosen_number = random.randint(min_reveal, max_reveal)
        num_to_reveal = min(chosen_number, available_to_reveal_count)

    return random.sample(hidden_letter_coords_list, num_to_reveal)


def get_coords_for_word_reveal(
    words_to_find: dict[str, list[tuple[int, int]]],
    correct_guesses_set: set[str],
) -> list[tuple[int, int]]:
    """Selects the coordinates of a random, not-yet-guessed word."""
    unrevealed_words = [word for word in words_to_find if word not in correct_guesses_set]
    if not unrevealed_words:
        return []
    chosen_word = random.choice(unrevealed_words)
    return words_to_find[chosen_word]


def use_powerup(
    game_st: GameStateData,
    current_selected_wizard: WizardData,
    words_to_find: dict[str, list[tuple[int, int]]],
    final_grid: list[list[str | None]],
) -> None:
    """Activates the selected wizard's power-up and updates the game state."""
    stats = game_st.statistics  # stats is GameStatisticsData
    wizard_color = current_selected_wizard.color

    coords_to_reveal: list[tuple[int, int]] = []
    powerup_message = ""
    stats.power_points -= 1

    if wizard_color == "red":
        coords_to_reveal = get_coords_for_word_reveal(words_to_find, game_st.correctly_guessed_words)
    elif wizard_color == "green":
        coords_to_reveal = get_coords_for_random_reveal(
            game_st.hidden_letter_coords,
            game_constants.MIN_RANDOM_REVEAL,
            game_constants.MAX_RANDOM_REVEAL,
        )
    elif wizard_color == "magenta":
        stats.shield_turns += game_constants.SHIELD_INCREMENT
        powerup_message = game_constants.SHIELD_ACTIVATED_MSG
    elif wizard_color == "blue":
        stats.lives_left += 1
        powerup_message = game_constants.LIFE_GAINED_MSG

    game_st.next_message_color = wizard_color

    if wizard_color in {"red", "green"}:
        if not coords_to_reveal:
            powerup_message = game_constants.POWERUP_NO_REVEAL_MSG
        else:
            # apply_coordinate_reveal expects GameStateData
            apply_coordinate_reveal(game_st, final_grid, coords_to_reveal)
            # check_for_completed_words expects GameStateData
            completed_words = check_for_completed_words(game_st, words_to_find)

            if completed_words:
                game_st.correctly_guessed_words.update(completed_words)
                powerup_message = game_constants.POWERUP_REVEAL_WORDS_MSG.format(", ".join(completed_words))
            else:
                powerup_message = game_constants.POWERUP_REVEAL_LETTERS_MSG

    game_st.next_message = powerup_message
