import pytest

from gameplay.game_state_handler import GameStateData, GameStatisticsData


@pytest.fixture
def sample_statistics_fixture() -> GameStatisticsData:
    """Create a sample statistics object.

    Returns:
        GameStatisticsData: A sample statistics object.

    """
    return GameStatisticsData(
        letters="A B C",
        lives_left=3,
        points=10,
        last_guess=None,
        combo=0,
        power_points=1,
        shield_turns=0,
    )


@pytest.fixture
def sample_game_state_fixture(
    sample_statistics_fixture: GameStatisticsData,
) -> GameStateData:
    """Create a sample game state object.

    Returns:
        GameStateData: A sample game state object.

    """
    hidden_coords = {(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)}
    found_coords = {(0, 0)}
    return GameStateData(
        player_name="Power Tester",
        statistics=sample_statistics_fixture,
        hidden_grid=[["#"] * 2 for _ in range(3)],
        last_guess_coords=[],
        correctly_guessed_words=set(),
        hidden_letter_coords=hidden_coords - found_coords,
        found_letter_coords=found_coords.copy(),
        next_message="",
        next_message_color="white",
    )


@pytest.fixture(
    params=[
        # Wizard, initial_combo, expected_powerpoint_increment
        ({"combo_requirement": 3, "color": "red"}, 2, 0),  # Combo < req
        ({"combo_requirement": 3, "color": "red"}, 3, 1),  # Combo == req
        ({"combo_requirement": 3, "color": "red"}, 4, 0),  # Combo > req, not multiple
        ({"combo_requirement": 3, "color": "red"}, 6, 1),  # Combo multiple of req
        ({"combo_requirement": None, "color": "white"}, 5, 0),  # No req
        ({"combo_requirement": 4, "color": "green"}, 0, 0),  # Combo is 0
    ],
)
def power_point_update_data(
    request: pytest.FixtureRequest,
) -> tuple[object, int, int]:
    """Provide data for testing update_power_points.

    Returns:
        tuple[object, int, int]: Wizard, initial combo, and expected increment.

    """
    wizard_dict, initial_combo, expected_increment = request.param

    class DummyWizard:
        pass

    dummy = DummyWizard()
    for k, v in wizard_dict.items():
        setattr(dummy, k, v)
    return dummy, initial_combo, expected_increment


@pytest.fixture(
    params=[
        # Wizard Color, Expected Action/Result
        ("red", "word_reveal"),
        ("green", "random_reveal"),
        ("magenta", "shield_increase"),
        ("blue", "life_increase"),
    ],
)
def use_powerup_data(
    request: pytest.FixtureRequest,
) -> tuple[str, str]:
    """Provide data for testing use_powerup based on wizard color.

    Returns:
        tuple[str, str]: Wizard color and expected action/result.

    """
    return request.param


@pytest.fixture
def sample_words_to_find_fixture() -> dict[str, list[tuple[int, int]]]:
    """Provide sample words_to_find for powerup tests.

    Returns:
        dict[str, list[tuple[int, int]]]: Sample words to find.

    """
    return {
        "ONE": [(0, 0), (0, 1)],
        "TWO": [(1, 0), (1, 1)],
        "TEN": [(2, 0), (0, 0), (1, 0)],
    }


@pytest.fixture
def sample_final_grid_fixture() -> list[list[str | None]]:
    """Provide sample final grid for powerup tests.

    Returns:
        list[list[str | None]]: Sample final grid.

    """
    grid = [[None] * 2 for _ in range(3)]
    grid[0][0] = "O"
    grid[0][1] = "N"
    grid[1][0] = "T"
    grid[1][1] = "W"
    grid[2][0] = "E"
    return grid
