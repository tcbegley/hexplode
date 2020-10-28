import os

from fastapi import FastAPI, WebSocket

from hexplode.game import check_for_win
from hexplode.models import Game
from hexplode.store import get_store
from hexplode.utils import generate_id

STORE = get_store(os.getenv("REDIS_URL", "memory://"))

app = FastAPI(on_startup=[STORE.connect], on_shutdown=[STORE.disconnect])


@app.post("/game", response_model=Game)
async def new_game(size: int = 4) -> Game:
    return await STORE.create_game(generate_id(), size)


@app.websocket("/ws/{game_id}")
async def game_ws(websocket: WebSocket, game_id: str):
    await websocket.accept()
    async for data in websocket.iter_json():
        if data["action"] == "placeCounter":
            game = await STORE.place_counter(game_id, data["tile_id"])

            await websocket.send_json(
                {"action": "updateGame", "game": game.dict()}
            )

            if winner := check_for_win(game.board) is not None:
                await websocket.send_json(
                    {"action": "gameOver", "winner": winner}
                )
