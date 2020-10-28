import pytest

from hexplode.board import create_board
from hexplode.game import place_counter


@pytest.mark.parametrize("tile_id,repeat", [(1, 1), (2, 2), (3, 3)])
def test_place_counters_on_empty(tile_id, repeat):
    board = create_board(3)

    for _ in range(repeat):
        board = place_counter(tile_id, 1, board)

    assert board.tiles[tile_id].counters == repeat
    assert all(
        tile.counters == 0
        for id_, tile in board.tiles.items()
        if id_ != tile_id
    )


def test_disallow_placement_on_opponent():
    board = create_board(3)

    board = place_counter(1, 1, board)

    with pytest.raises(ValueError):
        place_counter(1, 2, board)
