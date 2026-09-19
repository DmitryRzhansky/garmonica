export function initFaq() {
  const root = document.querySelector("[data-faq]");

  if (!root) {
    return;
  }

  const items = root.querySelectorAll("[data-faq-item]");

  items.forEach((item) => {
    const button = item.querySelector("[data-faq-trigger]");
    const answer = item.querySelector("[data-faq-answer]");

    if (!button || !answer) {
      return;
    }

    button.addEventListener("click", () => {
      const isOpen = item.classList.contains("is-open");

      items.forEach((other) => {
        other.classList.remove("is-open");
        const otherButton = other.querySelector("[data-faq-trigger]");
        const otherAnswer = other.querySelector("[data-faq-answer]");
        otherButton?.setAttribute("aria-expanded", "false");
        otherAnswer?.setAttribute("hidden", "");
      });

      if (!isOpen) {
        item.classList.add("is-open");
        button.setAttribute("aria-expanded", "true");
        answer.removeAttribute("hidden");
      }
    });
  });
}
