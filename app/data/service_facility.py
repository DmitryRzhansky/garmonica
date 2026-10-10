"""Блок «Где будет находиться пациент» — стационар на ул. Люблинская, 46."""

from __future__ import annotations

from app.data.clinic_contacts import CLINIC_CONTACTS

FACILITY_TITLE = "Где будет находиться пациент"

FACILITY_FACTS_TITLE = "Бытовые условия"

FACILITY_FACTS = [
    {
        "icon": "/assets/icons/map-pin.svg",
        "label": "Адрес",
        "value": CLINIC_CONTACTS["address"],
    },
    {
        "icon": "/assets/icons/hospital.svg",
        "label": "Мест",
        "value": "до 32",
    },
    {
        "icon": "/assets/icons/buildings.svg",
        "label": "Палаты",
        "value": "общие 4–5 мест, трёхместные, двухместные комфорт, одноместные комфорт, VIP",
    },
    {
        "icon": "/assets/icons/house.svg",
        "label": "В палате",
        "value": "кровать, тумбочка, кондиционер, телевизор, санузел",
    },
    {
        "icon": "/assets/icons/clock.svg",
        "label": "Режим",
        "value": "круглосуточно, 24/7",
    },
    {
        "icon": "/assets/icons/leaf.svg",
        "label": "Питание",
        "value": "четырёхразовое, входит в стоимость",
    },
    {
        "icon": "/assets/icons/stethoscope.svg",
        "label": "Персонал",
        "value": "дежурные врач, медсестра и санитар",
    },
    {
        "icon": "/assets/icons/calendar-check.svg",
        "label": "Срок",
        "value": "от 3 до 21 дня — по состоянию",
    },
    {
        "icon": "/assets/icons/users.svg",
        "label": "Посещения",
        "value": "по регламенту клиники, по согласованию",
    },
    {
        "icon": "/assets/icons/phone.svg",
        "label": "Связь",
        "value": "телефон разрешён; обзвоны родственников — по договорённости",
    },
    {
        "icon": "/assets/icons/clipboard-text.svg",
        "label": "С собой",
        "value": "сменная одежда, средства гигиены, паспорт",
    },
]

FACILITY_PHOTOS = [
    {
        "src": "/assets/images/service-facility/ward-shared.webp",
        "alt": "Общая палата стационара: несколько кроватей, тумбочки и окно с дневным светом",
        "title": "Общая палата",
        "text": "4–5 мест. Базовое размещение: кровати, тумбочки, кондиционер и телевизор.",
    },
    {
        "src": "/assets/images/service-facility/ward-single.webp",
        "alt": "Одноместная палата комфорт со своей кроватью, тумбочкой и телевизором",
        "title": "Палата комфорт / VIP",
        "text": "Одноместные комфорт и VIP-палаты — когда важно больше личного пространства.",
    },
    {
        "src": "/assets/images/service-facility/exam.webp",
        "alt": "Кабинет осмотра в стационаре с кушеткой и диагностическим оборудованием",
        "title": "Осмотр и диагностика",
        "text": "Осмотр, ЭКГ, забор анализов и процедуры выполняют на месте в клинике.",
    },
    {
        "src": "/assets/images/service-facility/bathroom.webp",
        "alt": "Санузел в палате стационара: душ, раковина и унитаз",
        "title": "Санузел",
        "text": "В палатах есть санузел с душем. Гигиена и уборка входят в условия пребывания.",
    },
    {
        "src": "/assets/images/service-facility/common.webp",
        "alt": "Общая зона стационара со столами и стульями для отдыха и питания",
        "title": "Общая зона",
        "text": "Место вне палаты: можно посидеть, поговорить и принять пищу.",
    },
]

# Хабы услуг без привязки «на дому» / «в стационаре».
FACILITY_HUBS = frozenset(
    {
        "/uslugi/narkologicheskaya-pomosh/",
        "/uslugi/vyvod-iz-zapoya/",
        "/uslugi/kodirovanie/",
        "/uslugi/lechenie-alkogolizma/",
        "/uslugi/snyatie-lomki/",
        "/uslugi/lechenie-narkomanii/",
        "/uslugi/drugie-zavisimosti/",
        "/uslugi/psihiatriya/",
    }
)

FACILITY_PATH_MARKERS = (
    "/stacionar/",
    "/v-stacionare/",
    "/v-klinike/",
    "/gospitalizaciya/",
    "/ambulatorno/",
    "/chastnyj-vytrezvitel/",
)

HOME_FACILITY_MARKERS = (
    "/na-domu/",
    "/narkolog-na-dom/",
    "/psihiatr-na-dom/",
    "/kapelnitsy/",
)


def normalize_service_url(url: str) -> str:
    if not url or url == "/":
        return "/"
    return "/" + url.strip("/") + "/"


def _is_rehab(url: str) -> bool:
    return "/reabilitaciya/" in url


def should_show_service_facility(url: str) -> bool:
    """Клиника и стационар. Выезд и реабилитация этот блок не показывают."""
    current = normalize_service_url(url)
    if current == "/uslugi/":
        return True
    if _is_rehab(current):
        return False
    if any(marker in current for marker in HOME_FACILITY_MARKERS):
        return False
    if "/psihoterapiya-i-psihologiya/" in current:
        return True
    if "/psihiatriya/" in current:
        return True
    if "/onlajn" in current:
        return True
    if current in FACILITY_HUBS:
        return True
    return any(marker in current for marker in FACILITY_PATH_MARKERS)


def should_show_field_service(url: str) -> bool:
    current = normalize_service_url(url)
    if _is_rehab(current):
        return False
    return not should_show_service_facility(current)


def get_service_facility() -> dict:
    return {
        "title": FACILITY_TITLE,
        "facts_title": FACILITY_FACTS_TITLE,
        "facts": FACILITY_FACTS,
        "photos": FACILITY_PHOTOS,
        "address": CLINIC_CONTACTS["address"],
    }
