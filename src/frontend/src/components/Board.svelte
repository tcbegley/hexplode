<script>
  import { placeCounter } from "../gameService";
  import { board, players } from "../stores";
  import Tile from "./Tile.svelte";

  export let size = 4;

  let containerWidth;

  // calculate a sensible tile width according to container width
  $: w = (containerWidth - 5 * 2 * (size - 1)) / (2 * size - 1);

  let rows = [];
  let id = 1;

  for (let i = 0; i < 2 * size - 1; i++) {
    let row = [];
    for (let j = 0; j < Math.min(size + i, 3 * size - 2 - i); j++) {
      row.push(id);
      id += 1;
    }
    rows.push(row);
  }
</script>

<div class="container" bind:clientWidth="{containerWidth}">
  {#each rows as row}
    <div class="row" style="margin-top:{-0.238 * w}px">
      {#each row as tileID}
        <Tile
          w="{w}"
          disabled="{$board.tiles[tileID].player && $board.tiles[tileID].player !== $players.player}"
          handleClick="{() => {
            placeCounter(tileID, $players.player);
          }}"
          count="{$board.tiles[tileID].count}"
          player="{$board.tiles[tileID].player}"
        />
      {/each}
    </div>
  {/each}
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin: auto;
    max-width: 800px;
    height: 100vh;
  }

  .row {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
  }
</style>
