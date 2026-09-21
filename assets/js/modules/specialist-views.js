(function (global) {
  var ns = (global.GarmonicaSpecialist = global.GarmonicaSpecialist || {});

  var iconArrowRight = '<img class="button__icon" src="assets/icons/arrow-right.svg" alt="" width="16" height="16" decoding="async" aria-hidden="true">';
  var iconCaretLeft = '<img class="specialist-quiz__nav-icon" src="assets/icons/caret-left.svg" alt="" width="14" height="14" decoding="async" aria-hidden="true">';
  var iconArrowOut = '<img class="specialist-quiz__nav-icon" src="assets/icons/arrow-right.svg" alt="" width="14" height="14" decoding="async" aria-hidden="true">';

  ns.escapeHtml = function (value) {
    return String(value).replace(/[&<>"']/g, function (character) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character];
    });
  };

  ns.priceLabel = function (price) {
    return 'от ' + price.toLocaleString('ru-RU') + ' ₽';
  };

  ns.yearsLabel = function (years) {
    var mod10 = years % 10;
    var mod100 = years % 100;
    var word = (mod10 === 1 && mod100 !== 11)
      ? 'год'
      : (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14) ? 'года' : 'лет');
    return years + ' ' + word;
  };

  ns.countLabel = function (count) {
    var mod10 = count % 10;
    var mod100 = count % 100;
    var word = (mod10 === 1 && mod100 !== 11)
      ? 'специалист'
      : (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14) ? 'специалиста' : 'специалистов');
    return count + ' ' + word;
  };

  ns.availableFormats = function (specialists, direction, problems) {
    var selected = ns.resolveDirections(direction, problems);
    return ns.formats.filter(function (format) {
      return specialists.some(function (specialist) {
        var directionOk = !selected.length || specialist.specialties.some(function (id) {
          return selected.indexOf(id) !== -1;
        });
        return directionOk && specialist.formats.indexOf(format.id) !== -1;
      });
    });
  };

  function choice(item, name, selected, type) {
    type = type || 'radio';
    return '<label class="specialist-quiz__choice' + (name === 'problems' ? ' specialist-quiz__choice--compact' : '') + '">'
      + '<input class="specialist-quiz__input" type="' + type + '" name="' + name + '" value="' + ns.escapeHtml(item.id != null ? item.id : item.title) + '" ' + (selected ? 'checked' : '') + '>'
      + '<span class="specialist-quiz__choice-content">'
      + (item.icon ? '<span class="specialist-quiz__choice-number" aria-hidden="true">' + item.icon + '</span>' : '')
      + '<span class="specialist-quiz__choice-title">' + ns.escapeHtml(item.title) + '</span>'
      + (item.description ? '<span class="specialist-quiz__choice-description">' + ns.escapeHtml(item.description) + '</span>' : '')
      + (item.note ? '<span class="specialist-quiz__choice-note">' + ns.escapeHtml(item.note) + '</span>' : '')
      + '</span><span class="specialist-quiz__choice-mark" aria-hidden="true"></span></label>';
  }

  ns.stepView = function (step, answers, specialists) {
    var choices = '';
    if (step === 0) {
      choices = ns.directions.concat([ns.uncertainDirection]).map(function (item) {
        return choice(item, 'direction', answers.direction === item.id);
      }).join('');
    }
    if (step === 1) {
      var problems = answers.direction === 'unsure'
        ? ns.universalProblems.map(function (item) { return item.title; })
        : ((ns.directionById(answers.direction) || {}).problems || []);
      choices = problems.map(function (title) {
        return choice({ title: title }, 'problems', answers.problems.indexOf(title) !== -1, 'checkbox');
      }).join('');
    }
    if (step === 2) {
      choices = ns.availableFormats(specialists, answers.direction, answers.problems)
        .concat([{ id: '', title: 'Пока не знаю', description: 'Покажем все доступные форматы' }])
        .map(function (item) {
          return choice(item, 'format', answers.format === item.id);
        }).join('');
    }
    if (step === 3) {
      choices = ns.timings.map(function (item) {
        return choice(item, 'when', answers.when === item.id);
      }).join('');
    }

    var inferred = '';
    if (answers.direction === 'unsure' && step === 2) {
      inferred = ns.resolveDirections(answers.direction, answers.problems).map(function (id) {
        return ns.directionById(id).title;
      }).join(' · ');
    }

    return '<div class="specialist-quiz__progress-heading"><span>Шаг ' + (step + 1) + ' из 4</span><span>'
      + ['Направление', 'Ваш запрос', 'Формат', 'Дата'][step] + '</span></div>'
      + '<progress class="specialist-quiz__progress" value="' + (step + 1) + '" max="4" aria-label="Шаг ' + (step + 1) + ' из 4"></progress>'
      + '<form data-quiz-step><fieldset class="specialist-quiz__fieldset">'
      + '<legend class="specialist-quiz__question" data-step-title tabindex="-1">' + ns.questions[step].title + '</legend>'
      + '<p class="specialist-quiz__hint">' + ns.questions[step].hint + '</p>'
      + (inferred ? '<p class="specialist-quiz__recommendation">По вашему запросу могут подойти: <strong>' + inferred + '</strong></p>' : '')
      + '<div class="specialist-quiz__choices">' + choices + '</div>'
      + (step === 1
        ? '<details class="specialist-quiz__urgent-options"><summary>Есть признаки экстренного состояния?</summary><p>Если есть хотя бы один из этих признаков, отметьте его.</p><div class="specialist-quiz__choices">'
          + ns.emergencyProblems.map(function (title) {
            return choice({ title: title }, 'problems', answers.problems.indexOf(title) !== -1, 'checkbox');
          }).join('')
          + '</div></details>'
        : '')
      + '</fieldset><p class="specialist-quiz__error" data-step-error role="alert"></p>'
      + '<div class="specialist-quiz__navigation">'
      + '<button class="specialist-quiz__text-button" type="button" data-action="back">' + iconCaretLeft + ' Назад</button>'
      + '<button class="button specialist-quiz__primary" type="submit">'
      + (step === 3 ? 'Подобрать специалистов' : 'Продолжить') + ' ' + iconArrowRight
      + '</button></div></form>';
  };

  ns.emergencyView = function () {
    return '<div class="specialist-quiz__emergency" role="alert">'
      + '<span class="specialist-quiz__question" tabindex="-1" data-step-title>Не откладывайте обращение за помощью</span>'
      + '<p>При угрожающем жизни состоянии не используйте онлайн-запись. Обратитесь за экстренной медицинской помощью.</p>'
      + '<a class="button specialist-quiz__primary" href="tel:112">Позвонить 112</a>'
      + '<p class="specialist-quiz__hint">Подбор специалиста не заменяет экстренную помощь.</p></div>'
      + '<div class="specialist-quiz__navigation">'
      + '<button class="specialist-quiz__text-button" type="button" data-action="emergency-back">' + iconCaretLeft + ' Изменить ответы</button>'
      + '<button class="specialist-quiz__text-button" type="button" data-action="emergency-browse">Посмотреть специалистов ' + iconArrowOut + '</button>'
      + '</div>';
  };

  ns.cardView = function (specialist) {
    return '<article class="specialist-card" aria-labelledby="' + specialist.id + '-title">'
      + '<div class="specialist-card__portrait"><img class="specialist-card__photo" src="' + specialist.photo + '" alt="' + ns.escapeHtml(specialist.name) + '" width="480" height="640" loading="lazy" decoding="async">'
      + '<span class="specialist-card__experience">Стаж ' + ns.yearsLabel(specialist.experience) + '</span></div>'
      + '<div class="specialist-card__body">'
      + '<p class="specialist-card__role">' + specialist.role
      + (specialist.specialties[0] === 'psychology' ? ' · не врач' : '') + '</p>'
      + '<h4 class="specialist-card__name" id="' + specialist.id + '-title">' + specialist.name + '</h4>'
      + '<p class="specialist-card__description">' + specialist.description + '</p>'
      + '<p class="specialist-card__price">Первичный приём <strong>' + ns.priceLabel(specialist.price) + '</strong></p>'
      + '<button class="button specialist-quiz__primary" type="button" data-book="' + specialist.id + '">Записаться</button>'
      + '<a class="specialist-card__details" href="#profile-' + specialist.id + '" data-profile="' + specialist.id + '">Подробнее о специалисте ' + iconArrowOut + '</a>'
      + '</div></article>';
  };
})(window);
