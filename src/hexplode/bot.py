import abc
from random import choice
from typing import List

from hexplode.game import check_for_win, place_counter
from hexplode.models import Board


class BaseBot(abc.ABC):
    """
    Base class for computer players.
    """

    @abc.abstractmethod
    def choose_move(self, board: Board, player: int) -> int:
        pass


class RandomBot(BaseBot):
    """
    A bot that plays randomly.
    """

    def choose_move(self, board: Board, player: int) -> int:
        valid_choices = [
            t.id
            for t in board.tiles.values()
            if t.player is None or t.player == player
        ]
        return choice(valid_choices)


class MinMaxBot(BaseBot):
    """
    A bot that plays to minimise the worst case scenario (i.e. the impact of
    the opponent playing optimally).

    Uses alpha-beta pruning to slightly optimise search time.

    Position quality is determined by difference in score.
    """

    def __init__(self, depth: int) -> None:
        self.depth = depth

    @staticmethod
    def _get_valid_moves(player, board: Board) -> List[int]:
        # valid moves are tiles with a counter already placed, or neighbours
        # thereof. This helps reduce the search space by quite a lot leading
        # to faster decisions.
        current_tiles = [t for t in board.tiles.values() if t.player == player]
        valid_moves_set = {t.id for t in current_tiles}
        for tile in current_tiles:
            valid_moves_set.update(
                [
                    tid
                    for tid in tile.neighbours
                    if board.tiles[tid].player == player
                    or board.tiles[tid].player is None
                ]
            )
        valid_moves = [move for move in valid_moves_set]
        if not valid_moves:
            # if no tiles have been placed yet, start on a random edge tile
            valid_moves = [
                choice(
                    [
                        t.id
                        for t in board.tiles.values()
                        if len(t.neighbours) < 6 and t.player is None
                    ]
                )
            ]
        return valid_moves

    def choose_move(self, board: Board, player: int) -> int:
        def minmax(
            board: Board,
            depth: int,
            maximising_player: bool,
            alpha=-float("inf"),
            beta=float("inf"),
        ):
            if (winner := check_for_win(board)) is not None:
                if winner == player:
                    return float("inf"), None
                return float("-inf"), None
            elif depth == 0:
                return (
                    board.score.get(player, 0)
                    - board.score.get(player % 2 + 1, 0),
                    None,
                )

            current_player = player if maximising_player else player % 2 + 1
            valid_moves = self._get_valid_moves(current_player, board)

            if maximising_player:
                best_value, best_move = -float("inf"), None
            else:
                best_value, best_move = float("inf"), None

            for move in valid_moves:
                new_board = place_counter(move, current_player, board)
                value, _ = minmax(
                    board=new_board,
                    depth=depth - 1,
                    maximising_player=not maximising_player,
                )
                if maximising_player:
                    alpha = max(alpha, value)
                    if value > best_value:
                        best_value, best_move = value, move
                else:
                    beta = min(beta, value)
                    if value < best_value:
                        best_value, best_move = value, move
                if beta <= alpha:
                    break

            return best_value, best_move

        _, move = minmax(board, self.depth, True)
        return move
