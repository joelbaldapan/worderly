# ****************
# IMPORTS
# ****************
from gameplay.grid_gameplay import (
    create_hidden_grid,
    reveal_coords_in_hidden_grid,
    get_all_letter_coords,
    get_coords_for_random_reveal,
    get_coords_for_word_reveal,
)
from display.display_interface import (
    print_grid,
    shuffle_letters_statistic,
    print_message,
    print_statistics,
    print_leaderboard,
    get_input,
)
from display.display_utils import clear_screen
from leaderboard.leaderboard import (
    load_leaderboard,
    save_score,
)

# ****************
# CONSTANTS
# ****************

# GAMEPLAY COMMANDS
POWERUP_COMMAND = "!p"
# TODO: Add help command idk?

# MESSAGES
WELCOME_MSG = "Welcome to Wizards of Worderly Place!"
INVALID_GUESS_EMPTY_MSG = "Invalid guess! Guess must not be empty!"
INVALID_GUESS_ALPHA_MSG = "Invalid guess! Guess must contain letters only!"
NO_POWERUP_MSG = "White wizards do not have any powers!"
INSUFFICIENT_POWER_MSG = "Cannot use powerup! Insufficient conditions for activation!"
SHIELD_ACTIVATED_MSG = "Shields up! You shall not take any damage for the next turn."
LIFE_GAINED_MSG = "Life flows again. You gained one more life."
WIN_MSG = "CONGRATULATIONS! You found all the words!"
LOSE_MSG = "WOMP WOMP. You ran out of lives!"
POWERUP_REVEAL_WORDS_MSG = "Revealed from powerup! {}!"
POWERUP_REVEAL_LETTERS_MSG = "Revealed new letters on the board!"
POWERUP_NO_REVEAL_MSG = "No more letters left to reveal!"
ALREADY_FOUND_MSG = "You already found '{}'!"
NOT_A_WORD_MSG = "'{}' is not one of the words!"
CORRECT_GUESS_MSG = "Correct! You found '{}'!"
THANKS_MSG = "Thanks for playing, {}!\nFinal score: {}"

# DISPLAY DEFAULTS
DEFAULT_HIGHLIGHT_COLOR = "green"
DEFAULT_LETTERS_COLOR = "bright_white"
ERROR_COLOR = "red"
WIN_COLOR = "green"
LOSE_COLOR = "red"
FINAL_SCORE_BORDER = "bold yellow"

# GAMEPLAY CONSTANTS
MIN_RANDOM_REVEAL = 5
MAX_RANDOM_REVEAL = 8
SHIELD_INCREMENT = 2


# ****************
# GAME LOGIC
# ****************


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


def update_display(settings, game_state, selected_wizard):
    clear_screen()
    print_grid(
        settings,
        game_state["hidden_grid"],
        highlighted_coords=game_state["last_guess_coords"],
        highlight_color=DEFAULT_HIGHLIGHT_COLOR,
        letters_color=DEFAULT_LETTERS_COLOR,
        border_style=game_state["next_message_color"],
        hidden_color=game_state["next_message_color"],
    )
    print_statistics(
        settings,
        game_state["statistics"],
        game_state["next_message_color"],  # Use message color for stats border
        game_state["hidden_grid"],
        selected_wizard,
        game_state,
    )
    print_message(
        settings,
        game_state["next_message"],
        border_style=game_state["next_message_color"],
    )


def check_power_point_increment(combo_req, statistics):
    return (
        combo_req is not None
        and statistics["combo"] > 0
        and statistics["combo"] % combo_req == 0
    )


def update_power_point_increment(game_state, selected_wizard):
    combo_req = selected_wizard["combo_requirement"]
    statistics = game_state["statistics"]

    if statistics["combo"] == 0:
        return

    if check_power_point_increment(combo_req, statistics):
        statistics["power_points"] += 1


def get_guess(settings, game_state, selected_wizard):
    wizard_color = selected_wizard["color"]
    power_points = game_state["statistics"]["power_points"]

    while True:
        user_input = get_input(settings, "  > Enter guess: ")
        guess = user_input.lower().strip()

        if not guess:
            game_state["next_message"] = INVALID_GUESS_EMPTY_MSG
            game_state["next_message_color"] = ERROR_COLOR
            update_display(settings, game_state, selected_wizard)
        elif (
            settings["heart_point_mode"] and guess == POWERUP_COMMAND
        ):  # Only have powerups when heart point mode
            # Check if powerup can be used
            if wizard_color == "bright_white":
                game_state["next_message"] = NO_POWERUP_MSG
                game_state["next_message_color"] = ERROR_COLOR
                update_display(settings, game_state, selected_wizard)
            elif not power_points:
                game_state["next_message"] = INSUFFICIENT_POWER_MSG
                game_state["next_message_color"] = ERROR_COLOR
                update_display(settings, game_state, selected_wizard)
            else:
                # Valid powerup attempt
                return guess  # Return the command itself
        elif not guess.isalpha():
            game_state["next_message"] = INVALID_GUESS_ALPHA_MSG
            game_state["next_message_color"] = ERROR_COLOR
            update_display(settings, game_state, selected_wizard)
        else:
            # Valid word guess
            game_state["next_message_color"] = wizard_color
            return guess


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

    # Note how RED and GREEN reveals letters on the board,
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


def update_state(guess, game_state, words_to_find, final_grid, wizard_color):
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


def check_game_over(game_state, words_to_find):
    if len(game_state["correctly_guessed_words"]) == len(words_to_find):
        return "win"
    elif game_state["statistics"]["lives_left"] <= 0:
        return "loss"
    else:
        return "continue"


def display_game_over(
    settings, game_over_status, game_state, final_grid, selected_wizard
):
    clear_screen()
    stats = game_state["statistics"]
    wizard_color = selected_wizard["color"]

    if game_over_status == "win":
        final_message = WIN_MSG
        print_grid(
            settings, final_grid, letters_color=WIN_COLOR, border_style=wizard_color
        )
    else:  # "loss"
        final_message = LOSE_MSG
        print_grid(
            settings,
            final_grid,
            highlighted_coords=game_state["found_letter_coords"],
            highlight_color=DEFAULT_HIGHLIGHT_COLOR,  # Highlight found letters
            letters_color=LOSE_COLOR,  # Show all letters, but in red
            border_style=wizard_color,
            hidden_color=wizard_color,  # Keep hidden letters consistent color
        )

    # Print final stats using the wizard color for the border
    print_statistics(
        settings, stats, wizard_color, final_grid, selected_wizard, game_state
    )
    print_message(settings, final_message, border_style=wizard_color)


def run_game(
    settings, final_grid, words_to_find, middle_word, player_name, selected_wizard
):
    # INITIALIZE GAME
    wizard_color = selected_wizard["color"]
    game_state = initialize_game_state(
        final_grid, middle_word, selected_wizard, player_name
    )
    game_over_status = "continue"

    # RUN GAME LOOP
    while game_over_status == "continue":
        # Update display and get guess
        update_display(settings, game_state, selected_wizard)
        guess = get_guess(settings, game_state, selected_wizard)

        # Handle guess
        if guess == POWERUP_COMMAND:
            use_powerup(game_state, selected_wizard, words_to_find, final_grid)
        else:
            update_state(guess, game_state, words_to_find, final_grid, wizard_color)
            # Increment power points only after a standard guess, not powerup use
            update_power_point_increment(game_state, selected_wizard)

        # Check for game over after handling the guess/powerup
        game_over_status = check_game_over(game_state, words_to_find)

    # DISPLAY GAME OVER
    display_game_over(
        settings, game_over_status, game_state, final_grid, selected_wizard
    )
    final_score = game_state["statistics"]["points"]

    # IF HEART POINTS ENABLED, SAVE SCORE AND DISPLAY LEADERBOARDS
    if settings["heart_point_mode"]:
        get_input(settings, "  > Press Enter to continue... ")

        clear_screen()
        save_score(player_name, final_score)
        leaderboard = load_leaderboard()
        print_leaderboard(settings, leaderboard)
        print_message(
            settings,
            THANKS_MSG.format(player_name, final_score),
            border_style=FINAL_SCORE_BORDER,
        )
        get_input(settings, "  > Press Enter to continue... ")
