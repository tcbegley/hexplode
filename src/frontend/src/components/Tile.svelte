<script>
  export let handleClick,
    w,
    disabled,
    count = 0,
    player = null;

  let colorMap = ["#cccccc", "#ff5555", "#0099ff"];
</script>

<div
  class="hexagon"
  style="--tile-width:{w}px;--tile-colour:{colorMap[player || 0]}"
>
  {count > 0 ? count : ''}
  <!-- pseudo-elements overlap, so handle click events on an inscribed circle instead -->
  <div
    class="target"
    style="--target-width:{w}px;cursor:{disabled ? 'default' : 'pointer'}"
    on:click="{() => {
      if (!disabled) {
        handleClick();
      }
    }}"
  ></div>
</div>

<style>
  .target {
    width: var(--target-width);
    height: var(--target-width);
    border-radius: 50%;
    position: absolute;
    top: calc(-0.2115 * var(--target-width));
    z-index: 1000;
  }

  .hexagon {
    color: white;
    font-size: calc(0.4 * var(--tile-width));
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background-color: var(--tile-colour);
    width: var(--tile-width);
    height: calc(0.577 * var(--tile-width));
    margin: calc(0.288 * var(--tile-width)) 0;
    margin-right: calc(0.05 * var(--tile-width));
    position: relative;
  }

  .hexagon::before,
  .hexagon::after {
    content: "";
    position: absolute;
    width: 0;
    left: 0;
    border-left: calc(0.5 * var(--tile-width)) solid transparent;
    border-right: calc(0.5 * var(--tile-width)) solid transparent;
  }

  .hexagon::before {
    bottom: 100%;
    border-bottom: calc(0.288 * var(--tile-width)) solid var(--tile-colour);
  }

  .hexagon::after {
    top: 100%;
    width: 0;
    border-top: calc(0.288 * var(--tile-width)) solid var(--tile-colour);
  }

  .hexagon:last-child {
    margin-right: 0;
  }
</style>
