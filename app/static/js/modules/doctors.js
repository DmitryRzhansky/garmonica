(function initDoctorsSliders() {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  function initRoot(root) {
    if (!root || root.dataset.doctorsReady === "true") {
      return;
    }

    const track = root.querySelector("[data-doctors-track]");
    const dotsWrap = root.querySelector("[data-doctors-dots]");
    const prev = root.querySelector("[data-doctors-prev]");
    const next = root.querySelector("[data-doctors-next]");

    if (!track || !dotsWrap) {
      return;
    }

    root.dataset.doctorsReady = "true";

    const slides = Array.from(track.children);
    let perView = 1;
    let pages = 0;
    let frame = 0;

    function getPerView() {
      const raw = getComputedStyle(track).getPropertyValue("--doctors-per-view").trim();
      const value = Number.parseInt(raw, 10);
      return Number.isFinite(value) && value > 0 ? value : 1;
    }

    function getStep() {
      if (slides.length > 1) {
        return slides[1].offsetLeft - slides[0].offsetLeft;
      }
      return track.clientWidth;
    }

    function getMaxScroll() {
      return Math.max(0, track.scrollWidth - track.clientWidth);
    }

    function getActivePage() {
      const maxScroll = getMaxScroll();
      if (maxScroll <= 1) {
        return 0;
      }
      if (track.scrollLeft >= maxScroll - 2) {
        return pages - 1;
      }
      const step = getStep() || 1;
      const index = Math.round(track.scrollLeft / step);
      return Math.min(pages - 1, Math.round(index / perView));
    }

    function goTo(page) {
      const target = Math.max(0, Math.min(pages - 1, page));
      track.scrollTo({
        left: Math.min(target * perView * getStep(), getMaxScroll()),
        behavior: reduceMotion.matches ? "auto" : "smooth",
      });
    }

    function update() {
      frame = 0;
      const active = getActivePage();
      Array.from(dotsWrap.children).forEach(function (dot, index) {
        const isActive = index === active;
        dot.classList.toggle("is-active", isActive);
        dot.setAttribute("aria-current", isActive ? "true" : "false");
      });

      if (prev) {
        prev.disabled = active <= 0;
      }
      if (next) {
        next.disabled = active >= pages - 1;
      }
    }

    function render() {
      perView = getPerView();
      const count = Math.ceil(slides.length / perView);

      if (count !== pages) {
        pages = count;
        dotsWrap.innerHTML = "";

        for (let i = 0; i < pages; i += 1) {
          const dot = document.createElement("button");
          dot.type = "button";
          dot.className = "doctors__dot";
          dot.setAttribute("aria-label", "Врачи, страница " + (i + 1) + " из " + pages);
          dotsWrap.appendChild(dot);
        }
      }

      const single = pages <= 1;
      dotsWrap.hidden = single;
      if (prev) {
        prev.hidden = single;
      }
      if (next) {
        next.hidden = single;
      }
      update();
    }

    dotsWrap.addEventListener("click", function (event) {
      const dot = event.target.closest(".doctors__dot");
      if (!dot) {
        return;
      }
      goTo(Array.from(dotsWrap.children).indexOf(dot));
    });

    if (prev) {
      prev.addEventListener("click", function () {
        goTo(getActivePage() - 1);
      });
    }

    if (next) {
      next.addEventListener("click", function () {
        goTo(getActivePage() + 1);
      });
    }

    track.addEventListener(
      "scroll",
      function () {
        if (!frame) {
          frame = requestAnimationFrame(update);
        }
      },
      { passive: true }
    );

    window.addEventListener("resize", render);
    render();
  }

  function init() {
    document.querySelectorAll("[data-doctors-slider]").forEach(initRoot);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
