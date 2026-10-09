"""Данные блока «Как работает наша выездная служба»."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_PAGES_PATH = Path(__file__).with_name("pages.json")

FIELD_SERVICE_TITLE = "Как работает наша выездная служба"

FIELD_SERVICE_TABS = [
    {"key": "equipment", "label": "Оборудование", "icon": "/assets/icons/first-aid-kit.svg"},
    {"key": "overview", "label": "География выезда", "icon": "/assets/icons/map-pin.svg"},
    {"key": "vehicles", "label": "Автомобили", "icon": "/assets/icons/car.svg"},
    {"key": "doctors", "label": "Специалисты", "icon": "/assets/icons/users.svg"},
    {"key": "process", "label": "Как проходит выезд", "icon": "/assets/icons/arrow-right.svg"},
]

FIELD_SERVICE_EQUIPMENT = [
    {
        "slug": "resuscitation-kit",
        "tab": "Реанимационный набор",
        "title": "Реанимационный набор",
        "icon": "/assets/icons/first-aid-kit.svg",
        "photo": "/assets/images/field-service/instruments/resuscitation-kit.webp",
        "photo_alt": "Реанимационный набор выездной бригады с аппаратом ИВЛ, интубационными трубками и масками",
        "model": "",
        "purpose": "Оказание помощи пациентам в критических ситуациях: кома, тяжёлая интоксикация, клиническая смерть.",
        "measures": "Проходимость дыхательных путей, вентиляция лёгких, аспирация, подготовка к интубации.",
        "when": "При угрозе дыханию и кровообращению на выезде, до приезда реанимации или параллельно с ней.",
        "on_every_visit": "Да, в базовой укладке каждой бригады",
    },
    {
        "slug": "ambu-bag",
        "tab": "Мешок Амбу",
        "title": "Мешок Амбу",
        "icon": "/assets/icons/first-aid.svg",
        "photo": "/assets/images/field-service/instruments/ambu-bag.webp",
        "photo_alt": "Ручной аппарат ИВЛ — мешок Амбу для искусственной вентиляции лёгких",
        "model": "Ручной аппарат ИВЛ (мешок Амбу)",
        "purpose": "Нагнетать воздух в лёгкие, когда пациент не дышит самостоятельно или дыхание недостаточно.",
        "measures": "Объём и ритм вентиляции при ручной ИВЛ.",
        "when": "При остановке дыхания, глубокой коме и подготовке к интубации на выезде.",
        "on_every_visit": "Да, в реанимационном наборе",
    },
    {
        "slug": "laryngoscope",
        "tab": "Ларингоскоп",
        "title": "Ларингоскоп",
        "icon": "/assets/icons/stethoscope.svg",
        "photo": "/assets/images/field-service/instruments/laryngoscope.webp",
        "photo_alt": "Ларингоскоп с клинком для интубации трахеи на выезде",
        "model": "Ларингоскоп с рукоятью",
        "purpose": "Визуализировать гортань и провести интубацию трахеи для защиты дыхательных путей.",
        "measures": "Контроль проходимости дыхательных путей при интубации.",
        "when": "При необходимости интубации на выезде вместе с интубационными трубками и анестезиологической маской.",
        "on_every_visit": "Да, в реанимационном наборе",
    },
    {
        "slug": "ecg",
        "tab": "Аппарат ЭКГ",
        "title": "Аппарат ЭКГ",
        "icon": "/assets/icons/heartbeat.svg",
        "photo": "/assets/images/field-service/instruments/ecg.webp",
        "photo_alt": "Портативный аппарат ЭКГ с кабелями и электродами для выезда",
        "model": "Портативный электрокардиограф",
        "purpose": "Выявить острую коронарную патологию и нарушения ритма сердца прямо на выезде.",
        "measures": "Электрокардиограмма по стандартным и грудным отведениям, печать ленты.",
        "when": "При боли в груди, одышке, обмороке, нарушении ритма и в любой критической кардиологической ситуации.",
        "on_every_visit": "Да, в составе каждой бригады",
    },
    {
        "slug": "tonometer",
        "tab": "Тонометр",
        "title": "Тонометр",
        "icon": "/assets/icons/heartbeat.svg",
        "photo": "/assets/images/field-service/instruments/tonometer.webp",
        "photo_alt": "Автоматический тонометр для измерения артериального давления на выезде",
        "brand": "Omron",
        "model": "M2 Basic (HEM-7121-RU)",
        "purpose": "Оценка гемодинамики при осмотре и во время терапии на дому.",
        "measures": "Систолическое и диастолическое давление, пульс.",
        "when": "На первичном осмотре, до и во время капельницы, при ухудшении самочувствия.",
        "on_every_visit": "Да, в базовой укладке",
    },
    {
        "slug": "pulse-oximeter",
        "tab": "Пульсоксиметр",
        "title": "Пульсоксиметр",
        "icon": "/assets/icons/heartbeat.svg",
        "photo": "/assets/images/field-service/instruments/pulse-oximeter.webp",
        "photo_alt": "Пульсоксиметр на пальце для измерения насыщения крови кислородом и пульса",
        "model": "Пульсоксиметр",
        "purpose": "Быстро оценить дыхательную функцию и состояние кровообращения без инвазивных процедур.",
        "measures": "Насыщение крови кислородом (SpO₂) и пульс.",
        "when": "При одышке, интоксикации, во время инфузий и при любом ухудшении состояния на выезде.",
        "on_every_visit": "Да, в базовой укладке",
    },
    {
        "slug": "glucometer",
        "tab": "Глюкометр",
        "title": "Глюкометр",
        "icon": "/assets/icons/syringe.svg",
        "photo": "/assets/images/field-service/instruments/glucometer.webp",
        "photo_alt": "Глюкометр для измерения уровня сахара в крови на выезде",
        "model": "Глюкометр",
        "purpose": "Исключить гипо- и гипергликемию как причину слабости, спутанности или потери сознания.",
        "measures": "Уровень глюкозы в крови.",
        "when": "При подозрении на диабетический криз, обмороке, интоксикации и перед/во время инфузионной терапии.",
        "on_every_visit": "Да, в базовой укладке",
    },
    {
        "slug": "meds-kit",
        "tab": "Укладка с препаратами",
        "title": "Укладка с препаратами",
        "icon": "/assets/icons/first-aid-kit.svg",
        "photo": "/assets/images/field-service/instruments/meds-kit.webp",
        "photo_alt": "Медицинская укладка выездной бригады с препаратами, шприцами и расходными материалами",
        "model": "Медицинская укладка + мини-укладка с таблетками",
        "purpose": "Быстро оказать помощь на месте: инъекции, катетеризация, таблетированные препараты.",
        "measures": "Лекарства, шприцы, катетеры, системы, спиртовые салфетки и мини-набор таблеток.",
        "when": "На каждом вызове: препараты подписаны для скорости оказания помощи.",
        "on_every_visit": "Да, в составе каждой бригады",
    },
    {
        "slug": "solutions-kit",
        "tab": "Укладка с растворами",
        "title": "Укладка с растворами",
        "icon": "/assets/icons/syringe.svg",
        "photo": "/assets/images/field-service/instruments/solutions-kit.webp",
        "photo_alt": "Укладка с инфузионными растворами и системами для капельниц на выезде",
        "model": "Инфузионная укладка",
        "purpose": "Экстренная помощь при обезвоживании, отравлениях и восполнении объёма циркулирующей крови.",
        "measures": "Запас инфузионных растворов для капельниц на дому.",
        "when": "При детоксикации, инфузионной терапии и состояниях с потерей жидкости.",
        "on_every_visit": "Да, в составе каждой бригады",
    },
]

FIELD_SERVICE_COVERAGE = {
    "title": "География и время выезда",
    "rings": ["МКАД", "10 км", "30 км", "60 км"],
    "zones": [
        {"zone": "Москва в пределах МКАД", "eta": "30–45", "unit": "мин", "fill": 26},
        {"zone": "До 10 км за МКАД", "eta": "40–55", "unit": "мин", "fill": 38},
        {"zone": "10–30 км от МКАД", "eta": "55–80", "unit": "мин", "fill": 55},
        {"zone": "30–60 км от МКАД", "eta": "1–2", "unit": "ч", "fill": 72},
        {"zone": "Более 60 км от МКАД", "eta": "индивидуально", "unit": "", "fill": 88},
    ],
    "footnote": "Ориентир прибытия уточняет диспетчер при принятии вызова: зависит от адреса, трафика и свободного борта.",
}

FIELD_SERVICE_FLEET = {
    "count": "4",
    "title": "автомобиля выездной службы",
    "lead": "Каждый борт закреплён за сменой, проходит регламентное ТО и выезжает с укомплектованной укладкой. Машины без наружной рекламы — соседи не замечают выезд.",
    "source": "Число адресов — завершённые выезды по журналу колтрекинга клиники «НОВА» за последние 12 месяцев.",
    "cars": [
        {
            "id": "creta",
            "tab": "Creta",
            "name": "Hyundai Creta",
            "role": "Основной борт дневной смены",
            "text": "Универсальный кроссовер для большинства вызовов в пределах МКАД и ближнего Подмосковья: врач, укладка и место под инфузионную терапию.",
            "gallery": [
                {
                    "file": "/assets/images/field-service/fleet/fleet-creta-exterior.webp",
                    "alt": "Белый Hyundai Creta выездной службы у жилого двора",
                    "label": "Экстерьер",
                },
                {
                    "file": "/assets/images/field-service/fleet/fleet-creta-interior.webp",
                    "alt": "Салон Hyundai Creta с медицинской сумкой на пассажирском сиденье",
                    "label": "Интерьер",
                },
                {
                    "file": "/assets/images/field-service/fleet/fleet-creta-equipment.webp",
                    "alt": "Укладка и инфузии в багажнике Hyundai Creta",
                    "label": "Оборудование",
                },
            ],
            "facts": [
                {"icon": "/assets/icons/car.svg", "label": "Марка и модель", "value": "Hyundai Creta"},
                {"icon": "/assets/icons/calendar-check.svg", "label": "Год выпуска", "value": "2022"},
                {"icon": "/assets/icons/seal-check.svg", "label": "ТО", "value": "Официальный сервис, раз в 10 000 км"},
                {"icon": "/assets/icons/phone.svg", "label": "Адресов за 12 мес.", "value": "980"},
                {"icon": "/assets/icons/first-aid-kit.svg", "label": "Оснащение", "value": "ЭКГ, реанимационный набор, инфузии"},
                {"icon": "/assets/icons/clock.svg", "label": "Смена", "value": "День / вечер"},
            ],
        },
        {
            "id": "karoq",
            "tab": "Karoq",
            "name": "Škoda Karoq",
            "role": "Ночной дежурный борт",
            "text": "Кроссовер ночной смены: выше клиренс, проще дворы и парковка. Держит дежурство после полуночи, когда важен надёжный запуск и полный заряд АКБ.",
            "gallery": [
                {
                    "file": "/assets/images/field-service/fleet/fleet-karoq-exterior.webp",
                    "alt": "Тёмный Škoda Karoq выездной службы вечером у подъезда",
                    "label": "Экстерьер",
                },
                {
                    "file": "/assets/images/field-service/fleet/fleet-karoq-interior.webp",
                    "alt": "Салон Škoda Karoq с кейсом ЭКГ на заднем сиденье",
                    "label": "Интерьер",
                },
                {
                    "file": "/assets/images/field-service/fleet/fleet-karoq-equipment.webp",
                    "alt": "Компактная укладка в багажнике Škoda Karoq",
                    "label": "Оборудование",
                },
            ],
            "facts": [
                {"icon": "/assets/icons/car.svg", "label": "Марка и модель", "value": "Škoda Karoq"},
                {"icon": "/assets/icons/calendar-check.svg", "label": "Год выпуска", "value": "2021"},
                {"icon": "/assets/icons/seal-check.svg", "label": "ТО", "value": "Дилер + предсменная проверка"},
                {"icon": "/assets/icons/phone.svg", "label": "Адресов за 12 мес.", "value": "760"},
                {"icon": "/assets/icons/first-aid-kit.svg", "label": "Оснащение", "value": "Полная укладка, пульсоксиметр, тонометр"},
                {"icon": "/assets/icons/clock.svg", "label": "Смена", "value": "Ночь 24/7"},
            ],
        },
        {
            "id": "passat",
            "tab": "Passat",
            "name": "Volkswagen Passat",
            "role": "Резерв и пиковые часы",
            "text": "Резервный седан на пики пятницы и праздников. Подключается, когда основные машины уже на адресах, чтобы не сдвигать ориентир прибытия.",
            "gallery": [
                {
                    "file": "/assets/images/field-service/fleet/fleet-passat-exterior.webp",
                    "alt": "Серебристый Volkswagen Passat выездной службы на улице",
                    "label": "Экстерьер",
                },
                {
                    "file": "/assets/images/field-service/fleet/fleet-passat-interior.webp",
                    "alt": "Салон Volkswagen Passat с медицинским рюкзаком",
                    "label": "Интерьер",
                },
                {
                    "file": "/assets/images/field-service/fleet/fleet-passat-equipment.webp",
                    "alt": "Стандартная укладка выезда в багажнике Passat",
                    "label": "Оборудование",
                },
            ],
            "facts": [
                {"icon": "/assets/icons/car.svg", "label": "Марка и модель", "value": "Volkswagen Passat"},
                {"icon": "/assets/icons/calendar-check.svg", "label": "Год выпуска", "value": "2020"},
                {"icon": "/assets/icons/seal-check.svg", "label": "ТО", "value": "По регламенту VW, сезонная подготовка"},
                {"icon": "/assets/icons/phone.svg", "label": "Адресов за 12 мес.", "value": "640"},
                {"icon": "/assets/icons/first-aid-kit.svg", "label": "Оснащение", "value": "Стандартная укладка выезда"},
                {"icon": "/assets/icons/clock.svg", "label": "Смена", "value": "Пиковые часы / резерв"},
            ],
        },
        {
            "id": "multivan",
            "tab": "Multivan",
            "name": "Volkswagen Multivan",
            "role": "Бригада и госпитализация",
            "text": "Вместительный борт, когда на адрес едут врач и медбрат или нужна перевозка в стационар. Салон позволяет разместить оборудование и сопровождение пациента.",
            "gallery": [
                {
                    "file": "/assets/images/field-service/fleet/fleet-multivan-exterior.webp",
                    "alt": "Белый Volkswagen Multivan выездной службы у дома",
                    "label": "Экстерьер",
                },
                {
                    "file": "/assets/images/field-service/fleet/fleet-multivan-interior.webp",
                    "alt": "Просторный салон Multivan с местами под укладку",
                    "label": "Интерьер",
                },
                {
                    "file": "/assets/images/field-service/fleet/fleet-multivan-equipment.webp",
                    "alt": "Расширенная укладка и кислород в багажном отделении Multivan",
                    "label": "Оборудование",
                },
            ],
            "facts": [
                {"icon": "/assets/icons/car.svg", "label": "Марка и модель", "value": "Volkswagen Multivan"},
                {"icon": "/assets/icons/calendar-check.svg", "label": "Год выпуска", "value": "2019"},
                {"icon": "/assets/icons/seal-check.svg", "label": "ТО", "value": "Дилер VW, расширенный регламент"},
                {"icon": "/assets/icons/phone.svg", "label": "Адресов за 12 мес.", "value": "520"},
                {"icon": "/assets/icons/users.svg", "label": "Состав", "value": "Врач + медбрат / перевозка"},
                {"icon": "/assets/icons/ambulance.svg", "label": "Задача", "value": "Бригада и госпитализация"},
            ],
        },
    ],
}

FIELD_SERVICE_TEAM = [
    {
        "name": "Морозов Игорь Сергеевич",
        "duty": "Фельдшер выездной службы",
        "icon": "/assets/icons/syringe.svg",
        "experience": "14 лет",
        "photo": "/assets/images/field-service/team/team-morozov.webp",
        "lead": "Основной специалист на типовом вызове: осмотр, капельница и контроль состояния на месте.",
        "duties": [
            "Проводит первичный осмотр и готовит пациента к инфузии",
            "Ставит капельницу и ведёт детоксикацию по согласованной схеме",
            "Следит за самочувствием во время и сразу после процедуры",
            "Сообщает врачу, если состояние меняется или помощь нужно усилить",
        ],
    },
    {
        "name": "Кузнецов Дмитрий Алексеевич",
        "duty": "Врач неотложной помощи",
        "icon": "/assets/icons/ambulance.svg",
        "experience": "18 лет",
        "photo": "/assets/images/field-service/team/team-kuznetsov.webp",
        "lead": "Выезжает на острые и нестабильные случаи, когда нужна быстрая стабилизация.",
        "duties": [
            "Оказывает неотложную помощь при резком ухудшении состояния",
            "Работает с возбуждением, судорожной готовностью и критическими симптомами",
            "Снимает ЭКГ и базовые показатели перед решением о госпитализации",
            "Сопровождает транспортировку, если домашний формат уже небезопасен",
        ],
    },
    {
        "name": "Белов Андрей Николаевич",
        "duty": "Анестезиолог-реаниматолог",
        "icon": "/assets/icons/first-aid-kit.svg",
        "experience": "22 года",
        "photo": "/assets/images/field-service/team/team-belov.webp",
        "lead": "Подключается к тяжёлым интоксикациям и случаям, где нужен контроль жизненных функций.",
        "duties": [
            "Оценивает дыхание, гемодинамику и риск декомпенсации на адресе",
            "Подбирает интенсивную инфузионную и поддерживающую терапию",
            "Контролирует жизненные показатели во время детоксикации",
            "Определяет, можно ли продолжать помощь дома или нужен стационар",
        ],
    },
    {
        "name": "Орлов Павел Викторович",
        "duty": "Медбрат выездной бригады",
        "icon": "/assets/icons/stethoscope.svg",
        "experience": "9 лет",
        "photo": "/assets/images/field-service/team/team-orlov.webp",
        "lead": "Работает в паре с врачом на бригадных выездах и при подготовке к госпитализации.",
        "duties": [
            "Готовит системы, катетеры и расходники до начала инфузии",
            "Помогает при заборе анализов и мониторинге на адресе",
            "Сопровождает пациента при транспортировке в стационар",
            "Проверяет комплектность укладки после каждого вызова",
        ],
    },
]

FIELD_SERVICE_STEPS = [
    {
        "number": "01",
        "icon": "/assets/icons/phone.svg",
        "title": "Принимаем обращение",
        "text": "Диспетчер уточняет причину вызова, состояние пациента, адрес и основные обстоятельства ситуации.",
        "photo": "/assets/images/field-service/steps/step-call.webp",
        "alt": "Диспетчер выездной службы принимает обращение",
    },
    {
        "number": "02",
        "icon": "/assets/icons/stethoscope.svg",
        "title": "Подбираем специалиста",
        "text": "На основании полученной информации определяется специалист или состав выездной команды.",
        "photo": "/assets/images/field-service/steps/step-select.webp",
        "alt": "Специалисты обсуждают состав выезда",
    },
    {
        "number": "03",
        "icon": "/assets/icons/car.svg",
        "title": "Передаём вызов",
        "text": "Специалист получает адрес и информацию по обращению, сверяет укладку и готовится к выезду.",
        "photo": "/assets/images/field-service/steps/step-prep.webp",
        "alt": "Специалист выездной службы готовится к выезду у автомобиля",
    },
    {
        "number": "04",
        "icon": "/assets/icons/map-pin.svg",
        "title": "Выезжаем по адресу",
        "text": "Выездная команда направляется к пациенту на автомобиле службы с ориентиром прибытия по зоне.",
        "photo": "/assets/images/field-service/steps/step-depart.webp",
        "alt": "Специалист выездной службы прибывает по адресу",
    },
    {
        "number": "05",
        "icon": "/assets/icons/seal-check.svg",
        "title": "Определяем дальнейшие действия",
        "text": "После оценки состояния специалист объясняет дальнейшие шаги: рекомендации, продолжение лечения или стационарный формат.",
        "photo": "/assets/images/field-service/steps/step-followup.webp",
        "alt": "Специалист выездной службы связывается с клиникой после выезда",
    },
]


@lru_cache(maxsize=1)
def _load_pages() -> list[dict]:
    with _PAGES_PATH.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    return list(payload.get("pages") or [])


def get_field_service_geo_groups(service_base: str = "/uslugi/narkolog-na-dom/") -> list[dict]:
    """Метро / округа / города МО со ссылками из pages.json."""
    base = service_base if service_base.endswith("/") else f"{service_base}/"
    mo_hub = f"{base}moskovskaya-oblast/"

    groups_meta = {
        "metro": {"label": "Метро", "icon": "/assets/icons/map-pin.svg"},
        "okrug": {"label": "Округа", "icon": "/assets/icons/house.svg"},
        "mo": {"label": "Города МО", "icon": "/assets/icons/buildings.svg"},
    }
    buckets: dict[str, list[dict]] = {"metro": [], "okrug": [], "mo": []}

    for page in _load_pages():
        url = str(page.get("url") or "")
        if not url.startswith(base) or url == base:
            continue

        geo_type = str(page.get("geo_type") or "")
        name = str(page.get("geo_name") or page.get("name") or "").strip()
        if not name:
            continue

        if geo_type == "metro":
            buckets["metro"].append({"url": url, "anchor": name})
        elif geo_type == "okrug":
            buckets["okrug"].append({"url": url, "anchor": name})
        elif geo_type == "mo" and url.startswith(mo_hub) and url != mo_hub:
            buckets["mo"].append({"url": url, "anchor": name})

    for key in buckets:
        buckets[key].sort(key=lambda item: item["anchor"].casefold())

    groups = []
    for key, meta in groups_meta.items():
        items = buckets[key]
        if not items:
            continue
        groups.append(
            {
                "key": key,
                "label": meta["label"],
                "icon": meta["icon"],
                "links": items,
            }
        )
    return groups


DEFAULT_FIELD_SERVICE_BASE = "/uslugi/narkolog-na-dom/"
_CATALOG_ROOT = "/uslugi/"


def resolve_field_service_base(url: str) -> str:
    """Ближайший предок URL с geo-страницами; иначе база «Нарколог на дом»."""
    current = url if url.endswith("/") else f"{url}/"
    while current and current not in {"/", _CATALOG_ROOT}:
        if get_field_service_geo_groups(current):
            return current
        parts = [part for part in current.strip("/").split("/") if part]
        if len(parts) <= 1:
            break
        current = "/" + "/".join(parts[:-1]) + "/"
    return DEFAULT_FIELD_SERVICE_BASE


def get_field_service_context(service_base: str = DEFAULT_FIELD_SERVICE_BASE) -> dict:
    return {
        "title": FIELD_SERVICE_TITLE,
        "tabs": FIELD_SERVICE_TABS,
        "equipment": FIELD_SERVICE_EQUIPMENT,
        "coverage": FIELD_SERVICE_COVERAGE,
        "geo_groups": get_field_service_geo_groups(service_base),
        "fleet": FIELD_SERVICE_FLEET,
        "team": FIELD_SERVICE_TEAM,
        "steps": FIELD_SERVICE_STEPS,
        "doctors_url": "/vrachi/",
    }
