from typing import List, Optional


def create_board(size: int = 4):
    # first create a grid for easy calculation of neighbours
    grid = _create_grid(size)

    tiles = []

    for r, row in enumerate(grid):
        for c, id_ in enumerate(row):
            if id_ is None:
                continue

            tiles.append(
                {"id": id_, "neighbours": _get_neighbours(r, c, grid)}
            )

    return tiles


def _create_grid(size: int) -> List[List[Optional[int]]]:
    grid = []
    id_ = 1
    for i in range(2 * size - 1):
        row_length = min(size + i, 3 * size - 2 - i)

        row: List[Optional[int]] = []
        if i >= size:
            row.extend([None] * (2 * size - 1 - row_length))

        for j in range(row_length):
            row.append(id_)
            id_ += 1

        if i < size:
            row.extend([None] * (2 * size - 1 - row_length))

        grid.append(row)

    return grid


def _get_neighbours(r: int, c: int, grid: List[List[Optional[int]]]):
    grid_len = len(grid)
    perturbations = ((-1, -1), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 1))

    neighbours = []

    for dr, dc in perturbations:
        if 0 <= r + dr < grid_len and 0 <= c + dc < grid_len:
            neighbour = grid[r + dr][c + dc]
            if neighbour is not None:
                neighbours.append(neighbour)

    return neighbours
