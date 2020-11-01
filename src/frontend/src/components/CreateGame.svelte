<script>
  import { createGame } from "../gameService";
  import Button from "./Button.svelte";
  import Range from "./Range.svelte";

  let size = 4;
</script>

<div class="container">
  <h1>Hexplode</h1>
  <!-- <p>Set the board size then click to get started.</p> -->
  <label for="range-input">Board size:</label>
  <div class="range-container">
    <Range
      min="3"
      max="6"
      handleChange="{value => {
        size = value;
      }}"
    /><span>{size}</span>
  </div>
  <Button handleClick="{() => createGame(size)}">Start game</Button>
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

  .range-container {
    display: flex;
    align-items: center;
    padding: 10px 0;
  }

  .range-container span {
    margin-left: 10px;
  }
</style>
