"""Врачи клиники для страницы «Наши врачи» (BUSINESS-INFO.MD §9)."""

from __future__ import annotations

CLINIC_DOCTORS = [
    {
        "slug": "antipov-dmitriy-evgenevich",
        "name": "Антипов Дмитрий Евгеньевич",
        "role": "Главный врач",
        "specialty": "Психиатр-нарколог, терапевт",
        "experience": "с 2007 года",
        "degree": None,
        "icon": "/assets/icons/phosphor/stethoscope.svg",
        "lead": (
            "Руководит медицинской работой клиники: определяет маршрут помощи, "
            "оценивает противопоказания к госпитализации и согласовывает план "
            "лечения с профильными специалистами."
        ),
        "focus": [
            "Оценка состояния и решение о формате помощи",
            "Психиатрия и наркология: диагностика и ведение",
            "Терапевтический контроль сопутствующих рисков",
            "Организация здравоохранения в клинике",
        ],
        "certificates": [
            "Организация здравоохранения",
            "Психиатрия-наркология",
            "Терапия",
        ],
        "formats": [
            {"label": "Стационар", "icon": "/assets/icons/phosphor/hospital.svg"},
            {"label": "Амбулаторно", "icon": "/assets/icons/phosphor/clipboard-text.svg"},
            {"label": "Консультация", "icon": "/assets/icons/phosphor/chat-circle-dots.svg"},
        ],
    },
    {
        "slug": "sychev-artemiy-valerevich",
        "name": "Сычев Артемий Валерьевич",
        "role": "Врач психиатр-нарколог",
        "specialty": "Психиатр-нарколог, психиатр, психотерапевт",
        "experience": "более 20 лет",
        "degree": None,
        "icon": "/assets/icons/phosphor/brain.svg",
        "lead": (
            "Ведёт пациентов психиатрического и наркологического профиля: "
            "от первичной оценки до психофармакотерапии и психотерапевтической "
            "работы — в стационаре и амбулаторно."
        ),
        "focus": [
            "Психиатрическая и наркологическая диагностика",
            "Подбор и коррекция психофармакотерапии",
            "Психотерапевтическое сопровождение",
            "Амбулаторное наблюдение после стационара",
        ],
        "certificates": [
            "Психиатрия-наркология",
            "Психотерапия",
        ],
        "formats": [
            {"label": "Стационар", "icon": "/assets/icons/phosphor/hospital.svg"},
            {"label": "Амбулаторно", "icon": "/assets/icons/phosphor/clipboard-text.svg"},
            {"label": "Психотерапия", "icon": "/assets/icons/phosphor/brain.svg"},
        ],
    },
    {
        "slug": "mishcherekova-kristina-dmitrievna",
        "name": "Мищерекова Кристина Дмитриевна",
        "role": "Заведующая отделением",
        "specialty": "Врач-психиатр",
        "experience": "10 лет",
        "degree": None,
        "icon": "/assets/icons/phosphor/hospital.svg",
        "lead": (
            "Отвечает за организацию работы отделения: маршрутизация пациентов, "
            "согласованность наблюдений и контроль качества психиатрической "
            "помощи на всём сроке пребывания."
        ),
        "focus": [
            "Психиатрическая диагностика и наблюдение",
            "Ведение пациентов в отделении",
            "Организация здравоохранения в отделении",
            "Координация с врачами смежных специальностей",
        ],
        "certificates": [
            "Психиатрия",
            "Организация здравоохранения",
        ],
        "formats": [
            {"label": "Стационар", "icon": "/assets/icons/phosphor/hospital.svg"},
            {"label": "Амбулаторно", "icon": "/assets/icons/phosphor/clipboard-text.svg"},
            {"label": "Наблюдение", "icon": "/assets/icons/phosphor/first-aid.svg"},
        ],
    },
    {
        "slug": "poplevchenkov-konstantin-nikolaevich",
        "name": "Поплевченков Константин Николаевич",
        "role": "Врач психиатр-нарколог",
        "specialty": "Психиатр-нарколог, психиатр, психотерапевт",
        "experience": "с 2007 года",
        "degree": "Доктор медицинских наук",
        "icon": "/assets/icons/phosphor/certificate.svg",
        "lead": (
            "Специалист с учёной степенью: психиатрия, наркология и психотерапия. "
            "Участвует в сложных клинических случаях, где нужна расширенная "
            "оценка и согласованный план лечения."
        ),
        "focus": [
            "Сложные и коморбидные случаи",
            "Психиатрия-наркология: диагностика и терапия",
            "Психотерапевтическая работа",
            "Организация медицинской помощи",
        ],
        "certificates": [
            "Психиатрия-наркология",
            "Организация здравоохранения",
            "Психиатрия",
            "Психотерапия",
        ],
        "formats": [
            {"label": "Стационар", "icon": "/assets/icons/phosphor/hospital.svg"},
            {"label": "Амбулаторно", "icon": "/assets/icons/phosphor/clipboard-text.svg"},
            {"label": "Психотерапия", "icon": "/assets/icons/phosphor/brain.svg"},
        ],
    },
]


def get_clinic_doctors() -> list[dict]:
    return list(CLINIC_DOCTORS)
