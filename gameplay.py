# ****************
# GAMEPLAY
# ****************

from grid_gameplay import create_hidden_grid, reveal_coords_in_hidden_grid
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


def initialize_game_state(settings, final_grid, middle_word, wizard_color):
    hidden_grid = create_hidden_grid(final_grid)
    statistics = {
        "letters": shuffle_letters_statistic(middle_word),
        "lives_left": settings["starting_lives"],
        "points": 0,
        "last_guess": None,
    }
    game_state = {
        "hidden_grid": hidden_grid,
        "statistics": statistics,
        "last_guess_coords": [],
        "correct_guesses": set(),
        "correct_guesses_coords": set(),
        "message": "Welcome to Wizards of Worderly Place!",  # default message
        "wizard_color": wizard_color,
    }
    return game_state


def update_display(game_state):
    clear_screen()
    print_grid(
        game_state["hidden_grid"],
        highlighted_coords=game_state["last_guess_coords"],
        highlight_color="green",
        letters_color="bold cyan",
        border_style=game_state["wizard_color"],
    )
    print_message(game_state["message"], border_style=game_state["wizard_color"])
    print_statistics(game_state["statistics"], border_style=game_state["wizard_color"])


def get_guess(game_state, wizard_color):
    while True:
        inp = get_input("  > Enter guess: ")
        guess = inp.lower().strip()
        if not guess:
            game_state["message"] = "Invalid guess! Guess must not be empty!"
            game_state["wizard_color"] = "red"
            update_display(game_state)
        elif not guess.isalpha():
            game_state["message"] = "Invalid guess! Guess must not be empty!"
            game_state["wizard_color"] = "red"
            update_display(game_state)
        else:
            game_state["wizard_color"] = wizard_color
            return guess


def update_state(guess, game_state, words_to_find, final_grid):
    statistics = game_state["statistics"]
    correct_guesses = game_state["correct_guesses"]

    statistics["last_guess"] = guess
    game_state["last_guess_coords"] = []

    if guess in correct_guesses:
        # DUPLICATE GUESS
        statistics["lives_left"] -= 1
        game_state["message"] = f"You already found '{guess}'!"
    elif guess not in words_to_find:
        # WRONG GUESS
        statistics["lives_left"] -= 1
        game_state["message"] = f"'{guess}' is not one of the words!"
    else:
        # CORRECT GUESS
        game_state["message"] = f"Correct! You found '{guess}'!"
        statistics["points"] += len(guess)
        word_coords = words_to_find[guess]

        correct_guesses.add(guess)
        game_state["correct_guesses_coords"].update(word_coords)
        game_state["last_guess_coords"] = word_coords

        # Update hidden grid
        reveal_coords_in_hidden_grid(final_grid, game_state["hidden_grid"], word_coords)


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
        final_message = "YOU WIN!!"
        print_grid(
            final_grid, letters_color="green", border_style=game_state["wizard_color"]
        )
    else:
        final_message = "WOMP WOMP. You lose!"
        print_grid(
            final_grid,
            highlighted_coords=game_state["correct_guesses_coords"],
            highlight_color=game_state["wizard_color"],
            letters_color="red",
        )

    print_message(final_message, border_style=game_state["wizard_color"])
    print_statistics(game_state["statistics"], border_style=game_state["wizard_color"])


def run_game(
    settings, final_grid, words_to_find, middle_word, player_name, selected_wizard
):
    # INITIALIZE GAME
    wizard_color = selected_wizard["color"]
    game_state = initialize_game_state(settings, final_grid, middle_word, wizard_color)
    game_over_status = "continue"

    # RUN GAME LOOP
    while True:
        # Update display and get guess
        update_display(game_state)
        guess = get_guess(game_state, wizard_color)

        # Handle guess
        update_state(guess, game_state, words_to_find, final_grid)

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
        border_style=wizard_color,
    )
