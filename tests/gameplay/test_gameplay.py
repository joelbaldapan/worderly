import copy
from unittest.mock import MagicMock, patch

import pytest

from gameplay import game_constants, gameplay
from gameplay.game_state_handler import GameStateData, GameStatisticsData

# ************************************************
# Fixtures
# ************************************************


@pytest.fixture
def sample_settings() -> object:
    """Create sample settings.

    Returns:
        object: Dummy settings object with heart_point_mode True.

    """

    class DummySettings:
        heart_point_mode = True

    return DummySettings()


@pytest.fixture
def sample_settings_no_hp() -> object:
    """Create sample settings with heart_point_mode set to False.

    Returns:
        object: Dummy settings object with heart_point_mode False.

    """

    class DummySettings:
        heart_point_mode = False

    return DummySettings()


@pytest.fixture
def sample_wizard() -> object:
    """Create sample wizard data.

    Returns:
        object: Dummy wizard object.

    """

    class DummyWizard:
        name = "Mock Wizard"
        color = "cyan"
        starting_lives = 3
        combo_requirement = 3
        small_art = "artplaceholdere"

    return DummyWizard()


@pytest.fixture
def sample_game_state(sample_wizard: object) -> GameStateData:
    """Create a basic game state object.

    Args:
        sample_wizard (object): The wizard object.

    Returns:
        GameStateData: The sample game state.

    """
    stats = GameStatisticsData(
        letters="A B C",
        lives_left=3,
        points=0,
        last_guess=None,
        combo=0,
        power_points=1,
        shield_turns=0,
    )
    return GameStateData(
        player_name="Tester",
        statistics=stats,
        hidden_grid=[["#"]],
        last_guess_coords=[],
        correctly_guessed_words=set(),
        hidden_letter_coords={(0, 0)},
        found_letter_coords=set(),
        next_message="Welcome",
        next_message_color=sample_wizard.color,
    )


@pytest.fixture
def sample_final_grid() -> list[list[str]]:
    """Create a sample minimal final grid.

    Returns:
        list[list[str]]: A 1x1 grid with "A".

    """
    return [["A"]]


@pytest.fixture
def sample_words_to_find() -> dict[str, list[tuple[int, int]]]:
    """Create a sample minimal words_to_find.

    Returns:
        dict[str, list[tuple[int, int]]]: Mapping of word to coordinates.

    """
    return {"A": [(0, 0)]}


# ************************************************
# Helper for GameConfig
# ************************************************


class DummyGameConfig:
    def __init__(  # noqa: ANN204, PLR0913, PLR0917
        self,
        difficulty_conf: object,
        selected_wizard: object,
        final_grid: list[list[str]] | None = None,
        words_to_find: dict[str, list[tuple[int, int]]] | None = None,
        middle_word: str | None = None,
        player_name: str | None = None,
    ):
        """Initialize DummyGameConfig.

        Args:
            difficulty_conf (object): The difficulty configuration.
            selected_wizard (object): The selected wizard.
            final_grid (Optional[list[list[str]]], optional): The final grid.
            words_to_find (Optional[dict[str, list[tuple[int, int]]]], optional): Words to find.
            middle_word (Optional[str], optional): The middle word.
            player_name (Optional[str], optional): The player name.

        """
        self.difficulty_conf = difficulty_conf
        self.selected_wizard = selected_wizard
        self.final_grid = final_grid
        self.words_to_find = words_to_find
        self.middle_word = middle_word
        self.player_name = player_name


# ************************************************
# Paths For Convenience
# ************************************************


PATCH_PRINT_GRID = "gameplay.gameplay.print_grid"
PATCH_PRINT_STATS = "gameplay.gameplay.print_statistics"
PATCH_PRINT_MSG = "gameplay.gameplay.print_message"
PATCH_PRINT_LB = "gameplay.gameplay.print_streak_leaderboard"
PATCH_GET_INPUT = "gameplay.gameplay.get_input"
PATCH_GET_GUESS = "gameplay.gameplay.get_guess"
PATCH_CLEAR_SCREEN = "gameplay.gameplay.clear_screen"
PATCH_INIT_STATE = "gameplay.gameplay.initialize_game_state"
PATCH_PROC_GUESS = "gameplay.gameplay.process_guess"
PATCH_CHECK_GO = "gameplay.gameplay.check_game_over"
PATCH_UPDATE_PP = "gameplay.gameplay.update_power_points"
PATCH_USE_PU = "gameplay.gameplay.use_powerup"
PATCH_LOAD_LB = "gameplay.gameplay.load_streaks"
PATCH_UPDATE_DISPLAY = "gameplay.gameplay.update_display"
PATCH_UPDATE_GO_DISPLAY = "gameplay.gameplay.update_game_over_display"
PATCH_UPDATE_END_DISPLAY = "gameplay.gameplay.end_game"

# ************************************************
# Tests for: Update Displays
# ************************************************


@patch(PATCH_CLEAR_SCREEN)
@patch(PATCH_PRINT_GRID)
@patch(PATCH_PRINT_STATS)
@patch(PATCH_PRINT_MSG)
def test_update_display(  # noqa: PLR0913, PLR0917
    mock_print_msg: MagicMock,
    mock_print_stats: MagicMock,
    mock_print_grid: MagicMock,
    mock_clear: MagicMock,
    sample_settings: object,
    sample_game_state: GameStateData,
    sample_wizard: object,
) -> None:
    """Test that update_display calls all the necessary display functions."""
    game_config = DummyGameConfig(
        difficulty_conf=sample_settings,
        selected_wizard=sample_wizard,
        final_grid=[["A"]],
    )
    gameplay.update_display(game_config, sample_game_state)
    mock_clear.assert_called_once()
    mock_print_grid.assert_called_once()
    mock_print_stats.assert_called_once()
    mock_print_msg.assert_called_once()


@patch(PATCH_GET_INPUT)
@patch(PATCH_CLEAR_SCREEN)
@patch(PATCH_LOAD_LB)
@patch(PATCH_PRINT_LB)
@patch(PATCH_PRINT_MSG)
def test_update_end_game_display(  # noqa: PLR0913, PLR0917
    mock_print_msg: MagicMock,
    mock_print_lb: MagicMock,
    mock_load_lb: MagicMock,
    mock_clear: MagicMock,
    mock_get_input: MagicMock,
    sample_settings: object,
) -> None:
    """Test the sequence of actions in the end game display."""
    game_config = DummyGameConfig(
        difficulty_conf=sample_settings,
        selected_wizard=None,
        final_grid=[["A"]],
        player_name="WINNAHHH",
    )
    final_score = 100
    mock_leaderboard_data = [{"name": "WINNAHHH", "score": 100}]
    mock_load_lb.return_value = mock_leaderboard_data

    gameplay.end_game(game_config, final_score)

    mock_clear.assert_called_once()
    mock_load_lb.assert_called_once()
    mock_print_lb.assert_called_once_with(sample_settings, mock_leaderboard_data)


# ************************************************
# Tests for: Getting Guesses
# ************************************************


@patch(PATCH_GET_INPUT)
@patch(PATCH_UPDATE_DISPLAY)
def test_get_guess_valid_word(
    mock_update_disp: MagicMock,
    mock_get_input: MagicMock,
    sample_settings: object,
    sample_game_state: GameStateData,
    sample_wizard: object,
) -> None:
    """Test get_guess returns a valid word input."""
    mock_get_input.return_value = "  VALID  "
    expected_guess = "valid"
    game_config = DummyGameConfig(
        difficulty_conf=sample_settings,
        selected_wizard=sample_wizard,
    )
    guess = gameplay.get_guess(game_config, sample_game_state)
    assert guess == expected_guess
    mock_get_input.assert_called_once()
    mock_update_disp.assert_not_called()


@patch(PATCH_GET_INPUT)
@patch(PATCH_UPDATE_DISPLAY)
def test_get_guess_invalid_then_valid(
    mock_update_disp: MagicMock,
    mock_get_input: MagicMock,
    sample_settings: object,
    sample_game_state: GameStateData,
    sample_wizard: object,
) -> None:
    """Test get_guess handles invalid input then accepts valid input."""
    mock_get_input.side_effect = ["", "123", "GOOD"]
    expected_guess = "good"
    game_config = DummyGameConfig(
        difficulty_conf=sample_settings,
        selected_wizard=sample_wizard,
    )
    guess = gameplay.get_guess(game_config, sample_game_state)
    assert guess == expected_guess


@patch(PATCH_GET_INPUT)
@patch(PATCH_UPDATE_DISPLAY)
def test_get_guess_powerup_command_valid(
    mock_update_disp: MagicMock,
    mock_get_input: MagicMock,
    sample_settings: object,
    sample_game_state: GameStateData,
    sample_wizard: object,
) -> None:
    """Test get_guess returns the powerup command when valid."""
    wizard = sample_wizard
    wizard.color = "red"
    state = copy.deepcopy(sample_game_state)
    state.statistics.power_points = 1
    game_config = DummyGameConfig(
        difficulty_conf=sample_settings,
        selected_wizard=wizard,
    )
    mock_get_input.return_value = game_constants.POWERUP_COMMAND
    guess = gameplay.get_guess(game_config, state)
    assert guess == game_constants.POWERUP_COMMAND
    mock_get_input.assert_called_once()
    mock_update_disp.assert_not_called()


@patch(PATCH_GET_INPUT)
@patch(PATCH_UPDATE_DISPLAY)
def test_get_guess_powerup_command_invalid_wizard(
    mock_update_disp: MagicMock,
    mock_get_input: MagicMock,
    sample_settings: object,
    sample_game_state: GameStateData,
    sample_wizard: object,
) -> None:
    """Test get_guess handles powerup attempt with white wizard."""
    wizard_white = sample_wizard
    wizard_white.color = "bright_white"
    state = copy.deepcopy(sample_game_state)
    state.statistics.power_points = 1
    game_config = DummyGameConfig(
        difficulty_conf=sample_settings,
        selected_wizard=wizard_white,
    )
    mock_get_input.side_effect = [
        game_constants.POWERUP_COMMAND,
        "valid",
    ]
    guess = gameplay.get_guess(game_config, state)
    assert guess == "valid"
    assert mock_update_disp.call_count == 1


@patch(PATCH_GET_INPUT)
@patch(PATCH_UPDATE_DISPLAY)
def test_get_guess_powerup_command_invalid_points(
    mock_update_disp: MagicMock,
    mock_get_input: MagicMock,
    sample_settings: object,
    sample_game_state: GameStateData,
    sample_wizard: object,
) -> None:
    """Test get_guess handles powerup attempt with insufficient points."""
    wizard_red = sample_wizard
    wizard_red.color = "red"
    state = copy.deepcopy(sample_game_state)
    state.statistics.power_points = 0
    game_config = DummyGameConfig(
        difficulty_conf=sample_settings,
        selected_wizard=wizard_red,
    )
    mock_get_input.side_effect = [
        game_constants.POWERUP_COMMAND,
        "valid",
    ]
    guess = gameplay.get_guess(game_config, state)
    assert guess == "valid"
    assert mock_update_disp.call_count == 1


# ************************************************
# Tests for: Running Game
# We will see if the flow is accurate
# ************************************************


@patch(PATCH_INIT_STATE)
@patch(PATCH_UPDATE_DISPLAY)
@patch(PATCH_GET_GUESS)
@patch(PATCH_PROC_GUESS)
@patch(PATCH_UPDATE_PP)
@patch(PATCH_USE_PU)
@patch(PATCH_CHECK_GO)
@patch(PATCH_UPDATE_GO_DISPLAY)
@patch(PATCH_UPDATE_END_DISPLAY)
def test_run_game_win_hp_mode(  # noqa: PLR0913, PLR0917
    mock_end_disp: MagicMock,
    mock_go_disp: MagicMock,
    mock_check_go: MagicMock,
    mock_use_pu: MagicMock,
    mock_update_pp: MagicMock,
    mock_proc_guess: MagicMock,
    mock_get_guess_func: MagicMock,
    mock_update_disp: MagicMock,
    mock_init_state: MagicMock,
    sample_settings: object,
    sample_final_grid: list[list[str]],
    sample_words_to_find: dict[str, list[tuple[int, int]]],
    sample_wizard: object,
) -> None:
    """Test a winning game flow in Heart Point mode."""
    player_name = "Player1"
    middle_word = "MIDDLE"
    game_config = DummyGameConfig(
        difficulty_conf=sample_settings,
        selected_wizard=sample_wizard,
        final_grid=sample_final_grid,
        words_to_find=sample_words_to_find,
        middle_word=middle_word,
        player_name=player_name,
    )

    class DummyStats:
        def __init__(self) -> None:
            """Initialize DummyStats."""
            self.points = 50

    class DummyGameState:
        def __init__(self) -> None:
            """Initialize DummyGameState."""
            self.statistics = DummyStats()
            self.player_name = player_name

    mock_init_state.return_value = DummyGameState()
    mock_get_guess_func.return_value = "goodguess"
    mock_check_go.side_effect = [
        "continue",
        "win",
    ]
    gameplay.run_game(game_config)
    mock_init_state.assert_called_once_with(
        sample_final_grid,
        middle_word,
        sample_wizard,
        player_name,
    )
    mock_update_disp.assert_called()
    mock_get_guess_func.assert_called()
    mock_proc_guess.assert_called()
    mock_update_pp.assert_called()
    mock_use_pu.assert_not_called()
    mock_go_disp.assert_called_once()
    mock_end_disp.assert_called_once()


@patch(PATCH_INIT_STATE)
@patch(PATCH_UPDATE_DISPLAY)
@patch(PATCH_GET_GUESS)
@patch(PATCH_PROC_GUESS)
@patch(PATCH_UPDATE_PP)
@patch(PATCH_USE_PU)
@patch(PATCH_CHECK_GO)
@patch(PATCH_UPDATE_GO_DISPLAY)
@patch(PATCH_UPDATE_END_DISPLAY)
def test_run_game_loss_no_hp_mode(  # noqa: PLR0913, PLR0917
    mock_end_disp: MagicMock,
    mock_go_disp: MagicMock,
    mock_check_go: MagicMock,
    mock_use_pu: MagicMock,
    mock_update_pp: MagicMock,
    mock_proc_guess: MagicMock,
    mock_get_guess_func: MagicMock,
    mock_update_disp: MagicMock,
    mock_init_state: MagicMock,
    sample_settings_no_hp: object,
    sample_final_grid: list[list[str]],
    sample_words_to_find: dict[str, list[tuple[int, int]]],
    sample_wizard: object,
) -> None:
    """Test a losing game flow NOT in Heart Point mode."""
    player_name = None
    middle_word = "MIDDLE"
    game_config = DummyGameConfig(
        difficulty_conf=sample_settings_no_hp,
        selected_wizard=sample_wizard,
        final_grid=sample_final_grid,
        words_to_find=sample_words_to_find,
        middle_word=middle_word,
        player_name=player_name,
    )

    class DummyStats:
        def __init__(self) -> None:
            """Initialize DummyStats."""
            self.points = 10

    class DummyGameState:
        def __init__(self) -> None:
            """Initialize DummyGameState."""
            self.statistics = DummyStats()
            self.player_name = player_name

    mock_init_state.return_value = DummyGameState()
    mock_get_guess_func.return_value = "badguess"
    mock_check_go.side_effect = ["continue", "loss"]

    gameplay.run_game(game_config)
    mock_init_state.assert_called_once_with(
        sample_final_grid,
        middle_word,
        sample_wizard,
        player_name,
    )
    mock_update_disp.assert_called()
    mock_get_guess_func.assert_called()
    mock_proc_guess.assert_called()
    mock_update_pp.assert_called()
    mock_use_pu.assert_not_called()
    mock_go_disp.assert_called_once()


@patch(PATCH_INIT_STATE)
@patch(PATCH_UPDATE_DISPLAY)
@patch("gameplay.gameplay.get_guess")
@patch(PATCH_PROC_GUESS)
@patch(PATCH_UPDATE_PP)
@patch(PATCH_USE_PU)
@patch(PATCH_CHECK_GO)
@patch(PATCH_UPDATE_GO_DISPLAY)
@patch(PATCH_UPDATE_END_DISPLAY)
def test_run_game_uses_powerup(  # noqa: PLR0913, PLR0917
    mock_end_disp: MagicMock,
    mock_go_disp: MagicMock,
    mock_check_go: MagicMock,
    mock_use_pu: MagicMock,
    mock_update_pp: MagicMock,
    mock_proc_guess: MagicMock,
    mock_get_guess_func: MagicMock,
    mock_update_disp: MagicMock,
    mock_init_state: MagicMock,
    sample_settings: object,
    sample_final_grid: list[list[str]],
    sample_words_to_find: dict[str, list[tuple[int, int]]],
    sample_wizard: object,
) -> None:
    """Test game flow when a powerup is used."""
    player_name = "PlayerPU"
    middle_word = "MIDDLE"
    game_config = DummyGameConfig(
        difficulty_conf=sample_settings,
        selected_wizard=sample_wizard,
        final_grid=sample_final_grid,
        words_to_find=sample_words_to_find,
        middle_word=middle_word,
        player_name=player_name,
    )

    class DummyStats:
        def __init__(self) -> None:
            """Initialize DummyStats."""
            self.points = 0

    class DummyGameState:
        def __init__(self) -> None:
            """Initialize DummyGameState."""
            self.statistics = DummyStats()
            self.player_name = player_name

    mock_init_state.return_value = DummyGameState()
    mock_get_guess_func.return_value = game_constants.POWERUP_COMMAND
    mock_check_go.side_effect = ["continue", "win"]
    gameplay.run_game(game_config)
    mock_init_state.assert_called_once()
    mock_update_disp.assert_called()
    mock_get_guess_func.assert_called()
    mock_use_pu.assert_called()
    mock_proc_guess.assert_not_called()
    mock_update_pp.assert_not_called()
    mock_go_disp.assert_called_once()
    mock_end_disp.assert_called_once()
