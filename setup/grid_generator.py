# setup/grid_generator.py

# ************************************
#         GRID GENERATION
# ************************************
import random

# ************************************
# Changing Grid (IMPERATIVE)
# ************************************


def create_empty_grid(height, width):
    """Creates a 2D list representing an empty grid filled with None.

    Args:
        height (int): The desired height of the grid (number of rows).
        width (int): The desired width of the grid (number of columns).

    Returns:
        list[list[None]]: A list of lists initialized with None values.

    """
    return [[None] * width for _ in range(height)]


def place_letters_on_grid(grid, word, coords_to_place) -> None:
    """Places the letters of a word onto the grid at specified coordinates.

    Modifies the grid in place. Assumes coordinates are valid and correspond
    to the letters in the word.

    Args:
        grid (list[list[str | None]]): The 2D grid to modify.
        word (str): The word whose letters are to be placed.
        coords_to_place (list[tuple[int, int]]): A list of (row, col) tuples
            corresponding to each letter in the word.

    Returns:
        None: Modifies the input grid directly.

    """
    for idx, coord in enumerate(coords_to_place):
        row, col = coord
        # Basic check to prevent IndexError if coords are somehow invalid
        if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
            grid[row][col] = word[idx]
        # Else: Silently ignore out-of-bounds coords (or add error handling)


# ***********************************************
# Updating Coordinates Data Logic (IMPERATIVE)
# ***********************************************
def update_placed_word_coords(
    chosen_placement,
    coords_to_place,
    placed_words_coords,
    middle_word_coords,
    used_middle_word_coords,
) -> None:
    """Updates state dictionaries after a word is successfully placed.

    Adds the word and its coordinates to `placed_words_coords`.
    Adds the intersection coordinate to `used_middle_word_coords` if it
    was part of the original middle word's coordinates.

    Args:
        chosen_placement (dict):
            Dictionary describing the placement,
            Contains 'word' (str) and 'coord' (tuple[int, int]).
        coords_to_place (list[tuple[int, int]]):
            The list of coordinates where the word's letters are to be placed.
        placed_words_coords (dict):
            Dictionary mapping placed words (str) to their coordinate lists.
            Modified in place.
        middle_word_coords (set[tuple[int, int]]):
            Set of coordinates belonging to the initially placed middle word.
        used_middle_word_coords (set[tuple[int, int]]): Set of middle word
            coordinates that have been used as intersections.
            Modified in place.

    Returns:
        None: Modifies placed_words_coords and used_middle_word_coords.

    """
    word = chosen_placement["word"]
    intersection_coord = chosen_placement["coord"]

    # Update placed words data
    placed_words_coords[word] = coords_to_place

    # Mark middle word coordinate as used if it was intersected
    if intersection_coord in middle_word_coords:
        used_middle_word_coords.add(intersection_coord)


def update_placed_letter_coords(placed_letter_coords, word, placed_coords) -> None:
    """Updates the dictionary tracking all placed letters and their coordinates.

    For each letter in the placed word, adds its coordinate to the list
    associated with that letter in the `placed_letter_coords` dictionary.
    Avoids adding duplicate coordinates for the same letter.

    Args:
        placed_letter_coords (dict): Dictionary mapping letters (str) to lists
            of coordinates (tuple[int, int]). Modified in place.
        word (str): The word that was placed.
        placed_coords (list[tuple[int, int]]): The list of coordinates where the
            word's letters were placed.

    Returns:
        None: Modifies placed_letter_coords.

    """
    for i, coord in enumerate(placed_coords):
        letter = word[i]
        if letter in placed_letter_coords:
            # Add coord only if it's not already tracked for this letter
            if coord not in placed_letter_coords[letter]:
                placed_letter_coords[letter].append(coord)
        else:
            # Initialize list if letter is new
            placed_letter_coords[letter] = [coord]


# ***************************************************
# Placement Validation Logic (And Internal Helpers)
# ***************************************************


def _is_within_bounds(r, c, height, width):
    """Checks if a given coordinate (r, c) is within the grid boundaries.

    Args:
        r (int): The row index.
        c (int): The column index.
        height (int): The total height of the grid.
        width (int): The total width of the grid.

    Returns:
        bool: True if the coordinate is within bounds, False otherwise.

    """
    return 0 <= r < height and 0 <= c < width


def _check_parallel_cells(grid, r, c, dr, dc) -> bool:
    """Checks if cells perpendicular to a given cell along a direction are empty.

    This prevents words from running parallel and adjacent to each other.

    Args:
        grid (list[list[str | None]]): The current state of the grid.
        r (int): The row index of the cell to check around.
        c (int): The column index of the cell to check around.
        dr (int): The row direction of focus (1 for Vertical, 0 for Horizontal).
        dc (int): The column direction of focus (0 for Vertical, 1 for Horizontal).

    Returns:
        bool:
            True if both perpendicular neighbors are empty or out of bounds,
            False if either perpendicular neighbor is occupied.

        For example, this placement would be invalid:
            . . . . . .
            . T E S T .
            . W O R D .
            . . . . . .

    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    # Calculate perpendicular direction vectors
    perp_dr, perp_dc = dc, dr

    # Check neighbor 1 (r - perp_dr, c - perp_dc)
    check_r1, check_c1 = r - perp_dr, c - perp_dc
    neighbor1_occupied = _is_within_bounds(check_r1, check_c1, height, width) and grid[check_r1][check_c1] is not None

    # Check neighbor 2 (r + perp_dr, c + perp_dc)
    check_r2, check_c2 = r + perp_dr, c + perp_dc
    neighbor2_occupied = _is_within_bounds(check_r2, check_c2, height, width) and grid[check_r2][check_c2] is not None

    # Return True only if BOTH neighbors are empty/OOB
    return not (neighbor1_occupied or neighbor2_occupied)


def _check_adjacent_before_start(grid, start_row, start_col, dr, dc) -> bool:
    """Checks if the cell immediately before the start of a word path is empty.

    Args:
        grid (list[list[str | None]]): The current state of the grid.
        start_row (int): The starting row index of the potential word placement.
        start_col (int): The starting column index of the potential word placement.
        dr (int): The row direction of focus (1 for Vertical, 0 for Horizontal).
        dc (int): The column direction of focus (0 for Vertical, 1 for Horizontal).

    Returns:
        bool:
            True if the cell before the start is empty or out of bounds,
            False if it is occupied.

        For example, this placement for "NEW" before "OLD" would be invalid:
            . . . . . . . .
            . N E W O L D .
            . . . . . . . .

    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    # Calculate coordinate of the cell before the start
    before_r, before_c = start_row - dr, start_col - dc

    # Check if that cell is within bounds and occupied
    cell_occupied = _is_within_bounds(before_r, before_c, height, width) and grid[before_r][before_c] is not None
    # Return True if the cell is NOT occupied
    return not cell_occupied


def _check_adjacent_after_end(grid, end_row, end_col, dr, dc) -> bool:
    """Checks if the cell immediately after the end of a word path is empty.

    Args:
        grid (list[list[str | None]]): The current state of the grid.
        end_row (int): The ending row index of the potential word placement.
        end_col (int): The ending column index of the potential word placement.
        dr (int): The row direction of focus (1 for Vertical, 0 for Horizontal).
        dc (int): The column direction of focus (0 for Vertical, 1 for Horizontal).

    Returns:
        bool:
            True if the cell after the end is empty or out of bounds,
            False if it is occupied.

        For example, this placement for "NEW" after "OLD" would be invalid:
            . . . . . . . .
            . O L D N E W .
            . . . . . . . .

    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    # Calculate coordinate of the cell after the end
    after_r, after_c = end_row + dr, end_col + dc

    # Check if that cell is within bounds and occupied
    cell_occupied = _is_within_bounds(after_r, after_c, height, width) and grid[after_r][after_c] is not None
    # Return True if the cell is NOT occupied
    return not cell_occupied


def _check_for_all_letters(
    grid,
    word,
    words_to_place,
    word_len,
    start_row,
    start_col,
    dr,
    dc,
):
    """Checks conditions along the entire path of a potential word placement.

    Verifies that for all letters in a given word:
    1. Letters match at intersections.
    2. No parallel words are adjacent to empty cells where the word would go.
    3. The placement doesn't overwrite an existing word completely.
    4. At least one new letter is placed (doesn't just trace over existing letters).

    Args:
        grid (list[list[str | None]]): The current state of the grid.
        word (str): The word being considered for placement.
        words_to_place (set[str]):
            A set of all words intended for the board
            (used to check for overwriting).
        word_len (int): The length of the word.
        start_row (int): The starting row index of the potential placement.
        start_col (int): The starting column index of the potential placement.
        dr (int): The row direction of focus (1 for Vertical, 0 for Horizontal).
        dc (int): The column direction of focus (0 for Vertical, 1 for Horizontal).

    Returns:
        bool: True if all checks pass for all letters, False otherwise.

        For example, overwriting "TOLD" over "TOLD" would be invalid:
            . . . . .    . . . . .
            . O L D . -> T O L D .
            . . . . .    . . . . .

        Or for example, placing "NEW" at "N", conflicting with "OLD" would be invalid:
            . N . O .    . N E W .
            . O . L . -> . O . L .
            . W . D .    . W . D .

    """
    placed_new_letter = False
    checked_letters = ""  # String to accumulate letters at occupied cells along path
    for i in range(word_len):
        current_row = start_row + i * dr
        current_col = start_col + i * dc

        # Should not place if path goes OOB
        if not _is_within_bounds(current_row, current_col, len(grid), len(grid[0])):
            return False

        current_cell = grid[current_row][current_col]

        if current_cell:
            # Cell is occupied: Check for letter conflict
            checked_letters += current_cell
            if current_cell.lower() != word[i].lower():
                return False  # Conflict with another word's letter
        else:
            # Cell is empty: Check for parallel conflicts
            placed_new_letter = True  # Mark that we are placing at least one letter
            if not _check_parallel_cells(grid, current_row, current_col, dr, dc):
                return False  # Parallel conflict found

        # Check if the letters collected so far form a complete existing word
        # (Prevents placing WORD on top of an existing WORD)
        if len(checked_letters) > 1 and checked_letters.lower() in words_to_place:
            # Check only if checked_letters could potentially be a word > 1 char
            # Check against lowercase version since words_to_place is lowercase
            return False  # Overwriting an already placed word

    # After checking all letters, make sure at least one new letter was placed.
    # This prevents placing a word entirely over its own existing letters.
    return placed_new_letter


def is_valid_placement(
    grid,
    word,
    words_to_place,
    intersect_row,
    intersect_col,
    intersect_idx,
    orientation,
) -> bool:
    """Determines if placing a word at a specific intersection is valid.

    Handles functions that check for bounds, adjacent cells before start/after end,
    and conditions for all letters along the word's path (conflicts, parallels,
    overwriting, new letter placement).

    Args:
        grid (list[list[str | None]]): The current state of the grid.
        word (str): The word to potentially place.
        words_to_place (set[str]): Set of all words intended for the board.
        intersect_row (int): The row index of the intersection point.
        intersect_col (int): The column index of the intersection point.
        intersect_idx (int):
            The index within the `word` that matches the letter at the
            intersection point.
        orientation (str): 'V' for vertical, 'H' for horizontal placement.

    Returns:
        bool: True if the placement is valid according to all rules, False otherwise.

    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    word_len = len(word)

    # Determine direction vectors and start/end coordinates
    dr, dc = (1, 0) if orientation == "V" else (0, 1)
    start_row = intersect_row - intersect_idx * dr
    start_col = intersect_col - intersect_idx * dc
    end_row = start_row + (word_len - 1) * dr
    end_col = start_col + (word_len - 1) * dc

    # 1.) Check if the entire word fits within bounds
    if not (
        _is_within_bounds(start_row, start_col, height, width) and _is_within_bounds(end_row, end_col, height, width)
    ):
        return False

    # 2.) Check cells immediately before the start and after the end
    if not (
        _check_adjacent_before_start(grid, start_row, start_col, dr, dc)
        and _check_adjacent_after_end(grid, end_row, end_col, dr, dc)
    ):
        return False

    # 3.) Check conditions for all letters along the path
    if not _check_for_all_letters(
        grid,
        word,
        words_to_place,
        word_len,
        start_row,
        start_col,
        dr,
        dc,
    ):
        return False

    # If all checks pass
    return True


# ******************************************************
# Placement Finding, Categorizing, Selecting, Applying
# ******************************************************


def find_possible_placements(grid, word, words_to_place, placed_letter_coords):
    """Finds all valid horizontal and vertical placements for a given word.

    Iterates through each letter of the word and checks potential intersections
    with letters already placed on the grid. Uses `is_valid_placement` to
    verify each potential placement.

    Args:
        grid (list[list[str | None]]): The current state of the grid.
        word (str): The word to find placements for.
        words_to_place (set[str]): Set of all words intended for the board.
        placed_letter_coords (dict):
            Dictionary mapping placed letters to their list of coordinates.

    Returns:
        list[dict]:
            A list of dictionaries, where each dictionary represents a valid
            placement and contains keys: 'word', 'coord' (intersection point),
            'idx' (intersection index in word), 'orientation' ('V' or 'H').

        For example:
            . . . . . .
            . T E S T .
            . . . . . .
            Placing "BET", intersecting at "E" would have:
            {
                "word": "BET",
                "coord": (1, 2),
                "idx": 1, since 'E' in "BET" is in the index 1
                "orientation": "V", since Vertical
            }

    """
    possible_placements = []

    # Iterate through each letter of the word to check for intersections
    for idx, letter in enumerate(word):
        # Skip if this letter hasn't been placed anywhere yet
        if letter not in placed_letter_coords:
            continue

        # Check against all known coordinates for this letter
        for coord in placed_letter_coords[letter]:
            intersect_row, intersect_col = coord

            # Check VERTICAL placement possibility
            if is_valid_placement(
                grid,
                word,
                words_to_place,
                intersect_row,
                intersect_col,
                idx,
                "V",
            ):
                possible_placements.append(
                    {
                        "word": word,
                        "coord": coord,
                        "idx": idx,
                        "orientation": "V",
                    },
                )

            # Check HORIZONTAL placement possibility
            if is_valid_placement(
                grid,
                word,
                words_to_place,
                intersect_row,
                intersect_col,
                idx,
                "H",
            ):
                possible_placements.append(
                    {
                        "word": word,
                        "coord": coord,
                        "idx": idx,
                        "orientation": "H",
                    },
                )

    return possible_placements


def categorize_placement(
    possible_placements,
    middle_word_coords,
    used_middle_word_coords_set,
):
    """Categorizes possible placements into priority and other lists.

    Priority is given to placements that intersect with a coordinate from the
    original middle word placement that hasn't been used as an intersection yet.

    Args:
        possible_placements (list[dict]): List of valid placement dictionaries.
        middle_word_coords (set[tuple[int, int]]):
            Set of coordinates for the original middle word.
        used_middle_word_coords_set (set[tuple[int, int]]):
            Set of middle word coordinates already used.

    Returns:
        tuple[list[dict], list[dict]]: A tuple containing two lists:
            - priority_placements: Placements intersecting unused middle coords.
            - other_placements: All other valid placements.

    """
    priority_placements = []
    other_placements = []

    for placement in possible_placements:
        # Check if intersection coord is a middle word coord and not yet used
        if placement["coord"] in middle_word_coords and placement["coord"] not in used_middle_word_coords_set:
            priority_placements.append(placement)
        else:
            other_placements.append(placement)
    return priority_placements, other_placements


def select_random_placement(priority_placements, other_placements):
    """Selects a random placement, prioritizing the priority list.

    This is done to make sure that the middle words are prioritized to have
    their letters used before placing other words.

    Args:
        priority_placements (list[dict]): List of high-priority placements.
        other_placements (list[dict]): List of standard placements.

    Returns:
        dict | None:
            A randomly chosen placement dictionary,
            or None if both input lists are empty.

    """
    if priority_placements:
        return random.choice(priority_placements)
    elif other_placements:
        return random.choice(other_placements)
    else:
        # No possible placements found
        return None


def apply_placement(
    grid,
    chosen_placement,
    placed_letter_coords,
    placed_words_coords,
    middle_word_coords,
    used_middle_word_coords,
) -> None:
    """Applies a chosen placement to the grid and updates tracking dictionaries.

    Calculates the full coordinates for the placement, updates the letter and
    word coordinate tracking, marks middle word coordinates as used if necessary,
    and places the letters onto the grid itself.

    Args:
        grid (list[list[str | None]]): The game grid (modified in place).
        chosen_placement (dict): The dictionary describing the selected placement.
        placed_letter_coords (dict): Letter coordinate tracker (modified in place).
        placed_words_coords (dict): Word coordinate tracker (modified in place).
        middle_word_coords (set): Set of original middle word coordinates.
        used_middle_word_coords (set):
            Set of used middle word coordinates (modified in place).

    Returns:
        None: Modifies grid and various tracking dictionaries/sets directly.

    """
    # Calculate the full list of coordinates for the word placement
    word = chosen_placement["word"]
    coords_to_place = calculate_straight_word_placement_coords(chosen_placement)

    # Update coordinate tracking dictionaries/sets
    update_placed_letter_coords(placed_letter_coords, word, coords_to_place)
    update_placed_word_coords(
        chosen_placement,
        coords_to_place,
        placed_words_coords,
        middle_word_coords,
        used_middle_word_coords,
    )

    # Place the actual letters onto the grid
    place_letters_on_grid(grid, word, coords_to_place)


# ************************************
# Calculating Coordinates Logic
# ************************************
def _calculate_middle_word_start(height, width, word_len):
    """Calculates the starting (top-left) coordinate for diagonal middle word.

    Determines the required diagonal space and calculates the center alignment.
    Checks if the word fits within the grid dimensions.

    Args:
        height (int): Grid height.
        width (int): Grid width.
        word_len (int): Length of the middle word.

    Returns:
        tuple[int, int] | tuple[None, None]:
            The (row, col) starting coordinates,
            or (None, None) if the word doesn't fit.

    """
    # Diagonal placement needs more space (letters + gaps)
    diag_space = word_len * 2 - 1
    # Calculate centered starting position
    start_row = (height - diag_space) // 2
    start_col = (width - diag_space) // 2

    # Check if the calculated start/end positions are within bounds
    if (
        start_row < 0
        or start_col < 0
        # Check end position based on start + space needed
        or start_row + diag_space > height  # Check if end row goes beyond height
        or start_col + diag_space > width  # Check if end col goes beyond width
    ):
        return None, None  # Word doesn't fit
    else:
        return start_row, start_col


def calculate_middle_word_placement_coords(height, width, middle_word):
    """Calculates the list of diagonal coordinates for the middle word.

    Uses _calculate_middle_word_start to find the starting point, then
    iterates through the word, incrementing row and column by 2 for each letter
    to create the diagonal placement with gaps.

    Args:
        height (int): Grid height.
        width (int): Grid width.
        middle_word (str): The middle word to place.

    Returns:
        list[tuple[int, int]] | None:
            A list of (row, col) coordinates for the diagonal placement,
            or None if the word cannot fit on the grid.

    """
    # Calculate the starting position first
    result = _calculate_middle_word_start(height, width, len(middle_word))
    # Check if _calculate_middle_word_start failed (returned None, None)
    if result == (None, None):
        # print(...) # Optional error message
        return None  # Explicitly return None if start calculation failed

    start_row, start_col = result  # Unpack only if result is valid coords
    coords_to_place = []
    row, col = start_row, start_col

    # Generate coordinates with step 2 for diagonal placement
    for _ in middle_word:
        coord = (row, col)
        coords_to_place.append(coord)
        row += 2
        col += 2

    return coords_to_place


def calculate_straight_word_placement_coords(chosen_placement):
    """Calculates the list of coordinates for a straight (H or V) placement.

    Determines the start row/col based on the intersection point, index, and
    orientation, then generates the list of coordinates along that line.

    Args:
        chosen_placement (dict):
            Dictionary describing the placement, which contains: 'word',
            'coord' (intersection point), 'idx' (intersection index in word),
            'orientation' ('V' or 'H').

    Returns:
        list[tuple[int, int]]: A list of (row, col) coordinates for the placement.

    """
    word = chosen_placement["word"]
    intersect_row, intersect_col = chosen_placement["coord"]
    intersect_idx = chosen_placement["idx"]
    orientation = chosen_placement["orientation"]
    word_len = len(word)

    # Determine direction vectors based on orientation
    dr, dc = (1, 0) if orientation == "V" else (0, 1)
    # Calculate the starting coordinate based on intersection and index
    start_row = intersect_row - intersect_idx * dr
    start_col = intersect_col - intersect_idx * dc

    # Generate the list of coordinates along the placement path
    coords_to_place = []
    for i in range(word_len):
        current_row = start_row + i * dr
        current_col = start_col + i * dc
        coords_to_place.append((current_row, current_col))

    return coords_to_place


# ************************************
# MAIN BOARD GENERATION HELPERS (Internal)
# ************************************


def initialize_board_state(height, width):
    """Initializes the state dictionary required for board generation.

    Creates an empty grid and initializes dictionaries/sets for tracking
    placed words, letters, and middle word coordinates.

    Args:
        height (int): The height of the grid.
        width (int): The width of the grid.

    Returns:
        dict: An initialized state dictionary with the following keys:
            - 'grid' (list[list[str | None]]):
                The 2D list representing the empty game grid,
                initialized with None.
            - 'placed_words_coords' (dict):
                An empty dictionary that will store placed words (str)
                mapped to their coordinate lists (list[tuple[int, int]]).
            - 'placed_letter_coords' (dict):
                An empty dictionary that will store placed letters (str)
                mapped to a list of coordinates (tuple[int, int]) where
                they appear.
            - 'used_middle_word_coords' (set):
                An empty set that will store coordinates (tuple[int, int]) of
                the middle word that have been used as intersection points.
            - 'middle_word_coords' (set): An empty set that will store the
                coordinates (tuple[int, int]) where the middle word is initially
                placed.

    """
    return {
        "grid": create_empty_grid(height, width),
        "placed_words_coords": {},
        "placed_letter_coords": {},
        "used_middle_word_coords": set(),
        "middle_word_coords": set(),
    }


def place_middle_word(state, middle_word) -> bool:
    """Places the initial diagonal middle word onto the grid and updates state.

    Calculates the placement coordinates, places the letters, and updates
    the relevant tracking dictionaries and sets within the state dictionary.

    Args:
        state (dict): The board generation state dictionary (modified in place).
        middle_word (str): The middle word to place.

    Returns:
        bool:
            True if the middle word was placed successfully, False if it
            could not fit on the grid.

    """
    grid = state["grid"]
    # Calculate grid dimensions from the state's grid
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Calculate the diagonal coordinates
    middle_word_placement_coords = calculate_middle_word_placement_coords(
        height,
        width,
        middle_word,
    )
    # Check if placement calculation failed
    if middle_word_placement_coords is None:
        # print(f"ERROR: Grid too small for middle word '{middle_word}'") # Optional debug
        return False  # FAIL

    # Get references to state components for updates
    placed_letter_coords = state["placed_letter_coords"]
    placed_words_coords = state["placed_words_coords"]

    # Place letters and update tracking data
    place_letters_on_grid(grid, middle_word, middle_word_placement_coords)
    update_placed_letter_coords(
        placed_letter_coords,
        middle_word,
        middle_word_placement_coords,
    )
    placed_words_coords[middle_word] = middle_word_placement_coords
    state["middle_word_coords"] = set(middle_word_placement_coords)

    return True  # ALL GOOD


def place_other_words(state, words_to_place, max_total_words) -> None:
    """Attempts to place the remaining words onto the grid.

    Iterates through a shuffled list of words, finds possible placements,
    prioritizes middle word intersections, selects a random valid placement,
    and applies it to the grid and state until the maximum word count is
    reached or all words have been attempted.

    Args:
        state (dict): The board generation state dictionary (modified in place).
        words_to_place (list[str]): List of words to attempt placing.
        max_total_words (int): The maximum number of words allowed on the board.

    Returns:
        None: Modifies the state dictionary in place.

    """
    # Get references to state components
    grid = state["grid"]
    placed_letter_coords = state["placed_letter_coords"]
    placed_words_coords = state["placed_words_coords"]
    middle_word_coords = state["middle_word_coords"]
    used_middle_word_coords = state["used_middle_word_coords"]

    # Shuffle words for variety in placement order
    shuffled_words = list(words_to_place)
    random.shuffle(shuffled_words)

    for word in shuffled_words:
        # Skip if already placed (e.g., as part of middle word or previous placement)
        if word in placed_words_coords:
            continue

        # Stop if maximum number of words has been reached
        if len(placed_words_coords) >= max_total_words:
            break

        # Find and evaluate possible placements for the current word
        possible_placements = find_possible_placements(
            grid,
            word,
            words_to_place,
            placed_letter_coords,
        )
        priority_placements, other_placements = categorize_placement(
            possible_placements,
            middle_word_coords,
            used_middle_word_coords,
        )
        chosen_placement = select_random_placement(
            priority_placements,
            other_placements,
        )

        # Apply the placement if a valid one was found
        if chosen_placement:
            apply_placement(
                grid,
                chosen_placement,
                placed_letter_coords,
                placed_words_coords,
                middle_word_coords,
                used_middle_word_coords,
            )


def validate_final_grid(state, min_total_words) -> bool:
    """Validates the generated grid against placement requirements.

    Checks if the minimum number of words have been placed and if all
    coordinates of the original middle word have been used as intersections.

    Args:
        state (dict): The final board generation state dictionary.
        min_total_words (int): The minimum required number of placed words.

    Returns:
        bool: True if the grid is valid, False otherwise.

    """
    placed_words_coords = state["placed_words_coords"]
    middle_word_coords = state["middle_word_coords"]
    used_middle_word_coords_set = state["used_middle_word_coords"]

    total_placed_count = len(placed_words_coords)

    # 1.) Check if minimum word count is met
    if total_placed_count < min_total_words:
        return False

    # 2.) Check if all middle word coordinates were used (if middle word exists)
    return not (middle_word_coords and middle_word_coords != used_middle_word_coords_set)


def capitalize_middle_word_appearance(state, middle_word) -> None:
    """Capitalizes the letters of the middle word on the final grid.

    Args:
        state (dict): The final board generation state dictionary.
        middle_word (str): The middle word that was placed.

    Returns:
        None: Modifies the grid within the state dictionary in place.

    """
    middle_word_coords = state["placed_words_coords"][middle_word]
    middle_word_upper = middle_word.upper()
    place_letters_on_grid(state["grid"], middle_word_upper, middle_word_coords)


# ************************************
# MAIN BOARD GENERATION FUNCTION
# ************************************


def generate_board(settings, middle_word, words_to_place):
    """Generates the final game board and word coordinate data.

    Handles functions for board generation process: initializes state, places the
    middle word, places other words, validates the result, and capitalizes
    the middle word.

    Args:
        settings (dict):
            The game settings dictionary. With the required keys:
                - 'grid' (dict with 'height', 'width'),
                - 'words_on_board_needed' (dict with 'minimum', 'maximum').
                - Other keys exist but are not directly used by this function.
        middle_word (str): The chosen middle word.
        words_to_place (list[str]): The list of subwords to place.

    Returns:
        tuple[list[list[str | None]] | None, dict | None]: A tuple containing:
            - The final generated grid (list of lists) or None if generation failed.
            - The dictionary mapping placed words to coordinates or None if failed.

    """
    # Extract necessary settings
    min_total_words = settings["words_on_board_needed"]["minimum"]
    max_total_words = settings["words_on_board_needed"]["maximum"]
    height = settings["grid"]["height"]
    width = settings["grid"]["width"]

    # Step 1. Initialize board state
    state = initialize_board_state(height, width)

    # Step 2. Place the middle word
    if not place_middle_word(state, middle_word):
        return None, None  # Failed!

    # Step 3. Place the other words
    place_other_words(state, words_to_place, max_total_words)

    # Step 4. Validate the final grid configuration
    is_valid = validate_final_grid(state, min_total_words)
    if not is_valid:
        # print("\nFAILED to generate a valid grid satisfying all conditions") # Optional debug
        return None, None

    # Step 5. Capitalize the middle word on the grid
    capitalize_middle_word_appearance(state, middle_word)

    # Step 6. Return the successful result
    return state["grid"], state["placed_words_coords"]
