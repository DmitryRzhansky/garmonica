from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from app.services.seo.generator import SeoCopy, build_page_seo

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "pages.json"
BANNED_SEGMENTS = frozenset({"pomosh", "pomoshch"})

MENU_ALIASES = {
    "Капельница на дому": "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/",
    "Капельница от алкоголя": "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/",
    "Капельница от запоя": "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/",
    "Лечение наркомании по городам МО": "/uslugi/lechenie-narkomanii/moskovskaya-oblast/",
    "Лечение наркомании в Московской области": "/uslugi/lechenie-narkomanii/moskovskaya-oblast/",
    "Лечение алкоголизма в Московской области": "/uslugi/lechenie-alkogolizma/moskovskaya-oblast/",
    "Реабилитация по городам МО": "/uslugi/reabilitaciya/moskovskaya-oblast/",
    "Реабилитация зависимых в Московской области": "/uslugi/reabilitaciya/moskovskaya-oblast/",
    "Медико-социальная реабилитация": "/uslugi/reabilitaciya/",
    "Метод Шичко": "/uslugi/reabilitaciya/",
}

@dataclass(frozen=True)
class Crumb:
    name: str
    url: str


@dataclass(frozen=True)
class PageView:
    url: str
    name: str
    h1_before: str
    h1_accent: str
    meta_title: str
    meta_description: str
    lead: str
    breadcrumbs: tuple[Crumb, ...]
    seo: SeoCopy


class PageCatalog:
    def __init__(self, pages: list[dict]):
        self.pages = pages
        self.by_url = {page["url"]: page for page in pages}

    @classmethod
    def load(cls, path: Path = DATA_PATH) -> PageCatalog:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(payload["pages"])

    def get(self, url: str) -> dict | None:
        return self.by_url.get(normalize_url(url))

    def public_urls(self) -> list[str]:
        return [page["url"] for page in self.pages]

    def view(self, url: str) -> PageView | None:
        page = self.get(url)
        if page is None:
            return None
        seo = build_page_seo(page)
        return PageView(
            url=page["url"],
            name=page["name"],
            h1_before=seo.h1_before,
            h1_accent=seo.h1_accent,
            meta_title=seo.meta_title,
            meta_description=seo.meta_description,
            lead=seo.lead,
            breadcrumbs=tuple(self.breadcrumbs(page["url"])),
            seo=seo,
        )

    def breadcrumbs(self, url: str) -> list[Crumb]:
        chain: list[Crumb] = []
        current = normalize_url(url)
        while current and current != "/":
            page = self.by_url.get(current)
            if page is None:
                break
            chain.append(Crumb(page["name"], page["url"]))
            current = parent_url(current)
        chain.append(Crumb("Главная", "/"))
        chain.reverse()
        return chain

    def menu_targets(self) -> dict[str, str]:
        targets: dict[str, str] = {}
        for page in self.pages:
            if page["kind"] not in {"silo-root", "child", "structural"}:
                continue
            name = page["name"]
            previous = targets.get(name)
            if previous and previous != page["url"]:
                raise ValueError(f"Повторяющееся название страницы: {name}")
            targets[name] = page["url"]
        targets.update(MENU_ALIASES)
        return targets


def normalize_url(url: str) -> str:
    if not url or url == "/":
        return "/"
    return "/" + url.strip("/") + "/"


def parent_url(url: str) -> str:
    parts = [part for part in url.strip("/").split("/") if part]
    if len(parts) <= 1:
        return "/"
    return "/" + "/".join(parts[:-1]) + "/"


def has_banned_segment(url: str) -> bool:
    return any(part in BANNED_SEGMENTS for part in url.strip("/").split("/"))


_catalog: PageCatalog | None = None


def get_catalog() -> PageCatalog:
    global _catalog
    if _catalog is None:
        _catalog = PageCatalog.load()
    return _catalog
