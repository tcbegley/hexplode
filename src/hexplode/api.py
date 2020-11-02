import os

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from hexplode.bot import RandomBot
from hexplode.game import check_for_win
from hexplode.models import Game
from hexplode.store import get_store
from hexplode.utils import generate_id

STORE = get_store(os.getenv("REDIS_URL", "memory://"))
BOTS = [{"label": "Random", "value": "random"}]
BOT_LOOKUP = {"random": RandomBot()}

app = FastAPI(on_startup=[STORE.connect], on_shutdown=[STORE.disconnect])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/bots")
async def available_bots():
    return BOTS


@app.post("/game", response_model=Game)
async def new_game(size: int = 4) -> Game:
    return await STORE.create_game(generate_id(), size)


@app.websocket("/ws/{game_id}")
async def game_ws(websocket: WebSocket, game_id: str):
    await websocket.accept()
    async for data in websocket.iter_json():
        if data["action"] in ["placeCounter", "requestMove"]:
            if data["action"] == "placeCounter":
                tile_id = data["tile_id"]
            elif data["action"] == "requestMove":
                bot = data["bot"]
                player = data["player"]
                game = await STORE._get(game_id)

                tile_id = BOT_LOOKUP[bot].choose_move(game.board, player)

            game = await STORE.place_counter(game_id, tile_id)

            await websocket.send_json(
                {"action": "updateGameState", "game": game.dict()}
            )

            if (winner := check_for_win(game.board)) is not None:
                await websocket.send_json(
                    {"action": "gameOver", "winner": winner}
                )
