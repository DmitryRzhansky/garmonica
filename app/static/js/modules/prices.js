function initPrices() {
  const root = document.querySelector("[data-prices]");

  if (!root || root.dataset.pricesReady === "true") {
    return;
  }

  root.dataset.pricesReady = "true";

  // Клик по label не должен скроллить к скрытому radio вверху секции
  root.querySelectorAll("label.prices__tab[for]").forEach((label) => {
    label.addEventListener("click", (event) => {
      const inputId = label.getAttribute("for");
      const input = inputId ? root.querySelector(`#${CSS.escape(inputId)}`) : null;

      if (!input || input.disabled || input.type !== "radio") {
        return;
      }

      event.preventDefault();

      if (!input.checked) {
        input.checked = true;
        input.dispatchEvent(new Event("change", { bubbles: true }));
      }

      if (typeof input.focus === "function") {
        input.focus({ preventScroll: true });
      }
    });
  });
}

window.initPrices = initPrices;
