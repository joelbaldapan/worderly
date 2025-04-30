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


def get_coords_for_random_reveal(hidden_letter_coords_set, percentage):
    # Convert set to list for random.sample
    hidden_letter_coords_list = list(hidden_letter_coords_set)

    # Calculate how many letters to reveal based on the percentage of *available* hidden letters
    num_to_reveal = int(percentage * len(hidden_letter_coords_list))

    # Ensure we don't try to reveal more than available
    num_to_reveal = min(num_to_reveal, len(hidden_letter_coords_list))

    # Randomly select the coordinates to reveal directly from the list of hidden coords
    # random.sample handles the case where num_to_reveal is 0 or list is empty
    return random.sample(hidden_letter_coords_list, num_to_reveal)


def get_coords_for_word_reveal(words_to_find, correct_guesses_set):
    # Find all words that haven't been guessed yet
    unrevealed_words = [
        word for word in words_to_find.keys() if word not in correct_guesses_set
    ]

    if not unrevealed_words:
        return []  # No unrevealed words left to reveal

    # Randomly select one word from the unrevealed list
    chosen_word = random.choice(unrevealed_words)

    # Return the list of coordinates for the chosen word
    return words_to_find[chosen_word]
