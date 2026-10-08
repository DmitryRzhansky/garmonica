function initExclusiveFaq() {
  var root = document.querySelector("[data-faq]");
  if (!root || root.dataset.faqReady === "true") {
    return;
  }

  root.dataset.faqReady = "true";
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

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initExclusiveFaq);
} else {
  initExclusiveFaq();
}
