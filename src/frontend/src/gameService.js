import axios from "axios";

import { board, gameID, players } from "./stores";

let socket;

gameID.subscribe(async id => {
  if (id) {
    socket = new WebSocket(`ws://${process.env.HEXPLODE_BACKEND}/ws/${id}`);
    socket.onmessage = event => {
      const data = JSON.parse(event.data);
      if (data.action === "updateGameState") {
        board.set(data.game.board);
        players.setPlayer(data.game.player);
      } else if (data.action === "gameOver") {
        players.setWinner(data.winner);
      }
    };
    socket.onclose = event => {
      console.log("socket closed for some reason", event);
    };
  }
});

const createGame = async size => {
  let res = await axios.post(
    `http://${process.env.HEXPLODE_BACKEND}/game`,
    null,
    {
      params: { size },
    }
  );
  players.setWinner(null);
  gameID.set(res.data.id);
  board.set(res.data.board);
};

const placeCounter = (tileID, player) => {
  if (socket) {
    waitForConnection(() =>
      socket.send(
        JSON.stringify({
          action: "placeCounter",
          tile_id: tileID,
          player: player,
        })
      )
    );
  }
};

const waitForConnection = (callback, interval = 50, retries = 10) => {
  if (socket.readyState === 1) {
    return callback();
  }
  if (retries > 0) {
    setTimeout(
      () => waitForConnection(callback, interval, retries - 1),
      interval
    );
  } else {
    throw "Connection failed.";
  }
};

export { createGame, placeCounter };
