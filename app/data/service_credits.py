"""Блок «Автор / дата / проверено» в конце страницы услуги."""

from __future__ import annotations

from datetime import date

from app.data.service_doctors import SERVICE_DOCTORS


def _doctor_by_slug(slug: str) -> dict:
    for doctor in SERVICE_DOCTORS:
        if doctor["slug"] == slug:
            return doctor
    raise KeyError(f"Doctor not found: {slug}")


def get_service_credits() -> dict:
    author = _doctor_by_slug("saveliev-igor-nikolaevich")
    reviewer = _doctor_by_slug("voronov-pavel-igorevich")
    today = date.today()

    return {
        "author": {
            "name": author["name"],
            "role": author["role"],
            "photo": author["photo"],
            "slug": author["slug"],
        },
        "reviewer": {
            "name": reviewer["name"],
            "role": reviewer["role"],
            "photo": reviewer["photo"],
            "slug": reviewer["slug"],
        },
        "updated_iso": today.isoformat(),
        "updated_label": today.strftime("%d.%m.%Y"),
        "service": {
            "title": "ПроДокторов",
            "icon": "/assets/icons/reviews/prodoctorov-favicon.png",
        },
    }
