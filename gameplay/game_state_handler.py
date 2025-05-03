from gameplay.game_constants import *
import random


# ****************
# UTILS
# ****************


def shuffle_letters_statistic(middle_word):
    letters_list = list(str(middle_word).upper())
    random.shuffle(letters_list)
    return " ".join(letters_list)


# ******************
# GRID RELATED
# ******************
def create_hidden_grid(final_grid):
    return [["#" if col else None for col in row] for row in final_grid]


def reveal_coords_in_hidden_grid(final_grid, hidden_grid, coords):
    print(coords)
    for i, j in coords:
        hidden_grid[i][j] = final_grid[i][j]


def get_all_letter_coords(final_grid):
    all_coords = set()
    height = len(final_grid)
    width = len(final_grid[0])
    for r in range(height):
        for c in range(width):
            if final_grid[r][c] is not None:
                all_coords.add((r, c))
    return all_coords


def apply_coordinate_reveal(game_state, final_grid, coords_to_reveal):
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
        "next_message": WELCOME_MSG,
        "next_message_color": selected_wizard["color"],
    }
    return game_state


def process_guess(guess, game_state, words_to_find, final_grid, wizard_color):
    stats = game_state["statistics"]
    correctly_guessed_words = game_state["correctly_guessed_words"]

    stats["last_guess"] = guess
    game_state["last_guess_coords"] = []  # Reset highlight from previous turn/powerup
    took_damage = False

    if guess in correctly_guessed_words:
        # DUPLICATE GUESS
        stats["combo"] = 0
        game_state["next_message"] = ALREADY_FOUND_MSG.format(guess)
        game_state["next_message_color"] = ERROR_COLOR
        took_damage = True

    elif guess not in words_to_find:
        # WRONG GUESS
        stats["combo"] = 0
        game_state["next_message"] = NOT_A_WORD_MSG.format(guess)
        game_state["next_message_color"] = ERROR_COLOR
        took_damage = True

    else:
        # CORRECT GUESS
        game_state["next_message"] = CORRECT_GUESS_MSG.format(guess)
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
    if len(game_state["correctly_guessed_words"]) == len(words_to_find):
        return "win"
    elif game_state["statistics"]["lives_left"] <= 0:
        return "loss"
    else:
        return "continue"
