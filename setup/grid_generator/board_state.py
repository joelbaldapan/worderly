from dataclasses import dataclass, field


@dataclass
class PlacementDetail:
    """Represents the details of a potential or chosen word placement.

    Attributes:
        word (str): The word to be placed.
        coord (tuple[int, int]): Intersection coordinate on the grid.
        idx (int): Index in 'word' that matches the letter at 'coord'.
        orientation (str): "V" for vertical, "H" for horizontal.

    """

    word: str
    coord: tuple[int, int]
    idx: int
    orientation: str


@dataclass
class BoardGenerationState:
    """Holds the mutable state during the board generation process.

    Attributes:
        grid (list[list[str | None]]): The 2D grid representing the board.
        placed_words_coords (dict[str, list[tuple[int, int]]]): Mapping of words to their placed coordinates.
        placed_letter_coords (dict[str, list[tuple[int, int]]]): Mapping of letters to their placed coordinates.
        used_middle_word_coords (set[tuple[int, int]]): Set of coordinates used for the middle word.
        middle_word_coords (set[tuple[int, int]]): Set of coordinates for the middle word.

    """

    grid: list[list[str | None]]
    placed_words_coords: dict[str, list[tuple[int, int]]] = field(default_factory=dict)
    placed_letter_coords: dict[str, list[tuple[int, int]]] = field(default_factory=dict)
    used_middle_word_coords: set[tuple[int, int]] = field(default_factory=set)
    middle_word_coords: set[tuple[int, int]] = field(default_factory=set)


def create_empty_grid(height: int, width: int) -> list[list[str | None]]:
    """Create a 2D list representing an empty grid filled with None.

    Args:
        height (int): The number of rows in the grid.
        width (int): The number of columns in the grid.

    Returns:
        list[list[str | None]]: A 2D list of shape (height, width) filled with None.

    """
    return [[None] * width for _ in range(height)]


def place_letters_on_grid(
    grid: list[list[str | None]],
    word: str,
    coords_to_place: list[tuple[int, int]],
) -> None:
    """Place the letters of a word onto the grid at specified coordinates.

    Args:
        grid (list[list[str | None]]): The 2D grid to place letters on.
        word (str): The word whose letters are to be placed.
        coords_to_place (list[tuple[int, int]]): List of (row, col) coordinates for each letter in the word.

    """
    for idx, coord_pair in enumerate(coords_to_place):
        row, col = coord_pair
        if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
            grid[row][col] = word[idx]


def initialize_board_state(height: int, width: int) -> BoardGenerationState:
    """Initialize the state object required for board generation.

    Args:
        height (int): The number of rows in the grid.
        width (int): The number of columns in the grid.

    Returns:
        BoardGenerationState: An instance of BoardGenerationState with an empty grid.

    """
    return BoardGenerationState(grid=create_empty_grid(height, width))


def _calculate_middle_word_start(
    height: int,
    width: int,
    word_len: int,
) -> tuple[int, int] | None:
    """Calculate the starting (top-left) coordinate for diagonal middle word.

    Args:
        height (int): The number of rows in the grid.
        width (int): The number of columns in the grid.
        word_len (int): The length of the word to be placed diagonally.

    Returns:
        tuple[int, int] | None: The (row, col) coordinate to start placing the word, or None if it doesn't fit.

    """
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
    """Calculate the list of diagonal coordinates for the middle word.

    Args:
        height (int): The number of rows in the grid.
        width (int): The number of columns in the grid.
        middle_word (str): The word to be placed diagonally.

    Returns:
        list[tuple[int, int]] | None: A list of (row, col) coordinates for each letter in the word,
            or None if it doesn't fit.

    """
    start_coords = _calculate_middle_word_start(height, width, len(middle_word))
    if start_coords is None:
        return None

    start_row, start_col = start_coords
    coords_to_place: list[tuple[int, int]] = []
    current_row, current_col = start_row, start_col
    for _ in middle_word:
        coords_to_place.append((current_row, current_col))
        current_row += 2
        current_col += 2
    return coords_to_place


def calculate_straight_word_placement_coords(
    chosen_placement: PlacementDetail,
) -> list[tuple[int, int]]:
    """Calculate the list of coordinates for a straight (horizontal or vertical) word placement.

    Args:
        chosen_placement (PlacementDetail):
            PlacementDetail object describing the word, its orientation, and intersection.

    Returns:
        list[tuple[int, int]]: A list of (row, col) coordinates for each letter in the word.

    """
    word_len = len(chosen_placement.word)
    dr, dc = (1, 0) if chosen_placement.orientation == "V" else (0, 1)

    start_row = chosen_placement.coord[0] - chosen_placement.idx * dr
    start_col = chosen_placement.coord[1] - chosen_placement.idx * dc

    coords_to_place: list[tuple[int, int]] = [(start_row + i * dr, start_col + i * dc) for i in range(word_len)]
    return coords_to_place
