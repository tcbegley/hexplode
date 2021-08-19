<script>
  import { board, players } from "./stores";
  import Board from "./components/Board.svelte";
  import CreateGame from "./components/CreateGame.svelte";
  import GameOver from "./components/GameOver.svelte";

</script>

{#if $board}
  {#if $players.winner}
    <GameOver />
  {/if}
  <Board size="{$board.size}" />
{:else}
  <CreateGame />
{/if}
