function initExclusiveFaq() {
  var roots = document.querySelectorAll("[data-faq]");
  if (!roots.length) {
    return;
  }

  roots.forEach(function (root) {
    if (root.dataset.faqReady === "true") {
      return;
    }

    root.dataset.faqReady = "true";

    if (root.getAttribute("data-faq-mode") === "accordion") {
      initButtonAccordion(root);
      return;
    }

    initDetailsAccordion(root);
  });
}

function initDetailsAccordion(root) {
  var items = root.querySelectorAll("details[data-faq-item]");

  root.addEventListener("click", function (event) {
    var summary = event.target.closest("summary.faq__question");
    if (!summary || !root.contains(summary)) {
      return;
    }

    var details = summary.closest("details[data-faq-item]");
    if (!details) {
      return;
    }

    event.preventDefault();

    var willOpen = !details.open;

    for (var i = 0; i < items.length; i += 1) {
      items[i].open = false;
    }

    if (willOpen) {
      details.open = true;
    }
  });
}

function initButtonAccordion(root) {
  var items = Array.prototype.slice.call(root.querySelectorAll("[data-faq-item]"));

  function setOpen(item, isOpen) {
    var trigger = item.querySelector("[data-faq-trigger]");
    var panel = item.querySelector("[data-faq-panel]");

    if (!trigger || !panel) {
      return;
    }

    item.classList.toggle("is-open", isOpen);
    trigger.setAttribute("aria-expanded", String(isOpen));
    panel.setAttribute("aria-hidden", String(!isOpen));
    panel.toggleAttribute("inert", !isOpen);
  }

  items.forEach(function (item) {
    var trigger = item.querySelector("[data-faq-trigger]");
    if (!trigger) {
      return;
    }

    trigger.addEventListener("click", function () {
      var willOpen = !item.classList.contains("is-open");
      items.forEach(function (otherItem) {
        setOpen(otherItem, willOpen && otherItem === item);
      });
    });
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initExclusiveFaq);
} else {
  initExclusiveFaq();
}
