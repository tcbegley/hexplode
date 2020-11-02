<script>
  import { onMount } from "svelte";

  import { createGame, getBots } from "../gameService";
  import Button from "./Button.svelte";
  import Range from "./Range.svelte";

  let size = 4;
  let bots = [];
  let player1, player2;

  onMount(async () => {
    let res = await getBots();
    bots = res.data;
  });
</script>

<div class="container">
  <h1>Hexplode</h1>
  <label for="player-1-select">Player 1</label>
  <select name="player-1" id="player-1-select" bind:value="{player1}">
    <option value="human">Human</option>
    {#each bots as bot}
      <option value="{bot.value}">{bot.label}</option>
    {/each}
  </select>
  <label for="player-2-select">Player 2</label>
  <select name="player-2" id="player-2-select" bind:value="{player2}">
    <option value="human">Human</option>
    {#each bots as bot}
      <option value="{bot.value}">{bot.label}</option>
    {/each}
  </select>
  <label for="range-input">Board size</label>
  <div class="range-container">
    <Range
      min="3"
      max="6"
      handleChange="{value => {
        size = value;
      }}"
    /><span>{size}</span>
  </div>
  <Button handleClick="{() => createGame(size, player1, player2)}">
    Start game
  </Button>
</div>

<style>
  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }

  label {
    font-weight: 600;
    font-size: 1.2em;
    margin-bottom: 0.5em;
  }

  select {
    display: inline-block;
    width: 100%;
    height: calc(1.5em + 0.75rem + 2px);
    padding: 0.375rem 1.75rem 0.375rem 0.75rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: #495057;
    vertical-align: middle;
    background: #fff
      url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='4' height='5' viewBox='0 0 4 5'%3e%3cpath fill='%23343a40' d='M2 0L0 2h4zm0 5L0 3h4z'/%3e%3c/svg%3e")
      no-repeat right 0.75rem center/8px 10px;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    margin-bottom: 1em;
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
    margin-bottom: 20px;
  }

  .range-container span {
    margin-left: 10px;
  }
</style>
