# ************************************
#            GRID STUFF
# ************************************
"""
IDEA for grid creation:
- We store:
    > placed_letter_coords (dict | key: letter, value: all coords (list))
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

# ************************************
# Changing Grid (IMPERATIVE)
# ************************************


def create_empty_grid(height, width):
    return [[None] * width for _ in range(height)]


def place_letters_on_grid(grid, word, coords_to_place):
    for idx, coord in enumerate(coords_to_place):
        row, col = coord
        grid[row][col] = word[idx]


# ***********************************************
# Updating Coordinates Data Logic (IMPERATIVE)
# ***********************************************
def update_placed_word_coords(
    chosen_placement,
    coords_to_place,
    placed_words_coords,
    middle_word_coords,
    used_middle_word_coords,
):
    word = chosen_placement["word"]
    intersection_coord = chosen_placement["coord"]

    # Update placed words data
    placed_words_coords[word] = coords_to_place

    # Mark middle word coordinate as used if was intersected
    if intersection_coord in middle_word_coords:
        used_middle_word_coords.add(chosen_placement["coord"])


def update_placed_letter_coords(placed_letter_coords, word, placed_coords):
    for i, coord in enumerate(placed_coords):
        letter = word[i]
        if letter in placed_letter_coords:
            if coord not in placed_letter_coords[letter]:
                placed_letter_coords[letter].append(coord)
        else:
            placed_letter_coords[letter] = [coord]


# ************************************
# Placement Validation Logic
# ************************************


def _is_within_bounds(r, c, height, width):
    return 0 <= r < height and 0 <= c < width


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


def _check_for_all_letters(
    grid, word, words_to_place, word_len, start_row, start_col, dr, dc
):
    placed_new_letter = False
    checked_letters = ""
    for i in range(word_len):
        current_row = start_row + i * dr
        current_col = start_col + i * dc

        current_cell = grid[current_row][current_col]

        if current_cell:
            # If the cell is occupied
            checked_letters += current_cell
            if current_cell.lower() != word[i].lower():
                return False  # Conflict with another word
        else:
            # If the cell is empty
            placed_new_letter = True

            # Check cells that are parallel to current cell
            if not _check_parallel_cells(grid, current_row, current_col, dr, dc):
                return False

        if checked_letters in words_to_place:
            return False  # Overwriting an already placed word

    # Check if we placed new letter
    return placed_new_letter


def is_valid_placement(
    grid,
    word,
    words_to_place,
    intersect_row,
    intersect_col,
    intersect_idx,
    orientation,
):
    height = len(grid)
    width = len(grid[0])
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
    if not _check_for_all_letters(
        grid, word, words_to_place, word_len, start_row, start_col, dr, dc
    ):
        return False

    return True


# ******************************************************
# Placement Finding, Categorizing, Selecting, Applying
# ******************************************************


def find_possible_placements(grid, word, words_to_place, placed_letter_coords):
    possible_placements = []

    # For every word, and for every letter,
    # find ALL valid placements for HORIZONTAL and VERTICAL
    for idx, letter in enumerate(word):
        if letter not in placed_letter_coords:
            continue

        for coord in placed_letter_coords[letter]:
            intersect_row, intersect_col = coord

            # VERTICAL
            if is_valid_placement(
                grid, word, words_to_place, intersect_row, intersect_col, idx, "V"
            ):
                possible_placements.append(
                    {
                        "word": word,
                        "coord": coord,
                        "idx": idx,
                        "orientation": "V",
                    }
                )

            # HORIZONTAL
            if is_valid_placement(
                grid, word, words_to_place, intersect_row, intersect_col, idx, "H"
            ):
                possible_placements.append(
                    {
                        "word": word,
                        "coord": coord,
                        "idx": idx,
                        "orientation": "H",
                    }
                )

    return possible_placements


def categorize_placement(
    possible_placements, middle_word_coords, used_middle_word_coords_set
):
    priority_placements = []
    other_placements = []

    # We have to prioritize placing the middle words,
    # so we'll split coords based on whether they're in middle_words_set
    for placement in possible_placements:
        if (
            placement["coord"] in middle_word_coords
            and placement["coord"] not in used_middle_word_coords_set
        ):
            priority_placements.append(placement)
        else:
            other_placements.append(placement)
    return priority_placements, other_placements


def select_random_placement(priority_placements, other_placements):
    if priority_placements:
        return random.choice(priority_placements)
    elif other_placements:
        return random.choice(other_placements)
    else:
        return None


def apply_placement(
    grid,
    chosen_placement,
    placed_letter_coords,
    placed_words_coords,
    middle_word_coords,
    used_middle_word_coords,
):
    # Calculate PLACEMENT COORDS
    word = chosen_placement["word"]
    coords_to_place = calculate_straight_word_placement_coords(chosen_placement)

    # Update letter coords and
    # Update word coords
    update_placed_letter_coords(placed_letter_coords, word, coords_to_place)
    update_placed_word_coords(
        chosen_placement,
        coords_to_place,
        placed_words_coords,
        middle_word_coords,
        used_middle_word_coords,
    )

    # Place letters on the grid
    place_letters_on_grid(grid, word, coords_to_place)


# ************************************
# Calculating Coordinates Logic
# ************************************
def _calculate_middle_word_start(height, width, word_len):
    diag_space = word_len * 2 - 1
    start_row = (height - diag_space) // 2
    start_col = (width - diag_space) // 2

    if (
        start_row < 0
        or start_col < 0
        or start_row + diag_space > height
        or start_col + diag_space > width
    ):
        return None
    else:
        return start_row, start_col


def calculate_middle_word_placement_coords(height, width, middle_word):
    result = _calculate_middle_word_start(height, width, len(middle_word))
    if not result:
        # print(
        #     f"ERROR: Grid too small for calculating middle word '{middle_word}' placement"
        # )
        return None

    start_row, start_col = result
    coords_to_place = []
    row, col = start_row, start_col

    for _ in middle_word:
        coord = (row, col)
        coords_to_place.append(coord)
        row += 2
        col += 2

    return coords_to_place


def calculate_straight_word_placement_coords(chosen_placement):
    word = chosen_placement["word"]
    intersect_row, intersect_col = chosen_placement["coord"]
    intersect_idx = chosen_placement["idx"]
    orientation = chosen_placement["orientation"]
    word_len = len(word)

    # Calculate start position
    dr, dc = (1, 0) if orientation == "V" else (0, 1)
    start_row = intersect_row - intersect_idx * dr
    start_col = intersect_col - intersect_idx * dc

    coords_to_place = []
    for i in range(word_len):
        current_row = start_row + i * dr
        current_col = start_col + i * dc
        coords_to_place.append((current_row, current_col))

    return coords_to_place


# ************************************
# MAIN BOARD GENERATION HELPERS
# ************************************


def initialize_board_state(height, width):
    return {
        "grid": create_empty_grid(height, width),
        "placed_words_coords": {},
        "placed_letter_coords": {},
        "used_middle_word_coords": set(),
        "middle_word_coords": set(),
    }


def place_middle_word(state, middle_word):
    grid = state["grid"]
    height = len(grid)
    width = len(grid[0])

    middle_word_placement_coords = calculate_middle_word_placement_coords(
        height, width, middle_word
    )
    if middle_word_placement_coords is None:
        # print(f"ERROR: Grid too small for middle word '{middle_word}'")
        return False  # FAIL

    grid = state["grid"]
    placed_letter_coords = state["placed_letter_coords"]
    placed_words_coords = state["placed_words_coords"]

    place_letters_on_grid(grid, middle_word, middle_word_placement_coords)
    update_placed_letter_coords(
        placed_letter_coords, middle_word, middle_word_placement_coords
    )
    placed_words_coords[middle_word] = middle_word_placement_coords
    state["middle_word_coords"] = set(middle_word_placement_coords)

    return True  # ALL GOOD


def place_other_words(state, words_to_place, max_total_words):
    grid = state["grid"]
    placed_letter_coords = state["placed_letter_coords"]
    placed_words_coords = state["placed_words_coords"]
    middle_word_coords = state["middle_word_coords"]
    used_middle_word_coords = state["used_middle_word_coords"]

    shuffled_words = list(words_to_place)
    random.shuffle(shuffled_words)

    for word in shuffled_words:
        if word in placed_words_coords:
            continue

        if len(placed_words_coords) >= max_total_words:
            break

        possible_placements = find_possible_placements(
            grid, word, words_to_place, placed_letter_coords
        )
        priority_placements, other_placements = categorize_placement(
            possible_placements, middle_word_coords, used_middle_word_coords
        )
        chosen_placement = select_random_placement(
            priority_placements, other_placements
        )

        if chosen_placement:
            apply_placement(
                grid,
                chosen_placement,
                placed_letter_coords,
                placed_words_coords,
                middle_word_coords,
                used_middle_word_coords,
            )


def validate_final_grid(state, min_total_words):
    placed_words_coords = state["placed_words_coords"]
    middle_word_coords = state["middle_word_coords"]
    used_middle_word_coords_set = state["used_middle_word_coords"]

    total_placed_count = len(placed_words_coords)

    # Placed words must be ABOVE MINIMUM
    if total_placed_count < min_total_words:
        return False

    # ALL middle word letters must be used
    if middle_word_coords != used_middle_word_coords_set:
        return False

    return True


def capitalize_middle_word_appearance(state, middle_word):
    middle_word_coords = state["placed_words_coords"][middle_word]
    middle_word_upper = middle_word.upper()
    place_letters_on_grid(state["grid"], middle_word_upper, middle_word_coords)


# ************************************
# MAIN BOARD GENERATION FUNCTION
# ************************************


def generate_board(settings, middle_word, words_to_place):
    min_total_words = settings["words_on_board_needed"]["minimum"]
    max_total_words = settings["words_on_board_needed"]["maximum"]
    height = settings["grid"]["height"]
    width = settings["grid"]["width"]

    # INITIALIZE GRID
    state = initialize_board_state(height, width)

    # PLACE MIDDLE WORD
    if not place_middle_word(state, middle_word):
        return None, None  # Failed!

    # PLACE OTHER WORDS
    place_other_words(state, words_to_place, max_total_words)

    # VALIDATE FINAL GRID
    is_valid = validate_final_grid(state, min_total_words)

    if not is_valid:
        # print("\nFAILED to generate a valid grid satisfying all conditions")
        return None, None

    # CAPITALIZE MIDDLE WORD
    capitalize_middle_word_appearance(state, middle_word)

    # RETURN RESULT
    return state["grid"], state["placed_words_coords"]
