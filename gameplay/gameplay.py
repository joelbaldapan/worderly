from dataclasses import dataclass

from data.settings_details import DifficultyData
from data.wizards_details import WizardData
from display.display import (
    get_input,
    print_grid,
    print_message,
    print_statistics,
    print_streak_leaderboard,
)
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


@dataclass
class GameConfig:
    """configuration object holding all relevant game configuration and state."""

    difficulty_conf: DifficultyData
    final_grid: list[list[str | None]]
    words_to_find: dict[str, list[tuple[int, int]]]
    middle_word: str
    player_name: str | None
    selected_wizard: WizardData


def update_display(
    game_config: GameConfig,
    game_st: GameStateData,
) -> None:
    """Update the entire game display for the current turn.

    Args:
        game_config (GameConfig): The current game configuration.
        game_st (GameStateData): The current game state.

    """
    clear_screen()

    print_grid(
        game_config.difficulty_conf,
        game_st.hidden_grid,
        highlighted_coords=game_st.last_guess_coords,
        highlight_color=game_constants.DEFAULT_HIGHLIGHT_COLOR,
        letters_color=game_constants.DEFAULT_LETTERS_COLOR,
        border_style=game_st.next_message_color,
        hidden_color=game_st.next_message_color,
    )
    print_statistics(
        game_config.difficulty_conf,
        game_st.statistics,
        game_st.next_message_color,
        game_st.hidden_grid,
        game_config.selected_wizard,
        game_st,
    )
    print_message(
        game_config.difficulty_conf,
        game_st.next_message,
        border_style=game_st.next_message_color,
    )


def get_guess(
    game_config: GameConfig,
    game_st: GameStateData,
) -> str:
    """Prompt the player for input and validate it as a guess or powerup command.

    Args:
        game_config (GameConfig): The current game configuration.
        game_st (GameStateData): The current game state.

    Returns:
        str: The validated guess or powerup command.

    """
    wizard_color = game_config.selected_wizard.color
    power_points = game_st.statistics.power_points

    while True:
        prompt = "  > Enter guess: "
        if game_config.difficulty_conf.heart_point_mode and wizard_color != "bright_white":
            prompt = "  > Enter guess (Type `!p` to activate powerup!): "

        user_input = get_input(game_config.difficulty_conf, prompt)
        guess = user_input.lower().strip()

        if not guess:
            game_st.next_message = game_constants.INVALID_GUESS_EMPTY_MSG
            game_st.next_message_color = game_constants.ERROR_COLOR
            update_display(game_config, game_st)
        elif game_config.difficulty_conf.heart_point_mode and guess == game_constants.POWERUP_COMMAND:
            if wizard_color == "bright_white":
                game_st.next_message = game_constants.NO_POWERUP_MSG
                game_st.next_message_color = game_constants.ERROR_COLOR
                update_display(game_config, game_st)
            elif power_points <= 0:
                game_st.next_message = game_constants.INSUFFICIENT_POWER_MSG
                game_st.next_message_color = game_constants.ERROR_COLOR
                update_display(game_config, game_st)
            else:
                return guess
        elif not guess.isalpha():
            game_st.next_message = game_constants.INVALID_GUESS_ALPHA_MSG
            game_st.next_message_color = game_constants.ERROR_COLOR
            update_display(game_config, game_st)
        else:
            game_st.next_message_color = wizard_color
            return guess


def update_game_over_display(
    game_config: GameConfig,
    game_over_status: str,
    game_st: GameStateData,
) -> None:
    """Update the display to show the final game state after game over.

    Args:
        game_config (GameConfig): The current game configuration.
        game_over_status (str): The status of the game ("win" or "loss").
        game_st (GameStateData): The current game state.

    """
    clear_screen()
    stats = game_st.statistics
    wizard_color = game_config.selected_wizard.color
    final_message = game_constants.WIN_MSG if game_over_status == "win" else game_constants.LOSE_MSG
    letters_display_color = game_constants.WIN_COLOR if game_over_status == "win" else game_constants.LOSE_COLOR
    grid_to_show = game_config.final_grid
    highlight_coords_on_loss = game_st.found_letter_coords if game_over_status == "loss" else []
    print_grid(
        game_config.difficulty_conf,
        grid_to_show,
        highlighted_coords=highlight_coords_on_loss,
        highlight_color=game_constants.DEFAULT_HIGHLIGHT_COLOR,
        letters_color=letters_display_color,
        border_style=wizard_color,
        hidden_color=wizard_color,
    )
    print_statistics(
        game_config.difficulty_conf,
        stats,
        wizard_color,
        game_config.final_grid,
        game_config.selected_wizard,
        game_st,
    )
    print_message(game_config.difficulty_conf, final_message, border_style=wizard_color)


def end_game(
    game_config: GameConfig,
    final_score: int,
) -> None:
    """Handle display and interaction after a game ends, show leaderboards.

    Args:
        game_config (GameConfig): The current game configuration.
        final_score (int): The final score achieved in the game.

    """
    get_input(game_config.difficulty_conf, "  > Game Over. Press Enter to see summary and leaderboards... ")
    clear_screen()

    print_message(
        game_config.difficulty_conf,
        game_constants.THANKS_MSG.format(game_config.player_name, final_score),
        border_style=game_constants.FINAL_SCORE_BORDER,
    )

    print_message(game_config.difficulty_conf, "Winning Streaks Leaderboard:", border_style="cyan")
    streaks = load_streaks()
    print_streak_leaderboard(game_config.difficulty_conf, streaks)

    # Conditional prompt based on game mode
    if game_config.difficulty_conf.heart_point_mode:
        get_input(game_config.difficulty_conf, "  > Press Enter to return to the main menu... ")
    else:  # No Heart Points Mode
        get_input(game_config.difficulty_conf, "  > Press Enter for the next puzzle... ")


def run_game(
    game_config: GameConfig,
) -> tuple[str, int]:
    """Run the main game loop for a single game session.

    Args:
        game_config (GameConfig): The current game configuration.

    Returns:
        tuple[str, int]: A tuple containing the game over status ("win" or "loss")
            and the final score for this game.

    """
    wizard_color = game_config.selected_wizard.color
    game_st: GameStateData = initialize_game_state(
        game_config.final_grid,
        game_config.middle_word,
        game_config.selected_wizard,
        game_config.player_name,
    )
    game_over_status: str = "continue"

    while game_over_status == "continue":
        update_display(game_config, game_st)
        print(game_config.words_to_find.keys())
        guess = get_guess(game_config, game_st)

        if guess == game_constants.POWERUP_COMMAND:
            use_powerup(game_st, game_config.selected_wizard, game_config.words_to_find, game_config.final_grid)
        else:
            process_guess(guess, game_st, game_config.words_to_find, game_config.final_grid, wizard_color)
            update_power_points(game_st, game_config.selected_wizard)

        game_over_status = check_game_over(game_st, game_config.words_to_find)

    update_game_over_display(
        game_config,
        game_over_status,
        game_st,
    )
    final_score_this_game: int = game_st.statistics.points

    end_game(game_config, final_score_this_game)

    return game_over_status, final_score_this_game
