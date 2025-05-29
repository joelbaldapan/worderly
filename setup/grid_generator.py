# setup/grid_generator.py
import random
from typing import Any

# Import DifficultyData for type hinting
from data.settings_details import DifficultyData

# Type Aliases for complex internal dictionary structures
PlacementDict = dict[str, Any]  # For dictionaries describing a word placement
BoardStateDict = dict[str, Any]  # For the internal 'state' dictionary during board generation


def create_empty_grid(height: int, width: int) -> list[list[str | None]]:
    """Creates a 2D list representing an empty grid filled with None."""
    return [[None] * width for _ in range(height)]


def place_letters_on_grid(grid: list[list[str | None]], word: str, coords_to_place: list[tuple[int, int]]) -> None:
    """Places the letters of a word onto the grid at specified coordinates."""
    for idx, coord in enumerate(coords_to_place):
        row, col = coord
        if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
            grid[row][col] = word[idx]


def update_placed_word_coords(
    chosen_placement: PlacementDict,
    coords_to_place: list[tuple[int, int]],
    placed_words_coords: dict[str, list[tuple[int, int]]],
    middle_word_coords: set[tuple[int, int]],
    used_middle_word_coords: set[tuple[int, int]],
) -> None:
    """Updates state dictionaries after a word is successfully placed."""
    word: str = chosen_placement["word"]
    intersection_coord: tuple[int, int] = chosen_placement["coord"]

    placed_words_coords[word] = coords_to_place
    if intersection_coord in middle_word_coords:
        used_middle_word_coords.add(intersection_coord)


def update_placed_letter_coords(
    placed_letter_coords: dict[str, list[tuple[int, int]]],
    word: str,
    placed_coords: list[tuple[int, int]],
) -> None:
    """Updates the dictionary tracking all placed letters and their coordinates."""
    for i, coord in enumerate(placed_coords):
        letter = word[i]
        if letter not in placed_letter_coords:
            placed_letter_coords[letter] = []
        # Add coord only if it's not already tracked for this letter
        if coord not in placed_letter_coords[letter]:
            placed_letter_coords[letter].append(coord)


def _is_within_bounds(r: int, c: int, height: int, width: int) -> bool:
    """Checks if a given coordinate (r, c) is within the grid boundaries."""
    return 0 <= r < height and 0 <= c < width


def _check_parallel_cells(grid: list[list[str | None]], r: int, c: int, dr: int, dc: int) -> bool:
    """Checks if cells perpendicular to a given cell along a direction are empty."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    perp_dr, perp_dc = dc, dr

    check_r1, check_c1 = r - perp_dr, c - perp_dc
    neighbor1_occupied = _is_within_bounds(check_r1, check_c1, height, width) and grid[check_r1][check_c1] is not None

    check_r2, check_c2 = r + perp_dr, c + perp_dc
    neighbor2_occupied = _is_within_bounds(check_r2, check_c2, height, width) and grid[check_r2][check_c2] is not None
    return not (neighbor1_occupied or neighbor2_occupied)


def _check_adjacent_before_start(
    grid: list[list[str | None]],
    start_row: int,
    start_col: int,
    dr: int,
    dc: int,
) -> bool:
    """Checks if the cell immediately before the start of a word path is empty."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    before_r, before_c = start_row - dr, start_col - dc

    cell_occupied = _is_within_bounds(before_r, before_c, height, width) and grid[before_r][before_c] is not None
    return not cell_occupied


def _check_adjacent_after_end(grid: list[list[str | None]], end_row: int, end_col: int, dr: int, dc: int) -> bool:
    """Checks if the cell immediately after the end of a word path is empty."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    after_r, after_c = end_row + dr, end_col + dc
    cell_occupied = _is_within_bounds(after_r, after_c, height, width) and grid[after_r][after_c] is not None
    return not cell_occupied


def _check_for_all_letters(
    grid: list[list[str | None]],
    word: str,
    words_to_place_set: set[str],
    word_len: int,
    start_row: int,
    start_col: int,
    dr: int,
    dc: int,
) -> bool:
    """Checks conditions along the entire path of a potential word placement."""
    placed_new_letter = False
    checked_letters = ""
    for i in range(word_len):
        current_row = start_row + i * dr
        current_col = start_col + i * dc

        if not _is_within_bounds(current_row, current_col, len(grid), len(grid[0])):
            return False

        current_cell = grid[current_row][current_col]

        if current_cell:
            checked_letters += current_cell
            if current_cell.lower() != word[i].lower():
                return False
        else:
            placed_new_letter = True
            if not _check_parallel_cells(grid, current_row, current_col, dr, dc):
                return False

        if len(checked_letters) > 1 and checked_letters.lower() in words_to_place_set:
            return False
    return placed_new_letter


def is_valid_placement(
    grid: list[list[str | None]],
    word: str,
    words_to_place_set: set[str],
    intersect_row: int,
    intersect_col: int,
    intersect_idx: int,
    orientation: str,
) -> bool:
    """Determines if placing a word at a specific intersection is valid."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    word_len = len(word)

    dr, dc = (1, 0) if orientation == "V" else (0, 1)
    start_row = intersect_row - intersect_idx * dr
    start_col = intersect_col - intersect_idx * dc
    end_row = start_row + (word_len - 1) * dr
    end_col = start_col + (word_len - 1) * dc

    if not (
        _is_within_bounds(start_row, start_col, height, width) and _is_within_bounds(end_row, end_col, height, width)
    ):
        return False

    if not (
        _check_adjacent_before_start(grid, start_row, start_col, dr, dc)
        and _check_adjacent_after_end(grid, end_row, end_col, dr, dc)
    ):
        return False

    if not _check_for_all_letters(grid, word, words_to_place_set, word_len, start_row, start_col, dr, dc):
        return False
    return True


def find_possible_placements(
    grid: list[list[str | None]],
    word: str,
    words_to_place_set: set[str],
    placed_letter_coords: dict[str, list[tuple[int, int]]],
) -> list[PlacementDict]:
    """Finds all valid horizontal and vertical placements for a given word."""
    possible_placements: list[PlacementDict] = []
    for idx, letter in enumerate(word):
        if letter not in placed_letter_coords:
            continue
        for coord in placed_letter_coords[letter]:
            intersect_row, intersect_col = coord
            if is_valid_placement(grid, word, words_to_place_set, intersect_row, intersect_col, idx, "V"):
                possible_placements.append({"word": word, "coord": coord, "idx": idx, "orientation": "V"})
            if is_valid_placement(grid, word, words_to_place_set, intersect_row, intersect_col, idx, "H"):
                possible_placements.append({"word": word, "coord": coord, "idx": idx, "orientation": "H"})
    return possible_placements


def categorize_placement(
    possible_placements: list[PlacementDict],
    middle_word_coords: set[tuple[int, int]],
    used_middle_word_coords_set: set[tuple[int, int]],
) -> tuple[list[PlacementDict], list[PlacementDict]]:
    """Categorizes possible placements into priority and other lists."""
    priority_placements: list[PlacementDict] = []
    other_placements: list[PlacementDict] = []
    for placement in possible_placements:
        if placement["coord"] in middle_word_coords and placement["coord"] not in used_middle_word_coords_set:
            priority_placements.append(placement)
        else:
            other_placements.append(placement)
    return priority_placements, other_placements


def select_random_placement(
    priority_placements: list[PlacementDict],
    other_placements: list[PlacementDict],
) -> PlacementDict | None:
    """Selects a random placement, prioritizing the priority list."""
    if priority_placements:
        return random.choice(priority_placements)
    elif other_placements:
        return random.choice(other_placements)
    return None


def apply_placement(
    grid: list[list[str | None]],
    chosen_placement: PlacementDict,
    placed_letter_coords: dict[str, list[tuple[int, int]]],
    placed_words_coords: dict[str, list[tuple[int, int]]],
    middle_word_coords: set[tuple[int, int]],
    used_middle_word_coords: set[tuple[int, int]],
) -> None:
    """Applies a chosen placement to the grid and updates tracking dictionaries."""
    word: str = chosen_placement["word"]
    coords_to_place = calculate_straight_word_placement_coords(chosen_placement)

    update_placed_letter_coords(placed_letter_coords, word, coords_to_place)
    update_placed_word_coords(
        chosen_placement,
        coords_to_place,
        placed_words_coords,
        middle_word_coords,
        used_middle_word_coords,
    )
    place_letters_on_grid(grid, word, coords_to_place)


def _calculate_middle_word_start(height: int, width: int, word_len: int) -> tuple[int, int] | None:
    """Calculates the starting (top-left) coordinate for diagonal middle word."""
    diag_space = word_len * 2 - 1
    start_row = (height - diag_space) // 2
    start_col = (width - diag_space) // 2
    if start_row < 0 or start_col < 0 or start_row + diag_space > height or start_col + diag_space > width:
        return None
    return start_row, start_col


def calculate_middle_word_placement_coords(
    height: int,
    width: int,
    middle_word: str,
) -> list[tuple[int, int]] | None:
    """Calculates the list of diagonal coordinates for the middle word."""
    start_coords = _calculate_middle_word_start(height, width, len(middle_word))
    if start_coords is None:
        return None

    start_row, start_col = start_coords
    coords_to_place: list[tuple[int, int]] = []
    row, col = start_row, start_col
    for _ in middle_word:
        coords_to_place.append((row, col))
        row += 2
        col += 2
    return coords_to_place


def calculate_straight_word_placement_coords(chosen_placement: PlacementDict) -> list[tuple[int, int]]:
    """Calculates the list of coordinates for a straight (H or V) placement."""
    word: str = chosen_placement["word"]
    intersect_row, intersect_col = chosen_placement["coord"]
    intersect_idx: int = chosen_placement["idx"]
    orientation: str = chosen_placement["orientation"]
    word_len = len(word)

    dr, dc = (1, 0) if orientation == "V" else (0, 1)
    start_row = intersect_row - intersect_idx * dr
    start_col = intersect_col - intersect_idx * dc

    coords_to_place: list[tuple[int, int]] = []
    for i in range(word_len):
        coords_to_place.append((start_row + i * dr, start_col + i * dc))
    return coords_to_place


def initialize_board_state(height: int, width: int) -> BoardStateDict:
    """Initializes the state dictionary required for board generation."""
    return {
        "grid": create_empty_grid(height, width),
        "placed_words_coords": {},
        "placed_letter_coords": {},
        "used_middle_word_coords": set(),
        "middle_word_coords": set(),
    }


def place_middle_word(state: BoardStateDict, middle_word: str) -> bool:
    """Places the initial diagonal middle word onto the grid and updates state."""
    grid: list[list[str | None]] = state["grid"]
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    middle_word_placement_coords = calculate_middle_word_placement_coords(height, width, middle_word)
    if middle_word_placement_coords is None:
        return False

    place_letters_on_grid(grid, middle_word, middle_word_placement_coords)
    update_placed_letter_coords(state["placed_letter_coords"], middle_word, middle_word_placement_coords)
    state["placed_words_coords"][middle_word] = middle_word_placement_coords
    state["middle_word_coords"] = set(middle_word_placement_coords)
    return True


def place_other_words(state: BoardStateDict, words_to_place: list[str], max_total_words: int) -> None:
    """Attempts to place the remaining words onto the grid."""
    grid: list[list[str | None]] = state["grid"]
    placed_letter_coords: dict[str, list[tuple[int, int]]] = state["placed_letter_coords"]
    placed_words_coords: dict[str, list[tuple[int, int]]] = state["placed_words_coords"]
    middle_word_coords_set: set[tuple[int, int]] = state["middle_word_coords"]
    used_middle_word_coords_set: set[tuple[int, int]] = state["used_middle_word_coords"]

    # Ensure words_to_place is a set for efficient lookup in is_valid_placement
    words_to_place_as_set = set(words_to_place)
    # Also add the middle word to this set if it's not already, as it's a word on the board
    if "middle_word" in state["placed_words_coords"]:  # Assuming middle_word key exists if placed
        words_to_place_as_set.add(list(state["placed_words_coords"].keys())[0])  # Add the actual middle word string

    shuffled_words = list(words_to_place)  # These are subwords, not including middle word initially
    random.shuffle(shuffled_words)

    for word in shuffled_words:
        if word in placed_words_coords:
            continue
        if len(placed_words_coords) >= max_total_words:
            break

        possible_placements = find_possible_placements(grid, word, words_to_place_as_set, placed_letter_coords)
        priority_placements, other_placements = categorize_placement(
            possible_placements,
            middle_word_coords_set,
            used_middle_word_coords_set,
        )
        chosen_placement = select_random_placement(priority_placements, other_placements)

        if chosen_placement:
            apply_placement(
                grid,
                chosen_placement,
                placed_letter_coords,
                placed_words_coords,
                middle_word_coords_set,
                used_middle_word_coords_set,
            )


def validate_final_grid(state: BoardStateDict, min_total_words: int) -> bool:
    """Validates the generated grid against placement requirements."""
    placed_words_coords: dict[str, list[tuple[int, int]]] = state["placed_words_coords"]
    middle_word_coords_set: set[tuple[int, int]] = state["middle_word_coords"]
    used_middle_word_coords_set: set[tuple[int, int]] = state["used_middle_word_coords"]

    total_placed_count = len(placed_words_coords)
    if total_placed_count < min_total_words:
        return False
    if middle_word_coords_set and middle_word_coords_set != used_middle_word_coords_set:
        return False
    return True


def capitalize_middle_word_appearance(state: BoardStateDict, middle_word: str) -> None:
    """Capitalizes the letters of the middle word on the final grid."""
    # Ensure middle_word is in placed_words_coords before trying to access it
    if middle_word in state["placed_words_coords"]:
        middle_word_coords: list[tuple[int, int]] = state["placed_words_coords"][middle_word]
        middle_word_upper = middle_word.upper()
        place_letters_on_grid(state["grid"], middle_word_upper, middle_word_coords)


def generate_board(
    difficulty_conf: DifficultyData,
    middle_word: str,
    words_to_place: list[str],
) -> tuple[list[list[str | None]] | None, dict[str, list[tuple[int, int]]] | None]:
    """Generates the final game board and word coordinate data.

    Args:
        difficulty_conf (DifficultyData): The difficulty settings.
        middle_word (str): The chosen middle word.
        words_to_place (List[str]): The list of subwords to place.

    Returns:
        Tuple[Optional[List[List[Optional[str]]]], Optional[Dict[str, List[Tuple[int, int]]]]]:
            Grid and placed words dictionary, or (None, None) on failure.

    """
    min_total_words = difficulty_conf.words_on_board_needed.minimum
    max_total_words = difficulty_conf.words_on_board_needed.maximum
    height = difficulty_conf.grid.height
    width = difficulty_conf.grid.width

    state = initialize_board_state(height, width)

    if not place_middle_word(state, middle_word):
        return None, None

    # Pass all words that should be on the board to place_other_words for validation checks
    # This includes the middle_word itself.
    all_words_for_validation = set(words_to_place)
    all_words_for_validation.add(middle_word)

    # The 'words_to_place' list for the loop in place_other_words should be just subwords
    place_other_words(state, words_to_place, max_total_words)

    if not validate_final_grid(state, min_total_words):
        return None, None

    capitalize_middle_word_appearance(state, middle_word)

    return state["grid"], state["placed_words_coords"]
