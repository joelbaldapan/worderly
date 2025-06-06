import random
from collections.abc import Iterable
from dataclasses import dataclass, field

from data.wizards_details import WizardData
from gameplay import game_constants


@dataclass
class GameStatisticsData:
    letters: str = ""
    lives_left: int = 0
    points: int = 0
    last_guess: str | None = None
    combo: int = 0
    power_points: int = 0
    shield_turns: int = 0


@dataclass
class GameStateData:
    player_name: str | None
    statistics: GameStatisticsData
    hidden_grid: list[list[str | None]]
    next_message: str
    next_message_color: str
    last_guess_coords: list[tuple[int, int]] = field(default_factory=list)
    correctly_guessed_words: set[str] = field(default_factory=set)
    hidden_letter_coords: set[tuple[int, int]] = field(default_factory=set)
    found_letter_coords: set[tuple[int, int]] = field(default_factory=set)


def shuffle_letters_statistic(middle_word: str) -> str:
    """Shuffle the letters of the given word and return them as a space-separated string.

    Args:
        middle_word (str): The word whose letters will be shuffled.

    Returns:
        str: The shuffled letters as a space-separated string.

    """
    letters_list = list(str(middle_word).upper())
    random.shuffle(letters_list)
    return " ".join(letters_list)


def create_hidden_grid(final_grid: list[list[str | None]]) -> list[list[str | None]]:
    """Create a hidden grid for the player, masking all letters with '#'.

    Args:
        final_grid (list[list[str | None]]): The solution grid.

    Returns:
        list[list[str | None]]: The hidden grid with masked letters.

    """
    return [["#" if col else None for col in row] for row in final_grid]


def reveal_coords_in_hidden_grid(
    final_grid: list[list[str | None]],
    hidden_grid: list[list[str | None]],
    coords: Iterable[tuple[int, int]],
) -> None:
    """Reveal specific coordinates in the hidden grid by copying values from the final grid.

    Args:
        final_grid (list[list[str | None]]): The solution grid.
        hidden_grid (list[list[str | None]]): The player's hidden grid.
        coords (Iterable[tuple[int, int]]): Coordinates to reveal.

    """
    for r, c in coords:
        if 0 <= r < len(hidden_grid) and 0 <= c < len(hidden_grid[0]):
            hidden_grid[r][c] = final_grid[r][c]


def get_all_letter_coords(final_grid: list[list[str | None]]) -> set[tuple[int, int]]:
    """Get all coordinates in the grid that contain a letter.

    Args:
        final_grid (list[list[str | None]]): The solution grid.

    Returns:
        set[tuple[int, int]]: Set of coordinates containing letters.

    """
    all_coords: set[tuple[int, int]] = set()
    height = len(final_grid)
    width = len(final_grid[0]) if height > 0 else 0
    for r_idx in range(height):
        for c_idx in range(width):
            if final_grid[r_idx][c_idx] is not None:
                all_coords.add((r_idx, c_idx))
    return all_coords


def apply_coordinate_reveal(
    game_state: GameStateData,
    final_grid: list[list[str | None]],
    coords_to_reveal: Iterable[tuple[int, int]],
) -> None:
    """Reveal the specified coordinates in the game state and update points and found letters.

    Args:
        game_state (GameStateData): The current game state.
        final_grid (list[list[str | None]]): The solution grid.
        coords_to_reveal (Iterable[tuple[int, int]]): Coordinates to reveal.

    """
    coords_set = set(coords_to_reveal)

    reveal_coords_in_hidden_grid(final_grid, game_state.hidden_grid, coords_set)

    newly_revealed_coords = coords_set - game_state.found_letter_coords
    game_state.statistics.points += len(newly_revealed_coords)

    game_state.found_letter_coords.update(coords_set)
    game_state.last_guess_coords = list(coords_set)

    game_state.hidden_letter_coords.difference_update(coords_set)


def initialize_game_state(
    final_grid: list[list[str | None]],
    middle_word: str,
    selected_wizard: WizardData,
    player_name: str | None,
) -> GameStateData:
    """Initialize and return a new GameStateData object for a new game round.

    Args:
        final_grid (list[list[str | None]]): The solution grid.
        middle_word (str): The central word for the round.
        selected_wizard (WizardData): The selected wizard's data.
        player_name (str | None): The player's name.

    Returns:
        GameStateData: The initialized game state.

    """
    stats = GameStatisticsData(
        letters=shuffle_letters_statistic(middle_word),
        lives_left=selected_wizard.starting_lives,
        points=0,
        last_guess=None,
        combo=0,
        power_points=0,
        shield_turns=0,
    )

    initial_hidden_grid = create_hidden_grid(final_grid)
    all_coords_on_board = get_all_letter_coords(final_grid)

    return GameStateData(
        player_name=player_name,
        statistics=stats,
        hidden_grid=initial_hidden_grid,
        last_guess_coords=[],
        correctly_guessed_words=set(),
        hidden_letter_coords=all_coords_on_board,
        found_letter_coords=set(),
        next_message=game_constants.WELCOME_MSG,
        next_message_color=selected_wizard.color,
    )


def process_guess(
    guess: str,
    game_state: GameStateData,
    words_to_find: dict[str, list[tuple[int, int]]],
    final_grid: list[list[str | None]],
    wizard_color: str,
) -> None:
    """Process a player's guess, update the game state, and handle scoring and messages.

    Args:
        guess (str): The player's guessed word.
        game_state (GameStateData): The current game state.
        words_to_find (dict[str, list[tuple[int, int]]]): Words and their coordinates.
        final_grid (list[list[str | None]]): The solution grid.
        wizard_color (str): The color associated with the wizard.

    """
    stats = game_state.statistics

    stats.last_guess = guess
    game_state.last_guess_coords = []
    took_damage = False

    if guess in game_state.correctly_guessed_words:
        stats.combo = 0
        game_state.next_message = game_constants.ALREADY_FOUND_MSG.format(guess)
        game_state.next_message_color = game_constants.ERROR_COLOR
        took_damage = True
    elif guess not in words_to_find:
        stats.combo = 0
        game_state.next_message = game_constants.NOT_A_WORD_MSG.format(guess)
        game_state.next_message_color = game_constants.ERROR_COLOR
        took_damage = True
    else:  # Correct guess
        game_state.next_message = game_constants.CORRECT_GUESS_MSG.format(guess)
        game_state.next_message_color = wizard_color
        stats.combo += 1
        game_state.correctly_guessed_words.add(guess)

        word_coords = words_to_find[guess]
        apply_coordinate_reveal(game_state, final_grid, word_coords)

        completed_words = check_for_completed_words(game_state, words_to_find)
        if completed_words:
            game_state.correctly_guessed_words.update(completed_words)
            game_state.next_message += f" (Also completed: {', '.join(completed_words)})"

    if took_damage and stats.shield_turns <= 0:
        stats.lives_left -= 1

    if stats.shield_turns > 0:
        stats.shield_turns -= 1


def check_for_completed_words(
    game_state: GameStateData,
    words_to_find: dict[str, list[tuple[int, int]]],
) -> list[str]:
    """Check for words that have been completed by the last reveal but not explicitly guessed.

    Args:
        game_state (GameStateData): The current game state.
        words_to_find (dict[str, list[tuple[int, int]]]): Words and their coordinates.

    Returns:
        list[str]: List of newly completed words.

    """
    newly_found_words: list[str] = []

    for word, coords in words_to_find.items():
        if word not in game_state.correctly_guessed_words:
            all_letters_revealed = all(coord not in game_state.hidden_letter_coords for coord in coords)
            if all_letters_revealed:
                newly_found_words.append(word)
    return newly_found_words


def check_game_over(
    game_state: GameStateData,
    words_to_find: dict[str, list[tuple[int, int]]],
) -> str:
    """Determine if the game is over due to win or loss conditions.

    Args:
        game_state (GameStateData): The current game state.
        words_to_find (dict[str, list[tuple[int, int]]]): Words and their coordinates.

    Returns:
        str: "win" if all words found, "loss" if out of lives, "continue" otherwise.

    """
    if len(game_state.correctly_guessed_words) == len(words_to_find):
        return "win"
    elif game_state.statistics.lives_left <= 0:
        return "loss"
    else:
        return "continue"
