"""Контакты клиники из BUSINESS-INFO.MD."""

from __future__ import annotations

CLINIC_CONTACTS = {
    "brand": "НОВА",
    "legal_name": "ООО «НикаПроМЕД»",
    "inn": "9715492100",
    "ogrn": "1247700585186",
    "address": "г. Москва, ул. Люблинская, д. 46",
    "address_full": "109387, г. Москва, ул. Люблинская, д. 46",
    "hours": "Круглосуточно 24/7",
    "phone_display": "+7 (495) 120-45-67",
    "phone_tel": "+74951204567",
    "email": "novaklinika111@yandex.ru",
    "map_title": "НОВА на карте — ул. Люблинская, д. 46",
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
            "label": "Макс",
            "href": "https://max.ru/",
            "icon": "/assets/icons/messengers/max.png",
        },
        {
            "label": "Ватсап",
            "href": "https://wa.me/",
            "icon": "/assets/icons/messengers/whatsapp.png",
        },
    ],
}


def get_clinic_contacts() -> dict:
    return dict(CLINIC_CONTACTS)
