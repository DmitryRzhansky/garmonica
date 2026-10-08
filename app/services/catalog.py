from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "pages.json"
NARKOLOG_URL = "/uslugi/narkolog-na-dom/"
BANNED_SEGMENTS = frozenset({"pomosh", "pomoshch"})

MENU_ALIASES = {
    "Капельница на дому": "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/",
    "Капельница от алкоголя": "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/",
    "Капельница от запоя": "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/",
    "Лечение наркомании по городам МО": "/uslugi/lechenie-narkomanii/moskovskaya-oblast/",
    "Реабилитация по городам МО": "/uslugi/reabilitaciya/moskovskaya-oblast/",
    "Медико-социальная реабилитация": "/uslugi/reabilitaciya/",
    "Метод Шичко": "/uslugi/reabilitaciya/",
}

NARKOLOG_COPY = {
    "h1_before": "Вызов нарколога на дом в",
    "h1_accent": "Москве и области",
    "meta_title": "Вызов нарколога на дом в Москве — Нова клиник",
    "meta_description": (
        "Вызов нарколога на дом в Москве и области: осмотр, оценка состояния, "
        "помощь при запое и интоксикации. Круглосуточно, анонимно, стоимость от 5 000 ₽."
    ),
    "lead": (
        "Врач приедет на адрес, проведёт осмотр, оценит состояние и предложит, "
        "какую помощь можно оказать дома. В городе обычно укладываемся примерно "
        "в 40–60 минут после согласования адреса."
    ),
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
        if page["url"] == NARKOLOG_URL:
            copy = NARKOLOG_COPY
        else:
            copy = build_copy(page)
        return PageView(
            url=page["url"],
            name=page["name"],
            h1_before=copy["h1_before"],
            h1_accent=copy["h1_accent"],
            meta_title=copy["meta_title"],
            meta_description=copy["meta_description"],
            lead=copy["lead"],
            breadcrumbs=tuple(self.breadcrumbs(page["url"])),
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


def build_copy(page: dict) -> dict:
    accent = geo_accent(page)
    heading = page["service_name"] if accent else page["name"]
    if accent:
        title = f"{heading} — {accent} — Нова клиник"
        lead = f"{heading}: {accent}. Текст страницы будет дополнен."
    else:
        title = f"{heading} — Нова клиник"
        lead = f"{heading}. Текст страницы будет дополнен."
    return {
        "h1_before": heading,
        "h1_accent": accent,
        "meta_title": title,
        "meta_description": lead,
        "lead": lead,
    }


def geo_accent(page: dict) -> str:
    geo_type = page.get("geo_type") or ""
    geo_name = page.get("geo_name") or ""
    if geo_type == "metro" and geo_name:
        return f"метро {geo_name}"
    if geo_type in {"okrug", "mo", "city"} and geo_name:
        return geo_name
    if page.get("kind") == "geo-hub":
        return "Московская область"
    return ""


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
