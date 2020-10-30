<script>
  import { createGame } from "../gameService";
  import Button from "./Button.svelte";
  // import Range from "./Range.svelte";
</script>

<div class="container">
  <h1>Hexplode</h1>
  <!-- <p>Set the board size then click to get started.</p> -->
  <!-- <Range min="3" max="8" /> -->
  <Button handleClick="{() => createGame(4)}">Start game</Button>
</div>

<style>
  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }
  .container {
    max-width: 300px;
    margin: auto;
    text-align: center;
  }
</style>
