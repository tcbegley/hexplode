<script>
  export let min, max;
</script>

<input type="range" min="{min}" max="{max}" />

<style>
  input {
    width: 100%;
    height: 1.4rem;
    padding: 0;
    background-color: transparent;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
  }

  input:focus {
    outline: none;
  }

  input:focus::-webkit-slider-thumb {
    box-shadow: 0 0 0 1px #fff, 0 0 0 0.2rem rgba(255, 150, 150, 0.25);
  }

  input:focus::-moz-range-thumb {
    box-shadow: 0 0 0 1px #fff, 0 0 0 0.2rem rgba(255, 150, 150, 0.25);
  }

  input::-moz-focus-outer {
    border: 0;
  }

  input::-webkit-slider-thumb {
    width: 1rem;
    height: 1rem;
    margin-top: -0.25rem;
    background-color: #ff3e00;
    border: 0;
    border-radius: 1rem;
    -webkit-transition: background-color 0.15s ease-in-out,
      border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    transition: background-color 0.15s ease-in-out,
      border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    -webkit-appearance: none;
    appearance: none;
  }

  input::-webkit-slider-thumb:active {
    background-color: #ffaaaa;
  }

  input::-webkit-slider-runnable-track {
    width: 100%;
    height: 0.5rem;
    color: transparent;
    cursor: pointer;
    background-color: #dee2e6;
    border-color: transparent;
    border-radius: 1rem;
  }

  input::-moz-range-thumb {
    width: 1rem;
    height: 1rem;
    background-color: #ff3e00;
    border: 0;
    border-radius: 1rem;
    -moz-transition: background-color 0.15s ease-in-out,
      border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    transition: background-color 0.15s ease-in-out,
      border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    -moz-appearance: none;
    appearance: none;
  }

  input::-moz-range-thumb:active {
    background-color: #ffaaaa;
  }

  input::-moz-range-track {
    width: 100%;
    height: 0.5rem;
    color: transparent;
    cursor: pointer;
    background-color: #dee2e6;
    border-color: transparent;
    border-radius: 1rem;
  }
</style>
