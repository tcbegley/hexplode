import abc
from urllib.parse import urlparse

import asyncio_redis

from hexplode.board import create_board
from hexplode.game import place_counter
from hexplode.models import Game


class GameNotFoundError(Exception):
    pass


class GameStore(abc.ABC):
    @abc.abstractmethod
    async def connect(self) -> None:
        """
        Connect to the store. Called on application startup.
        """
        pass

    @abc.abstractmethod
    async def disconnect(self) -> None:
        """
        Disconnect from the store. Called on application shutdown.
        """
        pass

    @abc.abstractmethod
    async def _get(self, game_id: str) -> Game:
        """
        Get the current game state of game with id `game_id`.
        """
        pass

    @abc.abstractmethod
    async def _set(self, game_id: str, game: Game) -> Game:
        """
        Set the game state of game with id `game_id`.
        """
        pass

    async def create_game(self, game_id: str, size: int) -> Game:
        """
        Create a new game and save it in the store.
        """
        board = create_board(size)
        game_state = Game(id=game_id, board=board, player=1)
        return await self._set(game_id, game_state)

    async def place_counter(self, game_id: str, tile_id: int) -> Game:
        game = await self._get(game_id)

        board = place_counter(tile_id, game.player, game.board)

        return await self._set(
            game_id, Game(id=game_id, player=3 - game.player, board=board)
        )


class MemoryGameStore(GameStore):
    def __init__(self) -> None:
        self.store: dict[str, Game] = {}  # noqa

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass

    async def _get(self, game_id: str) -> Game:
        try:
            return self.store[game_id]
        except KeyError:
            raise GameNotFoundError(f"No game with id {game_id}")

    async def _set(self, game_id: str, game: Game) -> Game:
        self.store[game_id] = game
        return self.store[game_id]


class RedisGameStore(GameStore):
    def __init__(self, url: str) -> None:
        parsed_url = urlparse(url)
        self._host = parsed_url.hostname or "localhost"
        self._port = parsed_url.port or 6379

    async def connect(self) -> None:
        self._conn = await asyncio_redis.Pool.create(
            self._host, self._port, poolsize=4
        )

    async def disconnect(self) -> None:
        await self._conn.close()

    async def _get(self, game_id: str) -> Game:
        game_str = await self._conn.get(game_id)

        if game_str is None:
            raise GameNotFoundError(f"No game with id {game_id}")

        return Game.from_string(game_str)

    async def _set(self, game_id: str, game: Game) -> Game:
        await self._conn.set(game_id, game.json(), expire=3600)
        return await self._get(game_id)


def get_store(url: str) -> GameStore:
    parsed_url = urlparse(url)
    if parsed_url.scheme == "redis":
        return RedisGameStore(url)
    elif parsed_url.scheme == "memory":
        return MemoryGameStore()
    raise ValueError(f"Unsupported url: {url}")
