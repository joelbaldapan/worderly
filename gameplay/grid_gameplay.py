# ****************
# GRID GAMEPLAY
# ****************
import random


def create_hidden_grid(final_grid):
    return [["#" if col else None for col in row] for row in final_grid]


def reveal_coords_in_hidden_grid(final_grid, hidden_grid, coords):
    print(coords)
    for i, j in coords:
        hidden_grid[i][j] = final_grid[i][j]


# ****************
# POWER-UP
# ****************


def get_all_letter_coords(final_grid):
    all_coords = set()
    height = len(final_grid)
    width = len(final_grid[0])
    for r in range(height):
        for c in range(width):
            if final_grid[r][c] is not None:
                all_coords.add((r, c))
    return all_coords


def get_coords_for_random_reveal(hidden_letter_coords_set, min_reveal, max_reveal):
    hidden_letter_coords_list = list(hidden_letter_coords_set)

    # total number of available hidden letters
    available_to_reveal_count = len(hidden_letter_coords_list)

    # Choose a random number of letters to reveal within the specified range
    # and make suree that chosen number doesn't exceed the available hidden letters
    if available_to_reveal_count == 0:
        num_to_reveal = 0
    else:
        chosen_number = random.randint(min_reveal, max_reveal)
        num_to_reveal = min(chosen_number, available_to_reveal_count)

    # Randomly select the coordinates to reveal directly from the list of hidden coords
    # random.sample handles the case where num_to_reveal is 0 or the list is empty
    return random.sample(hidden_letter_coords_list, num_to_reveal)


def get_coords_for_word_reveal(words_to_find, correct_guesses_set):
    # Find all words that haven't been guessed yet
    unrevealed_words = [
        word for word in words_to_find.keys() if word not in correct_guesses_set
    ]

    if not unrevealed_words:
        return []

    # Randomly select one word from the unrevealed list
    chosen_word = random.choice(unrevealed_words)
    return words_to_find[chosen_word]
