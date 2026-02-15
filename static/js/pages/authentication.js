document.addEventListener("DOMContentLoaded", function () {

  function setupToggle(toggleId, inputId) {
    const toggle = document.getElementById(toggleId);
    const input = document.getElementById(inputId);

    if (!toggle || !input) return;

    toggle.addEventListener("click", function () {
      const icon = toggle.querySelector("i");
      const isPassword = input.type === "password";

      input.type = isPassword ? "text" : "password";

      icon.classList.toggle("bx-hide", !isPassword);
      icon.classList.toggle("bx-show", isPassword);
    });
  }

  setupToggle("togglePassword1", "password");
  setupToggle("togglePassword2", "confirm_password");

});