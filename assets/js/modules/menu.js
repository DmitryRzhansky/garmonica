function initMenu() {
  const toggle = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("[data-mobile-menu]");
  const header = document.querySelector("[data-header]");

  if (!toggle || !menu) {
    return;
  }

  const panel = menu.querySelector("[data-mobile-menu-panel]");
  const focusableSelector =
    'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])';

  function openMenu() {
    menu.classList.add("is-open");
    menu.removeAttribute("hidden");
    menu.setAttribute("aria-hidden", "false");
    toggle.setAttribute("aria-expanded", "true");
    document.body.classList.add("is-menu-open");

    const firstFocusable = panel?.querySelector(focusableSelector);
    firstFocusable?.focus();
  }

  function closeMenu() {
    menu.classList.remove("is-open");
    menu.setAttribute("aria-hidden", "true");
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

  menu.addEventListener("click", (event) => {
    if (event.target.closest("[data-menu-close]")) {
      closeMenu();
    }
  });

  menu.addEventListener("click", (event) => {
    const accordionBtn = event.target.closest("[data-mobile-accordion-btn]");
    if (!accordionBtn) {
      return;
    }

    const accordion = accordionBtn.closest("[data-mobile-accordion]");
    if (!accordion) {
      return;
    }

    const isOpen = accordion.classList.contains("is-open");
    accordion.classList.toggle("is-open", !isOpen);
    accordionBtn.setAttribute("aria-expanded", String(!isOpen));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menu.classList.contains("is-open")) {
      closeMenu();
    }
  });

  if (header) {
    const onScroll = () => {
      header.classList.toggle("hero-header--scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }
}

window.initMenu = initMenu;
