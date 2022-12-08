from typing import List
from util import read_file


Grid = List[List[int]]


def load_grid(filename: str) -> Grid:
    return list(map(lambda row: [int(d) for d in row], read_file(filename)))


def is_visible(row: int, col: int, grid: Grid) -> bool:

    if is_on_edge(row, col, grid):
        return True

    value = grid[row][col]

    grid_row = grid[row]
    if max(grid_row[:col]) < value:
        # visible from left
        return True
    if value > max(grid_row[col + 1 :]):
        # visible from right
        return True

    grid_col = [gr[col] for gr in grid]
    if max(grid_col[:row]) < value:
        # visible from top
        return True
    if value > max(grid_col[row + 1 :]):
        # visible from bottom
        return True

    return False


def is_on_edge(row: int, col: int, grid: Grid) -> bool:
    n_rows, n_cols = len(grid), len(grid[0])
    return (row in [0, n_rows - 1]) or (col in [0, n_cols - 1])


def scenic_score(row: int, col: int, grid: Grid) -> int:

    if is_on_edge(row, col, grid):
        return 0

    value = grid[row][col]

    def score(array, slice):
        array = [t >= value for t in array[slice]]
        if any(array):
            return array.index(True) + 1
        else:
            return len(array)

    grid_row = grid[row]
    left_dist = score(grid_row, slice(col - 1, None, -1))
    right_dist = score(grid_row, slice(col + 1, None, 1))

    grid_col = [gr[col] for gr in grid]
    top_dist = score(grid_col, slice(row - 1, None, -1))
    bottom_dist = score(grid_col, slice(row + 1, None, 1))

    return left_dist * right_dist * top_dist * bottom_dist


def n_visible_trees(grid: Grid) -> int:
    n_rows, n_cols = len(grid), len(grid[0])
    return sum(is_visible(row, col, grid) for row in range(n_rows) for col in range(n_cols))


def max_scenic_score(grid: Grid) -> int:
    n_rows, n_cols = len(grid), len(grid[0])
    return max(scenic_score(row, col, grid) for row in range(n_rows) for col in range(n_cols))


if __name__ == "__main__":

    grid = load_grid("input/test_day8.txt")
    assert n_visible_trees(grid) == 21
    assert max_scenic_score(grid) == 8

    grid = read_file("input/day8.txt")
    print(f"Part one: {n_visible_trees(grid)}")
    print(f"Part two: {max_scenic_score(grid)}")
