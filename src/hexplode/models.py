import json
from typing import Optional

from pydantic import BaseModel, constr, root_validator


class Tile(BaseModel):
    id: int
    count: int
    player: Optional[int]
    neighbours: list[int]

    @root_validator
    def player_set_if_counters_placed(cls, values):
        count = values.get("count")
        player = values.get("player")

        if count > 0 and player is None:
            raise ValueError("Player must be set if tile contains counters")
        return values

    def increment(self, player: int) -> "Tile":
        self.player = player
        self.count += 1
        return self

    def decrement(self, n: int = 1) -> "Tile":
        self.count -= n
        if self.count == 0:
            self.player = None
        return self


class Board(BaseModel):
    size: int
    score: dict[int, int]
    tiles: dict[int, Tile]

    def increment(self, tile_id: int, player: int) -> "Board":
        current_player = self.tiles[tile_id].player
        current_count = self.tiles[tile_id].count

        self.tiles[tile_id].increment(player)

        if current_player is not None and current_player != player:
            self.score[current_player] -= current_count
            self.score[player] += current_count + 1
        else:
            self.score[player] = self.score.get(player, 0) + 1

        return self

    def decrement(self, tile_id: int, n: int = 1) -> "Board":
        player = self.tiles[tile_id].player
        if player is not None:
            self.score[player] -= n
        self.tiles[tile_id].decrement(n)
        return self


class Game(BaseModel):
    id: constr(regex=r"[a-z]{3}-[a-z]{4}-[a-z]{3}")  # type: ignore  # noqa
    board: Board
    player: int

    @classmethod
    def from_string(cls, game_str: str) -> "Game":
        return cls(**json.loads(game_str))
