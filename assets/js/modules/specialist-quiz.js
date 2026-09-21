(function (global) {
  var ns = (global.GarmonicaSpecialist = global.GarmonicaSpecialist || {});

  function initSpecialistQuiz() {
    var root = document.querySelector('[data-specialist-quiz]');
    if (!root) return;

    var specialists = ns.getSpecialists();
    var intro = root.querySelector('[data-quiz-intro]');
    var panel = root.querySelector('[data-quiz-panel]');
    var results = root.querySelector('[data-quiz-results]');
    var list = root.querySelector('[data-specialist-list]');
    var dialog = ns.createSpecialistDialog(document.querySelector('[data-specialist-dialog]'), specialists);
    var step = 0;
    var answers = { direction: '', problems: [], format: null, when: '' };
    var matchCriteria = { direction: '', problems: [], format: '', when: '' };
    var expanded = false;
    var emergencyAcknowledged = false;
    var currentItems = [];

    function reveal(view) {
      intro.hidden = view !== 'intro';
      panel.hidden = view !== 'step' && view !== 'emergency';
      results.hidden = view !== 'results';
    }

    function focusView(element) {
      if (element) element.focus({ preventScroll: true });
      root.scrollIntoView({
        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth',
        block: 'start',
      });
    }

    function renderStep() {
      reveal('step');
      panel.innerHTML = ns.stepView(step, answers, specialists);
      focusView(panel.querySelector('[data-step-title]'));
    }

    function renderEmergency() {
      reveal('emergency');
      panel.innerHTML = ns.emergencyView();
      focusView(panel.querySelector('[data-step-title]'));
    }

    function renderCards() {
      var visible = expanded ? currentItems : currentItems.slice(0, 3);
      list.innerHTML = visible.map(ns.cardView).join('');
      var more = root.querySelector('[data-action="more"]');
      more.hidden = currentItems.length <= 3 || expanded;
      more.textContent = 'Показать всех подходящих специалистов (' + currentItems.length + ')';
    }

    function updateResults() {
      var result = ns.matchSpecialists(specialists, matchCriteria);
      currentItems = result.items;
      root.querySelector('[data-results-count]').textContent = 'Найдено: ' + ns.countLabel(currentItems.length);
      root.querySelector('[data-results-emergency]').hidden = !emergencyAcknowledged;
      renderCards();
    }

    function showResults(fromQuiz) {
      if (fromQuiz && ns.hasEmergency(answers.problems) && !emergencyAcknowledged) {
        renderEmergency();
        return;
      }
      if (fromQuiz) {
        matchCriteria = {
          direction: answers.direction,
          problems: answers.problems.slice(),
          format: answers.format || '',
          when: answers.when,
        };
      }
      reveal('results');
      expanded = false;
      updateResults();
      focusView(root.querySelector('[data-results-title]'));
    }

    root.addEventListener('change', function (event) {
      var input = event.target;
      if (!input.closest('[data-quiz-step]')) return;

      if (input.name === 'direction' && answers.direction !== input.value) {
        answers.direction = input.value;
        answers.problems = [];
        answers.format = null;
        emergencyAcknowledged = false;
      }
      if (input.name === 'problems') {
        answers.problems = Array.prototype.map.call(
          panel.querySelectorAll('input[name="problems"]:checked'),
          function (item) { return item.value; }
        );
        var allowedFormats = ns.availableFormats(specialists, answers.direction, answers.problems);
        if (answers.format && !allowedFormats.some(function (format) { return format.id === answers.format; })) {
          answers.format = null;
        }
        if (ns.hasEmergency(answers.problems)) {
          emergencyAcknowledged = false;
          renderEmergency();
          return;
        }
      }
      if (input.name === 'format') answers.format = input.value;
      if (input.name === 'when') answers.when = input.value;
      panel.querySelector('[data-step-error]').textContent = '';
    });

    root.addEventListener('submit', function (event) {
      if (!event.target.matches('[data-quiz-step]')) return;
      event.preventDefault();
      var valid = [
        Boolean(answers.direction),
        answers.problems.length > 0,
        answers.format !== null,
        Boolean(answers.when),
      ][step];
      if (!valid) {
        panel.querySelector('[data-step-error]').textContent = step === 1
          ? 'Выберите хотя бы один вариант.'
          : 'Выберите один вариант, чтобы продолжить.';
        return;
      }
      if (step < 3) {
        step += 1;
        renderStep();
      } else {
        showResults(true);
      }
    });

    root.addEventListener('click', function (event) {
      var profile = event.target.closest('[data-profile]');
      var booking = event.target.closest('[data-book]');
      if (profile) {
        event.preventDefault();
        if (dialog) dialog.open(profile.dataset.profile, 'profile', profile);
      }
      if (booking && dialog) dialog.open(booking.dataset.book, 'booking', booking);

      var trigger = event.target.closest('[data-action]');
      if (!trigger) return;
      var action = trigger.dataset.action;

      if (action === 'start') {
        step = 0;
        renderStep();
      }
      if (action === 'back') {
        if (step > 0) {
          step -= 1;
          renderStep();
        } else {
          reveal('intro');
          focusView(root.querySelector('[data-action="start"]'));
        }
      }
      if (action === 'emergency-back') {
        step = 1;
        renderStep();
      }
      if (action === 'emergency-browse') {
        emergencyAcknowledged = true;
        matchCriteria = {
          direction: ns.resolveDirections(answers.direction, answers.problems)[0] || '',
          problems: [],
          format: '',
          when: '',
        };
        showResults();
      }
      if (action === 'more') {
        expanded = true;
        renderCards();
        var bookButtons = list.querySelectorAll('[data-book]');
        if (bookButtons[3]) bookButtons[3].focus({ preventScroll: true });
      }
    });
  }

  global.initSpecialistQuiz = initSpecialistQuiz;
})(window);
