# ****************
# GRID CREATION
# ****************
def create_empty_grid(height, width):
    return [[None] * width for _ in range(height)]


def place_middle_word(grid, word, letter_coords):
    height = len(grid)
    width = len(grid[0])
    word_len = len(word)

    diag_space = word_len * 2 - 1
    start_row = (height - diag_space) // 2
    start_col = (width - diag_space) // 2

    if (
        start_row < 0
        or start_col < 0
        or start_row + diag_space > height
        or start_col + diag_space > width
    ):
        print(
            f"Error: Grid ({height}x{width}) too small for placing '{word}' (LENGTH {word_len}) diagonally with spacing."
        )
        return None

    letter_coords.clear()
    middle_word_coords = set()

    row, col = start_row, start_col
    for letter in word:
        grid[row][col] = letter.upper()
        coord = (row, col)
        letter_lower = letter.lower()
        letter_coords.setdefault(letter_lower, []).append(coord)
        middle_word_coords.add(coord)
        row += 2
        col += 2

    return middle_word_coords
