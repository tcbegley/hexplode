import os

from fastapi import FastAPI

from hexplode.models import Game
from hexplode.store import get_store
from hexplode.utils import generate_id

STORE = get_store(os.getenv("REDIS_URL", "memory://"))

app = FastAPI(on_startup=[STORE.connect], on_shutdown=[STORE.disconnect])


@app.post("/game", response_model=Game)
async def new_game(size: int = 4) -> Game:
    return await STORE.create_game(generate_id(), size)
