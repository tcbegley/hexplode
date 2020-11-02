import abc
from random import choice

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
