(function () {
  function initLicenseSection(section) {
    var dialog = section.querySelector("[data-license-dialog]");
    var dialogImage = section.querySelector("[data-license-dialog-image]");
    var closeButton = section.querySelector("[data-license-close]");
    var lastTrigger = null;

    section.addEventListener("click", function (event) {
      var openButton = event.target.closest("[data-license-open]");

      if (!openButton || !dialog || !dialogImage) {
        return;
      }

      lastTrigger = openButton;
      dialogImage.src = openButton.dataset.licenseImage || "";
      dialogImage.alt = openButton.dataset.licenseAlt || "Документ лицензии";
      dialog.showModal();
    });

    if (!dialog) {
      return;
    }

    function closeDialog() {
      dialog.close();
      if (lastTrigger) {
        lastTrigger.focus();
      }
    }

    if (closeButton) {
      closeButton.addEventListener("click", closeDialog);
    }

    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) {
        closeDialog();
      }
    });
  }

  function initLicenses() {
    var sections = document.querySelectorAll("[data-licenses]");

    Array.prototype.forEach.call(sections, function (section) {
      if (section.dataset.licensesReady === "true") {
        return;
      }

      section.dataset.licensesReady = "true";
      initLicenseSection(section);
    });
  }

  window.initLicenses = initLicenses;
})();
