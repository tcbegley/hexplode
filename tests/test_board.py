import pytest

from hexplode.board import create_board


@pytest.mark.parametrize("size", list(range(1, 10)))
def test_board_size(size):
    n_tiles = (2 * size - 1) ** 2 - size * (size - 1)

    tiles = create_board(size)

    assert len(tiles) == n_tiles


@pytest.mark.parametrize("size", list(range(1, 10)))
def test_neighbours(size):
    tiles = create_board(size)

    for tile in tiles:
        assert all(isinstance(n, int) for n in tile["neighbours"])
