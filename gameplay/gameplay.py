# gameplay/gameplay.py

# Import dataclasses
from data.settings_details import DifficultyData
from data.wizards_details import WizardData
from display.display import (
    get_input,
    print_grid,
    print_leaderboard,
    print_message,
    print_statistics,  # This will receive GameStatisticsData
)
from display.display_utils import clear_screen
from gameplay import game_constants

# GameStateData will be used here
from gameplay.game_state_handler import (
    GameStateData,  # Import the dataclass
    check_game_over,
    initialize_game_state,  # Returns GameStateData
    process_guess,  # Takes GameStateData
)

# These will also need to be updated to take GameStateData and WizardData
from gameplay.powerup_handler import update_power_points, use_powerup
from leaderboard.leaderboard import (
    load_leaderboard,
    save_score,
)


def update_display(
    current_difficulty_config: DifficultyData,
    game_st: GameStateData,  # Changed to GameStateData
    current_selected_wizard: WizardData,
) -> None:
    """Updates the entire game display for the current turn."""
    clear_screen()
    print_grid(
        current_difficulty_config,
        game_st.hidden_grid,  # Attribute access
        highlighted_coords=game_st.last_guess_coords,  # Attribute access
        highlight_color=game_constants.DEFAULT_HIGHLIGHT_COLOR,
        letters_color=game_constants.DEFAULT_LETTERS_COLOR,
        border_style=game_st.next_message_color,  # Attribute access
        hidden_color=game_st.next_message_color,  # Attribute access
    )
    print_statistics(
        current_difficulty_config,
        game_st.statistics,  # Pass GameStatisticsData object
        game_st.next_message_color,
        game_st.hidden_grid,
        current_selected_wizard,
        game_st,  # Pass GameStateData for player_name etc. if display needs more
    )
    print_message(
        current_difficulty_config,
        game_st.next_message,  # Attribute access
        border_style=game_st.next_message_color,  # Attribute access
    )


def get_guess(
    current_difficulty_config: DifficultyData,
    game_st: GameStateData,  # Changed to GameStateData
    current_selected_wizard: WizardData,
) -> str:
    """Prompts player for input, validates it as a guess or powerup command."""
    wizard_color = current_selected_wizard.color
    power_points = game_st.statistics.power_points  # Attribute access

    while True:
        prompt = "  > Enter guess: "
        if current_difficulty_config.heart_point_mode and wizard_color != "bright_white":
            prompt = "  > Enter guess (Type `!p` to activate powerup!): "

        user_input = get_input(current_difficulty_config, prompt)
        guess = user_input.lower().strip()

        if not guess:
            game_st.next_message = game_constants.INVALID_GUESS_EMPTY_MSG  # Attribute access
            game_st.next_message_color = game_constants.ERROR_COLOR  # Attribute access
            update_display(current_difficulty_config, game_st, current_selected_wizard)
        elif current_difficulty_config.heart_point_mode and guess == game_constants.POWERUP_COMMAND:
            if wizard_color == "bright_white":
                game_st.next_message = game_constants.NO_POWERUP_MSG
                game_st.next_message_color = game_constants.ERROR_COLOR
                update_display(current_difficulty_config, game_st, current_selected_wizard)
            elif power_points <= 0:
                game_st.next_message = game_constants.INSUFFICIENT_POWER_MSG
                game_st.next_message_color = game_constants.ERROR_COLOR
                update_display(current_difficulty_config, game_st, current_selected_wizard)
            else:
                return guess
        elif not guess.isalpha():
            game_st.next_message = game_constants.INVALID_GUESS_ALPHA_MSG
            game_st.next_message_color = game_constants.ERROR_COLOR
            update_display(current_difficulty_config, game_st, current_selected_wizard)
        else:
            game_st.next_message_color = wizard_color
            return guess


def update_game_over_display(
    current_difficulty_config: DifficultyData,
    game_over_status: str,
    game_st: GameStateData,  # Changed to GameStateData
    final_grid: list[list[str | None]],
    current_selected_wizard: WizardData,
) -> None:
    """Displays the final game over screen (win or loss)."""
    clear_screen()
    stats = game_st.statistics  # stats is now GameStatisticsData
    wizard_color = current_selected_wizard.color

    final_message = game_constants.WIN_MSG if game_over_status == "win" else game_constants.LOSE_MSG
    letters_display_color = game_constants.WIN_COLOR if game_over_status == "win" else game_constants.LOSE_COLOR

    grid_to_show = final_grid
    highlight_coords_on_loss = game_st.found_letter_coords if game_over_status == "loss" else []  # Attribute access

    print_grid(
        current_difficulty_config,
        grid_to_show,
        highlighted_coords=highlight_coords_on_loss,
        highlight_color=game_constants.DEFAULT_HIGHLIGHT_COLOR,
        letters_color=letters_display_color,
        border_style=wizard_color,
        hidden_color=wizard_color,
    )
    print_statistics(  # This will pass GameStatisticsData as 'stats'
        current_difficulty_config,
        stats,
        wizard_color,
        final_grid,
        current_selected_wizard,
        game_st,  # Pass GameStateData
    )
    print_message(current_difficulty_config, final_message, border_style=wizard_color)


def update_end_game_display(
    current_difficulty_config: DifficultyData,
    player_name: str | None,
    final_score: int,
) -> None:
    """Handles display after game over screen in Heart Points mode."""
    get_input(current_difficulty_config, "  > Press Enter to continue... ")
    clear_screen()

    if player_name is not None:
        save_score(player_name, final_score)
    else:
        print("Note: Score not saved as player name was not available.")

    leaderboard = load_leaderboard()
    print_leaderboard(current_difficulty_config, leaderboard)

    name_to_display = player_name if player_name is not None else "Wizard"
    print_message(
        current_difficulty_config,
        game_constants.THANKS_MSG.format(name_to_display, final_score),
        border_style=game_constants.FINAL_SCORE_BORDER,
    )
    get_input(current_difficulty_config, "  > Press Enter to continue... ")


def run_game(
    difficulty_conf: DifficultyData,
    final_grid: list[list[str | None]],
    words_to_find: dict[str, list[tuple[int, int]]],
    middle_word: str,
    player_name: str | None,
    selected_wizard: WizardData,
) -> None:
    """Runs the main gameplay loop for a single game instance."""
    wizard_color = selected_wizard.color

    game_st: GameStateData = initialize_game_state(  # Returns GameStateData
        final_grid,
        middle_word,
        selected_wizard,
        player_name,
    )
    game_over_status: str = "continue"

    while game_over_status == "continue":
        update_display(difficulty_conf, game_st, selected_wizard)
        guess = get_guess(difficulty_conf, game_st, selected_wizard)

        if guess == game_constants.POWERUP_COMMAND:
            # use_powerup expects GameStateData and WizardData
            use_powerup(game_st, selected_wizard, words_to_find, final_grid)
        else:
            # process_guess expects GameStateData
            process_guess(guess, game_st, words_to_find, final_grid, wizard_color)
            # update_power_points expects GameStateData and WizardData
            update_power_points(game_st, selected_wizard)

        # check_game_over expects GameStateData
        game_over_status = check_game_over(game_st, words_to_find)

    update_game_over_display(difficulty_conf, game_over_status, game_st, final_grid, selected_wizard)
    final_score: int = game_st.statistics.points  # Attribute access

    if difficulty_conf.heart_point_mode:
        update_end_game_display(difficulty_conf, player_name, final_score)
