from dataclasses import dataclass, field


@dataclass
class PlacementDetail:
    """Represents the details of a potential or chosen word placement."""

    word: str
    coord: tuple[int, int]  # Intersection coordinate on the grid
    idx: int  # Index in 'word' that matches the letter at 'coord'
    orientation: str  # "V" for vertical, "H" for horizontal


@dataclass
class BoardGenerationState:
    """Holds the mutable state during the board generation process."""

    grid: list[list[str | None]]
    placed_words_coords: dict[str, list[tuple[int, int]]] = field(default_factory=dict)
    placed_letter_coords: dict[str, list[tuple[int, int]]] = field(default_factory=dict)
    used_middle_word_coords: set[tuple[int, int]] = field(default_factory=set)
    middle_word_coords: set[tuple[int, int]] = field(default_factory=set)


def create_empty_grid(height: int, width: int) -> list[list[str | None]]:
    """Creates a 2D list representing an empty grid filled with None."""
    return [[None] * width for _ in range(height)]


def place_letters_on_grid(grid: list[list[str | None]], word: str, coords_to_place: list[tuple[int, int]]) -> None:
    """Places the letters of a word onto the grid at specified coordinates."""
    for idx, coord_pair in enumerate(coords_to_place):
        row, col = coord_pair
        if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
            grid[row][col] = word[idx]


def initialize_board_state(height: int, width: int) -> BoardGenerationState:
    """Initializes the state object required for board generation."""
    return BoardGenerationState(grid=create_empty_grid(height, width))


def _calculate_middle_word_start(height: int, width: int, word_len: int) -> tuple[int, int] | None:
    """Calculates the starting (top-left) coordinate for diagonal middle word."""
    diag_space = word_len * 2 - 1
    start_row = (height - diag_space) // 2
    start_col = (width - diag_space) // 2
    if start_row < 0 or start_col < 0 or start_row + diag_space > height or start_col + diag_space > width:
        return None
    return start_row, start_col


def calculate_middle_word_placement_coords(height: int, width: int, middle_word: str) -> list[tuple[int, int]] | None:
    """Calculates the list of diagonal coordinates for the middle word."""
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


def calculate_straight_word_placement_coords(chosen_placement: PlacementDetail) -> list[tuple[int, int]]:
    """Calculates the list of coordinates for a straight (H or V) placement."""
    word_len = len(chosen_placement.word)
    dr, dc = (1, 0) if chosen_placement.orientation == "V" else (0, 1)

    start_row = chosen_placement.coord[0] - chosen_placement.idx * dr
    start_col = chosen_placement.coord[1] - chosen_placement.idx * dc

    coords_to_place: list[tuple[int, int]] = []
    for i in range(word_len):
        coords_to_place.append((start_row + i * dr, start_col + i * dc))
    return coords_to_place
