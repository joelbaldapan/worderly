import random

from data.settings_details import DifficultyData

from .board_state import (
    BoardGenerationState,
    calculate_middle_word_placement_coords,
    initialize_board_state,
    place_letters_on_grid,
)
from .placement_logic import (
    apply_placement,
    categorize_placement,
    find_possible_placements,
    select_random_placement,
    update_placed_letter_coords,
)


def place_middle_word(state: BoardGenerationState, middle_word: str) -> bool:
    """Place the initial diagonal middle word onto the grid and update the board state.

    Args:
        state (BoardGenerationState): The current board generation state.
        middle_word (str): The word to be placed in the middle of the grid.

    Returns:
        bool: True if the middle word was successfully placed, False otherwise.

    """
    height = len(state.grid)
    width = len(state.grid[0]) if height > 0 else 0

    middle_word_coords = calculate_middle_word_placement_coords(height, width, middle_word)
    if middle_word_coords is None:
        return False

    place_letters_on_grid(state.grid, middle_word, middle_word_coords)
    update_placed_letter_coords(state, middle_word, middle_word_coords)
    state.placed_words_coords[middle_word] = middle_word_coords
    state.middle_word_coords = set(middle_word_coords)
    return True


def place_other_words(
    state: BoardGenerationState,
    words_to_place: list[str],
    max_total_words: int,
) -> None:
    """Attempt to place the remaining words onto the grid.

    Args:
        state (BoardGenerationState): The current board generation state.
        words_to_place (list[str]): List of sub-words to be placed on the grid.
        max_total_words (int): Maximum number of words allowed on the board.


    """
    all_potential_words_on_board = set(words_to_place)
    if state.placed_words_coords:
        middle_word_key = next(iter(state.placed_words_coords))
        all_potential_words_on_board.add(middle_word_key)

    shuffled_subwords = list(words_to_place)
    random.shuffle(shuffled_subwords)

    for word in shuffled_subwords:
        if word in state.placed_words_coords:
            continue
        if len(state.placed_words_coords) >= max_total_words:
            break

        possible_placements = find_possible_placements(
            state.grid,
            word,
            all_potential_words_on_board,
            state.placed_letter_coords,
        )
        priority_placements, other_placements = categorize_placement(
            possible_placements,
            state.middle_word_coords,
            state.used_middle_word_coords,
        )
        chosen_placement = select_random_placement(priority_placements, other_placements)

        if chosen_placement:
            apply_placement(state, chosen_placement)


def validate_final_grid(state: BoardGenerationState, min_total_words: int) -> bool:
    """Validate the generated grid against placement requirements.

    Args:
        state (BoardGenerationState): The current board generation state.
        min_total_words (int): Minimum number of words required on the board.

    Returns:
        bool: True if the grid meets all requirements, False otherwise.

    """
    total_placed_count = len(state.placed_words_coords)
    if total_placed_count < min_total_words:
        return False
    return not (state.middle_word_coords and state.middle_word_coords != state.used_middle_word_coords)


def capitalize_middle_word_appearance(state: BoardGenerationState, middle_word: str) -> None:
    """Capitalize the letters of the middle word on the final grid.

    Args:
        state (BoardGenerationState): The current board generation state.
        middle_word (str): The middle word to capitalize on the grid.

    """
    if middle_word in state.placed_words_coords:
        middle_word_coords_list: list[tuple[int, int]] = state.placed_words_coords[middle_word]
        middle_word_upper = middle_word.upper()
        place_letters_on_grid(state.grid, middle_word_upper, middle_word_coords_list)


def generate_board(
    difficulty_conf: DifficultyData,
    middle_word: str,
    words_to_place: list[str],
) -> tuple[list[list[str | None]] | None, dict[str, list[tuple[int, int]]] | None]:
    """Generate the final game board and word coordinate data.

    Args:
        difficulty_conf (DifficultyData): Difficulty configuration containing grid and word requirements.
        middle_word (str): The word to be placed in the middle of the grid.
        words_to_place (list[str]): List of sub-words to be placed on the grid.

    Returns:
        tuple[list[list[str | None]] | None, dict[str, list[tuple[int, int]]] | None]:
            A tuple containing the generated grid and a dictionary of placed word coordinates,
            or (None, None) if generation fails.

    """
    min_total_words = difficulty_conf.words_on_board_needed.minimum
    max_total_words = difficulty_conf.words_on_board_needed.maximum
    height = difficulty_conf.grid.height
    width = difficulty_conf.grid.width

    current_board_state = initialize_board_state(height, width)

    if not place_middle_word(current_board_state, middle_word):
        return None, None  # Failed to place middle word

    # words_to_place here are the sub-words to be added around the middle_word
    place_other_words(current_board_state, words_to_place, max_total_words)

    if not validate_final_grid(current_board_state, min_total_words):
        return None, None  # Grid validation failed

    capitalize_middle_word_appearance(current_board_state, middle_word)

    return current_board_state.grid, current_board_state.placed_words_coords
