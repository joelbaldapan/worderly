# ****************
# GRID GAMEPLAY
# ****************

def create_hidden_grid(final_grid):
    return [["#" if col else None for col in row] for row in final_grid]


def reveal_coords_in_hidden_grid(final_grid, hidden_grid, coords):
    print(coords)
    for i, j in coords:
        hidden_grid[i][j] = final_grid[i][j]