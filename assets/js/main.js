import { initMenu } from "./modules/menu.js";
import { initContactForm } from "./modules/contact-form.js";
import { initReviews } from "./modules/reviews.js";

function safeInit(label, fn) {
  try {
    fn();
  } catch (error) {
    console.error(`[garmonica] ${label} failed:`, error);
  }
}

function initApp() {
  safeInit("menu", initMenu);
  safeInit("contact-form", initContactForm);
  safeInit("reviews", initReviews);
}

document.addEventListener("DOMContentLoaded", initApp);
