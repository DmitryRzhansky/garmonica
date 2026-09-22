function initAboutSlider() {
  var root = document.querySelector("[data-about-slider]");

  if (!root || root.dataset.aboutReady === "true") {
    return;
  }

  var track = root.querySelector("[data-about-track]");
  var viewport = root.querySelector("[data-about-viewport]");
  var slides = Array.prototype.slice.call(root.querySelectorAll("[data-about-slide]"));
  var dots = Array.prototype.slice.call(root.querySelectorAll("[data-about-dot]"));
  var prevButton = root.querySelector("[data-about-prev]");
  var nextButton = root.querySelector("[data-about-next]");
  var label = root.querySelector("[data-about-label]");

  if (!track || !viewport || slides.length < 2) {
    return;
  }

  root.dataset.aboutReady = "true";

  var index = 0;
  var touchStartX = 0;
  var touchDeltaX = 0;

  function clampIndex(value) {
    if (value < 0) {
      return slides.length - 1;
    }

    if (value >= slides.length) {
      return 0;
    }

    return value;
  }

  function syncViewportHeight() {
    var activeSlide = slides[index];

    if (!activeSlide) {
      return;
    }

    viewport.style.height = activeSlide.offsetHeight + "px";
  }

  function goTo(nextIndex) {
    index = clampIndex(nextIndex);
    track.style.transform = "translate3d(-" + index * 100 + "%, 0, 0)";

    slides.forEach(function (slide, slideIndex) {
      var isActive = slideIndex === index;
      slide.setAttribute("aria-hidden", String(!isActive));

      if (isActive) {
        slide.removeAttribute("inert");
      } else {
        slide.setAttribute("inert", "");
      }
    });

    dots.forEach(function (dot, dotIndex) {
      var isActive = dotIndex === index;
      dot.classList.toggle("about-slider__dot--active", isActive);

      if (isActive) {
        dot.setAttribute("aria-current", "true");
      } else {
        dot.removeAttribute("aria-current");
      }
    });

    if (label) {
      label.textContent = slides[index].getAttribute("data-about-name") || "";
    }

    window.requestAnimationFrame(syncViewportHeight);
  }

  function goNext() {
    goTo(index + 1);
  }

  function goPrev() {
    goTo(index - 1);
  }

  if (prevButton) {
    prevButton.addEventListener("click", goPrev);
  }

  if (nextButton) {
    nextButton.addEventListener("click", goNext);
  }

  dots.forEach(function (dot, dotIndex) {
    dot.addEventListener("click", function () {
      goTo(dotIndex);
    });
  });

  root.addEventListener("keydown", function (event) {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      goPrev();
    }

    if (event.key === "ArrowRight") {
      event.preventDefault();
      goNext();
    }
  });

  viewport.addEventListener(
    "touchstart",
    function (event) {
      if (!event.changedTouches || !event.changedTouches.length) {
        return;
      }

      touchStartX = event.changedTouches[0].clientX;
      touchDeltaX = 0;
    },
    { passive: true }
  );

  viewport.addEventListener(
    "touchmove",
    function (event) {
      if (!event.changedTouches || !event.changedTouches.length) {
        return;
      }

      touchDeltaX = event.changedTouches[0].clientX - touchStartX;
    },
    { passive: true }
  );

  viewport.addEventListener(
    "touchend",
    function () {
      if (Math.abs(touchDeltaX) < 48) {
        return;
      }

      if (touchDeltaX < 0) {
        goNext();
      } else {
        goPrev();
      }
    },
    { passive: true }
  );

  window.addEventListener("resize", syncViewportHeight);

  Array.prototype.forEach.call(root.querySelectorAll("img"), function (image) {
    if (image.complete) {
      return;
    }

    image.addEventListener("load", syncViewportHeight, { once: true });
  });

  if (window.location.hash === "#about-psychiatry") {
    goTo(2);
  } else if (window.location.hash === "#about-narcology" || window.location.hash === "#about-team") {
    goTo(1);
  } else if (window.location.hash === "#about-outpatient") {
    goTo(0);
  } else {
    goTo(0);
  }

  window.addEventListener("hashchange", function () {
    if (window.location.hash === "#about-outpatient") {
      goTo(0);
    }

    if (window.location.hash === "#about-narcology" || window.location.hash === "#about-team") {
      goTo(1);
    }

    if (window.location.hash === "#about-psychiatry") {
      goTo(2);
    }
  });
}

window.initAboutSlider = initAboutSlider;
