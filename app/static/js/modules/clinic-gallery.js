(function () {
  function initClinicGallery() {
    var section = document.querySelector("[data-clinic-gallery]");

    if (!section) {
      return;
    }

    var tabs = Array.prototype.slice.call(section.querySelectorAll("[data-gallery-tab]"));
    var panels = Array.prototype.slice.call(section.querySelectorAll("[data-gallery-panel]"));
    var lightbox = section.querySelector("[data-gallery-lightbox]");
    var lightboxImage = section.querySelector("[data-gallery-lightbox-image]");
    var lightboxCaption = section.querySelector("[data-gallery-lightbox-caption]");
    var currentPhotos = [];
    var currentIndex = 0;
    var lastTrigger = null;

    function selectTab(tab) {
      var targetId = tab.getAttribute("aria-controls");

      tabs.forEach(function (item) {
        var isSelected = item === tab;
        item.setAttribute("aria-selected", String(isSelected));
        item.tabIndex = isSelected ? 0 : -1;
      });

      panels.forEach(function (panel) {
        panel.hidden = panel.id !== targetId;
      });
    }

    function photosOf(trigger) {
      var panel = trigger.closest("[data-gallery-panel]");

      if (!panel) {
        return [];
      }

      return Array.prototype.slice.call(panel.querySelectorAll("[data-gallery-open]"));
    }

    function showPhoto(index) {
      if (!currentPhotos.length || !lightboxImage) {
        return;
      }

      currentIndex = (index + currentPhotos.length) % currentPhotos.length;

      var trigger = currentPhotos[currentIndex];
      var photo = trigger.querySelector(".clinic-gallery__photo");
      var caption = trigger.getAttribute("data-gallery-caption") || "";

      if (!photo) {
        return;
      }

      lightboxImage.src = photo.currentSrc || photo.getAttribute("src") || "";
      lightboxImage.alt = photo.alt || caption;

      if (lightboxCaption) {
        lightboxCaption.textContent = caption + " · " + (currentIndex + 1) + " из " + currentPhotos.length;
      }
    }

    function openLightbox(trigger) {
      if (!lightbox) {
        return;
      }

      currentPhotos = photosOf(trigger);
      lastTrigger = trigger;
      showPhoto(currentPhotos.indexOf(trigger));
      lightbox.showModal();
    }

    function closeLightbox() {
      if (lightbox && lightbox.open) {
        lightbox.close();
      }
    }

    tabs.forEach(function (tab, index) {
      tab.addEventListener("click", function () {
        selectTab(tab);
      });

      tab.addEventListener("keydown", function (event) {
        var nextIndex = null;

        if (event.key === "ArrowRight") {
          nextIndex = (index + 1) % tabs.length;
        }

        if (event.key === "ArrowLeft") {
          nextIndex = (index - 1 + tabs.length) % tabs.length;
        }

        if (event.key === "Home") {
          nextIndex = 0;
        }

        if (event.key === "End") {
          nextIndex = tabs.length - 1;
        }

        if (nextIndex === null) {
          return;
        }

        event.preventDefault();
        tabs[nextIndex].focus();
        selectTab(tabs[nextIndex]);
      });
    });

    section.addEventListener("click", function (event) {
      var openButton = event.target.closest("[data-gallery-open]");
      var closeButton = event.target.closest("[data-gallery-close]");
      var prevButton = event.target.closest("[data-gallery-prev]");
      var nextButton = event.target.closest("[data-gallery-next]");

      if (openButton) {
        openLightbox(openButton);
        return;
      }

      if (closeButton) {
        closeLightbox();
        return;
      }

      if (prevButton) {
        showPhoto(currentIndex - 1);
        return;
      }

      if (nextButton) {
        showPhoto(currentIndex + 1);
      }
    });

    if (!lightbox) {
      return;
    }

    lightbox.addEventListener("click", function (event) {
      var clickedFrame = event.target.classList && event.target.classList.contains("clinic-gallery__lightbox-frame");

      if (event.target === lightbox || clickedFrame) {
        closeLightbox();
      }
    });

    lightbox.addEventListener("close", function () {
      if (lightboxImage) {
        lightboxImage.removeAttribute("src");
        lightboxImage.alt = "";
      }

      if (lastTrigger) {
        lastTrigger.focus();
      }
    });

    lightbox.addEventListener("keydown", function (event) {
      if (event.key === "ArrowRight") {
        event.preventDefault();
        showPhoto(currentIndex + 1);
      }

      if (event.key === "ArrowLeft") {
        event.preventDefault();
        showPhoto(currentIndex - 1);
      }
    });
  }

  window.initClinicGallery = initClinicGallery;
})();
