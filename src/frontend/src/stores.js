import { writable } from "svelte/store";

const createPlayerStore = () => {
  const { subscribe, set, update } = writable({
    player1: null,
    player2: null,
    player: null,
    winner: null,
  });

  return {
    subscribe,
    set,
    setPlayer: player => update(state => ({ ...state, player })),
    setWinner: winner => update(state => ({ ...state, winner })),
    setPlayer1: player1 => update(state => ({ ...state, player1 })),
    setPlayer2: player2 => update(state => ({ ...state, player2 })),
  };
};

export const gameID = writable(null);
export const players = createPlayerStore();
export const board = writable(null);
