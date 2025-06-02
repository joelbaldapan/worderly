from unittest.mock import patch

import pytest

from gameplay import game_constants, game_state_handler


@pytest.fixture
def sample_final_grid() -> list[list[str | None]]:
    """Create a simple 3x5 final grid for testing.

    Returns:
        list[list[str | None]]: The sample grid.

    """
    grid = [[None] * 5 for _ in range(3)]
    grid[0][1] = "H"
    grid[0][2] = "I"
    grid[1][1] = "A"
    grid[2][1] = "T"
    return grid


@pytest.fixture
def sample_words_to_find() -> dict[str, list[tuple[int, int]]]:
    """Create a sample words_to_find dictionary matching the grid.

    Returns:
        dict[str, list[tuple[int, int]]]: The sample words-to-coords mapping.

    """
    return {
        "HI": [(0, 1), (0, 2)],
        "HAT": [(0, 1), (1, 1), (2, 1)],
        "AT": [(1, 1), (2, 1)],
    }


@pytest.fixture
def sample_wizard_data() -> object:
    """Create sample wizard data.

    Returns:
        object: Dummy wizard data.

    """

    class DummyWizard:
        def __init__(self) -> None:
            self.name = "JOEL THE GOD OF CODE"
            self.starting_lives = 3
            self.color = "blue"

    return DummyWizard()


@pytest.fixture
def sample_initial_game_state(
    sample_final_grid: list[list[str | None]],
    sample_wizard_data: object,
) -> object:
    """Create a basic initial game state for modification in tests.

    Returns:
        object: Dummy game state.

    """
    all_coords = game_state_handler.get_all_letter_coords(sample_final_grid)

    class DummyStats:
        def __init__(self) -> None:
            self.letters = "A H I T"
            self.lives_left = sample_wizard_data.starting_lives
            self.points = 0
            self.last_guess = None
            self.combo = 0
            self.power_points = 0
            self.shield_turns = 0

    class DummyGameState:
        def __init__(self) -> None:
            self.player_name = "Tester"
            self.statistics = DummyStats()
            self.hidden_grid = game_state_handler.create_hidden_grid(sample_final_grid)
            self.last_guess_coords = []
            self.correctly_guessed_words = set()
            self.hidden_letter_coords = set(all_coords)
            self.found_letter_coords = set()
            self.next_message = game_constants.WELCOME_MSG
            self.next_message_color = sample_wizard_data.color

    return DummyGameState()


@patch("random.shuffle")
def test_shuffle_letters_statistic(
    mock_shuffle: object,
) -> None:
    """Test shuffling letters of the middle word.

    Check that shuffle is called and output is as expected.

    """
    middle_word = "WORD"

    def mock_shuffle_side_effect(letters: list[str]) -> list[str]:
        return letters

    mock_shuffle.side_effect = mock_shuffle_side_effect

    result = game_state_handler.shuffle_letters_statistic(middle_word)

    mock_shuffle.assert_called_once_with(["W", "O", "R", "D"])
    assert result == "W O R D"


def test_create_hidden_grid(
    sample_final_grid: list[list[str | None]],
) -> None:
    """Test creating the hidden grid to be displayed to the player.

    Assert that the hidden grid matches expected structure and values.

    """
    hidden = game_state_handler.create_hidden_grid(sample_final_grid)
    assert len(hidden) == len(sample_final_grid)
    assert len(hidden[0]) == len(sample_final_grid[0])
    assert hidden[0][0] is None
    assert hidden[0][1] == "#"
    assert hidden[0][2] == "#"
    assert hidden[0][3] is None
    assert hidden[1][1] == "#"
    assert hidden[2][1] == "#"
    assert hidden[1][2] is None


def test_reveal_coords_in_hidden_grid(
    sample_final_grid: list[list[str | None]],
) -> None:
    """Test revealing specific coordinates in the hidden grid.

    Assert that only specified coordinates are revealed.

    """
    hidden = game_state_handler.create_hidden_grid(sample_final_grid)
    coords_to_reveal: list[tuple[int, int]] = [(0, 1), (2, 1)]
    game_state_handler.reveal_coords_in_hidden_grid(
        sample_final_grid,
        hidden,
        coords_to_reveal,
    )

    assert hidden[0][1] == "H"
    assert hidden[2][1] == "T"
    assert hidden[0][2] == "#"
    assert hidden[1][1] == "#"

    coords_to_reveal2: list[tuple[int, int]] = [(1, 2)]
    game_state_handler.reveal_coords_in_hidden_grid(
        sample_final_grid,
        hidden,
        coords_to_reveal2,
    )
    assert hidden[1][2] is None


def test_get_all_letter_coords(
    sample_final_grid: list[list[str | None]],
) -> None:
    """Test getting the set of all non-None coordinates.

    Assert that all letter coordinates are found.

    """
    expected_coords = {(0, 1), (0, 2), (1, 1), (2, 1)}
    actual_coords = game_state_handler.get_all_letter_coords(sample_final_grid)
    assert actual_coords == expected_coords


@patch("gameplay.game_state_handler.reveal_coords_in_hidden_grid")
def test_apply_coordinate_reveal(
    mock_reveal: object,
    sample_final_grid: list[list[str | None]],
    sample_initial_game_state: object,
) -> None:
    """Test applying coordinate reveals and updating game state.

    Assert that points and tracking sets are updated correctly.

    """
    game_state = sample_initial_game_state

    coords_to_reveal: list[tuple[int, int]] = [(0, 1), (1, 1)]
    initial_hidden_coords = set(game_state.hidden_letter_coords)
    initial_points = game_state.statistics.points

    game_state_handler.apply_coordinate_reveal(
        game_state,
        sample_final_grid,
        coords_to_reveal,
    )

    mock_reveal.assert_called_once_with(
        sample_final_grid,
        game_state.hidden_grid,
        set(coords_to_reveal),
    )
    assert game_state.statistics.points == initial_points + 2
    assert game_state.found_letter_coords == set(coords_to_reveal)
    assert game_state.last_guess_coords == list(coords_to_reveal)
    assert game_state.hidden_letter_coords == initial_hidden_coords - set(coords_to_reveal)

    coords_to_reveal_2: list[tuple[int, int]] = [(1, 1), (2, 1)]
    game_state_handler.apply_coordinate_reveal(
        game_state,
        sample_final_grid,
        coords_to_reveal_2,
    )
    assert game_state.statistics.points == initial_points + 2 + 1
    assert game_state.found_letter_coords == {(0, 1), (1, 1), (2, 1)}
    assert game_state.last_guess_coords == list(coords_to_reveal_2)
    assert game_state.hidden_letter_coords == initial_hidden_coords - {
        (0, 1),
        (1, 1),
        (2, 1),
    }


@patch("gameplay.game_state_handler.shuffle_letters_statistic")
@patch("gameplay.game_state_handler.create_hidden_grid")
@patch("gameplay.game_state_handler.get_all_letter_coords")
def test_initialize_game_state(
    mock_get_coords: object,
    mock_create_hidden: object,
    mock_shuffle_letters: object,
    sample_final_grid: list[list[str | None]],
    sample_wizard_data: object,
) -> None:
    """Test the initialization of the main game state dictionary.

    Assert that all fields are initialized as expected.

    """
    middle_word = "TEST"
    player_name = "Hero"

    mock_shuffled = "E S T T"
    mock_hidden_grid = [
        [None, "#", "#", None, None],
        [None, "#", None, None, None],
        [None, "#", None, None, None],
    ]
    mock_all_coords = {(0, 0), (1, 1)}
    mock_shuffle_letters.return_value = mock_shuffled
    mock_create_hidden.return_value = mock_hidden_grid
    mock_get_coords.return_value = mock_all_coords

    game_state = game_state_handler.initialize_game_state(
        sample_final_grid,
        middle_word,
        sample_wizard_data,
        player_name,
    )

    mock_create_hidden.assert_called_once_with(sample_final_grid)
    mock_shuffle_letters.assert_called_once_with(middle_word)
    mock_get_coords.assert_called_once_with(sample_final_grid)

    assert game_state.player_name == player_name
    assert game_state.hidden_grid == mock_hidden_grid
    assert game_state.last_guess_coords == []
    assert game_state.correctly_guessed_words == set()
    assert game_state.hidden_letter_coords == mock_all_coords
    assert game_state.found_letter_coords == set()
    assert game_state.next_message == game_constants.WELCOME_MSG
    assert game_state.next_message_color == sample_wizard_data.color

    stats = game_state.statistics
    assert stats.letters == mock_shuffled
    assert stats.lives_left == sample_wizard_data.starting_lives
    assert stats.points == 0
    assert stats.last_guess is None
    assert stats.combo == 0
    assert stats.power_points == 0
    assert stats.shield_turns == 0


@patch("gameplay.game_state_handler.apply_coordinate_reveal")
@patch("gameplay.game_state_handler.check_for_completed_words")
def test_process_guess_correct_no_shield(
    mock_check_completed: object,
    mock_apply_reveal: object,
    sample_initial_game_state: object,
    sample_words_to_find: dict[str, list[tuple[int, int]]],
    sample_final_grid: list[list[str | None]],
) -> None:
    """Test processing a correct guess when shield is off.

    Assert that stats and state are updated for a correct guess.

    """
    game_state = sample_initial_game_state
    guess = "HI"
    wizard_color = game_state.next_message_color
    initial_lives = game_state.statistics.lives_left
    initial_combo = game_state.statistics.combo
    coords_for_hi = sample_words_to_find[guess]
    mock_check_completed.return_value = []

    game_state_handler.process_guess(
        guess,
        game_state,
        sample_words_to_find,
        sample_final_grid,
        wizard_color,
    )

    stats = game_state.statistics
    assert stats.last_guess == guess
    assert game_state.correctly_guessed_words == {guess}
    assert stats.combo == initial_combo + 1
    assert stats.lives_left == initial_lives
    assert game_state.next_message == game_constants.CORRECT_GUESS_MSG.format(guess)
    assert game_state.next_message_color == wizard_color

    mock_apply_reveal.assert_called_once_with(
        game_state,
        sample_final_grid,
        coords_for_hi,
    )
    mock_check_completed.assert_called_once_with(game_state, sample_words_to_find)


@patch("gameplay.game_state_handler.apply_coordinate_reveal")
@patch("gameplay.game_state_handler.check_for_completed_words")
def test_process_guess_correct_implicit_completion(
    mock_check_completed: object,
    mock_apply_reveal: object,
    sample_initial_game_state: object,
    sample_words_to_find: dict[str, list[tuple[int, int]]],
    sample_final_grid: list[list[str | None]],
) -> None:
    """Test correct guess that implicitly completes another word.

    Assert that both guessed and implicitly completed words are added.

    """
    game_state = sample_initial_game_state
    guess = "HAT"
    wizard_color = game_state.next_message_color
    coords_for_hat = sample_words_to_find[guess]
    mock_check_completed.return_value = ["AT"]

    game_state_handler.process_guess(
        guess,
        game_state,
        sample_words_to_find,
        sample_final_grid,
        wizard_color,
    )

    stats = game_state.statistics
    assert game_state.correctly_guessed_words == {"HAT", "AT"}
    assert stats.combo == 1
    assert game_constants.CORRECT_GUESS_MSG.format(guess) in game_state.next_message
    assert "Also completed: AT" in game_state.next_message

    mock_apply_reveal.assert_called_once_with(
        game_state,
        sample_final_grid,
        coords_for_hat,
    )
    mock_check_completed.assert_called_once_with(game_state, sample_words_to_find)


@patch("gameplay.game_state_handler.apply_coordinate_reveal")
@patch("gameplay.game_state_handler.check_for_completed_words")
def test_process_guess_wrong_no_shield(
    mock_check_completed: object,
    mock_apply_reveal: object,
    sample_initial_game_state: object,
    sample_words_to_find: dict[str, list[tuple[int, int]]],
    sample_final_grid: list[list[str | None]],
) -> None:
    """Test processing a wrong guess when shield is off.

    Assert that lives are decremented and no words are added.

    """
    game_state = sample_initial_game_state
    guess = "WRONG"
    wizard_color = game_state.next_message_color
    initial_lives = game_state.statistics.lives_left

    game_state_handler.process_guess(
        guess,
        game_state,
        sample_words_to_find,
        sample_final_grid,
        wizard_color,
    )

    stats = game_state.statistics
    assert stats.last_guess == guess
    assert game_state.correctly_guessed_words == set()
    assert stats.combo == 0
    assert stats.lives_left == initial_lives - 1
    assert game_state.next_message == game_constants.NOT_A_WORD_MSG.format(guess)
    assert game_state.next_message_color == game_constants.ERROR_COLOR

    mock_apply_reveal.assert_not_called()
    mock_check_completed.assert_not_called()


@patch("gameplay.game_state_handler.apply_coordinate_reveal")
@patch("gameplay.game_state_handler.check_for_completed_words")
def test_process_guess_duplicate_no_shield(
    mock_check_completed: object,
    mock_apply_reveal: object,
    sample_initial_game_state: object,
    sample_words_to_find: dict[str, list[tuple[int, int]]],
    sample_final_grid: list[list[str | None]],
) -> None:
    """Test processing a duplicate guess when shield is off.

    Assert that lives are decremented and duplicate word is not added.

    """
    game_state = sample_initial_game_state
    guess = "HI"
    game_state.correctly_guessed_words.add(guess)
    wizard_color = game_state.next_message_color
    initial_lives = game_state.statistics.lives_left

    game_state_handler.process_guess(
        guess,
        game_state,
        sample_words_to_find,
        sample_final_grid,
        wizard_color,
    )

    stats = game_state.statistics
    assert stats.last_guess == guess
    assert game_state.correctly_guessed_words == {guess}
    assert stats.combo == 0
    assert stats.lives_left == initial_lives - 1
    assert game_state.next_message == game_constants.ALREADY_FOUND_MSG.format(guess)
    assert game_state.next_message_color == game_constants.ERROR_COLOR

    mock_apply_reveal.assert_not_called()
    mock_check_completed.assert_not_called()


@patch("gameplay.game_state_handler.apply_coordinate_reveal")
@patch("gameplay.game_state_handler.check_for_completed_words")
def test_process_guess_wrong_with_shield(
    mock_check_completed: object,
    mock_apply_reveal: object,
    sample_initial_game_state: object,
    sample_words_to_find: dict[str, list[tuple[int, int]]],
    sample_final_grid: list[list[str | None]],
) -> None:
    """Test processing a wrong guess when shield is active.

    Assert that lives are not decremented and shield turns decrease.

    """
    game_state = sample_initial_game_state
    game_state.statistics.shield_turns = 2
    guess = "WRONG"
    wizard_color = game_state.next_message_color
    initial_lives = game_state.statistics.lives_left

    game_state_handler.process_guess(
        guess,
        game_state,
        sample_words_to_find,
        sample_final_grid,
        wizard_color,
    )

    stats = game_state.statistics
    assert stats.lives_left == initial_lives
    assert stats.shield_turns == 1
    assert stats.combo == 0
    assert game_state.next_message == game_constants.NOT_A_WORD_MSG.format(guess)

    mock_apply_reveal.assert_not_called()
    mock_check_completed.assert_not_called()


@patch("gameplay.game_state_handler.apply_coordinate_reveal")
@patch("gameplay.game_state_handler.check_for_completed_words")
def test_process_guess_correct_with_shield(
    mock_check_completed: object,
    mock_apply_reveal: object,
    sample_initial_game_state: object,
    sample_words_to_find: dict[str, list[tuple[int, int]]],
    sample_final_grid: list[list[str | None]],
) -> None:
    """Test processing a correct guess when shield is active.

    Assert that shield turns decrease and stats update for correct guess.

    """
    game_state = sample_initial_game_state
    game_state.statistics.shield_turns = 1
    guess = "HI"
    wizard_color = game_state.next_message_color
    initial_lives = game_state.statistics.lives_left
    coords_for_hi = sample_words_to_find[guess]
    mock_check_completed.return_value = []

    game_state_handler.process_guess(
        guess,
        game_state,
        sample_words_to_find,
        sample_final_grid,
        wizard_color,
    )

    stats = game_state.statistics
    assert stats.lives_left == initial_lives
    assert stats.shield_turns == 0
    assert stats.combo == 1
    assert game_state.next_message == game_constants.CORRECT_GUESS_MSG.format(guess)

    mock_apply_reveal.assert_called_once_with(
        game_state,
        sample_final_grid,
        coords_for_hi,
    )
    mock_check_completed.assert_called_once_with(game_state, sample_words_to_find)


def test_check_for_completed_words(
    sample_words_to_find: dict[str, list[tuple[int, int]]],
) -> None:
    """Test identifying words completed implicitly by revealed letters.

    Assert that implicitly completed words are detected.

    """

    class DummyGameState:
        pass

    game_state = DummyGameState()
    game_state.correctly_guessed_words = {"HAT"}
    game_state.hidden_letter_coords = {(0, 2)}
    game_state.found_letter_coords = {(0, 1), (1, 1), (2, 1)}
    newly_found = game_state_handler.check_for_completed_words(
        game_state,
        sample_words_to_find,
    )
    assert newly_found == ["AT"]

    game_state_all_revealed = DummyGameState()
    game_state_all_revealed.correctly_guessed_words = set()
    game_state_all_revealed.hidden_letter_coords = set()
    game_state_all_revealed.found_letter_coords = {(0, 1), (0, 2), (1, 1), (2, 1)}
    newly_found_all = game_state_handler.check_for_completed_words(
        game_state_all_revealed,
        sample_words_to_find,
    )
    assert set(newly_found_all) == {"HI", "HAT", "AT"}


def test_check_game_over(
    sample_words_to_find: dict[str, list[tuple[int, int]]],
) -> None:
    """Test the game over condition checks.

    Assert that win, loss, and continue conditions are detected.

    """

    class DummyStats:
        def __init__(self, lives_left: int) -> None:
            self.lives_left = lives_left

    class DummyGameState:
        def __init__(self, guessed: set[str], lives_left: int) -> None:
            self.correctly_guessed_words = guessed
            self.statistics = DummyStats(lives_left)

    game_state_win = DummyGameState({"HI", "HAT", "AT"}, 3)
    assert game_state_handler.check_game_over(game_state_win, sample_words_to_find) == "win"

    game_state_loss_0 = DummyGameState({"HI"}, 0)
    assert game_state_handler.check_game_over(game_state_loss_0, sample_words_to_find) == "loss"

    game_state_loss_neg = DummyGameState({"HI"}, -1)
    assert game_state_handler.check_game_over(game_state_loss_neg, sample_words_to_find) == "loss"

    game_state_continue = DummyGameState({"HI"}, 1)
    assert game_state_handler.check_game_over(game_state_continue, sample_words_to_find) == "continue"
