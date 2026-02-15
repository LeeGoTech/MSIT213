document.addEventListener("DOMContentLoaded", function () {

  const element = document.getElementById("django-messages");
  if (!element) return;

  const messages = JSON.parse(element.textContent);

  if (!messages.length) return;

  const notyf = new Notyf({
    position: { x: 'right', y: 'top' },
    duration: 3000
  });

  messages.forEach(msg => {
    if (msg.tags.includes("success")) {
      notyf.success(msg.text);
    } else if (msg.tags.includes("error")) {
      notyf.error(msg.text);
    } else {
      notyf.open({
        type: msg.tags,
        message: msg.text
      });
    }
  });

});