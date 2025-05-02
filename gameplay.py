# ****************
# GAMEPLAY
# ****************

from grid_gameplay import (
    create_hidden_grid,
    reveal_coords_in_hidden_grid,
    get_all_letter_coords,
    get_coords_for_random_reveal,
    get_coords_for_word_reveal,
)
from display import (
    print_grid,
    shuffle_letters_statistic,
    clear_screen,
    print_message,
    print_statistics,
    print_leaderboard,
    get_input,
)
from leaderboard import (
    load_leaderboard,
    save_score,
)


# TODO: MAKE CORRECT GUESSES COORDS MORE DESCRIPTIVE NAME!
def initialize_game_state(settings, final_grid, middle_word, wizard_color, player_name):
    hidden_grid = create_hidden_grid(final_grid)
    statistics = {
        "letters": shuffle_letters_statistic(middle_word),
        "lives_left": settings["starting_lives"],
        "points": 0,
        "last_guess": None,
        "combo": 0,
        "power_points": 0,
        "shield_turns": 0,
    }
    game_state = {
        "player_name": player_name,
        "hidden_grid": hidden_grid,
        "statistics": statistics,
        "last_guess_coords": [],
        "correct_guesses": set(),
        "correct_guesses_coords": set(),
        "message": "Welcome to Wizards of Worderly Place!",  # default message
        "wizard_color": wizard_color,
        "hidden_letter_coords": get_all_letter_coords(final_grid),
    }
    return game_state


def update_display(game_state, selected_wizard):
    clear_screen()
    print_grid(
        game_state["hidden_grid"],
        highlighted_coords=game_state["last_guess_coords"],
        highlight_color="green",
        letters_color="bright_white",
        border_style=game_state["wizard_color"],
        hidden_color=game_state["wizard_color"],
    )
    print_statistics(
        game_state["statistics"],
        game_state["wizard_color"],
        game_state["hidden_grid"],
        selected_wizard,
        game_state,
    )
    print_message(game_state["message"], border_style=game_state["wizard_color"])


def check_power_point_increment(wizard_color, statistics):
    if wizard_color == "red":
        return statistics["combo"] % 3 == 0
    elif wizard_color == "green":
        return statistics["combo"] % 4 == 0
    elif wizard_color == "blue":
        return statistics["combo"] % 3 == 0
    elif wizard_color == "magenta":
        return statistics["combo"] % 3 == 0


def update_power_point_increment(game_state, selected_wizard):
    wizard_color = selected_wizard["color"]
    statistics = game_state["statistics"]

    if statistics["combo"] == 0:
        return False

    if check_power_point_increment(wizard_color, statistics):
        statistics["power_points"] += 1


def get_guess(game_state, selected_wizard):
    wizard_color = selected_wizard["color"]
    power_points = game_state["statistics"]["power_points"]
    while True:
        inp = get_input("  > Enter guess: ")
        guess = inp.lower().strip()
        if not guess:
            game_state["message"] = "Invalid guess! Guess must not be empty!"
            game_state["wizard_color"] = "red"
            update_display(game_state, selected_wizard)
        elif guess == "!p":
            # Used powerup
            if wizard_color == "bright_white":
                game_state["message"] = "White wizards do not have any powers!"
                game_state["wizard_color"] = "red"
                update_display(game_state, selected_wizard)
            elif not power_points:
                game_state["message"] = (
                    "Cannot use powerup! Insufficient conditions for activation!"
                )
                game_state["wizard_color"] = "red"
                update_display(game_state, selected_wizard)
            else:
                return guess
        elif not guess.isalpha():
            game_state["message"] = "Invalid guess! Guess must contain letters only!"
            game_state["wizard_color"] = "red"
            update_display(game_state, selected_wizard)
        else:
            game_state["wizard_color"] = wizard_color
            return guess


def use_powerup(game_state, selected_wizard, words_to_find, final_grid):
    # Wizard color determines what the powerup is
    wizard_color = selected_wizard["color"]
    hidden_letter_coords = game_state["hidden_letter_coords"]
    correct_guesses = game_state["correct_guesses"]
    statistics = game_state["statistics"]

    MIN_REVEAL = 5
    MAX_REVEAL = 10
    coords_to_reveal = []

    statistics["power_points"] -= 1

    if wizard_color == "red":
        coords_to_reveal = get_coords_for_word_reveal(words_to_find, correct_guesses)
    elif wizard_color == "green":
        coords_to_reveal = get_coords_for_random_reveal(
            hidden_letter_coords, MIN_REVEAL, MAX_REVEAL
        )
    elif wizard_color == "magenta":
        statistics["shield_turns"] += 1
        game_state["message"] = (
            "Shields up! You shall not take any damage for the next turn."
        )
        return
    elif wizard_color == "blue":
        statistics["lives_left"] += 1
        game_state["message"] = "Life flows again. You gained one more life."
        return

    game_state["wizard_color"] = wizard_color

    if coords_to_reveal:
        apply_coordinate_reveal(game_state, final_grid, coords_to_reveal)
        completed_words = check_for_completed_words(game_state, words_to_find)

        if completed_words:
            powerup_message = f"Revealed from powerup! {', '.join(completed_words)}!"
        else:
            powerup_message = "Revealed new letters on the board!"
    else:
        powerup_message = "No more letters left to reveal!"

    game_state["message"] = powerup_message


def check_for_completed_words(game_state, words_to_find):
    newly_found_words = []
    correct_guesses = game_state["correct_guesses"]
    hidden_letter_coords_set = game_state["hidden_letter_coords"]

    # Iterate through all words that haven't been guessed yet
    for word, coords in words_to_find.items():
        # Only check words that are not already in correct_guesses
        if word not in correct_guesses:
            # Check if ALL coordinates for this word are NOT in the hidden_letter_coords set
            # If a coordinate is NOT in hidden_letter_coords_set, it means it HAS been revealed
            all_letters_revealed = all(
                coord not in hidden_letter_coords_set for coord in coords
            )

            if all_letters_revealed:
                # The word has been fully revealed!
                correct_guesses.add(word)
                newly_found_words.append(word)

    return newly_found_words  # Return list of words found implicitly


def apply_coordinate_reveal(game_state, final_grid, coords_to_reveal):
    # Update the visual hidden grid
    reveal_coords_in_hidden_grid(
        final_grid, game_state["hidden_grid"], coords_to_reveal
    )

    # Update points
    game_state["statistics"]["points"] += len(
        set(coords_to_reveal) - game_state["correct_guesses_coords"]
    )

    # Update coord tracking
    game_state["correct_guesses_coords"].update(coords_to_reveal)
    game_state["last_guess_coords"] = list(coords_to_reveal)
    for coord in coords_to_reveal:
        game_state["hidden_letter_coords"].discard(coord)


def update_state(guess, game_state, words_to_find, final_grid):
    statistics = game_state["statistics"]
    correct_guesses = game_state["correct_guesses"]

    statistics["last_guess"] = guess
    game_state["last_guess_coords"] = []
    is_incorrect_guess = False

    if guess in correct_guesses:
        # DUPLICATE GUESS
        is_incorrect_guess = True
        statistics["combo"] = 0
        game_state["message"] = f"You already found '{guess}'!"
    elif guess not in words_to_find:
        # WRONG GUESS
        is_incorrect_guess = True
        statistics["combo"] = 0
        game_state["message"] = f"'{guess}' is not one of the words!"
    else:
        # CORRECT GUESS
        game_state["message"] = f"Correct! You found '{guess}'!"
        statistics["combo"] += 1

        word_coords = words_to_find[guess]

        # Update hidden grid and currently hidden letter coordinates
        apply_coordinate_reveal(game_state, final_grid, word_coords)
        check_for_completed_words(game_state, words_to_find)

    if is_incorrect_guess and not statistics["shield_turns"]:
        statistics["lives_left"] -= 1

    if statistics["shield_turns"] > 0:
        statistics["shield_turns"] -= 1


def check_game_over(game_state, words_to_find):
    if len(game_state["correct_guesses"]) == len(words_to_find):
        return "win"
    elif game_state["statistics"]["lives_left"] <= 0:
        return "loss"
    else:
        return "continue"


def display_game_over(game_over_status, game_state, final_grid):
    clear_screen()

    if game_over_status == "win":
        final_message = "YOU WIN!!"  # TODO: CHANGE
        print_grid(
            final_grid, letters_color="green", border_style=game_state["wizard_color"]
        )
    else:
        final_message = "WOMP WOMP. You lose!"  # TODO: CHANGE
        print_grid(
            final_grid,
            highlighted_coords=game_state["correct_guesses_coords"],
            highlight_color="green",
            letters_color="red",
            border_style=game_state["wizard_color"],
        )

    print_message(final_message, border_style=game_state["wizard_color"])
    print_statistics(game_state["statistics"], border_style=game_state["wizard_color"])


def run_game(
    settings, final_grid, words_to_find, middle_word, player_name, selected_wizard
):
    # INITIALIZE GAME
    wizard_color = selected_wizard["color"]
    game_state = initialize_game_state(
        settings, final_grid, middle_word, wizard_color, player_name
    )
    game_over_status = "continue"

    # RUN GAME LOOP
    while True:
        # Update display and get guess
        update_display(game_state, selected_wizard)
        guess = get_guess(game_state, selected_wizard)

        # Handle guess
        if guess == "!p":
            # Powerup used
            use_powerup(game_state, selected_wizard, words_to_find, final_grid)
        else:
            # standard guess
            update_state(guess, game_state, words_to_find, final_grid)

            # Increment power points after guess
            update_power_point_increment(game_state, selected_wizard)

        # Check for game over
        game_over_status = check_game_over(game_state, words_to_find)
        if game_over_status != "continue":
            break

    # DISPLAY GAME OVER
    display_game_over(game_over_status, game_state, final_grid)
    final_score = game_state["statistics"]["points"]
    get_input("  > Press Enter to continue... ")

    # SAVE SCORE AND DISPLAY LEADERBOARDS
    clear_screen()
    save_score(player_name, final_score)
    leaderboard = load_leaderboard()
    print_leaderboard(leaderboard)
    print_message(
        f"Thanks for playing, {player_name}!\nFinal score: {final_score}",
        border_style="bold yellow",
    )
