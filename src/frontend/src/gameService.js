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

players.subscribe(async ({ player1, player2, player, winner }) => {
  if (socket && player !== null && winner === null) {
    if (player === 1 && player1 !== "human") {
      waitForConnection(() =>
        socket.send(
          JSON.stringify({
            action: "requestMove",
            bot: player1,
            player: player,
          })
        )
      );
    } else if (player === 2 && player2 !== "human") {
      waitForConnection(() =>
        socket.send(
          JSON.stringify({
            action: "requestMove",
            bot: player2,
            player: player,
          })
        )
      );
    }
  }
});

const createGame = async (size, player1, player2) => {
  let res = await axios.post(
    `http://${process.env.HEXPLODE_BACKEND}/game`,
    null,
    {
      params: { size },
    }
  );
  players.set({ player1, player2, player: 1, winner: null });
  gameID.set(res.data.id);
  board.set(res.data.board);
};

const getBots = async () => {
  return await axios.get(`http://${process.env.HEXPLODE_BACKEND}/bots`);
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

export { createGame, getBots, placeCounter };
