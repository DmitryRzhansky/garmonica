window.initFieldService = function initFieldService() {
  const root = document.querySelector("[data-field-service]");
  if (!root) {
    return;
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
    const equip = root.querySelector("[data-field-equip]");
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

  syncMainTabs();
  syncEquipment();
  syncFleet();
};
