"""Врач, отвечающий на FAQ — по кластеру страницы."""

from __future__ import annotations

from app.data.doctors import get_doctor_by_slug
from app.data.service_facility import normalize_service_url
from app.services.seo.presentation import presentation_of

# Психотерапия / реабилитация — психиатр с психотерапией.
# Психиатрия — профильный психиатр.
# Остальное (наркология, выезд, стационар, каталог, главная) — главный врач.
_PSYCHOTHERAPY_SLUG = "sychev-artemiy-valerevich"
_PSYCHIATRIST_SLUG = "mishcherekova-kristina-dmitrievna"
_DEFAULT_SLUG = "antipov-dmitriy-evgenevich"


def get_faq_answerer(url: str = "", presentation: str | None = None) -> dict:
    current = normalize_service_url(url) if url else ""
    cluster = presentation if presentation is not None else (
        presentation_of(current) if current else "catalog"
    )

    if "/psihoterapiya" in current or cluster == "rehab":
        slug = _PSYCHOTHERAPY_SLUG
    elif "/psihiatriya/" in current or cluster == "clinic":
        slug = _PSYCHIATRIST_SLUG
    else:
        slug = _DEFAULT_SLUG

    doctor = get_doctor_by_slug(slug)
    return {
        "name": doctor["name"],
        "role": doctor["role"],
        "specialty": doctor["specialty"],
        "icon": doctor["icon"],
        "slug": doctor["slug"],
    }
