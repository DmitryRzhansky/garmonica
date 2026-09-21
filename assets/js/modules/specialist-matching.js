(function (global) {
  var ns = (global.GarmonicaSpecialist = global.GarmonicaSpecialist || {});

  ns.hasEmergency = function (problems) {
    return problems.some(function (problem) {
      return ns.emergencyProblems.indexOf(problem) !== -1;
    });
  };

  ns.resolveDirections = function (direction, problems) {
    problems = problems || [];
    if (direction && direction !== 'unsure') return [direction];
    if (!direction) return [];
    var scores = new Map(ns.directions.map(function (item) { return [item.id, 0]; }));
    ns.universalProblems.filter(function (item) {
      return problems.indexOf(item.title) !== -1;
    }).forEach(function (item) {
      item.directions.forEach(function (id, index) {
        scores.set(id, scores.get(id) + 3 - index);
      });
    });
    return Array.from(scores).filter(function (entry) {
      return entry[1] > 0;
    }).sort(function (a, b) {
      return b[1] - a[1];
    }).slice(0, 2).map(function (entry) {
      return entry[0];
    });
  };

  ns.resolveProblems = function (problems) {
    problems = problems || [];
    var resolved = [];
    problems.forEach(function (problem) {
      var match = ns.universalProblems.find(function (item) { return item.title === problem; });
      var items = match ? match.problems : [problem];
      items.forEach(function (item) {
        if (resolved.indexOf(item) === -1) resolved.push(item);
      });
    });
    return resolved.filter(function (problem) {
      return problem !== 'Другое' && ns.emergencyProblems.indexOf(problem) === -1;
    });
  };

  ns.getAvailability = function (specialist, now) {
    now = now || new Date();
    return specialist.availability.map(function (slot) {
      var date = new Date(now);
      var parts = slot.time.split(':').map(Number);
      date.setDate(date.getDate() + slot.dayOffset);
      date.setHours(parts[0], parts[1], 0, 0);
      return date;
    }).filter(function (date) {
      return date > now;
    }).sort(function (a, b) {
      return a - b;
    });
  };

  ns.localDate = function (date) {
    return date.getFullYear() + '-' + String(date.getMonth() + 1).padStart(2, '0') + '-' + String(date.getDate()).padStart(2, '0');
  };

  ns.dateLabel = function (date, now) {
    now = now || new Date();
    if (!date) return 'Дата уточняется';
    var day = ns.localDate(date) === ns.localDate(now)
      ? 'Сегодня'
      : date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' });
    return day + ', ' + date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
  };

  ns.matchSpecialists = function (specialists, criteria, now) {
    now = now || new Date();
    var selectedDirections = ns.resolveDirections(criteria.direction, criteria.problems);
    var problems = ns.resolveProblems(criteria.problems);
    var timing = ns.timings.find(function (item) { return item.id === criteria.when; });
    var requestedDays = timing ? timing.days : Infinity;
    var midnight = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    var ranked = specialists.map(function (specialist) {
      var directionMatch = !selectedDirections.length || specialist.specialties.some(function (id) {
        return selectedDirections.indexOf(id) !== -1;
      });
      var formatMatch = !criteria.format || specialist.formats.indexOf(criteria.format) !== -1;
      var problemMatches = problems.filter(function (problem) {
        return specialist.problems.indexOf(problem) !== -1;
      }).length;
      var nearest = ns.getAvailability(specialist, now)[0];
      var days = nearest
        ? Math.round((new Date(nearest.getFullYear(), nearest.getMonth(), nearest.getDate()) - midnight) / 86400000)
        : Infinity;
      var score = (selectedDirections.length && directionMatch ? 10 : 0)
        + problemMatches * 5
        + (criteria.format && formatMatch ? 4 : 0)
        + (criteria.when && criteria.when !== 'any' && days <= requestedDays ? 3 : 0)
        + (specialist.specialties.slice(1).some(function (id) {
          return selectedDirections.indexOf(id) !== -1;
        }) ? 2 : 0);
      return {
        specialist: specialist,
        directionMatch: directionMatch,
        formatMatch: formatMatch,
        problemMatch: !problems.length || problemMatches > 0,
        nearest: nearest,
        score: score,
      };
    });

    var exact = ranked.filter(function (item) {
      return item.directionMatch && item.formatMatch && item.problemMatch;
    });
    var formatFallback = ranked.filter(function (item) {
      return item.directionMatch && item.formatMatch;
    });
    var pool = exact.length
      ? exact
      : (formatFallback.length ? formatFallback : ranked.filter(function (item) { return item.directionMatch; }));

    pool.sort(function (a, b) {
      return b.score - a.score
        || ((a.nearest && a.nearest.getTime()) || Infinity) - ((b.nearest && b.nearest.getTime()) || Infinity)
        || a.specialist.id.localeCompare(b.specialist.id);
    });

    return {
      items: pool.map(function (item) { return item.specialist; }),
      fallback: !exact.length,
      directions: selectedDirections,
    };
  };
})(window);
