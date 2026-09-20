function initServicesMenu() {
  const root = document.querySelector("[data-services-menu]");
  const panel = document.querySelector("[data-services-menu-panel]");
  const trigger = root?.querySelector("[data-services-menu-trigger]");

  if (!root || !panel || !trigger) {
    return;
  }

  if (panel.parentElement !== document.body) {
    document.body.appendChild(panel);
  }

  const cats = panel.querySelectorAll("[data-services-cat]");
  const panels = panel.querySelectorAll("[data-services-panel]");
  const searchInput = panel.querySelector("[data-services-search]");
  const clearButton = panel.querySelector("[data-services-clear]");
  const resultsBlock = panel.querySelector("[data-services-results]");
  const resultsList = panel.querySelector("[data-services-results-list]");
  const searchItems = panel.querySelectorAll("[data-services-search-item]");
  const emptyState = panel.querySelector("[data-services-empty]");
  const layout = panel.querySelector("[data-services-layout]");
  const searchForm = panel.querySelector("[data-services-search-form]");

  function isOpen() {
    return panel.classList.contains("is-open");
  }

  function positionPanel() {
    const header = document.querySelector("[data-header]");
    if (!header) {
      return;
    }
    panel.style.top = `${Math.round(header.getBoundingClientRect().bottom + 8)}px`;
    // 8px === --header-dropdown-gap (same as about-menu)
  }

  function openMenu() {
    positionPanel();
    root.classList.add("is-open");
    panel.classList.add("is-open");
    trigger.classList.add("hero-header__nav-link--active");
    trigger.setAttribute("aria-expanded", "true");
  }

  function closeMenu() {
    root.classList.remove("is-open");
    panel.classList.remove("is-open");
    trigger.classList.remove("hero-header__nav-link--active");
    trigger.setAttribute("aria-expanded", "false");
  }

  function toggleMenu() {
    if (isOpen()) {
      closeMenu();
    } else {
      openMenu();
    }
  }

  function setActiveCat(id) {
    cats.forEach((cat) => {
      cat.classList.toggle("is-active", cat.getAttribute("data-services-cat") === id);
    });
    panels.forEach((item) => {
      item.classList.toggle(
        "is-active",
        item.getAttribute("data-services-panel") === id
      );
    });
  }

  function applySearch(query) {
    const normalized = query.trim().toLowerCase();

    if (!normalized) {
      resultsBlock?.setAttribute("hidden", "");
      emptyState?.setAttribute("hidden", "");
      layout?.removeAttribute("hidden");
      searchItems.forEach((item) => item.setAttribute("hidden", ""));
      return;
    }

    let matchCount = 0;
    searchItems.forEach((item) => {
      const text = item.textContent?.toLowerCase() || "";
      const matched = text.includes(normalized);
      item.toggleAttribute("hidden", !matched);
      if (matched) {
        matchCount += 1;
      }
    });

    layout?.setAttribute("hidden", "");
    resultsBlock?.removeAttribute("hidden");
    emptyState?.toggleAttribute("hidden", matchCount > 0);
  }

  trigger.addEventListener("click", (event) => {
    event.preventDefault();
    event.stopPropagation();
    toggleMenu();
  });

  document.addEventListener("click", (event) => {
    if (!isOpen()) {
      return;
    }
    const target = event.target;
    if (!(target instanceof Node)) {
      return;
    }
    if (root.contains(target) || panel.contains(target)) {
      return;
    }
    closeMenu();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && isOpen()) {
      closeMenu();
      trigger.focus();
    }
  });

  cats.forEach((cat) => {
    cat.addEventListener("click", () => {
      setActiveCat(cat.getAttribute("data-services-cat"));
    });
  });

  searchInput?.addEventListener("input", () => {
    applySearch(searchInput.value);
  });

  clearButton?.addEventListener("click", () => {
    if (searchInput) {
      searchInput.value = "";
      searchInput.focus();
    }
    applySearch("");
  });

  searchForm?.addEventListener("submit", (event) => {
    event.preventDefault();
  });

  panel.querySelectorAll("a[href^='#']").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  window.addEventListener(
    "resize",
    () => {
      if (isOpen()) {
        positionPanel();
      }
    },
    { passive: true }
  );

  document.addEventListener(
    "scroll",
    () => {
      if (isOpen()) {
        positionPanel();
      }
    },
    { passive: true, capture: true }
  );
}

window.initServicesMenu = initServicesMenu;
