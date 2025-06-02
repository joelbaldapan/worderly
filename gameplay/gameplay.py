from data.settings_details import DifficultyData
from data.wizards_details import WizardData
from display.display import get_input, print_grid, print_message, print_statistics, print_streak_leaderboard
from display.display_utils import clear_screen
from gameplay import game_constants
from gameplay.game_state_handler import (
    GameStateData,
    check_game_over,
    initialize_game_state,
    process_guess,
)
from gameplay.powerup_handler import update_power_points, use_powerup
from leaderboard.streak_handler import load_streaks


def update_display(
    current_difficulty_config: DifficultyData,
    game_st: GameStateData,
    current_selected_wizard: WizardData,
) -> None:
    """Update the entire game display for the current turn."""
    clear_screen()
    print_grid(
        current_difficulty_config,
        game_st.hidden_grid,
        highlighted_coords=game_st.last_guess_coords,
        highlight_color=game_constants.DEFAULT_HIGHLIGHT_COLOR,
        letters_color=game_constants.DEFAULT_LETTERS_COLOR,
        border_style=game_st.next_message_color,
        hidden_color=game_st.next_message_color,
    )
    print_statistics(
        current_difficulty_config,
        game_st.statistics,
        game_st.next_message_color,
        game_st.hidden_grid,
        current_selected_wizard,
        game_st,
    )
    print_message(
        current_difficulty_config,
        game_st.next_message,
        border_style=game_st.next_message_color,
    )


def get_guess(
    current_difficulty_config: DifficultyData,
    game_st: GameStateData,
    current_selected_wizard: WizardData,
) -> str:
    """Prompts player for input, validates it as a guess or powerup command."""
    wizard_color = current_selected_wizard.color
    power_points = game_st.statistics.power_points

    while True:
        prompt = "  > Enter guess: "
        if current_difficulty_config.heart_point_mode and wizard_color != "bright_white":
            prompt = "  > Enter guess (Type `!p` to activate powerup!): "

        user_input = get_input(current_difficulty_config, prompt)
        guess = user_input.lower().strip()

        if not guess:
            game_st.next_message = game_constants.INVALID_GUESS_EMPTY_MSG
            game_st.next_message_color = game_constants.ERROR_COLOR
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
    game_st: GameStateData,
    final_grid: list[list[str | None]],
    current_selected_wizard: WizardData,
) -> None:
    """Display the final game over screen (win or loss)."""
    clear_screen()
    stats = game_st.statistics
    wizard_color = current_selected_wizard.color

    if game_over_status == "win":
        final_message = game_constants.WIN_MSG
        letters_display_color = game_constants.WIN_COLOR
    else:
        final_message = game_constants.LOSE_MSG
        letters_display_color = game_constants.LOSE_COLOR

    grid_to_show = final_grid
    highlight_coords_on_loss = game_st.found_letter_coords if game_over_status == "loss" else []

    print_grid(
        current_difficulty_config,
        grid_to_show,
        highlighted_coords=highlight_coords_on_loss,
        highlight_color=game_constants.DEFAULT_HIGHLIGHT_COLOR,
        letters_color=letters_display_color,
        border_style=wizard_color,
        hidden_color=wizard_color,
    )
    print_statistics(
        current_difficulty_config,
        stats,
        wizard_color,
        final_grid,
        current_selected_wizard,
        game_st,
    )
    print_message(current_difficulty_config, final_message, border_style=wizard_color)


def update_game_over_display(
    current_difficulty_config: DifficultyData,
    game_over_status: str,
    game_st: GameStateData,
    final_grid: list[list[str | None]],
    current_selected_wizard: WizardData,
) -> None:
    clear_screen()
    stats = game_st.statistics
    wizard_color = current_selected_wizard.color
    final_message = game_constants.WIN_MSG if game_over_status == "win" else game_constants.LOSE_MSG
    letters_display_color = game_constants.WIN_COLOR if game_over_status == "win" else game_constants.LOSE_COLOR
    grid_to_show = final_grid
    highlight_coords_on_loss = game_st.found_letter_coords if game_over_status == "loss" else []
    print_grid(
        current_difficulty_config,
        grid_to_show,
        highlighted_coords=highlight_coords_on_loss,
        highlight_color=game_constants.DEFAULT_HIGHLIGHT_COLOR,
        letters_color=letters_display_color,
        border_style=wizard_color,
        hidden_color=wizard_color,
    )
    print_statistics(
        current_difficulty_config,
        stats,
        wizard_color,
        final_grid,
        current_selected_wizard,
        game_st,
    )
    print_message(current_difficulty_config, final_message, border_style=wizard_color)


def end_game(
    current_difficulty_config: DifficultyData,
    player_name: str | None,
    final_score: int,
) -> None:
    """Handles display and interaction after a game ends, shows leaderboards,
    and provides a mode-specific prompt to continue.
    """
    get_input(current_difficulty_config, "  > Game Over. Press Enter to see summary and leaderboards... ")
    clear_screen()

    player_name
    print_message(
        current_difficulty_config,
        game_constants.THANKS_MSG.format(player_name, final_score),
        border_style=game_constants.FINAL_SCORE_BORDER,
    )

    print_message(current_difficulty_config, "Winning Streaks Leaderboard:", border_style="cyan")
    streaks = load_streaks()
    print_streak_leaderboard(current_difficulty_config, streaks)

    # Conditional prompt based on game mode
    if current_difficulty_config.heart_point_mode:
        get_input(current_difficulty_config, "  > Press Enter to return to the main menu... ")
    else:  # No Heart Points Mode
        get_input(current_difficulty_config, "  > Press Enter for the next puzzle... ")


def run_game(
    difficulty_conf: DifficultyData,
    final_grid: list[list[str | None]],
    words_to_find: dict[str, list[tuple[int, int]]],
    middle_word: str,
    player_name: str | None,
    selected_wizard: WizardData,
) -> tuple[str, int]:
    wizard_color = selected_wizard.color
    game_st: GameStateData = initialize_game_state(
        final_grid,
        middle_word,
        selected_wizard,
        player_name,
    )
    game_over_status: str = "continue"

    while game_over_status == "continue":
        update_display(difficulty_conf, game_st, selected_wizard)
        print(words_to_find.keys())
        guess = get_guess(difficulty_conf, game_st, selected_wizard)

        if guess == game_constants.POWERUP_COMMAND:
            use_powerup(game_st, selected_wizard, words_to_find, final_grid)
        else:
            process_guess(guess, game_st, words_to_find, final_grid, wizard_color)
            update_power_points(game_st, selected_wizard)

        game_over_status = check_game_over(game_st, words_to_find)

    update_game_over_display(
        difficulty_conf,
        game_over_status,
        game_st,
        final_grid,
        selected_wizard,
    )
    final_score_this_game: int = game_st.statistics.points

    end_game(difficulty_conf, player_name, final_score_this_game)

    return game_over_status, final_score_this_game
