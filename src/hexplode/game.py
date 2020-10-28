from copy import deepcopy

from hexplode.models import Tile


def place_counter(tile_id, player, board):
    """Place a single counter on tile with id tile_id"""
    if tile_id not in board.tiles:
        raise ValueError(f"No tile with id {tile_id}")

    tile = board.tiles[tile_id]

    if tile.player is not None and tile.player != player:
        raise ValueError(
            "Invalid move: tile already contains opponent's counters"
        )

    new_board = deepcopy(board)
    new_board.tiles[tile_id] = Tile(
        counters=tile.counters + 1, player=player, neighbours=tile.neighbours
    )

    return new_board
