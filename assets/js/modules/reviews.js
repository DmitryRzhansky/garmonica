export function initReviews() {
  const root = document.querySelector("[data-reviews]");

  if (!root || root.dataset.reviewsReady === "true") {
    return;
  }

  root.dataset.reviewsReady = "true";

  const tabs = Array.from(root.querySelectorAll(".reviews__tab-input"));
  const panels = Array.from(root.querySelectorAll("[data-reviews-panel]"));
  const panelState = new WeakMap();

  panels.forEach((panel) => {
    panelState.set(panel, { index: 0 });
  });

  function getActivePanel() {
    const checked = root.querySelector(".reviews__tab-input:checked");
    const key = checked ? checked.getAttribute("data-reviews-tab") : "yandex";
    return panels.find((panel) => panel.getAttribute("data-reviews-panel") === key) || null;
  }

  function getPerView(track) {
    const raw = getComputedStyle(track).getPropertyValue("--reviews-per-view").trim();
    const value = Number.parseFloat(raw);
    return Number.isFinite(value) && value > 0 ? value : 1;
  }

  function getSlides(panel) {
    return Array.from(panel.querySelectorAll(".reviews__slide"));
  }

  function getMaxIndex(panel) {
    const track = panel.querySelector("[data-reviews-track]");
    const slides = getSlides(panel);

    if (!track || !slides.length) {
      return 0;
    }

    return Math.max(0, slides.length - getPerView(track));
  }

  function getStep(panel) {
    const track = panel.querySelector("[data-reviews-track]");
    const slides = getSlides(panel);

    if (!track || !slides.length) {
      return 0;
    }

    const styles = getComputedStyle(track);
    const gap = Number.parseFloat(styles.columnGap || styles.gap) || 0;
    const width = slides[0].getBoundingClientRect().width;

    return width > 0 ? width + gap : 0;
  }

  function setNavState(button, isInactive) {
    if (!button) {
      return;
    }

    button.disabled = isInactive;
    button.classList.toggle("reviews__nav--hidden", isInactive);
    button.setAttribute("aria-hidden", String(isInactive));

    if (isInactive) {
      button.setAttribute("tabindex", "-1");
    } else {
      button.removeAttribute("tabindex");
    }
  }

  function syncViewportHeight(panel, state) {
    const viewport = panel.querySelector(".reviews__viewport");
    const track = panel.querySelector("[data-reviews-track]");
    const slides = getSlides(panel);

    if (!viewport || !track || !slides.length) {
      return;
    }

    const perView = Math.ceil(getPerView(track));
    const start = state.index;
    const end = Math.min(slides.length, start + perView);
    let maxHeight = 0;

    for (let i = start; i < end; i += 1) {
      maxHeight = Math.max(maxHeight, slides[i].getBoundingClientRect().height);
    }

    viewport.style.height = maxHeight > 0 ? `${maxHeight}px` : "";
  }

  function updatePanel(panel) {
    if (!panel) {
      return;
    }

    const track = panel.querySelector("[data-reviews-track]");
    const prevButton = panel.querySelector("[data-reviews-prev]");
    const nextButton = panel.querySelector("[data-reviews-next]");
    const state = panelState.get(panel) || { index: 0 };
    const maxIndex = getMaxIndex(panel);

    state.index = Math.min(Math.max(0, state.index), maxIndex);
    panelState.set(panel, state);

    if (track) {
      const step = getStep(panel);
      track.style.transform =
        step > 0
          ? `translate3d(-${state.index * step}px, 0, 0)`
          : "translate3d(0, 0, 0)";
    }

    setNavState(prevButton, state.index <= 0);
    setNavState(nextButton, state.index >= maxIndex);

    requestAnimationFrame(() => {
      syncViewportHeight(panel, state);
    });
  }

  function movePanel(panel, delta) {
    if (!panel) {
      return;
    }

    const state = panelState.get(panel) || { index: 0 };
    const maxIndex = getMaxIndex(panel);
    state.index = Math.min(maxIndex, Math.max(0, state.index + delta));
    panelState.set(panel, state);
    updatePanel(panel);
  }

  function onTabChange() {
    const panel = getActivePanel();

    if (!panel) {
      return;
    }

    panelState.set(panel, { index: 0 });
    requestAnimationFrame(() => {
      updatePanel(panel);
    });
  }

  tabs.forEach((tab) => {
    tab.addEventListener("change", onTabChange);
  });

  panels.forEach((panel) => {
    const prevButton = panel.querySelector("[data-reviews-prev]");
    const nextButton = panel.querySelector("[data-reviews-next]");

    if (prevButton) {
      prevButton.removeAttribute("hidden");
      prevButton.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();

        if (prevButton.disabled || prevButton.classList.contains("reviews__nav--hidden")) {
          return;
        }

        movePanel(panel, -1);
      });
    }

    if (nextButton) {
      nextButton.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();

        if (nextButton.disabled || nextButton.classList.contains("reviews__nav--hidden")) {
          return;
        }

        movePanel(panel, 1);
      });
    }
  });

  window.addEventListener("resize", () => {
    updatePanel(getActivePanel());
  });

  onTabChange();
}
