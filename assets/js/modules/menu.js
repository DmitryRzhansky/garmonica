export function initMenu() {
  const toggle = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("[data-mobile-menu]");
  const closeButtons = document.querySelectorAll("[data-menu-close]");

  if (!toggle || !menu) {
    return;
  }

  const panel = menu.querySelector("[data-mobile-menu-panel]");
  const focusableSelector =
    'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])';

  function openMenu() {
    menu.classList.add("is-open");
    menu.removeAttribute("hidden");
    toggle.setAttribute("aria-expanded", "true");
    document.body.classList.add("is-menu-open");

    const firstFocusable = panel?.querySelector(focusableSelector);
    firstFocusable?.focus();
  }

  function closeMenu() {
    menu.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    document.body.classList.remove("is-menu-open");
    toggle.focus();

    window.setTimeout(() => {
      if (!menu.classList.contains("is-open")) {
        menu.setAttribute("hidden", "");
      }
    }, 200);
  }

  toggle.addEventListener("click", () => {
    const isOpen = toggle.getAttribute("aria-expanded") === "true";
    if (isOpen) {
      closeMenu();
    } else {
      openMenu();
    }
  });

  closeButtons.forEach((button) => {
    button.addEventListener("click", closeMenu);
  });

  menu.querySelectorAll("a[href^='#']").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menu.classList.contains("is-open")) {
      closeMenu();
    }
  });
}
