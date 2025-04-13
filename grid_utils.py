# ************************************
#            GRID STUFF
# ************************************
"""
IDEA for grid creation:
- We store:
    > letter_coords (dict | key: letter, value: all coords (list))
    > possible_placements (list with dicts (keys: word, coord, idx, orientation))
    > placed_word_data (dict | key: word, value: its letter's coords (list))
    > used_middle_word_coords (set)
        - since we have to PRIORITIZE middle words
    > middle_word_coords (set)
- We keep track of the COORDINATES for:
    > POSSIBLE PLACEMENTS
    > each PLACED WORD
        - to be used for gameplay purposes!
    > each LETTERS
        - to be used for faster placements in grid
- We split the code for:
    > IMPERATIVE changing of grid
    > NON-IMPERATIVE calculations for coordinates, etc.
"""

import random
from config import settings

# ************************************
# Changing Grid (IMPERATIVE)
# ************************************


def create_empty_grid(height, width):
    return [[None] * width for _ in range(height)]


def calculate_middle_word_start(height, width, word_len):
    diag_space = word_len * 2 - 1
    start_row = (height - diag_space) // 2
    start_col = (width - diag_space) // 2

    if (
        start_row < 0
        or start_col < 0
        or start_row + diag_space > height
        or start_col + diag_space > width
    ):
        return None, None

    else:
        return start_row, start_col


def _is_within_bounds(r, c, height, width):
    return 0 <= r < height and 0 <= c < width


def place_middle_word(grid, middle_word):
    height = len(grid)
    width = len(grid[0])
    word_len = len(middle_word)

    result = calculate_middle_word_start(height, width, word_len)
    if not result:
        print(f"ERROR: Grid too small for placing '{middle_word}'")
        return None

    start_row, start_col = result
    middle_word_coords_set = set()
    initial_letter_coords = {}

    row, col = start_row, start_col
    for letter in middle_word:
        if _is_within_bounds(row, col, height, width):
            grid[row][col] = letter.upper()
            coord = (row, col)
            middle_word_coords_set.add(coord)
            initial_letter_coords.setdefault(letter, []).append(coord)
            row += 2
            col += 2
        else:
            print(
                f"ERROR: Calculated position ({row},{col}) for middle word is out of bounds"
            )
            return None, None

    return middle_word_coords_set, initial_letter_coords


def place_word_on_grid(grid, word, start_row, start_col, orientation):
    dr, dc = (1, 0) if orientation == "V" else (0, 1)
    placed_coords = []
    for i, letter in enumerate(word):
        current_row = start_row + i * dr
        current_col = start_col + i * dc
        grid[current_row][current_col] = letter
        placed_coords.append((current_row, current_col))
    return placed_coords


# ************************************
# Placement Validation Logic
# ************************************


def _check_parallel_cells(grid, r, c, dr, dc):
    height = len(grid)
    width = len(grid[0])
    perp_dr, perp_dc = dc, dr

    check_r1, check_c1 = r - perp_dr, c - perp_dc
    neighbor1_occupied = (
        _is_within_bounds(check_r1, check_c1, height, width)
        and grid[check_r1][check_c1] is not None
    )

    check_r2, check_c2 = r + perp_dr, c + perp_dc
    neighbor2_occupied = (
        _is_within_bounds(check_r2, check_c2, height, width)
        and grid[check_r2][check_c2] is not None
    )

    return not (neighbor1_occupied or neighbor2_occupied)


def _check_adjacent_before_start(grid, start_row, start_col, dr, dc):
    height = len(grid)
    width = len(grid[0])
    before_r, before_c = start_row - dr, start_col - dc

    cell_occupied = (
        _is_within_bounds(before_r, before_c, height, width)
        and grid[before_r][before_c] is not None
    )
    return not cell_occupied


def _check_adjacent_after_end(grid, end_row, end_col, dr, dc):
    height = len(grid)
    width = len(grid[0])
    after_r, after_c = end_row + dr, end_col + dc

    cell_occupied = (
        _is_within_bounds(after_r, after_c, height, width)
        and grid[after_r][after_c] is not None
    )
    return not cell_occupied


def _check_for_all_letters(word, grid, word_len, start_row, start_col, dr, dc):
    placed_new_letter = False
    for i in range(word_len):
        current_row = start_row + i * dr
        current_col = start_col + i * dc
        existing_char = grid[current_row][current_col]

        if existing_char:
            if existing_char.lower() != word[i].lower():
                return False
        else:
            placed_new_letter = True

            if not _check_parallel_cells(grid, current_row, current_col, dr, dc):
                return False

    # Check if we placed new letter  
    return placed_new_letter


def is_valid_placement(
    grid,
    word,
    intersect_row,
    intersect_col,
    intersect_idx,
    orientation,
):
    height = settings["grid"]["height"]
    width = settings["grid"]["width"]
    word_len = len(word)

    dr, dc = (1, 0) if orientation == "V" else (0, 1)
    start_row = intersect_row - intersect_idx * dr
    start_col = intersect_col - intersect_idx * dc
    end_row = start_row + (word_len - 1) * dr
    end_col = start_col + (word_len - 1) * dc

    # Check if within bounds
    if not (
        _is_within_bounds(start_row, start_col, height, width)
        and _is_within_bounds(end_row, end_col, height, width)
    ):
        return False

    # Check if no words adjacent at the start and at the end
    if not (
        _check_adjacent_before_start(grid, start_row, start_col, dr, dc)
        and _check_adjacent_after_end(grid, end_row, end_col, dr, dc)
    ):
        return False
    
    # Check if no words parallel for all letters
    if not _check_for_all_letters(word, grid, word_len, start_row, start_col, dr, dc):
        return False

    return True


# ***************************************
# Placement Finding, Selecting, Applying
# ***************************************


def find_possible_placements(grid, word, letter_coords):
    possible_placements = []

    # For every word, and for every letter, find ALL valid placements for HORIZONTAL and VERTICAL
    for idx, letter in enumerate(word):
        if letter not in letter_coords:
            continue

        for coord in letter_coords[letter]:
            intersect_row, intersect_col = coord

            # VERTICAL
            if is_valid_placement(grid, word, intersect_row, intersect_col, idx, "V"):
                possible_placements.append(
                    {
                        "word": word,
                        "coord": coord,
                        "idx": idx,
                        "orientation": "V",
                    }
                )

            # HORIZONTAL
            if is_valid_placement(grid, word, intersect_row, intersect_col, idx, "H"):
                possible_placements.append(
                    {
                        "word": word,
                        "coord": coord,
                        "idx": idx,
                        "orientation": "H",
                    }
                )

    return possible_placements


def categorize_and_select_placement(
    possible_placements, middle_word_coords_set, used_middle_word_coords_set
):
    priority_placements = []
    other_placements = []

    # We have to prioritize placing the middle words,
    # so we'll split coords based on whether they're in middle_words_set
    for placement in possible_placements:
        if (
            placement["coord"] in middle_word_coords_set
            and placement["coord"] not in used_middle_word_coords_set
        ):
            priority_placements.append(placement)
        else:
            other_placements.append(placement)

    if priority_placements:
        return random.choice(priority_placements)
    elif other_placements:
        return random.choice(other_placements)
    else:
        return None


def apply_placement(
    grid,
    chosen_placement,
    letter_coords,
    placed_words_data,
    middle_word_coords,
    used_middle_word_coords,
):
    word = chosen_placement["word"]
    intersect_row, intersect_col = chosen_placement["coord"]
    intersect_idx = chosen_placement["idx"]
    orientation = chosen_placement["orientation"]

    dr, dc = (1, 0) if orientation == "V" else (0, 1)
    start_row = intersect_row - intersect_idx * dr
    start_col = intersect_col - intersect_idx * dc

    placed_coords = place_word_on_grid(grid, word, start_row, start_col, orientation)

    # Update dictionaries and set
    placed_words_data[word] = placed_coords
    update_letter_coords(letter_coords, word, placed_coords)

    # Mark middle word coordinate as used if was intersected
    if chosen_placement["coord"] in middle_word_coords:
        used_middle_word_coords.add(chosen_placement["coord"])


# ************************************
# Grid Validation
# ************************************


def validate_final_grid(
    placed_words_data,
    min_total_words,
    middle_word_coords_set,
    used_middle_word_coords_set,
):
    total_placed_count = len(placed_words_data)

    # Placed words must be above minimum
    if total_placed_count < min_total_words:
        return False

    # ALL middle word letters must be used
    if middle_word_coords_set != used_middle_word_coords_set:
        return False

    return True


# ************************************
# Board Generation
# ************************************


def update_letter_coords(letter_coords, word, placed_coords):
    for i, coord in enumerate(placed_coords):
        letter = word[i]
        if letter in letter_coords:
            if coord not in letter_coords[letter]:
                letter_coords[letter].append(coord)
        else:
            letter_coords[letter] = [coord]


def generate_board(middle_word, words_to_place):
    min_total_words = settings["words_on_board"]["minimum"]
    max_total_words = settings["words_on_board"]["maximum"]
    height = settings["grid"]["height"]
    width = settings["grid"]["width"]

    grid = create_empty_grid(height, width)
    placed_words_data = {}
    letter_coords = {}
    used_middle_word_coords = set()

    # PLACE MIDDLE WORD
    middle_word_coords, letter_coords = place_middle_word(grid, middle_word)
    if middle_word_coords is None:
        print(f"Failed to place the initial middle word: {middle_word}")
        return None, None
    else:
        placed_words_data[middle_word] = list(middle_word_coords)

    # Shuffle for randomness
    random.shuffle(words_to_place)

    # TRY TO PLACE ALL WORDS
    for word in words_to_place:
        if word in placed_words_data:
            continue

        if len(placed_words_data) >= max_total_words:
            break

        possible_placements = find_possible_placements(grid, word, letter_coords)
        chosen_placement = categorize_and_select_placement(
            possible_placements, middle_word_coords, used_middle_word_coords
        )

        if chosen_placement:
            apply_placement(
                grid,
                chosen_placement,
                letter_coords,
                placed_words_data,
                middle_word_coords,
                used_middle_word_coords,
            )

    # CHECK IF GRID IS VALID
    is_valid_grid = validate_final_grid(
        placed_words_data,
        min_total_words,
        middle_word_coords,
        used_middle_word_coords,
    )

    if is_valid_grid:
        print(f"\nGENERATED GRID: {len(placed_words_data)} words.")
        place_middle_word(grid, middle_word)  # capitalize middle word
        return grid, placed_words_data
    else:
        return None, None
