# ****************
# MAIN LOGIC
# ****************

from config import settings
from word_utils import generate_word_list
from display_utils import print_grid
from grid_utils import create_empty_grid, place_middle_word


def main():
    # CREATE WORD LIST
    word_setup_result = generate_word_list()

    if word_setup_result is None:
        raise ValueError("Failed to set up word list!")

    middle_word, words_to_place = word_setup_result

    # CREATE GRID
    grid = create_empty_grid(settings["grid"]["height"], settings["grid"]["width"])
    print_grid(grid)

    # TODO: separate functioanlities for setting letter coords dictionary
    print()
    letter_coords = {}
    middle_word_coords = place_middle_word(grid, middle_word, letter_coords)
    print_grid(grid)
    print(middle_word_coords)

    # GAMEPLAY
    ...


if __name__ == "__main__":
    main()
