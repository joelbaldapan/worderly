from dataclasses import dataclass

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


@dataclass
class GameContext:
    difficulty_conf: DifficultyData
    final_grid: list[list[str | None]]
    words_to_find: dict[str, list[tuple[int, int]]]
    middle_word: str
    player_name: str | None
    selected_wizard: WizardData


def update_display(
    ctx: GameContext,
    game_st: GameStateData,
) -> None:
    """Update the entire game display for the current turn."""
    clear_screen()

    print_grid(
        ctx.difficulty_conf,
        game_st.hidden_grid,
        highlighted_coords=game_st.last_guess_coords,
        highlight_color=game_constants.DEFAULT_HIGHLIGHT_COLOR,
        letters_color=game_constants.DEFAULT_LETTERS_COLOR,
        border_style=game_st.next_message_color,
        hidden_color=game_st.next_message_color,
    )
    print_statistics(
        ctx.difficulty_conf,
        game_st.statistics,
        game_st.next_message_color,
        game_st.hidden_grid,
        ctx.selected_wizard,
        game_st,
    )
    print_message(
        ctx.difficulty_conf,
        game_st.next_message,
        border_style=game_st.next_message_color,
    )


def get_guess(
    ctx: GameContext,
    game_st: GameStateData,
) -> str:
    """Prompts player for input, validates it as a guess or powerup command."""
    wizard_color = ctx.selected_wizard.color
    power_points = game_st.statistics.power_points

    while True:
        prompt = "  > Enter guess: "
        if ctx.difficulty_conf.heart_point_mode and wizard_color != "bright_white":
            prompt = "  > Enter guess (Type `!p` to activate powerup!): "

        user_input = get_input(ctx.difficulty_conf, prompt)
        guess = user_input.lower().strip()

        if not guess:
            game_st.next_message = game_constants.INVALID_GUESS_EMPTY_MSG
            game_st.next_message_color = game_constants.ERROR_COLOR
            update_display(ctx, game_st)
        elif ctx.difficulty_conf.heart_point_mode and guess == game_constants.POWERUP_COMMAND:
            if wizard_color == "bright_white":
                game_st.next_message = game_constants.NO_POWERUP_MSG
                game_st.next_message_color = game_constants.ERROR_COLOR
                update_display(ctx, game_st)
            elif power_points <= 0:
                game_st.next_message = game_constants.INSUFFICIENT_POWER_MSG
                game_st.next_message_color = game_constants.ERROR_COLOR
                update_display(ctx, game_st)
            else:
                return guess
        elif not guess.isalpha():
            game_st.next_message = game_constants.INVALID_GUESS_ALPHA_MSG
            game_st.next_message_color = game_constants.ERROR_COLOR
            update_display(ctx, game_st)
        else:
            game_st.next_message_color = wizard_color
            return guess


def update_game_over_display(
    ctx: GameContext,
    game_over_status: str,
    game_st: GameStateData,
) -> None:
    clear_screen()
    stats = game_st.statistics
    wizard_color = ctx.selected_wizard.color
    final_message = game_constants.WIN_MSG if game_over_status == "win" else game_constants.LOSE_MSG
    letters_display_color = game_constants.WIN_COLOR if game_over_status == "win" else game_constants.LOSE_COLOR
    grid_to_show = ctx.final_grid
    highlight_coords_on_loss = game_st.found_letter_coords if game_over_status == "loss" else []
    print_grid(
        ctx.difficulty_conf,
        grid_to_show,
        highlighted_coords=highlight_coords_on_loss,
        highlight_color=game_constants.DEFAULT_HIGHLIGHT_COLOR,
        letters_color=letters_display_color,
        border_style=wizard_color,
        hidden_color=wizard_color,
    )
    print_statistics(
        ctx.difficulty_conf,
        stats,
        wizard_color,
        ctx.final_grid,
        ctx.selected_wizard,
        game_st,
    )
    print_message(ctx.difficulty_conf, final_message, border_style=wizard_color)


def end_game(
    ctx: GameContext,
    final_score: int,
) -> None:
    """Handles display and interaction after a game ends, shows leaderboards,
    and provides a mode-specific prompt to continue.
    """
    get_input(ctx.difficulty_conf, "  > Game Over. Press Enter to see summary and leaderboards... ")
    clear_screen()

    print_message(
        ctx.difficulty_conf,
        game_constants.THANKS_MSG.format(ctx.player_name, final_score),
        border_style=game_constants.FINAL_SCORE_BORDER,
    )

    print_message(ctx.difficulty_conf, "Winning Streaks Leaderboard:", border_style="cyan")
    streaks = load_streaks()
    print_streak_leaderboard(ctx.difficulty_conf, streaks)

    # Conditional prompt based on game mode
    if ctx.difficulty_conf.heart_point_mode:
        get_input(ctx.difficulty_conf, "  > Press Enter to return to the main menu... ")
    else:  # No Heart Points Mode
        get_input(ctx.difficulty_conf, "  > Press Enter for the next puzzle... ")


def run_game(
    ctx: GameContext,
) -> tuple[str, int]:
    wizard_color = ctx.selected_wizard.color
    game_st: GameStateData = initialize_game_state(
        ctx.final_grid,
        ctx.middle_word,
        ctx.selected_wizard,
        ctx.player_name,
    )
    game_over_status: str = "continue"

    while game_over_status == "continue":
        update_display(ctx, game_st)
        print(ctx.words_to_find.keys())
        guess = get_guess(ctx, game_st)

        if guess == game_constants.POWERUP_COMMAND:
            use_powerup(game_st, ctx.selected_wizard, ctx.words_to_find, ctx.final_grid)
        else:
            process_guess(guess, game_st, ctx.words_to_find, ctx.final_grid, wizard_color)
            update_power_points(game_st, ctx.selected_wizard)

        game_over_status = check_game_over(game_st, ctx.words_to_find)

    update_game_over_display(
        ctx,
        game_over_status,
        game_st,
    )
    final_score_this_game: int = game_st.statistics.points

    end_game(ctx, final_score_this_game)

    return game_over_status, final_score_this_game
