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


def run_game(settings, final_grid, words_to_find, middle_word):
    hidden_grid = create_hidden_grid(final_grid)

    statistics = {
        "letters": shuffle_letters_statistic(middle_word),
        "lives_left": settings["starting_lives"],
        "points": 0,
        "last_guess": None,
    }

    guess_coords = []
    correct_guesses = set()
    correct_guesses_coords = set()
    message = "Welcome to Wizards of Worderly Place!"
    has_won = False

    while True:
        clear_screen()
        print()
        print_grid(
            hidden_grid,
            highlighted_coords=guess_coords,
            highlight="green",
            letters_color="cyan",
        )
        print_message(message)
        print_statistics(statistics)
        inp = get_input()

        # Check if input is in the words_to_find
        guess = inp.lower().strip()
        if guess in correct_guesses:
            # Duplicate
            # statistics["lives_left"] -= 1
            message = "Already guessed!"
            guess_coords = []
        elif guess not in words_to_find:
            # Wrong
            statistics["lives_left"] -= 1
            message = "Wrong guess!"
            guess_coords = []
        else:
            # Correct
            message = "Correct guess!"
            statistics["points"] += len(guess)

            word_coords = words_to_find[guess]

            correct_guesses.add(guess)
            correct_guesses_coords.update(word_coords)
            guess_coords = word_coords

            reveal_coords_in_hidden_grid(final_grid, hidden_grid, word_coords)

        statistics["last_guess"] = guess

        if len(correct_guesses) == len(words_to_find):
            has_won = True
            break
        elif statistics["lives_left"] <= 0:
            break

    clear_screen()
    print("\nWords:")
    print(len(words_to_find))
    print(list(words_to_find.keys()))

    if has_won:
        message = "YOU WIN!!"
        print_grid(final_grid, letters_color="green")
    else:
        message = "WOMP WOMP. You lose!"
        print_grid(
            final_grid,
            highlighted_coords=correct_guesses_coords,
            highlight="cyan",
            letters_color="red",
        )

    print_message(message)
    print_statistics(statistics)
