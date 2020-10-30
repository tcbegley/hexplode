<script>
  import { board, players } from "../stores";
  import Button from "./Button.svelte";
</script>

<div class="backdrop">
  <div class="modal">
    <h1>Player {$players.winner} wins!</h1>
    <Button handleClick="{() => board.set(null)}">New game</Button>
  </div>
</div>

<style>
  .backdrop {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.3);
    z-index: 1050;
    backdrop-filter: blur(5px);
  }
  .modal {
    padding: 1em 2em;
    background: white;
    border-radius: 0.25em;
    width: 400px;
    margin: 4em auto;
    text-align: center;
  }
</style>
