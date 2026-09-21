(function () {
  function initLicenses() {
    var section = document.querySelector("[data-licenses]");

    if (!section) {
      return;
    }

    var dialog = section.querySelector("[data-license-dialog]");
    var dialogImage = section.querySelector("[data-license-dialog-image]");
    var closeButton = section.querySelector("[data-license-close]");
    var notice = section.querySelector("[data-license-notice]");
    var lastTrigger = null;

    section.addEventListener("click", function (event) {
      var openButton = event.target.closest("[data-license-open]");
      var downloadButton = event.target.closest("[data-license-download]");

      if (openButton && dialog && dialogImage) {
        lastTrigger = openButton;
        dialogImage.src = openButton.dataset.licenseImage || "";
        dialogImage.alt = openButton.dataset.licenseAlt || "Демонстрационный образец документа";
        dialog.showModal();
        return;
      }

      if (downloadButton && notice) {
        notice.textContent = "Демонстрационная кнопка: файл для скачивания пока не подключён.";
      }
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

  window.initLicenses = initLicenses;
})();
