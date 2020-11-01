import json
from typing import Dict, List, Optional

from pydantic import BaseModel, constr, root_validator


class Tile(BaseModel):
    id: int
    count: int
    player: Optional[int]
    neighbours: List[int]

    @root_validator
    def player_set_if_counters_placed(cls, values):
        count = values.get("count")
        player = values.get("player")

        if count > 0 and player is None:
            raise ValueError("Player must be set if tile contains counters")
        return values


class Board(BaseModel):
    size: int
    tiles: Dict[int, Tile]


class Game(BaseModel):
    id: constr(regex=r"[a-z]{3}-[a-z]{4}-[a-z]{3}")  # type: ignore  # noqa
    board: Board
    player: int

    @classmethod
    def from_string(cls, game_str: str) -> "Game":
        return cls(**json.loads(game_str))
