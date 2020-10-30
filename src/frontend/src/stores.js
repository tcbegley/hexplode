import { writable } from "svelte/store";

const createPlayerStore = () => {
  const { subscribe, set, update } = writable({
    player1: "human",
    player2: "human",
    player: 1,
    winner: null,
  });

  return {
    subscribe,
    set,
    setPlayer: player => update(state => ({ ...state, player })),
    setWinner: winner => update(state => ({ ...state, winner })),
  };
};

export const gameID = writable(null);
export const players = createPlayerStore();
export const board = writable(null);
