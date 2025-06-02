from unittest.mock import patch

import pytest

from gameplay import game_constants, game_state_handler


@pytest.fixture
def sample_final_grid():
    """Creates a simple 3x5 final grid for testing."""
    #  . H I . .
    #  . A . . .
    #  . T . . .
    grid = [[None] * 5 for _ in range(3)]
    grid[0][1] = "H"
    grid[0][2] = "I"
    grid[1][1] = "A"
    grid[2][1] = "T"
    return grid


@pytest.fixture
def sample_words_to_find():
    """Creates a sample words_to_find dictionary matching the grid."""
    return {
        "HI": [(0, 1), (0, 2)],
        "HAT": [(0, 1), (1, 1), (2, 1)],
        "AT": [(1, 1), (2, 1)],
    }
    # Note: AT is implicitly found if HAT is guessed
    # However, this is not possible for normal board creation
    #   (check pytest for grid generating. AT is not allowed!)
    # This is only done for convenience for the unit tests in this file


@pytest.fixture
def sample_wizard_data():
    """Creates sample wizard data."""
    # Other details not needed for this file's testing
    class DummyWizard:
        def __init__(self):
            self.name = "JOEL THE GOD OF CODE"
            self.starting_lives = 3
            self.color = "blue"
    return DummyWizard()


@pytest.fixture
def sample_initial_game_state(sample_final_grid, sample_wizard_data):
    """Creates a basic initial game state for modification in tests."""
    # Note: This manually creates state.
    # For testing initialize_game_state itself, we call the actual function
    all_coords = game_state_handler.get_all_letter_coords(sample_final_grid)

    class DummyStats:
        def __init__(self):
            self.letters = "A H I T"
            self.lives_left = sample_wizard_data.starting_lives
            self.points = 0
            self.last_guess = None
            self.combo = 0
            self.power_points = 0
            self.shield_turns = 0

    class DummyGameState:
        def __init__(self):
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


# ************************************************
# Tests for: Utils
# ************************************************


@patch("random.shuffle")
def test_shuffle_letters_statistic(mock_shuffle):
    """Test shuffling letters of the middle word."""
    middle_word = "WORD"

    # Mock shuffle to do nothing
    def mock_shuffle_side_effect(letters):
        return letters

    mock_shuffle.side_effect = mock_shuffle_side_effect

    result = game_state_handler.shuffle_letters_statistic(middle_word)

    # Check that shuffle was called with the correct list
    # Check if format is correct (which is supposed to be the same)
    mock_shuffle.assert_called_once_with(["W", "O", "R", "D"])
    assert result == "W O R D"


# ************************************************
# Tests for: Grid Related
# ************************************************


def test_create_hidden_grid(sample_final_grid):
    """Test creating the hidden grid to be dispayed to the player."""
    hidden = game_state_handler.create_hidden_grid(sample_final_grid)
    # Expected (where N is None):
    # N # # N N
    # N # N N N
    # N # N N N
    assert len(hidden) == len(sample_final_grid)
    assert len(hidden[0]) == len(sample_final_grid[0])
    assert hidden[0][0] is None
    assert hidden[0][1] == "#"
    assert hidden[0][2] == "#"
    assert hidden[0][3] is None
    assert hidden[1][1] == "#"
    assert hidden[2][1] == "#"
    assert hidden[1][2] is None  # Check an empty spot


def test_reveal_coords_in_hidden_grid(sample_final_grid):
    """Test revealing specific coordinates in the hidden grid."""
    hidden = game_state_handler.create_hidden_grid(sample_final_grid)

    # Grid after revealing:
    #  . H # . .
    #  . # . . .
    #  . T . . .

    # 1.) Revealing Letters
    coords_to_reveal = [(0, 1), (2, 1)]  # Reveal 'H' and 'T'
    game_state_handler.reveal_coords_in_hidden_grid(
        sample_final_grid, hidden, coords_to_reveal,
    )

    assert hidden[0][1] == "H"  # Revealed
    assert hidden[2][1] == "T"  # Revealed
    assert hidden[0][2] == "#"  # Still hidden
    assert hidden[1][1] == "#"  # Still hidden

    # 2.) Revealing empty space:
    # This will never happen during gameplay, but it won't cause issues anyways
    coords_to_reveal2 = [(1, 2)]  # Reveal nothing
    game_state_handler.reveal_coords_in_hidden_grid(
        sample_final_grid, hidden, coords_to_reveal2,
    )
    assert hidden[1][2] is None  # Still None


def test_get_all_letter_coords(sample_final_grid):
    """Test getting the set of all non-None coordinates."""
    expected_coords = {(0, 1), (0, 2), (1, 1), (2, 1)}
    actual_coords = game_state_handler.get_all_letter_coords(sample_final_grid)
    assert actual_coords == expected_coords


@patch("gameplay.game_state_handler.reveal_coords_in_hidden_grid")
def test_apply_coordinate_reveal(
    mock_reveal, sample_final_grid, sample_initial_game_state,
):
    """Test applying coordinate reveals and updating game state."""
    game_state = sample_initial_game_state

    # 1.) Reveal new coords
    coords_to_reveal = [(0, 1), (1, 1)]  # Reveal H, A
    initial_hidden_coords = set(game_state.hidden_letter_coords)
    initial_points = game_state.statistics.points

    game_state_handler.apply_coordinate_reveal(
        game_state, sample_final_grid, coords_to_reveal,
    )

    # Check reveal function was called and points increased (2 new letters revealed)
    mock_reveal.assert_called_once_with(
        sample_final_grid, game_state.hidden_grid, set(coords_to_reveal),
    )
    assert game_state.statistics.points == initial_points + 2

    # Check tracking sets if accurate
    assert game_state.found_letter_coords == set(coords_to_reveal)
    assert game_state.last_guess_coords == list(coords_to_reveal)  # Should be a list
    assert game_state.hidden_letter_coords == initial_hidden_coords - set(coords_to_reveal)

    # 2.) Reveal one overlapping coord and one new coord
    coords_to_reveal_2 = [(1, 1), (2, 1)]  # Reveal A (already found), T (new)
    game_state_handler.apply_coordinate_reveal(
        game_state, sample_final_grid, coords_to_reveal_2,
    )
    # Chceck:
    #   - Points should only increase by 1 (for 'T')
    #   - Found coords should be union
    #   - Last guess coords updated
    #   - Hidden coords further reduced
    assert game_state.statistics.points == initial_points + 2 + 1
    assert game_state.found_letter_coords == {(0, 1), (1, 1), (2, 1)}
    assert game_state.last_guess_coords == list(coords_to_reveal_2)
    assert game_state.hidden_letter_coords == initial_hidden_coords - {
        (0, 1),
        (1, 1),
        (2, 1),
    }


# ************************************************
# Tests for: Gameplay Related
# ************************************************


@patch("gameplay.game_state_handler.shuffle_letters_statistic")
@patch("gameplay.game_state_handler.create_hidden_grid")
@patch("gameplay.game_state_handler.get_all_letter_coords")
def test_initialize_game_state(
    mock_get_coords,
    mock_create_hidden,
    mock_shuffle_letters,
    sample_final_grid,
    sample_wizard_data,
):
    """Test the initialization of the main game state dictionary."""
    middle_word = "TEST"
    player_name = "Hero"

    # MOCK
    mock_shuffled = "E S T T"
    mock_hidden_grid = [
        [None, "#", "#", None, None],
        [None, "#", None, None, None],
        [None, "#", None, None, None],
    ]  # Example hidden grid
    mock_all_coords = {(0, 0), (1, 1)}  # Dummy coords
    mock_shuffle_letters.return_value = mock_shuffled
    mock_create_hidden.return_value = mock_hidden_grid
    mock_get_coords.return_value = mock_all_coords

    game_state = game_state_handler.initialize_game_state(
        sample_final_grid, middle_word, sample_wizard_data, player_name,
    )

    # Check if all mocks were called
    mock_create_hidden.assert_called_once_with(sample_final_grid)
    mock_shuffle_letters.assert_called_once_with(middle_word)
    mock_get_coords.assert_called_once_with(sample_final_grid)

    # Check structure and initial values
    assert game_state.player_name == player_name
    assert game_state.hidden_grid == mock_hidden_grid
    assert game_state.last_guess_coords == []
    assert game_state.correctly_guessed_words == set()
    assert game_state.hidden_letter_coords == mock_all_coords
    assert game_state.found_letter_coords == set()
    assert game_state.next_message == game_constants.WELCOME_MSG
    assert game_state.next_message_color == sample_wizard_data.color

    # Check statistics dictionary
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
    mock_check_completed,
    mock_apply_reveal,
    sample_initial_game_state,
    sample_words_to_find,
    sample_final_grid,
):
    """Test processing a correct guess when shield is off."""
    game_state = sample_initial_game_state
    guess = "HI"
    wizard_color = game_state.next_message_color
    initial_lives = game_state.statistics.lives_left
    initial_combo = game_state.statistics.combo
    coords_for_hi = sample_words_to_find[guess]
    mock_check_completed.return_value = []  # No implicit words found

    game_state_handler.process_guess(
        guess, game_state, sample_words_to_find, sample_final_grid, wizard_color,
    )

    # Check if all stats were updated correctly
    # Most importantly, Lives should not be negated (since correct!)
    stats = game_state.statistics
    assert stats.last_guess == guess
    assert game_state.correctly_guessed_words == {guess}
    assert stats.combo == initial_combo + 1
    assert stats.lives_left == initial_lives  # No damage
    assert game_state.next_message == game_constants.CORRECT_GUESS_MSG.format(guess)
    assert game_state.next_message_color == wizard_color

    # Check if mock functions were called
    mock_apply_reveal.assert_called_once_with(
        game_state, sample_final_grid, coords_for_hi,
    )
    mock_check_completed.assert_called_once_with(game_state, sample_words_to_find)


@patch("gameplay.game_state_handler.apply_coordinate_reveal")
@patch("gameplay.game_state_handler.check_for_completed_words")
def test_process_guess_correct_implicit_completion(
    mock_check_completed,
    mock_apply_reveal,
    sample_initial_game_state,
    sample_words_to_find,
    sample_final_grid,
):
    """Test correct guess that implicitly completes another word."""
    game_state = sample_initial_game_state
    guess = "HAT"  # Guessing HAT should reveal coords for AT
    wizard_color = game_state.next_message_color
    coords_for_hat = sample_words_to_find[guess]
    mock_check_completed.return_value = ["AT"]  # Simulate finding AT

    game_state_handler.process_guess(
        guess, game_state, sample_words_to_find, sample_final_grid, wizard_color,
    )

    # Check if all stats were updated correctly
    # Most importantly, "AT" must now be part of correctly_guessed_words
    stats = game_state.statistics
    assert game_state.correctly_guessed_words == {"HAT", "AT"}  # Both added
    assert stats.combo == 1
    assert game_constants.CORRECT_GUESS_MSG.format(guess) in game_state.next_message
    assert "Also completed: AT" in game_state.next_message

    # Check if mock functions were called
    mock_apply_reveal.assert_called_once_with(
        game_state, sample_final_grid, coords_for_hat,
    )
    mock_check_completed.assert_called_once_with(game_state, sample_words_to_find)


@patch("gameplay.game_state_handler.apply_coordinate_reveal")
@patch("gameplay.game_state_handler.check_for_completed_words")
def test_process_guess_wrong_no_shield(
    mock_check_completed,
    mock_apply_reveal,
    sample_initial_game_state,
    sample_words_to_find,
    sample_final_grid,
):
    """Test processing a wrong guess when shield is off."""
    game_state = sample_initial_game_state
    guess = "WRONG"
    wizard_color = game_state.next_message_color
    initial_lives = game_state.statistics.lives_left

    game_state_handler.process_guess(
        guess, game_state, sample_words_to_find, sample_final_grid, wizard_color,
    )

    # Check if all stats were updated correctly
    # Most importantly, no words should be added and lives is negated
    stats = game_state.statistics
    assert stats.last_guess == guess
    assert game_state.correctly_guessed_words == set()  # No words added
    assert stats.combo == 0  # Combo reset
    assert stats.lives_left == initial_lives - 1  # Damage taken
    assert game_state.next_message == game_constants.NOT_A_WORD_MSG.format(guess)
    assert game_state.next_message_color == game_constants.ERROR_COLOR

    # Check if mock functions were NOT called
    mock_apply_reveal.assert_not_called()
    mock_check_completed.assert_not_called()


@patch("gameplay.game_state_handler.apply_coordinate_reveal")
@patch("gameplay.game_state_handler.check_for_completed_words")
def test_process_guess_duplicate_no_shield(
    mock_check_completed,
    mock_apply_reveal,
    sample_initial_game_state,
    sample_words_to_find,
    sample_final_grid,
):
    """Test processing a duplicate guess when shield is off."""
    game_state = sample_initial_game_state
    guess = "HI"
    game_state.correctly_guessed_words.add(guess)  # Pre-add the guess
    wizard_color = game_state.next_message_color
    initial_lives = game_state.statistics.lives_left

    game_state_handler.process_guess(
        guess, game_state, sample_words_to_find, sample_final_grid, wizard_color,
    )

    # Check if all stats were updated correctly
    # Most importantly, life should still be negated, but correctly_guessed_words is the same
    stats = game_state.statistics
    assert stats.last_guess == guess
    assert game_state.correctly_guessed_words == {guess}  # Set unchanged
    assert stats.combo == 0  # Combo reset
    assert stats.lives_left == initial_lives - 1  # Damage taken
    assert game_state.next_message == game_constants.ALREADY_FOUND_MSG.format(guess)
    assert game_state.next_message_color == game_constants.ERROR_COLOR

    # Check if mock functions were NOT called
    mock_apply_reveal.assert_not_called()
    mock_check_completed.assert_not_called()


@patch("gameplay.game_state_handler.apply_coordinate_reveal")
@patch("gameplay.game_state_handler.check_for_completed_words")
def test_process_guess_wrong_with_shield(
    mock_check_completed,
    mock_apply_reveal,
    sample_initial_game_state,
    sample_words_to_find,
    sample_final_grid,
):
    """Test processing a wrong guess when shield is active."""
    game_state = sample_initial_game_state
    game_state.statistics.shield_turns = 2  # Activate shield
    guess = "WRONG"
    wizard_color = game_state.next_message_color
    initial_lives = game_state.statistics.lives_left

    game_state_handler.process_guess(
        guess, game_state, sample_words_to_find, sample_final_grid, wizard_color,
    )

    # Check if all stats were updated correctly
    # Most importantly, life should NOT be negated,and shield turns is decremented
    stats = game_state.statistics
    assert stats.lives_left == initial_lives  # No damage taken
    assert stats.shield_turns == 1  # Shield decremented
    assert stats.combo == 0
    assert game_state.next_message == game_constants.NOT_A_WORD_MSG.format(guess)

    # Check if mock functions were NOT called, since it was still wrong
    mock_apply_reveal.assert_not_called()
    mock_check_completed.assert_not_called()


@patch("gameplay.game_state_handler.apply_coordinate_reveal")
@patch("gameplay.game_state_handler.check_for_completed_words")
def test_process_guess_correct_with_shield(
    mock_check_completed,
    mock_apply_reveal,
    sample_initial_game_state,
    sample_words_to_find,
    sample_final_grid,
):
    """Test processing a correct guess when shield is active."""
    game_state = sample_initial_game_state
    game_state.statistics.shield_turns = 1
    guess = "HI"
    wizard_color = game_state.next_message_color
    initial_lives = game_state.statistics.lives_left
    coords_for_hi = sample_words_to_find[guess]
    mock_check_completed.return_value = []

    game_state_handler.process_guess(
        guess, game_state, sample_words_to_find, sample_final_grid, wizard_color,
    )

    # Check if all stats were updated correctly
    # Most importantly, life should NOT be negated, and shield turns is still decremented
    stats = game_state.statistics
    assert stats.lives_left == initial_lives  # No damage
    assert stats.shield_turns == 0  # Shield decremented
    assert stats.combo == 1
    assert game_state.next_message == game_constants.CORRECT_GUESS_MSG.format(guess)

    # Check if mock functions was called (correct guess!)
    mock_apply_reveal.assert_called_once_with(
        game_state, sample_final_grid, coords_for_hi,
    )
    mock_check_completed.assert_called_once_with(game_state, sample_words_to_find)


def test_check_for_completed_words(sample_words_to_find):
    """Test identifying words completed implicitly by revealed letters."""
    # 1.) 'HAT' and 'HI' revealed, implies 'AT' is also revealed
    class DummyGameState:
        pass

    game_state = DummyGameState()
    game_state.correctly_guessed_words = {"HAT"}
    game_state.hidden_letter_coords = {(0, 2)}
    game_state.found_letter_coords = {(0, 1), (1, 1), (2, 1)}
    newly_found = game_state_handler.check_for_completed_words(
        game_state, sample_words_to_find,
    )
    # Only AT should be newly found
    assert newly_found == ["AT"]

    # 2.) All letters revealed
    game_state_all_revealed = DummyGameState()
    game_state_all_revealed.correctly_guessed_words = set()
    game_state_all_revealed.hidden_letter_coords = set()
    game_state_all_revealed.found_letter_coords = {(0, 1), (0, 2), (1, 1), (2, 1)}
    newly_found_all = game_state_handler.check_for_completed_words(
        game_state_all_revealed, sample_words_to_find,
    )
    # Should find all words not already guessed
    assert set(newly_found_all) == {"HI", "HAT", "AT"}


def test_check_game_over(sample_words_to_find):
    """Test the game over condition checks."""
    # 1.) Win condition
    class DummyStats:
        def __init__(self, lives_left):
            self.lives_left = lives_left

    class DummyGameState:
        def __init__(self, guessed, lives_left):
            self.correctly_guessed_words = guessed
            self.statistics = DummyStats(lives_left)

    game_state_win = DummyGameState({"HI", "HAT", "AT"}, 3)
    assert (
        game_state_handler.check_game_over(game_state_win, sample_words_to_find)
        == "win"
    )

    # 2.) Loss condition (0 lives)
    game_state_loss_0 = DummyGameState({"HI"}, 0)
    assert (
        game_state_handler.check_game_over(game_state_loss_0, sample_words_to_find)
        == "loss"
    )

    # 3.) Loss condition (< 0 lives)
    game_state_loss_neg = DummyGameState({"HI"}, -1)
    assert (
        game_state_handler.check_game_over(game_state_loss_neg, sample_words_to_find)
        == "loss"
    )

    # 4.) Continue condition
    game_state_continue = DummyGameState({"HI"}, 1)
    assert (
        game_state_handler.check_game_over(game_state_continue, sample_words_to_find)
        == "continue"
    )
