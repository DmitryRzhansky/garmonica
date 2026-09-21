(function (global) {
  var ns = (global.GarmonicaSpecialist = global.GarmonicaSpecialist || {});

  var profiles = [
    ['Луговцев Андрей Викторович', 'Андрею Викторовичу Луговцеву', 'Медицинское сопровождение детоксикации', 14],
    ['Вереснин Павел Олегович', 'Павлу Олеговичу Вереснину', 'Профилактика повторных срывов', 22],
    ['Долинцев Кирилл Алексеевич', 'Кириллу Алексеевичу Долинцеву', 'Тревожные и панические состояния', 18],
    ['Миролесов Иван Дмитриевич', 'Ивану Дмитриевичу Миролесову', 'Расстройства сна у взрослых', 7],
    ['Ладоречев Александр Игоревич', 'Александру Игоревичу Ладоречеву', 'Когнитивно-поведенческая психотерапия', 15],
    ['Белоозерцев Пётр Владимирович', 'Петру Владимировичу Белоозерцеву', 'Психотерапия эмоциональных кризисов', 25],
    ['Озернин Марк Евгеньевич', 'Марку Евгеньевичу Озернину', 'Клиническая психологическая диагностика', 8],
    ['Липовцев Константин Павлович', 'Константину Павловичу Липовцеву', 'Психологическая работа с созависимостью', 22],
  ];

  var medicalSchools = ['Пермский государственный медицинский университет', 'Казанский государственный медицинский университет', 'Уральский государственный медицинский университет'];
  var psychologySchools = ['Московский государственный университет имени М. В. Ломоносова', 'Санкт-Петербургский государственный университет'];
  var descriptions = [
    'Помогает разобраться с зависимостью и обсудить последовательный план медицинской помощи.',
    'Проводит оценку состояния, объясняет возможные варианты помощи и наблюдения.',
    'Помогает замечать повторяющиеся реакции и постепенно осваивать способы справляться с трудностями.',
    'Помогает исследовать эмоциональные трудности, привычные способы поведения и ресурсы для изменений.',
  ];

  ns.specialists = profiles.map(function (profile, index) {
    var name = profile[0];
    var bookingName = profile[1];
    var focus = profile[2];
    var experience = profile[3];
    var group = Math.floor(index / 2);
    var direction = ns.directions[group];
    var primaryProblems = direction.problems.filter(function (problem) { return problem !== 'Другое'; });
    var problems = Array.from({ length: 6 }, function (_, offset) {
      return primaryProblems[(index + offset) % primaryProblems.length];
    });
    var specialties = [direction.id];
    if (group === 0 && index === 0) specialties.push('psychiatry');
    if (group === 2 && index === 4) specialties.push('psychiatry');
    var role = specialties.length === 1
      ? direction.role
      : (group === 0 ? 'Врач-психиатр, психиатр-нарколог' : 'Врач-психиатр, врач-психотерапевт');
    var receptionFormats = group === 0
      ? [['clinic', 'home'], ['clinic', 'hospital']][index % 2]
      : [['clinic', 'online'], ['clinic'], ['online']][index % 3];

    return {
      id: 'specialist-' + String(index + 1).padStart(2, '0'),
      name: name,
      bookingName: bookingName,
      role: role,
      focus: focus,
      experience: experience,
      specialties: specialties,
      problems: problems,
      photo: 'assets/images/specialists/specialist-' + String(index + 1).padStart(2, '0') + '.webp',
      description: descriptions[group] + ' Основной фокус — ' + focus.toLocaleLowerCase('ru') + '.',
      about: [
        name + ' — ' + role.toLocaleLowerCase('ru') + '. Стаж: ' + experience + ' лет. Основное направление работы — ' + focus.toLocaleLowerCase('ru') + '.',
        group === 3
          ? 'На встрече обсуждает запрос, проводит психологическую оценку и помогает определить цели совместной работы. Не назначает лекарства и не заменяет консультацию врача.'
          : 'На первой встрече уточняет запрос и историю обращения, объясняет подход к помощи и вместе с пациентом обсуждает дальнейшие шаги.',
      ],
      workAreas: problems.concat([focus, group === 3 ? 'Психологическое сопровождение изменений' : 'Планирование дальнейшего сопровождения']),
      education: group === 3
        ? [psychologySchools[index % 2] + ' — специалитет «Клиническая психология»', 'Повышение квалификации: психологическая диагностика и консультирование взрослых']
        : [medicalSchools[index % 3] + ' — специалитет «Лечебное дело»', 'Ординатура по психиатрии'].concat(
          group === 0 ? ['Профессиональная переподготовка по психиатрии-наркологии'] : group === 2 ? ['Профессиональная переподготовка по психотерапии'] : ['Повышение квалификации по психиатрии']
        ),
      formats: receptionFormats,
      price: [4500, 4800, 5200, 3200][group] + index * 50,
      availability: [0, 2, 5].map(function (gap, slot) {
        return {
          dayOffset: index % 6 + gap,
          time: String(10 + (index + slot * 2) % 10).padStart(2, '0') + ':' + (index % 2 ? '30' : '00'),
        };
      }),
    };
  });

  ns.getSpecialists = function () {
    return ns.specialists;
  };
})(window);
