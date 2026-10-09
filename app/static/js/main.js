function safeInit(label, fn) {
  if (typeof fn !== "function") {
    return;
  }

  try {
    fn();
  } catch (error) {
    console.error(`[nova-clinic] ${label} failed:`, error);
  }
}

function initApp() {
  safeInit("menu", window.initMenu);
  safeInit("services-menu", window.initServicesMenu);
  safeInit("contact-form", window.initContactForm);
  safeInit("service-call-form", window.initServiceCallForm);
  safeInit("reviews", window.initReviews);
  safeInit("licenses", window.initLicenses);
  safeInit("clinic-gallery", window.initClinicGallery);
  safeInit("about-slider", window.initAboutSlider);
  safeInit("specialist-quiz", window.initSpecialistQuiz);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initApp);
} else {
  initApp();
}
