# ****************
# DISPLAY
# ****************
def print_grid(grid):
    for row in grid:
        print(" ".join(cell if cell else "." for cell in row))
