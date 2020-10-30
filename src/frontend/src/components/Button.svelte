<script>
  export let disabled = false,
    handleClick = null;
</script>

<button on:click="{handleClick}" disabled="{disabled}"><slot /></button>

<style>
  button {
    display: block;
    font-weight: 400;
    text-align: center;
    border: 1px solid rgb(193, 42, 47);
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    border-radius: 0.25rem;
    transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out,
      border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    color: #fff;
    background-color: rgb(193, 42, 47);
    cursor: pointer;
    width: 100%;
  }
  button:hover:not(:disabled) {
    background-color: rgb(160, 20, 20);
    border-color: rgb(160, 20, 20);
  }
  button:disabled {
    color: #ddd;
    background-color: rgb(200, 110, 110);
    border-color: rgb(200, 110, 110);
    cursor: default;
  }
  button:not(:disabled):active {
    background-color: #ddd;
  }
  button:focus {
    border-color: #666;
  }
</style>
