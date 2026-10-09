function initServiceCallForm() {
  function formatPhone(value) {
    const digits = value.replace(/\D/g, "");

    let normalized = digits;
    if (normalized.startsWith("8")) {
      normalized = `7${normalized.slice(1)}`;
    }
    if (!normalized.startsWith("7")) {
      normalized = `7${normalized}`;
    }

    normalized = normalized.slice(0, 11);
    const local = normalized.slice(1);

    let formatted = "+7";
    if (local.length > 0) {
      formatted += ` (${local.slice(0, 3)}`;
    }
    if (local.length >= 3) {
      formatted += `) ${local.slice(3, 6)}`;
    }
    if (local.length >= 6) {
      formatted += `-${local.slice(6, 8)}`;
    }
    if (local.length >= 8) {
      formatted += `-${local.slice(8, 10)}`;
    }

    return formatted;
  }

  function formatName(value) {
    return value
      .replace(/[^A-Za-zА-Яа-яЁё\s\-']/g, "")
      .replace(/\s{2,}/g, " ")
      .replace(/-{2,}/g, "-")
      .replace(/'{2,}/g, "'")
      .slice(0, 40);
  }

  function clearFieldError(field) {
    field.removeAttribute("aria-invalid");
    const wrapper = field.closest(".service-call-form__field, .service-call-form__fieldset");
    const error = wrapper?.querySelector("[data-field-error]");
    if (error) {
      error.hidden = true;
      error.textContent = "";
    }
  }

  function setFieldError(field, message) {
    field.setAttribute("aria-invalid", "true");
    const wrapper = field.closest(".service-call-form__field, .service-call-form__fieldset");
    const error = wrapper?.querySelector("[data-field-error]");
    if (error) {
      error.hidden = false;
      error.textContent = message;
    }
  }

  function initNameMask(form) {
    const input = form.querySelector("[data-name-mask]");

    if (!(input instanceof HTMLInputElement)) {
      return;
    }

    input.addEventListener("input", () => {
      const caret = input.selectionStart;
      const next = formatName(input.value);
      input.value = next;
      if (typeof caret === "number") {
        input.setSelectionRange(Math.min(caret, next.length), Math.min(caret, next.length));
      }
    });

    input.addEventListener("blur", () => {
      input.value = formatName(input.value).trim();
    });
  }

  function initPhoneMask(form) {
    const input = form.querySelector("[data-phone-mask]");

    if (!(input instanceof HTMLInputElement)) {
      return;
    }

    input.addEventListener("input", () => {
      input.value = formatPhone(input.value);
    });

    input.addEventListener("focus", () => {
      if (!input.value) {
        input.value = "+7 (";
      }
    });

    input.addEventListener("blur", () => {
      if (input.value === "+7 (" || input.value === "+7") {
        input.value = "";
      }
    });
  }

  function validateForm(form) {
    const requiredFields = Array.from(form.querySelectorAll("[data-required]"));
    let isValid = true;
    const messages = [];
    const seenRadios = new Set();

    requiredFields.forEach((field) => {
      if (!(field instanceof HTMLInputElement || field instanceof HTMLSelectElement || field instanceof HTMLTextAreaElement)) {
        return;
      }

      if (field instanceof HTMLInputElement && field.type === "radio") {
        if (seenRadios.has(field.name)) {
          return;
        }
        seenRadios.add(field.name);

        const checked = form.querySelector(`input[name="${field.name}"]:checked`);
        if (!checked) {
          messages.push("Выберите, кому нужна помощь");
          isValid = false;
        }
        return;
      }

      clearFieldError(field);

      const value = field.value.trim();
      const label = field.getAttribute("data-label") || "Поле";

      if (!value) {
        setFieldError(field, "Заполните поле");
        messages.push(`${label}: заполните поле`);
        isValid = false;
        return;
      }

      if (field.name === "name") {
        const letters = value.replace(/[\s\-']/g, "");
        if (letters.length < 2 || !/^[A-Za-zА-Яа-яЁё\s\-']+$/.test(value)) {
          setFieldError(field, "Укажите имя буквами");
          messages.push(`${label}: укажите имя буквами`);
          isValid = false;
        }
      }

      if (field.name === "phone") {
        const digits = value.replace(/\D/g, "");
        if (digits.length !== 11) {
          setFieldError(field, "Укажите телефон полностью");
          messages.push(`${label}: укажите телефон полностью`);
          isValid = false;
        }
      }
    });

    const consent = form.querySelector('input[name="consent"]');
    if (consent instanceof HTMLInputElement && !consent.checked) {
      messages.push("Нужно согласие на обработку персональных данных");
      isValid = false;
    }

    return { isValid, messages };
  }

  const forms = document.querySelectorAll("[data-service-call-form]");

  forms.forEach((form) => {
    if (!(form instanceof HTMLFormElement) || form.dataset.serviceCallReady === "true") {
      return;
    }

    form.dataset.serviceCallReady = "true";
    initNameMask(form);
    initPhoneMask(form);

    const summary = form.querySelector("[data-form-error-summary]");
    const status = form.querySelector("[data-form-success]");

    form.querySelectorAll("[data-required]").forEach((field) => {
      field.addEventListener("input", () => clearFieldError(field));
      field.addEventListener("change", () => clearFieldError(field));
    });

    form.addEventListener("submit", (event) => {
      event.preventDefault();

      if (status) {
        status.hidden = true;
      }

      const honeypot = form.querySelector('input[name="website"]');
      if (honeypot instanceof HTMLInputElement && honeypot.value.trim()) {
        return;
      }

      const { isValid, messages } = validateForm(form);

      if (!isValid) {
        if (summary) {
          summary.hidden = false;
          summary.textContent = messages[0] || "Проверьте поля формы";
          summary.focus();
        }
        return;
      }

      if (summary) {
        summary.hidden = true;
      }

      if (status) {
        status.hidden = false;
        status.textContent =
          "Заявка принята локально. Отправка на сервер пока не подключена — позвоните в клинику.";
        status.focus();
      }
    });
  });
}

window.initServiceCallForm = initServiceCallForm;
