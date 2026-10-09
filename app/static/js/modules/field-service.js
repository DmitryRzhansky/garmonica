window.initFieldService = function initFieldService() {
  const root = document.querySelector("[data-field-service]");
  if (!root) {
    return;
  }

  const equip = root.querySelector("[data-field-equip]");
  let equipResizeTimer = 0;

  function fitEquipPhotoHeight() {
    if (!equip) {
      return;
    }

    const desktop = window.matchMedia("(min-width: 48rem)").matches;
    const panels = Array.from(equip.querySelectorAll("[data-field-equip-panel]"));

    panels.forEach((panel) => {
      const photo = panel.querySelector(".field-equip__photo");
      const facts = panel.querySelector(".field-equip__facts");
      if (!photo) {
        return;
      }

      if (!desktop || !facts || panel.hidden) {
        photo.style.removeProperty("--field-equip-photo-max");
        return;
      }

      // Cap photo frame to facts height — shorten image, never stretch the text block.
      photo.style.removeProperty("--field-equip-photo-max");
      const factsHeight = Math.round(facts.getBoundingClientRect().height);
      if (factsHeight > 0) {
        photo.style.setProperty("--field-equip-photo-max", `${factsHeight}px`);
      }
    });
  }

  function syncMainTabs() {
    const inputs = Array.from(root.querySelectorAll(".field-service__tab-input"));
    const panels = Array.from(root.querySelectorAll("[data-field-service-panel]"));
    const filters = Array.from(root.querySelectorAll("[data-field-service-filter]"));

    function activate(slug) {
      panels.forEach((panel) => {
        const active = panel.getAttribute("data-field-service-panel") === slug;
        panel.classList.toggle("is-active", active);
        panel.hidden = !active;
      });
      filters.forEach((chip) => {
        chip.classList.toggle("is-active", chip.getAttribute("data-field-service-filter") === slug);
      });
      if (slug === "equipment") {
        requestAnimationFrame(fitEquipPhotoHeight);
      }
    }

    inputs.forEach((input) => {
      input.addEventListener("change", () => {
        if (input.checked) {
          activate(input.getAttribute("data-field-service-tab"));
        }
      });
    });

    const checked = inputs.find((input) => input.checked) || inputs[0];
    if (checked) {
      activate(checked.getAttribute("data-field-service-tab"));
    }
  }

  function syncEquipment() {
    if (!equip) {
      return;
    }

    const inputs = Array.from(equip.querySelectorAll(".field-equip__tab-input"));
    const panels = Array.from(equip.querySelectorAll("[data-field-equip-panel]"));
    const filters = Array.from(equip.querySelectorAll("[data-field-equip-filter]"));
    const select = equip.querySelector("[data-field-equip-select]");

    function activate(slug) {
      panels.forEach((panel) => {
        const active = panel.getAttribute("data-field-equip-panel") === slug;
        panel.classList.toggle("is-active", active);
        panel.hidden = !active;
      });
      filters.forEach((chip) => {
        chip.classList.toggle("is-active", chip.getAttribute("data-field-equip-filter") === slug);
      });
      inputs.forEach((input) => {
        input.checked = input.getAttribute("data-field-equip-tab") === slug;
      });
      if (select && select.value !== slug) {
        select.value = slug;
      }
      requestAnimationFrame(fitEquipPhotoHeight);
    }

    inputs.forEach((input) => {
      input.addEventListener("change", () => {
        if (input.checked) {
          activate(input.getAttribute("data-field-equip-tab"));
        }
      });
    });

    if (select) {
      select.addEventListener("change", () => {
        activate(select.value);
      });
    }

    const checked = inputs.find((input) => input.checked) || inputs[0];
    if (checked) {
      activate(checked.getAttribute("data-field-equip-tab"));
    }
  }

  function syncFleet() {
    const fleet = root.querySelector(".field-service__fleet-cars");
    if (!fleet) {
      return;
    }

    const inputs = Array.from(fleet.querySelectorAll(".field-service__car-input"));
    const panels = Array.from(fleet.querySelectorAll("[data-fleet-car-panel]"));
    const filters = Array.from(fleet.querySelectorAll("[data-fleet-car-filter]"));

    function activate(slug) {
      panels.forEach((panel) => {
        const active = panel.getAttribute("data-fleet-car-panel") === slug;
        panel.classList.toggle("is-active", active);
        panel.hidden = !active;
      });
      filters.forEach((chip) => {
        chip.classList.toggle("is-active", chip.getAttribute("data-fleet-car-filter") === slug);
      });
    }

    inputs.forEach((input) => {
      input.addEventListener("change", () => {
        if (input.checked) {
          activate(input.getAttribute("data-fleet-car"));
        }
      });
    });

    const checked = inputs.find((input) => input.checked) || inputs[0];
    if (checked) {
      activate(checked.getAttribute("data-fleet-car"));
    }
  }

  // Клик по label не должен скроллить к скрытому radio (как в отзывах)
  function bindLabelClicksWithoutScroll(scope) {
    scope.querySelectorAll("label[for]").forEach((label) => {
      label.addEventListener("click", (event) => {
        const inputId = label.getAttribute("for");
        const input = inputId ? scope.querySelector(`#${CSS.escape(inputId)}`) : null;

        if (!input || input.disabled || input.type !== "radio") {
          return;
        }

        event.preventDefault();

        if (!input.checked) {
          input.checked = true;
          input.dispatchEvent(new Event("change", { bubbles: true }));
        }

        if (typeof input.focus === "function") {
          input.focus({ preventScroll: true });
        }
      });
    });
  }

  syncMainTabs();
  syncEquipment();
  syncFleet();
  bindLabelClicksWithoutScroll(root);

  window.addEventListener("resize", () => {
    window.clearTimeout(equipResizeTimer);
    equipResizeTimer = window.setTimeout(fitEquipPhotoHeight, 100);
  });
};
