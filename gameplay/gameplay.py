# ****************
# IMPORTS
# ****************
from gameplay.game_constants import *
from gameplay.game_state_handler import (
    initialize_game_state,
    process_guess,
    check_game_over,
)
from gameplay.powerup_handler import update_power_points, use_powerup
from display.display import (
    print_grid,
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
# GAME LOGIC
# ****************


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


def update_game_over_display(
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


def update_end_game_display(settings, player_name, final_score):
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


# *******************
# MAIN GAME FUNCTION
# *******************


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
            process_guess(guess, game_state, words_to_find, final_grid, wizard_color)
            # Increment power points only after a standard guess, not powerup use
            update_power_points(game_state, selected_wizard)

        # Check for game over after handling the guess/powerup
        game_over_status = check_game_over(game_state, words_to_find)

    # DISPLAY GAME OVER
    update_game_over_display(
        settings, game_over_status, game_state, final_grid, selected_wizard
    )
    final_score = game_state["statistics"]["points"]

    # IF HEART POINTS ENABLED, SAVE SCORE AND DISPLAY LEADERBOARDS
    if settings["heart_point_mode"]:
        update_end_game_display(settings, player_name, final_score)
