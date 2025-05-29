from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple, Dict, Any, Iterable
import random

# Assuming WizardData is imported if not defined here (it's defined in data.wizards_details)
from data.wizards_details import WizardData
from gameplay import game_constants  # Your constants module


@dataclass
class GameStatisticsData:
    letters: str = ""
    lives_left: int = 0
    points: int = 0
    last_guess: Optional[str] = None
    combo: int = 0
    power_points: int = 0
    shield_turns: int = 0


@dataclass
class GameStateData:
    player_name: Optional[str]
    statistics: GameStatisticsData
    hidden_grid: List[List[Optional[str]]]
    next_message: str
    next_message_color: str
    last_guess_coords: List[Tuple[int, int]] = field(default_factory=list)
    correctly_guessed_words: Set[str] = field(default_factory=set)
    hidden_letter_coords: Set[Tuple[int, int]] = field(default_factory=set)
    found_letter_coords: Set[Tuple[int, int]] = field(default_factory=set)


def shuffle_letters_statistic(middle_word: str) -> str:
    """Shuffles the letters of the middle word for display in statistics."""
    letters_list = list(str(middle_word).upper())
    random.shuffle(letters_list)
    return " ".join(letters_list)


def create_hidden_grid(final_grid: List[List[Optional[str]]]) -> List[List[Optional[str]]]:
    """Creates the initial hidden grid for the player."""
    return [["#" if col else None for col in row] for row in final_grid]


def reveal_coords_in_hidden_grid(
    final_grid: List[List[Optional[str]]], hidden_grid: List[List[Optional[str]]], coords: Iterable[Tuple[int, int]]
) -> None:
    """Reveals specific coordinates on the hidden grid."""
    for r, c in coords:
        if 0 <= r < len(hidden_grid) and 0 <= c < len(hidden_grid[0]):
            hidden_grid[r][c] = final_grid[r][c]


def get_all_letter_coords(final_grid: List[List[Optional[str]]]) -> Set[Tuple[int, int]]:
    """Gets the set of all coordinates containing letters on the final grid."""
    all_coords: Set[Tuple[int, int]] = set()
    height = len(final_grid)
    width = len(final_grid[0]) if height > 0 else 0
    for r_idx in range(height):
        for c_idx in range(width):
            if final_grid[r_idx][c_idx] is not None:
                all_coords.add((r_idx, c_idx))
    return all_coords


def apply_coordinate_reveal(
    game_state: GameStateData, final_grid: List[List[Optional[str]]], coords_to_reveal: Iterable[Tuple[int, int]]
) -> None:
    """Applies the effects of revealing coordinates to the game state."""
    coords_set = set(coords_to_reveal)

    reveal_coords_in_hidden_grid(final_grid, game_state.hidden_grid, coords_set)

    newly_revealed_coords = coords_set - game_state.found_letter_coords
    game_state.statistics.points += len(newly_revealed_coords)

    game_state.found_letter_coords.update(coords_set)
    game_state.last_guess_coords = list(coords_set)

    game_state.hidden_letter_coords.difference_update(coords_set)


def initialize_game_state(
    final_grid: List[List[Optional[str]]], middle_word: str, selected_wizard: WizardData, player_name: Optional[str]
) -> GameStateData:
    """Initializes the game state object for a new game round."""
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
    words_to_find: Dict[str, List[Tuple[int, int]]],
    final_grid: List[List[Optional[str]]],
    wizard_color: str,
) -> None:
    """Processes a player's word guess and updates the game state."""
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


def check_for_completed_words(game_state: GameStateData, words_to_find: Dict[str, List[Tuple[int, int]]]) -> List[str]:
    """Checks if any words were implicitly completed by the last reveal."""
    newly_found_words: List[str] = []

    for word, coords in words_to_find.items():
        if word not in game_state.correctly_guessed_words:
            all_letters_revealed = all(coord not in game_state.hidden_letter_coords for coord in coords)
            if all_letters_revealed:
                newly_found_words.append(word)
    return newly_found_words


def check_game_over(game_state: GameStateData, words_to_find: Dict[str, List[Tuple[int, int]]]) -> str:
    """Checks if the game has reached a win or loss condition."""
    if len(game_state.correctly_guessed_words) == len(words_to_find):
        return "win"
    elif game_state.statistics.lives_left <= 0:
        return "loss"
    else:
        return "continue"
