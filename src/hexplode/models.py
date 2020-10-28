from typing import Dict, List, Optional

from pydantic import BaseModel, root_validator


class Tile(BaseModel):
    counters: int
    player: Optional[int]
    neighbours: List[int]

    @root_validator
    def player_set_if_counters_placed(cls, values):
        counters = values.get("counters")
        player = values.get("player")

        if counters > 0 and player is None:
            raise ValueError("Player must be set if tile contains counters")
        return values


class Board(BaseModel):
    tiles: Dict[int, Tile]
