(function (global) {
  var ns = (global.GarmonicaSpecialist = global.GarmonicaSpecialist || {});

  ns.createSpecialistDialog = function (dialog, specialists) {
    if (!dialog) return null;

    var activeSpecialist;
    var opener;
    var draft = null;
    var content = dialog.querySelector('[data-specialist-dialog-content]');

    function show(markup) {
      content.innerHTML = markup;
      if (!dialog.open) dialog.showModal();
      dialog.scrollTop = 0;
      var title = content.querySelector('[data-dialog-title]');
      if (title) title.focus();
    }

    function open(id, mode, trigger) {
      var specialist = specialists.find(function (item) { return item.id === id; });
      if (!specialist) return;
      activeSpecialist = specialist;
      draft = null;
      opener = trigger;
      if (mode === 'booking') renderBooking();
      else renderProfile();
    }

    function renderProfile() {
      var specialist = activeSpecialist;
      var slots = ns.getAvailability(specialist);
      show(
        '<div class="specialist-dialog__profile-header"><img class="specialist-dialog__photo" src="' + specialist.photo + '" alt="' + specialist.name + '" width="240" height="300" decoding="async"><div>'
        + '<h2 id="specialist-dialog-title" class="specialist-dialog__title" tabindex="-1" data-dialog-title>' + specialist.name + '</h2>'
        + '<p>' + specialist.role + (specialist.specialties[0] === 'psychology' ? ' · не врач' : '') + '</p>'
        + '<p class="specialist-dialog__experience">Стаж ' + ns.yearsLabel(specialist.experience) + '</p></div></div>'
        + '<section class="specialist-dialog__section"><span class="specialist-dialog__section-title">О специалисте</span>'
        + specialist.about.slice(0, 2).map(function (paragraph) { return '<p>' + paragraph + '</p>'; }).join('')
        + '</section>'
        + '<section class="specialist-dialog__section"><span class="specialist-dialog__section-title">С чем работает</span><ul class="specialist-dialog__list">'
        + specialist.workAreas.slice(0, 6).map(function (area) { return '<li>' + area + '</li>'; }).join('')
        + '</ul></section>'
        + '<section class="specialist-dialog__section"><span class="specialist-dialog__section-title">Образование</span><ul class="specialist-dialog__list">'
        + specialist.education.map(function (item) { return '<li>' + item + '</li>'; }).join('')
        + '</ul></section>'
        + '<section class="specialist-dialog__section"><span class="specialist-dialog__section-title">Стоимость</span><p>Первичный приём — <strong>' + ns.priceLabel(specialist.price) + '</strong></p></section>'
        + (slots.length
          ? '<section class="specialist-dialog__section"><span class="specialist-dialog__section-title">Ближайшее время</span><div class="specialist-dialog__slots">'
            + slots.map(function (date) {
              return '<button class="specialist-dialog__slot" type="button" data-slot="' + date.toISOString() + '">' + ns.dateLabel(date) + '</button>';
            }).join('') + '</div></section>'
          : '')
        + '<button class="button specialist-quiz__primary" type="button" data-dialog-book>Записаться к специалисту</button>'
      );
    }

    function renderBooking(selectedDate) {
      var specialist = activeSpecialist;
      var nearest = selectedDate || ns.getAvailability(specialist)[0];
      var date = (draft && draft.date) || (nearest ? ns.localDate(nearest) : '');
      var time = (draft && draft.time) || (nearest ? nearest.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' }) : '');
      show(
        '<h2 id="specialist-dialog-title" class="specialist-dialog__title" tabindex="-1" data-dialog-title>Запись к ' + specialist.bookingName + '</h2>'
        + '<p class="specialist-quiz__hint">' + specialist.role + ' · ' + ns.priceLabel(specialist.price) + '</p>'
        + '<form class="specialist-booking" data-specialist-booking>'
        + '<label class="specialist-booking__field">Имя<input name="name" type="text" autocomplete="given-name" maxlength="80" required value="' + ns.escapeHtml((draft && draft.name) || '') + '"></label>'
        + '<label class="specialist-booking__field">Телефон<input name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+7 (___) ___-__-__" maxlength="24" required value="' + ns.escapeHtml((draft && draft.phone) || '') + '" aria-describedby="booking-phone-hint"><span class="specialist-quiz__hint" id="booking-phone-hint">От 10 до 15 цифр, можно с кодом страны.</span></label>'
        + '<div class="specialist-booking__row"><label class="specialist-booking__field">Предпочтительная дата<input name="date" type="date" min="' + ns.localDate(new Date()) + '" value="' + date + '" required></label>'
        + '<label class="specialist-booking__field">Предпочтительное время<input name="time" type="time" value="' + time + '" required></label></div>'
        + '<label class="specialist-booking__field">Формат консультации<select name="format">'
        + specialist.formats.map(function (format) {
          return '<option value="' + format + '" ' + ((draft && draft.format === format) ? 'selected' : '') + '>' + ns.formatLabel(format) + '</option>';
        }).join('') + '</select></label>'
        + '<label class="specialist-booking__consent"><input type="checkbox" name="consent" required ' + ((draft && draft.consent) ? 'checked' : '') + '><span>Я согласен с <button class="specialist-booking__policy" type="button" data-dialog-policy>условиями обработки персональных данных</button></span></label>'
        + '<p class="specialist-quiz__error" data-booking-error role="alert"></p>'
        + '<button class="button specialist-quiz__primary" type="submit">Записаться</button></form>'
      );
    }

    dialog.addEventListener('click', function (event) {
      if (event.target.closest('[data-specialist-dialog-close]')) dialog.close();
      if (event.target === dialog) {
        var bounds = dialog.getBoundingClientRect();
        if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) {
          dialog.close();
        }
      }
      if (event.target.closest('[data-dialog-book]')) renderBooking();
      var slot = event.target.closest('[data-slot]');
      if (slot) renderBooking(new Date(slot.dataset.slot));
      if (event.target.closest('[data-dialog-policy]')) {
        draft = Object.fromEntries(new FormData(content.querySelector('form')));
        show(
          '<h2 id="specialist-dialog-title" class="specialist-dialog__title" tabindex="-1" data-dialog-title>Условия обработки данных</h2>'
          + '<p>Имя, телефон, дата и время используются для связи по заявке на приём. Не указывайте диагноз или другие медицинские сведения в этой форме.</p>'
          + '<button class="button specialist-quiz__primary" type="button" data-policy-back>Вернуться к записи</button>'
        );
      }
      if (event.target.closest('[data-policy-back]')) renderBooking();
    });

    dialog.addEventListener('input', function (event) {
      if (event.target.setCustomValidity) event.target.setCustomValidity('');
    });

    dialog.addEventListener('submit', function (event) {
      if (!event.target.matches('[data-specialist-booking]')) return;
      event.preventDefault();
      var form = event.target;
      var values = Object.fromEntries(new FormData(form));
      var digits = values.phone.replace(/\D/g, '');
      var phoneValid = /^[+\d\s()\-]+$/.test(values.phone) && digits.length >= 10 && digits.length <= 15;
      form.elements.name.setCustomValidity(values.name.trim() ? '' : 'Введите имя.');
      form.elements.phone.setCustomValidity(phoneValid ? '' : 'Введите телефон: от 10 до 15 цифр.');
      form.elements.time.setCustomValidity(new Date(values.date + 'T' + values.time) > new Date() ? '' : 'Выберите будущее время.');
      if (!form.reportValidity()) return;
      draft = null;
      show(
        '<div class="specialist-dialog__success"><span class="specialist-dialog__success-mark" aria-hidden="true">✓</span>'
        + '<h2 id="specialist-dialog-title" class="specialist-dialog__title" tabindex="-1" data-dialog-title>Заявка отправлена</h2>'
        + '<p>Администратор клиники свяжется с вами для подтверждения времени приёма.</p>'
        + '<button class="button specialist-quiz__primary" type="button" data-specialist-dialog-close>Вернуться к специалистам</button></div>'
      );
    });

    dialog.addEventListener('close', function () {
      content.innerHTML = '';
      draft = null;
      if (opener && opener.isConnected) opener.focus({ preventScroll: true });
    });

    return { open: open };
  };
})(window);
