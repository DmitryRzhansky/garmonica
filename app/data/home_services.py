"""Хабы услуг 2-го уровня для блока «Наши услуги» на главной (как в футере)."""

from __future__ import annotations

HOME_SERVICE_HUBS = [
    {
        "name": "Нарколог на дом",
        "url": "/uslugi/narkolog-na-dom/",
        "text": "Выезд врача на адрес: осмотр, помощь и понятный план действий.",
        "image": "/assets/images/home-services/hub-narkolog-na-dom-3d.webp",
    },
    {
        "name": "Вывод из запоя",
        "url": "/uslugi/vyvod-iz-zapoya/",
        "text": "Стабилизация состояния дома или в стационаре после оценки врача.",
        "image": "/assets/images/home-services/hub-vyvod-iz-zapoya-3d.webp",
    },
    {
        "name": "Кодирование",
        "url": "/uslugi/kodirovanie/",
        "text": "Методы кодирования подбирают после осмотра и подготовки пациента.",
        "image": "/assets/images/home-services/hub-kodirovanie-3d.webp",
    },
    {
        "name": "Раскодирование",
        "url": "/uslugi/kodirovanie/raskodirovanie/",
        "text": "Снятие кодирования с оценкой состояния и рекомендациями врача.",
        "image": "/assets/images/home-services/hub-raskodirovanie-3d.webp",
    },
    {
        "name": "Наркологическая помощь",
        "url": "/uslugi/narkologicheskaya-pomosh/",
        "text": "Срочная и плановая помощь при зависимости и острых состояниях.",
        "image": "/assets/images/home-services/hub-narkologicheskaya-pomosh-3d.webp",
    },
    {
        "name": "Лечение алкоголизма",
        "url": "/uslugi/lechenie-alkogolizma/",
        "text": "Программы лечения от детокса до сопровождения восстановления.",
        "image": "/assets/images/home-services/hub-lechenie-alkogolizma-3d.webp",
    },
    {
        "name": "Капельницы",
        "url": "/uslugi/kapelnitsy/",
        "text": "Инфузионная терапия на дому или в клинике после осмотра.",
        "image": "/assets/images/home-services/hub-kapelnitsy-3d.webp",
    },
    {
        "name": "Лечение наркомании",
        "url": "/uslugi/lechenie-narkomanii/",
        "text": "Снятие ломки, детокс и дальнейшее лечение зависимости.",
        "image": "/assets/images/home-services/hub-lechenie-narkomanii-3d.webp",
    },
    {
        "name": "Другие зависимости",
        "url": "/uslugi/drugie-zavisimosti/",
        "text": "Помощь при игромании, никотиновой и других формах зависимости.",
        "image": "/assets/images/home-services/hub-drugie-zavisimosti-3d.webp",
    },
    {
        "name": "Реабилитация зависимых",
        "url": "/uslugi/reabilitaciya/",
        "text": "Долгосрочные программы восстановления и ресоциализации.",
        "image": "/assets/images/home-services/hub-reabilitaciya-3d.webp",
    },
    {
        "name": "Психиатрическая помощь",
        "url": "/uslugi/psihiatriya/",
        "text": "Диагностика, лечение и наблюдение при психических расстройствах.",
        "image": "/assets/images/home-services/hub-psihiatriya-3d.webp",
    },
    {
        "name": "Психотерапия и психология",
        "url": "/uslugi/psihoterapiya-i-psihologiya/",
        "text": "Индивидуальная и семейная работа с психотерапевтом и психологом.",
        "image": "/assets/images/home-services/hub-psihoterapiya-3d.webp",
    },
]


def get_home_service_hubs() -> list[dict]:
    return list(HOME_SERVICE_HUBS)
