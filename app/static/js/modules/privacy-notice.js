(function () {
  const STORAGE_KEY = "nova-privacy-accepted";
  const SHOW_DELAY_MS = 600;

  function initPrivacyNotice() {
    const root = document.querySelector("[data-privacy-notice]");
    const accept = document.querySelector("[data-privacy-accept]");

    if (!root || !accept) {
      return;
    }

    try {
      if (window.localStorage.getItem(STORAGE_KEY) === "1") {
        return;
      }
    } catch (_error) {
      // localStorage may be blocked; still show the notice.
    }

    root.hidden = false;

    window.requestAnimationFrame(() => {
      window.setTimeout(() => {
        root.classList.add("is-visible");
      }, SHOW_DELAY_MS);
    });

    accept.addEventListener("click", () => {
      try {
        window.localStorage.setItem(STORAGE_KEY, "1");
      } catch (_error) {
        // Ignore storage errors and still dismiss the notice.
      }

      root.classList.remove("is-visible");

      window.setTimeout(() => {
        root.hidden = true;
      }, 280);
    });
  }

  window.initPrivacyNotice = initPrivacyNotice;
})();
