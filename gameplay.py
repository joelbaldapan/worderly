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
    get_input,
)


def initialize_game_state(settings, final_grid, middle_word):
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
        "message": "Welcome to Wizards of Worderly Place!",
    }
    return game_state


def update_display(game_state):
    clear_screen()
    print_grid(
        game_state["hidden_grid"],
        highlighted_coords=game_state["last_guess_coords"],
        highlight_color="green",
        letters_color="cyan",
    )
    print_message(game_state["message"])
    print_statistics(game_state["statistics"])


def handle_guess(guess, game_state, words_to_find, final_grid):
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


def display_game_over(game_over_status, game_state, final_grid, words_to_find):
    clear_screen()

    print("\n--- Game Over ---")
    print(f"Total Words ({len(words_to_find)}): {', '.join(words_to_find.keys())}")

    if game_over_status == "win":
        final_message = "YOU WIN!!"
        print_grid(final_grid, letters_color="green")
    else:
        final_message = "WOMP WOMP. You lose!"
        print_grid(
            final_grid,
            highlighted_coords=game_state["correct_guesses_coords"],
            highlight_color="cyan",
            letters_color="red",
        )

    print_message(final_message)
    print_statistics(game_state["statistics"])


def run_game(settings, final_grid, words_to_find, middle_word):
    # INITIALIZE STATE
    game_state = initialize_game_state(settings, final_grid, middle_word)

    # GAME LOOP
    while True:
        # Update display and get input
        update_display(game_state)
        guess = get_input()

        # Handle guess
        handle_guess(guess, game_state, words_to_find, final_grid)
        
        # Check for game over
        game_over_status = check_game_over(game_state, words_to_find)
        if game_over_status != "continue":
            break  # Exit game loop

    # DISPLAY GAME OVER
    display_game_over(game_over_status, game_state, final_grid, words_to_find)
