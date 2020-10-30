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
  }
});

const createGame = async size => {
  let res = await axios.post(`http://${process.env.HEXPLODE_BACKEND}/game`, {
    params: { size },
  });
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

const waitForConnection = (callback, interval = 50) => {
  if (socket.readyState === 1) {
    return callback();
  }
  setTimeout(() => waitForConnection(callback, interval), interval);
};

export { createGame, placeCounter };
