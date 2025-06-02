import random

from .board_state import (
    BoardGenerationState,
    PlacementDetail,
    calculate_straight_word_placement_coords,
    place_letters_on_grid,
)
from .placement_rules import is_valid_placement


def find_possible_placements(
    grid: list[list[str | None]],
    word: str,
    words_to_place_set: set[str],
    placed_letter_coords: dict[str, list[tuple[int, int]]],
) -> list[PlacementDetail]:
    """Find all valid horizontal and vertical placements for a given word.

    Args:
        grid: The current grid as a 2D list of strings or None.
        word: The word to place.
        words_to_place_set: Set of words that are yet to be placed.
        placed_letter_coords: Dictionary mapping letters to their coordinates on the grid.

    Returns:
        A list of PlacementDetail objects representing valid placements for the word.

    """
    possible_placements: list[PlacementDetail] = []
    for idx, letter_in_word in enumerate(word):
        if letter_in_word not in placed_letter_coords:
            continue
        for intersect_coord in placed_letter_coords[letter_in_word]:
            intersect_row, intersect_col = intersect_coord
            intersection_info: dict = {
                "row": intersect_row,
                "col": intersect_col,
                "idx": idx,
            }
            # Check VERTICAL placement
            if is_valid_placement(grid, word, words_to_place_set, intersection_info, "V"):
                possible_placements.append(
                    PlacementDetail(word=word, coord=intersect_coord, idx=idx, orientation="V"),
                )
            # Check HORIZONTAL placement
            if is_valid_placement(grid, word, words_to_place_set, intersection_info, "H"):
                possible_placements.append(
                    PlacementDetail(word=word, coord=intersect_coord, idx=idx, orientation="H"),
                )
    return possible_placements


def categorize_placement(
    possible_placements: list[PlacementDetail],
    middle_word_coords: set[tuple[int, int]],
    used_middle_word_coords: set[tuple[int, int]],
) -> tuple[list[PlacementDetail], list[PlacementDetail]]:
    """Categorize possible placements into priority and other lists.

    Args:
        possible_placements: List of possible PlacementDetail objects.
        middle_word_coords: Set of coordinates that are part of the middle word.
        used_middle_word_coords: Set of coordinates from the middle word that have already been used.

    Returns:
        A tuple containing:
            - List of priority placements (those using unused middle word coords).
            - List of other placements.

    """
    priority_placements: list[PlacementDetail] = []
    other_placements: list[PlacementDetail] = []
    for placement in possible_placements:
        if placement.coord in middle_word_coords and placement.coord not in used_middle_word_coords:
            priority_placements.append(placement)
        else:
            other_placements.append(placement)
    return priority_placements, other_placements


def select_random_placement(
    priority_placements: list[PlacementDetail],
    other_placements: list[PlacementDetail],
) -> PlacementDetail | None:
    """Select a random placement, prioritizing the priority list.

    Args:
        priority_placements: List of priority PlacementDetail objects.
        other_placements: List of other PlacementDetail objects.

    Returns:
        A randomly selected PlacementDetail from the priority list if available,
        otherwise from the other list, or None if both are empty.

    """
    if priority_placements:
        return random.choice(priority_placements)
    elif other_placements:
        return random.choice(other_placements)
    return None


def update_placed_word_coords(
    chosen_placement: PlacementDetail,
    coords_to_place: list[tuple[int, int]],
    state: BoardGenerationState,
) -> None:
    """Update the state after a word is successfully placed.

    Args:
        chosen_placement: The PlacementDetail of the placed word.
        coords_to_place: List of coordinates where the word was placed.
        state: The current BoardGenerationState to update.

    """
    state.placed_words_coords[chosen_placement.word] = coords_to_place
    if chosen_placement.coord in state.middle_word_coords:
        state.used_middle_word_coords.add(chosen_placement.coord)


def update_placed_letter_coords(
    state: BoardGenerationState,
    word: str,
    placed_coords: list[tuple[int, int]],
) -> None:
    """Update the dictionary tracking all placed letters and their coordinates.

    Args:
        state: The current BoardGenerationState to update.
        word: The word that was placed.
        placed_coords: List of coordinates where the word was placed.

    """
    for i, coord in enumerate(placed_coords):
        letter = word[i]
        if letter not in state.placed_letter_coords:
            state.placed_letter_coords[letter] = []
        if coord not in state.placed_letter_coords[letter]:
            state.placed_letter_coords[letter].append(coord)


def apply_placement(
    state: BoardGenerationState,
    chosen_placement: PlacementDetail,
) -> None:
    """Apply a chosen placement to the grid and update tracking state.

    Args:
        state: The current BoardGenerationState to update.
        chosen_placement: The PlacementDetail of the word to place.

    """
    coords_to_place = calculate_straight_word_placement_coords(chosen_placement)
    update_placed_letter_coords(state, chosen_placement.word, coords_to_place)
    update_placed_word_coords(chosen_placement, coords_to_place, state)
    place_letters_on_grid(state.grid, chosen_placement.word, coords_to_place)
