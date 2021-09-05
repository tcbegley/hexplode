from copy import deepcopy
from typing import Optional

from hexplode.models import Board


def check_for_win(board: Board) -> Optional[int]:
    """
    Return id of winning player. Game ends when both players have played at
    least one counter and one player has captured all other counters on the
    board.
    """
    score = board.score

    # no winners until both players have made at least one move
    if len(score) <= 1:
        return None

    if len(players := [p for p, s in score.items() if s != 0]) == 1:
        return players[0]

    return None


def place_counter(tile_id: int, player: int, board: Board) -> Board:
    """
    Place a single counter on tile with id tile_id.
    """
    if tile_id not in board.tiles:
        raise ValueError(f"No tile with id {tile_id}")

    tile = board.tiles[tile_id]

    if tile.player is not None and tile.player != player:
        raise ValueError(
            "Invalid move: tile already contains opponent's counters"
        )

    new_board = deepcopy(board)
    new_board.increment(tile_id, player)

    return _explode(new_board)


def _explode(board: Board) -> Board:
    """
    Explode counters onto neighbouring tiles if it has as many counters as
    neighbours.
    """

    def get_update_candidates():
        return [
            tile
            for tile in board.tiles.values()
            if tile.count >= len(tile.neighbours)
        ]

    while to_update := get_update_candidates():
        if check_for_win(board):
            break

        for tile in to_update:
            for nbr_id in tile.neighbours:
                board.increment(nbr_id, tile.player)

            board.decrement(tile.id, len(tile.neighbours))

    return board
