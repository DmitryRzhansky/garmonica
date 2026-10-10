"""Контакты клиники из BUSINESS-INFO.MD."""

from __future__ import annotations

CLINIC_CONTACTS = {
    "brand": "Нова",
    "positioning": "клиника психиатрии и наркологии",
    "legal_name": "ООО «НикаПроМЕД»",
    "inn": "9715492100",
    "ogrn": "1247700585186",
    "license_number": "Л041-01137-77/01838787",
    "legal_address": (
        "127018, г. Москва, вн.тер.г. муниципальный округ Марьина Роща, "
        "проезд Марьиной Рощи 3-й, д. 40, стр. 1, помещ. 22/22"
    ),
    "address": "г. Москва, ул. Люблинская, д. 46",
    "address_full": "109387, г. Москва, ул. Люблинская, д. 46",
    "hours": "Круглосуточно 24/7",
    "phone_display": "+7 (495) 120-45-67",
    "phone_tel": "+74951204567",
    "email": "novaklinika111@yandex.ru",
    "map_title": "Нова на карте — ул. Люблинская, д. 46",
    "map_embed": (
        "https://yandex.ru/map-widget/v1/"
        "?ll=37.7365%2C55.6709"
        "&z=16"
        "&pt=37.7365,55.6709,pm2rdm"
        "&l=map"
    ),
    "messengers": [
        {
            "label": "Телеграм",
            "href": "https://t.me/",
            "icon": "/assets/icons/messengers/telegram.svg",
        },
        {
            "label": "Ватсап",
            "href": "https://wa.me/74951204567",
            "icon": "/assets/icons/messengers/whatsapp.png",
        },
        {
            "label": "Макс",
            "href": "https://max.ru/",
            "icon": "/assets/icons/messengers/max.png",
        },
        {
            "label": "ВКонтакте",
            "href": "https://vk.com/",
            "icon": "/assets/icons/messengers/vk.png",
        },
    ],
}


def get_clinic_contacts() -> dict:
    return dict(CLINIC_CONTACTS)
