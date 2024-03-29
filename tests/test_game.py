import itertools

import pytest

from hexplode.board import create_board
from hexplode.game import check_for_win, place_counter
from hexplode.models import Board, Tile


@pytest.mark.parametrize(
    "tile_id_1,tile_id_2,repeat", [(1, 2, 1), (2, 3, 2), (5, 6, 3)]
)
def test_place_count_on_empty(tile_id_1, tile_id_2, repeat):
    board = create_board(3)

    for _ in range(repeat):
        board = place_counter(tile_id_1, 1, board)
        board = place_counter(tile_id_2, 2, board)

    assert board.tiles[tile_id_1].count == repeat
    assert board.tiles[tile_id_2].count == repeat
    assert all(
        tile.count == 0
        for id_, tile in board.tiles.items()
        if id_ not in (tile_id_1, tile_id_2)
    )


def test_disallow_placement_on_opponent():
    board = create_board(3)

    board = place_counter(1, 1, board)

    with pytest.raises(ValueError):
        place_counter(1, 2, board)


@pytest.mark.parametrize(
    "tile_id,player", itertools.product(range(1, 20), [1, 2])
)
def test_explode(tile_id, player):
    board = create_board(3)

    n_neighbours = len(board.tiles[tile_id].neighbours)

    for _ in range(n_neighbours):
        board = place_counter(tile_id, player, board)

    assert board.tiles[tile_id].count == 0
    assert board.tiles[tile_id].player is None

    for nbr_id in board.tiles[tile_id].neighbours:
        assert board.tiles[nbr_id].count == 1
        assert board.tiles[nbr_id].player == player


def test_chained_explosion():
    board = create_board(3)

    # place a counter to prevent win condition being met
    board = place_counter(10, 2, board)

    # place three count on the second tile
    for _ in range(3):
        board = place_counter(2, 2, board)

    # place three count on second tile, triggering explosion
    for _ in range(3):
        board = place_counter(1, 1, board)

    assert board.tiles[1].count == 1
    assert board.tiles[2].count == 0
    assert board.tiles[3].count == 1
    assert board.tiles[4].count == 1
    assert board.tiles[5].count == 2
    assert board.tiles[6].count == 1

    for i in [1, 3, 4, 5, 6]:
        # check successful capture
        assert board.tiles[i].player == 1


@pytest.mark.parametrize(
    "tile_id,player", itertools.product(range(1, 20), [1, 2])
)
def test_capture(tile_id, player):
    board = create_board(3)

    # place an opponent counter on each neighbour
    for nbr_id in board.tiles[tile_id].neighbours:
        board = place_counter(nbr_id, 3 - player, board)
        board = place_counter(tile_id, player, board)

    assert board.tiles[tile_id].player is None
    assert board.tiles[tile_id].count == 0

    for nbr_id in board.tiles[tile_id].neighbours:
        assert board.tiles[nbr_id].count == 2
        assert board.tiles[nbr_id].player == player


def test_win_condition():
    board = create_board(3)
    assert check_for_win(board) is None

    place_counter(1, 1, board)
    assert check_for_win(board) is None

    place_counter(2, 2, board)
    assert check_for_win(board) is None

    board = Board(
        size=0,
        score={1: 4, 2: 0},
        tiles={
            0: Tile(id=0, count=4, player=1, neighbours=[]),
            1: Tile(id=1, count=0, player=None, neighbours=[]),
        },
    )
    assert check_for_win(board) == 1
