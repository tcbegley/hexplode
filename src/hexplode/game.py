from copy import deepcopy
from typing import Optional

from hexplode.models import Board, Tile


def check_for_win(board: Board) -> Optional[int]:
    """
    Return id of winning player. Game ends when both players have played at
    least one counter and one player has captured all other counters on the
    board.
    """
    # no winners until both players have made at least one move
    if sum(t.count for t in board.tiles.values()) <= 1:
        return None

    players = [t.player for t in board.tiles.values() if t.player is not None]

    if len(set(players)) == 1:
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
    new_board.tiles[tile_id] = Tile(
        count=tile.count + 1, player=player, neighbours=tile.neighbours
    )

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
        for tile in to_update:
            n_nbrs = len(tile.neighbours)
            tile.count -= n_nbrs

            for nbr_id in tile.neighbours:
                nbr_tile = board.tiles[nbr_id]
                # spread to neighbouring tiles
                nbr_tile.count += 1
                # neighbouring tiles are conquered
                nbr_tile.player = tile.player

            if tile.count == 0:
                tile.player = None

    return board
