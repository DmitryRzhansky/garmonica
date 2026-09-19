export function initContactForm() {
  const form = document.querySelector("[data-contact-form]");

  if (!form) {
    return;
  }

  const status = form.querySelector("[data-form-status]");

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    if (status) {
      status.hidden = false;
      status.textContent =
        "Форма заполнена. На этом демо-сайте отправка на сервер не подключена — позвоните в клинику «Гармоника».";
    }
  });
}
