import pytest

from hexplode.board import create_board


@pytest.mark.parametrize("size", list(range(1, 10)))
def test_board_size(size):
    n_tiles = (2 * size - 1) ** 2 - size * (size - 1)

    board = create_board(size)

    assert len(board.tiles) == n_tiles


@pytest.mark.parametrize("size", list(range(1, 10)))
def test_neighbours(size):
    board = create_board(size)

    for _, tile in board.tiles.items():
        assert all(isinstance(n, int) for n in tile.neighbours)
