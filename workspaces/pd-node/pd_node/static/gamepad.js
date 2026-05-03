let interval;

window.addEventListener("gamepadconnected", (e) => {
  const gp = navigator.getGamepads()[e.gamepad.index];
  console.log(
    `Gamepad connected at index ${gp.index}: ${gp.id} with ${gp.buttons.length} buttons, ${gp.axes.length} axes.`,
  );
  interval = setInterval(gamepadLoop, 100);
});

window.addEventListener("gamepaddisconnected", (event) => {
  console.log("Gamepad Disconnected:", event);
  clearInterval(interval);
});

function gamepadLoop() {
  const gamepads = navigator.getGamepads();
  if (!gamepads) return;

  const gamepad = gamepads[0];

  const angle = $("#angle");

  if (isLeft(gamepad)) {
    angle.value -= 1;
    angle.dispatchEvent(new Event("change", { bubbles: true }));
  }

  if (isRight(gamepad)) {
    angle.value += 1;
    angle.dispatchEvent(new Event("change", { bubbles: true }));
  }
}

function isLeft(gp) {
  if (!gp) return false;

  const deadzone = 0.2;

  return (
    gp.buttons[14]?.pressed || // D-pad left
    gp.axes[0] < -deadzone || // left stick left
    gp.axes[2] < -deadzone // right stick left
  );
}

function isRight(gp) {
  if (!gp) return false;

  const deadzone = 0.2;

  return (
    gp.buttons[15]?.pressed || // D-pad right
    gp.axes[0] > deadzone || // left stick right
    gp.axes[2] > deadzone // right stick right
  );
}
