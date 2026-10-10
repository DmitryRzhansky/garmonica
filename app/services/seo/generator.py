"""Детерминированные SEO-поля страницы каталога."""

from __future__ import annotations

from dataclasses import dataclass

from app.services.seo.copy_text import render_copy
from app.services.seo.faq_bank import get_faq
from app.services.seo.geo_forms import city_locative, okrug_locative
from app.services.seo.phrases import PHRASES, Phrase, phrase_for
from app.services.seo.presentation import (
    DiffCard,
    FormCopy,
    HeroCopy,
    diff_cards_for,
    facility_title_override,
    form_for,
    hero_for,
    presentation_of,
    price_tab_for,
    title_tail,
)

THIN_COPY = frozenset({"ubod", "brand", "uncode", "rehab", "rehab_topic", "vytrezvitel"})


@dataclass(frozen=True)
class SeoCopy:
    h1_before: str
    h1_accent: str
    meta_title: str
    meta_description: str
    lead: str
    faq_title: str
    faq_items: tuple[tuple[str, str], ...]
    price_title: str
    price_tab: str
    presentation: str
    hero: HeroCopy
    form: FormCopy
    diff_cards: tuple[DiffCard, DiffCard, DiffCard, DiffCard]
    facility_title: str | None
    profile_id: str
    service_url: str
    copy_id: str
    thin_data: bool

    @property
    def h1(self) -> str:
        if self.h1_accent:
            return f"{self.h1_before} {self.h1_accent}"
        return self.h1_before


def service_url_of(page: dict) -> str:
    url = page["url"]
    kind = page.get("kind") or ""
    parts = [part for part in url.strip("/").split("/") if part]
    if kind == "city" and len(parts) >= 2:
        return "/" + "/".join(parts[:-2]) + "/"
    if kind in {"metro", "okrug", "geo-hub"} and len(parts) >= 1:
        return "/" + "/".join(parts[:-1]) + "/"
    if url.endswith("/"):
        return url
    return url + "/"


def _geo(page: dict) -> tuple[str, str]:
    """Возвращает (акцент H1, хвост « у метро …» / « в …»)."""
    kind = page.get("kind") or ""
    name = (page.get("geo_name") or "").strip()
    if kind == "metro" and name:
        return name, f" у метро {name}"
    if kind == "okrug" and name:
        locative = okrug_locative(name)
        return locative, f" в {locative}"
    if kind == "city" and name:
        locative = city_locative(name)
        return locative, f" в {locative}"
    if kind == "geo-hub":
        return "Московской области", " в Московской области"
    return "", ""


def _heading(phrase: Phrase, presentation: str, accent: str, place: str) -> tuple[str, str, str]:
    if accent:
        if place.startswith(" у метро"):
            return f"{phrase.query} у метро", accent, f"{phrase.query}{place}"
        return f"{phrase.query} в", accent, f"{phrase.query}{place}"
    if presentation == "home":
        return f"{phrase.query} в", "Москве", f"{phrase.query} в Москве"
    return phrase.query, "", phrase.query


def build_page_seo(page: dict) -> SeoCopy:
    service_url = service_url_of(page)
    phrase: Phrase = phrase_for(service_url, page.get("service_name") or page.get("name") or "")
    presentation = presentation_of(service_url)
    # Геостраница наследует кластер услуги, а не собственного URL с хвостом метро.
    if page.get("kind") in {"metro", "okrug", "city", "geo-hub"}:
        presentation = presentation_of(service_url)
    drip = "/kapelnitsy/" in service_url
    accent, place = _geo(page)
    h1_before, h1_accent, h1 = _heading(phrase, presentation, accent, place)
    tail = title_tail(service_url, presentation)
    description, lead = render_copy(phrase.copy_id, phrase.topic)
    faq_raw = get_faq(phrase.faq_id, phrase.topic or phrase.query)
    faq_items = tuple((item["ask"], item["answer"]) for item in faq_raw)
    hero = hero_for(presentation, drip)
    return SeoCopy(
        h1_before=h1_before,
        h1_accent=h1_accent,
        meta_title=f"{h1} — {tail}",
        meta_description=description,
        lead=lead,
        faq_title=f"Ответы на частые вопросы про {phrase.faq_about}{place}",
        faq_items=faq_items,
        price_title=f"Стоимость {phrase.price_of}{place}",
        price_tab=price_tab_for(service_url, presentation),
        presentation=presentation,
        hero=hero,
        form=form_for(presentation),
        diff_cards=diff_cards_for(presentation, drip),
        facility_title=facility_title_override(page["url"]),
        profile_id=service_url,
        service_url=service_url,
        copy_id=phrase.copy_id,
        thin_data=phrase.copy_id in THIN_COPY or service_url not in PHRASES,
    )


def known_phrase_urls() -> set[str]:
    return set(PHRASES)
