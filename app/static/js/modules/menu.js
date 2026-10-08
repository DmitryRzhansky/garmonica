const HEADER_DROPDOWN_GAP_PX = 8;

function syncAboutMenuOffset() {
  const header = document.querySelector("[data-header]");
  const item = document.querySelector(".hero-header__nav-item--about");
  const aboutPanel = item?.querySelector(".about-menu");

  if (!header || !item || !aboutPanel) {
    return;
  }

  const gap = Math.round(
    header.getBoundingClientRect().bottom -
      item.getBoundingClientRect().bottom +
      HEADER_DROPDOWN_GAP_PX
  );
  const safeGap = Math.max(gap, HEADER_DROPDOWN_GAP_PX);

  aboutPanel.style.top = `calc(100% + ${safeGap}px)`;
  aboutPanel.style.setProperty("--about-menu-bridge", `${safeGap}px`);
}

function initAboutMenu() {
  const item = document.querySelector(".hero-header__nav-item--about");

  if (!item) {
    return;
  }

  const sync = () => syncAboutMenuOffset();

  item.addEventListener("mouseenter", sync);
  item.addEventListener("focusin", sync);
  window.addEventListener("resize", sync, { passive: true });
  document.addEventListener("scroll", sync, { passive: true, capture: true });
  sync();
}

function initMenu() {
  const toggle = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("[data-mobile-menu]");
  const header = document.querySelector("[data-header]");

  initAboutMenu();

  if (header) {
    const onScroll = () => {
      header.classList.toggle("hero-header--scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  if (!toggle || !menu) {
    return;
  }

  const panel = menu.querySelector("[data-mobile-menu-panel]");
  const focusableSelector =
    'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])';

  function resetAccordions() {
    menu.querySelectorAll("[data-mobile-accordion].is-open").forEach((item) => {
      item.classList.remove("is-open");
      const btn = item.querySelector(":scope > [data-mobile-accordion-btn]");
      btn?.setAttribute("aria-expanded", "false");
    });
  }

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
    resetAccordions();
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

    const willOpen = !accordion.classList.contains("is-open");
    const parent = accordion.parentElement;

    if (parent) {
      parent.querySelectorAll(":scope > [data-mobile-accordion].is-open").forEach((item) => {
        if (item === accordion) {
          return;
        }
        item.classList.remove("is-open");
        item
          .querySelector(":scope > [data-mobile-accordion-btn]")
          ?.setAttribute("aria-expanded", "false");
      });
    }

    accordion.classList.toggle("is-open", willOpen);
    accordionBtn.setAttribute("aria-expanded", String(willOpen));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menu.classList.contains("is-open")) {
      closeMenu();
    }
  });
}

window.initMenu = initMenu;
