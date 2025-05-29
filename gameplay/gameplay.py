# ****************
# IMPORTS
# ****************
from display.display import (
    get_input,
    print_grid,
    print_leaderboard,
    print_message,
    print_statistics,
)
from display.display_utils import clear_screen
from gameplay import game_constants
from gameplay.game_state_handler import (
    check_game_over,
    initialize_game_state,
    process_guess,
)
from gameplay.powerup_handler import update_power_points, use_powerup
from leaderboard.leaderboard import (
    load_leaderboard,
    save_score,
)

# ****************
# GAME LOGIC
# ****************


def update_display(settings, game_state, selected_wizard) -> None:
    """Updates the entire game display for the current turn.

    Clears the screen and then prints the grid, statistics panel, and
    the current message based on the game state.

    Args:
        settings (dict): The current game settings.
        game_state (dict): The main game state dictionary.
        selected_wizard (dict):
            The dictionary containing data for the selected wizard.

    Returns:
        None

    """
    clear_screen()
    print_grid(
        settings,
        game_state["hidden_grid"],
        highlighted_coords=game_state["last_guess_coords"],
        highlight_color=game_constants.DEFAULT_HIGHLIGHT_COLOR,
        letters_color=game_constants.DEFAULT_LETTERS_COLOR,
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


def get_guess(settings, game_state, selected_wizard):
    """Prompts the player for input and validates it as a guess or powerup command.

    Loops until valid input is received. Validates against empty input,
    non-alphabetic characters (for guesses), and powerup command rules
    (heart point mode enabled, wizard type, sufficient power points).
    Updates the display with error messages for invalid inputs.

    Args:
        settings (dict): The current game settings.
        game_state (dict):
            The main game state dictionary (used for validation
            and potentially modified for error messages).
        selected_wizard (dict): The dictionary for the current wizard.

    Returns:
        str: The validated player input (lowercase, stripped word guess or
             the powerup command string).

    """
    wizard_color = selected_wizard["color"]
    power_points = game_state["statistics"]["power_points"]

    while True:
        # Show (Type `!p` to activate powerup!) if on heart point mode
        if settings["heart_point_mode"] and wizard_color != "bright_white":
            user_input = get_input(
                settings,
                "  > Enter guess (Type `!p` to activate powerup!): ",
            )
        else:
            user_input = get_input(settings, "  > Enter guess: ")
        guess = user_input.lower().strip()

        if not guess:
            # Handle empty input
            game_state["next_message"] = game_constants.INVALID_GUESS_EMPTY_MSG
            game_state["next_message_color"] = game_constants.ERROR_COLOR
            update_display(settings, game_state, selected_wizard)
        elif (
            settings["heart_point_mode"] and guess == game_constants.POWERUP_COMMAND
        ):  # Only have powerups when heart point mode
            # Handle powerup command attempt
            if wizard_color == "bright_white":
                # White wizard cannot use powerups
                game_state["next_message"] = game_constants.NO_POWERUP_MSG
                game_state["next_message_color"] = game_constants.ERROR_COLOR
                update_display(settings, game_state, selected_wizard)
            elif power_points <= 0:  # Check power points (use <= 0 for safety)
                # Insufficient power points
                game_state["next_message"] = game_constants.INSUFFICIENT_POWER_MSG
                game_state["next_message_color"] = game_constants.ERROR_COLOR
                update_display(settings, game_state, selected_wizard)
            else:
                # Valid powerup attempt
                return guess  # Return the command itself
        elif not guess.isalpha():
            # Handle non-alphabetic guess
            game_state["next_message"] = game_constants.INVALID_GUESS_ALPHA_MSG
            game_state["next_message_color"] = game_constants.ERROR_COLOR
            update_display(settings, game_state, selected_wizard)
        else:
            # Valid word guess
            game_state["next_message_color"] = wizard_color  # Reset color for next display
            return guess


def update_game_over_display(
    settings,
    game_over_status,
    game_state,
    final_grid,
    selected_wizard,
) -> None:
    """Displays the final game over screen (win or loss).

    Clears the screen, prints the final grid state (revealed or partially
    revealed based on win/loss), final statistics, and the win/loss message.

    Args:
        settings (dict): The current game settings.
        game_over_status (str): "win" or "loss".
        game_state (dict): The final game state dictionary.
        final_grid (list[list[str or None]]): The complete, revealed game grid.
        selected_wizard (dict): The dictionary for the selected wizard.

    Returns:
        None: This function prints directly to the console and returns nothing.

    """
    clear_screen()
    stats = game_state["statistics"]
    wizard_color = selected_wizard["color"]

    if game_over_status == "win":
        final_message = game_constants.WIN_MSG
        print_grid(
            settings,
            final_grid,  # Show fully revealed grid
            letters_color=game_constants.WIN_COLOR,
            border_style=wizard_color,
        )
    else:  # "loss"
        final_message = game_constants.LOSE_MSG
        print_grid(
            settings,
            final_grid,  # Show fully revealed grid
            highlighted_coords=game_state["found_letter_coords"],  # Highlight found letters
            highlight_color=game_constants.DEFAULT_HIGHLIGHT_COLOR,
            letters_color=game_constants.LOSE_COLOR,  # Show all letters in red
            border_style=wizard_color,
            hidden_color=wizard_color,  # Keep hidden letters consistent color
        )

    # Print final stats using the wizard color for the border
    print_statistics(
        settings,
        stats,
        wizard_color,
        final_grid,
        selected_wizard,
        game_state,
    )
    # Print the final win/loss message
    print_message(settings, final_message, border_style=wizard_color)


def update_end_game_display(settings, player_name, final_score) -> None:
    """Handles the display and actions after the game over screen in HP mode.

    Waits for user input, clears screen, saves the score, loads and prints
    the leaderboard, prints the final thank you message, and waits for input again.

    Args:
        settings (dict): The current game settings.
        player_name (str): The name of the player.
        final_score (int): The player's final score.

    Returns:
        None

    """
    get_input(
        settings,
        "  > Press Enter to continue... ",
    )  # Pause after game over screen

    clear_screen()
    save_score(player_name, final_score)
    leaderboard = load_leaderboard()
    print_leaderboard(settings, leaderboard)
    print_message(
        settings,
        game_constants.THANKS_MSG.format(player_name, final_score),
        border_style=game_constants.FINAL_SCORE_BORDER,
    )
    get_input(settings, "  > Press Enter to continue... ")  # Pause after leaderboard


# *******************
# MAIN GAME FUNCTION
# *******************


def run_game(
    settings,
    final_grid,
    words_to_find,
    middle_word,
    player_name,
    selected_wizard,
) -> None:
    """Runs the main gameplay loop for a single game instance.

    Initializes the game state, then enters a loop that updates the display,
    gets player input, processes the guess or powerup, updates power points,
    and checks for game over conditions. After the loop ends, displays the
    game over screen and potentially the end game display (leaderboard).

    Args:
        settings (dict): The settings for the current game.
        final_grid (list[list[str | None]]): The fully generated game grid.
        words_to_find (dict): Dictionary mapping placed words to their coordinates.
        middle_word (str): The central word used for setup.
        player_name (str | None): The player's name (can be None if not HP mode).
        selected_wizard (dict): The dictionary containing the selected wizard's data.

    Returns:
        None

    """
    # INITIALIZE GAME
    wizard_color = selected_wizard["color"]
    game_state = initialize_game_state(
        final_grid,
        middle_word,
        selected_wizard,
        player_name,
    )
    game_over_status = "continue"

    # RUN GAME LOOP
    while game_over_status == "continue":
        # Update display and get guess
        update_display(settings, game_state, selected_wizard)
        guess = get_guess(settings, game_state, selected_wizard)

        # Handle guess
        if guess == game_constants.POWERUP_COMMAND:
            use_powerup(game_state, selected_wizard, words_to_find, final_grid)
        else:
            process_guess(guess, game_state, words_to_find, final_grid, wizard_color)
            # Increment power points only after a standard guess, not powerup use
            update_power_points(game_state, selected_wizard)

        # Check for game over after handling the guess/powerup
        game_over_status = check_game_over(game_state, words_to_find)

    # DISPLAY GAME OVER
    update_game_over_display(
        settings,
        game_over_status,
        game_state,
        final_grid,
        selected_wizard,
    )
    final_score = game_state["statistics"]["points"]

    # IF HEART POINTS ENABLED, SAVE SCORE AND DISPLAY LEADERBOARDS
    if settings["heart_point_mode"]:
        update_end_game_display(settings, player_name, final_score)
