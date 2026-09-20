function safeInit(label, fn) {
  if (typeof fn !== "function") {
    return;
  }

  try {
    fn();
  } catch (error) {
    console.error(`[garmonica] ${label} failed:`, error);
  }
}

function initApp() {
  safeInit("menu", window.initMenu);
  safeInit("services-menu", window.initServicesMenu);
  safeInit("contact-form", window.initContactForm);
  safeInit("reviews", window.initReviews);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initApp);
} else {
  initApp();
}
