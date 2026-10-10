"""Прайс-лист клиники (BUSINESS-INFO.MD §5) — единый источник для /ceny/."""

from __future__ import annotations

PRICE_GROUPS = [
    {
        "id": "stationary",
        "title": "Стационар",
        "icon": "/assets/icons/phosphor/hospital.svg",
        "rows": [
            {
                "name": "4-местная палата",
                "includes": "Размещение, питание, наблюдение",
                "price": "от 12\u00a0000\u00a0₽",
                "unit": "сутки",
                "icon": "/assets/icons/phosphor/hospital.svg",
            },
            {
                "name": "3-местная палата",
                "includes": "Размещение, питание, наблюдение",
                "price": "от 15\u00a0000\u00a0₽",
                "unit": "сутки",
                "icon": "/assets/icons/phosphor/hospital.svg",
            },
            {
                "name": "2-местная палата",
                "includes": "Размещение, питание, наблюдение",
                "price": "от 18\u00a0000\u00a0₽",
                "unit": "сутки",
                "icon": "/assets/icons/phosphor/hospital.svg",
            },
            {
                "name": "1-местная палата «Комфорт»",
                "includes": "Размещение, питание, наблюдение",
                "price": "от 25\u00a0000\u00a0₽",
                "unit": "сутки",
                "icon": "/assets/icons/phosphor/house-line.svg",
            },
            {
                "name": "VIP-палата",
                "includes": "Размещение, питание, наблюдение",
                "price": "от 35\u00a0000\u00a0₽",
                "unit": "сутки",
                "icon": "/assets/icons/phosphor/shield-check.svg",
            },
        ],
    },
    {
        "id": "consultations",
        "title": "Консультации и ведение",
        "icon": "/assets/icons/phosphor/stethoscope.svg",
        "rows": [
            {
                "name": "Консультация психиатра",
                "includes": "Осмотр, диагноз, рецепты, рекомендации",
                "price": "8\u00a0000\u00a0₽",
                "unit": None,
                "icon": "/assets/icons/phosphor/brain.svg",
            },
            {
                "name": "Консультация нарколога",
                "includes": "Осмотр, диагноз, рецепты, рекомендации",
                "price": "8\u00a0000\u00a0₽",
                "unit": None,
                "icon": "/assets/icons/phosphor/stethoscope.svg",
            },
            {
                "name": "Наркологическое ведение",
                "includes": (
                    "Приём, диагноз, психофармакотерапия, выписные рекомендации "
                    "и рецепты на весь период госпитализации"
                ),
                "price": "12\u00a0000\u00a0₽",
                "unit": None,
                "icon": "/assets/icons/phosphor/clipboard-text.svg",
            },
            {
                "name": "Психиатрическое ведение",
                "includes": "Ведение пациента на весь период госпитализации",
                "price": "12\u00a0000\u00a0₽",
                "unit": None,
                "icon": "/assets/icons/phosphor/clipboard-text.svg",
            },
            {
                "name": "Консультация клинического психолога",
                "includes": "Консультация в стационаре",
                "price": "по запросу",
                "unit": None,
                "icon": "/assets/icons/phosphor/chat-circle-dots.svg",
            },
        ],
    },
    {
        "id": "procedures",
        "title": "Процедуры и физиотерапия",
        "icon": "/assets/icons/phosphor/first-aid.svg",
        "rows": [
            {
                "name": "Сосудистая терапия",
                "includes": "Капельница / инфузионная процедура",
                "price": "5\u00a0000\u00a0₽",
                "unit": "процедура",
                "icon": "/assets/icons/phosphor/first-aid.svg",
            },
            {
                "name": "«Здоровая печень»",
                "includes": "Гепатопротективная терапия (усиленная)",
                "price": "5\u00a0000\u00a0₽",
                "unit": "процедура",
                "icon": "/assets/icons/phosphor/first-aid.svg",
            },
            {
                "name": "ВЛОК",
                "includes": "Физиотерапия",
                "price": "5\u00a0000\u00a0₽",
                "unit": "процедура",
                "icon": "/assets/icons/phosphor/first-aid.svg",
            },
            {
                "name": "Электросон",
                "includes": "Физиотерапия",
                "price": "5\u00a0000\u00a0₽",
                "unit": "процедура",
                "icon": "/assets/icons/phosphor/brain.svg",
            },
            {
                "name": "ТЭС",
                "includes": "Транскраниальная электростимуляция головного мозга",
                "price": "5\u00a0000\u00a0₽",
                "unit": "процедура",
                "icon": "/assets/icons/phosphor/brain.svg",
            },
            {
                "name": "Физиопроцедуры",
                "includes": "По назначению врача",
                "price": "5\u00a0000\u00a0₽",
                "unit": "процедура",
                "icon": "/assets/icons/phosphor/first-aid.svg",
            },
        ],
    },
    {
        "id": "labs",
        "title": "Анализы и диагностика",
        "icon": "/assets/icons/phosphor/clipboard-text.svg",
        "rows": [
            {
                "name": "Анализы для госпитализации",
                "includes": (
                    "Основные показатели: общий анализ мочи, биохимия, инфекции"
                ),
                "price": "8\u00a0000–10\u00a0000\u00a0₽",
                "unit": None,
                "icon": "/assets/icons/phosphor/clipboard-text.svg",
            },
            {
                "name": "Скрининг-тест на наркотики",
                "includes": "Экспресс-скрининг",
                "price": "от 3\u00a0000\u00a0₽",
                "unit": None,
                "icon": "/assets/icons/phosphor/clipboard-text.svg",
            },
            {
                "name": "Анализ «Дионарк»",
                "includes": "Расширенное исследование",
                "price": "от 15\u00a0000–20\u00a0000\u00a0₽",
                "unit": None,
                "icon": "/assets/icons/phosphor/clipboard-text.svg",
            },
        ],
    },
    {
        "id": "support",
        "title": "Сопровождение родственников",
        "icon": "/assets/icons/phosphor/chat-circle-dots.svg",
        "rows": [
            {
                "name": "Информированное сопровождение",
                "includes": (
                    "Ежедневные обзвоны родственников по состоянию здоровья, "
                    "динамике и поведению"
                ),
                "price": "6\u00a0000\u00a0₽",
                "unit": None,
                "icon": "/assets/icons/phosphor/device-mobile.svg",
            },
        ],
    },
]


def get_price_groups() -> list[dict]:
    return list(PRICE_GROUPS)

