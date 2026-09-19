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
    return panels.find((panel) => panel.getAttribute("data-reviews-panel") === key);
  }

  function getPerView(track) {
    const raw = getComputedStyle(track).getPropertyValue("--reviews-per-view").trim();
    const value = Number.parseFloat(raw);
    return Number.isFinite(value) && value > 0 ? value : 1;
  }

  function getSlides(panel) {
    return Array.from(panel.querySelectorAll(".reviews__slide"));
  }

  function getStep(panel) {
    const track = panel.querySelector("[data-reviews-track]");
    const slides = getSlides(panel);

    if (!track || !slides.length) {
      return 0;
    }

    const styles = getComputedStyle(track);
    const gap = Number.parseFloat(styles.columnGap || styles.gap) || 0;
    return slides[0].getBoundingClientRect().width + gap;
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
    const slides = getSlides(panel);
    const perView = track ? getPerView(track) : 1;
    const maxIndex = Math.max(0, slides.length - perView);

    state.index = Math.min(Math.max(0, state.index), maxIndex);
    panelState.set(panel, state);

    if (track) {
      const step = getStep(panel);
      track.style.transform = step
        ? `translate3d(-${state.index * step}px, 0, 0)`
        : "translate3d(0, 0, 0)";
    }

    if (prevButton) {
      prevButton.disabled = state.index <= 0;
    }

    if (nextButton) {
      nextButton.disabled = state.index >= maxIndex;
    }

    requestAnimationFrame(() => {
      syncViewportHeight(panel, state);
    });
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

  root.addEventListener("click", (event) => {
    const prevButton = event.target.closest("[data-reviews-prev]");

    if (prevButton && root.contains(prevButton)) {
      event.preventDefault();
      const panel = prevButton.closest("[data-reviews-panel]") || getActivePanel();

      if (!panel) {
        return;
      }

      const state = panelState.get(panel) || { index: 0 };
      state.index = Math.max(0, state.index - 1);
      panelState.set(panel, state);
      updatePanel(panel);
      return;
    }

    const nextButton = event.target.closest("[data-reviews-next]");

    if (nextButton && root.contains(nextButton)) {
      event.preventDefault();
      const panel = nextButton.closest("[data-reviews-panel]") || getActivePanel();

      if (!panel) {
        return;
      }

      const track = panel.querySelector("[data-reviews-track]");
      const maxIndex = Math.max(
        0,
        getSlides(panel).length - (track ? getPerView(track) : 1)
      );
      const state = panelState.get(panel) || { index: 0 };
      state.index = Math.min(maxIndex, state.index + 1);
      panelState.set(panel, state);
      updatePanel(panel);
    }
  });

  window.addEventListener("resize", () => {
    updatePanel(getActivePanel());
  });

  onTabChange();
}
