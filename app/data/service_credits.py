"""Блок «Автор / дата / проверено» в конце страницы услуги."""

from __future__ import annotations

from datetime import date

from app.data.doctors import get_doctor_by_slug


def get_service_credits() -> dict:
    author = get_doctor_by_slug("sychev-artemiy-valerevich")
    reviewer = get_doctor_by_slug("antipov-dmitriy-evgenevich")
    today = date.today()

    return {
        "author": {
            "name": author["name"],
            "role": author["role"],
            "icon": author["icon"],
            "slug": author["slug"],
        },
        "reviewer": {
            "name": reviewer["name"],
            "role": reviewer["role"],
            "icon": reviewer["icon"],
            "slug": reviewer["slug"],
        },
        "updated_iso": today.isoformat(),
        "updated_label": today.strftime("%d.%m.%Y"),
        "service": {
            "title": "ПроДокторов",
            "icon": "/assets/icons/reviews/prodoctorov-favicon.png",
        },
    }
