"""HTML-карта сайта: разделы для страницы /karta-sajta/."""

from __future__ import annotations

from dataclasses import dataclass

from app.services.catalog import PageCatalog, get_catalog

DEFAULT_ICON = "/assets/icons/list.svg"
GEO_ICON = "/assets/icons/map-pin.svg"

SILO_ICONS: dict[str, str] = {
    "/uslugi/narkologicheskaya-pomosh/": "/assets/icons/first-aid.svg",
    "/uslugi/narkolog-na-dom/": "/assets/icons/ambulance.svg",
    "/uslugi/vyvod-iz-zapoya/": "/assets/icons/heartbeat.svg",
    "/uslugi/kapelnitsy/": "/assets/icons/syringe.svg",
    "/uslugi/kodirovanie/": "/assets/icons/lock.svg",
    "/uslugi/lechenie-alkogolizma/": "/assets/icons/heartbeat.svg",
    "/uslugi/snyatie-lomki/": "/assets/icons/first-aid-kit.svg",
    "/uslugi/lechenie-narkomanii/": "/assets/icons/stethoscope.svg",
    "/uslugi/drugie-zavisimosti/": "/assets/icons/hands-praying.svg",
    "/uslugi/reabilitaciya/": "/assets/icons/leaf.svg",
    "/uslugi/psihiatriya/": "/assets/icons/phosphor/brain.svg",
    "/uslugi/psihoterapiya-i-psihologiya/": "/assets/icons/chat-circle.svg",
}

GEO_BLOCK_TITLES = {
    "geo-hub": "Московская область",
    "okrug": "Округа Москвы",
    "metro": "Станции метро",
    "city": "Города Московской области",
}

GEO_KIND_ORDER = ("geo-hub", "okrug", "metro", "city")


@dataclass(frozen=True)
class SiteMapLink:
    title: str
    url: str
    icon: str = DEFAULT_ICON


@dataclass(frozen=True)
class SiteMapGeoBlock:
    title: str
    links: tuple[SiteMapLink, ...]


@dataclass(frozen=True)
class SiteMapGroup:
    title: str
    url: str
    icon: str
    links: tuple[SiteMapLink, ...]
    geo_blocks: tuple[SiteMapGeoBlock, ...] = ()


@dataclass(frozen=True)
class SiteMapSection:
    id: str
    title: str
    icon: str
    links: tuple[SiteMapLink, ...] = ()
    groups: tuple[SiteMapGroup, ...] = ()


def get_site_map(catalog: PageCatalog | None = None) -> list[SiteMapSection]:
    catalog = catalog or get_catalog()
    return [
        _clinic_section(),
        _services_section(catalog),
        _info_section(),
        _legal_section(),
    ]


def _clinic_section() -> SiteMapSection:
    return SiteMapSection(
        id="clinic",
        title="О клинике",
        icon="/assets/icons/hospital.svg",
        links=(
            SiteMapLink("Главная", "/", "/assets/icons/house.svg"),
            SiteMapLink("О клинике", "/o-klinike/", "/assets/icons/hospital.svg"),
            SiteMapLink("Врачи", "/vrachi/", "/assets/icons/users.svg"),
            SiteMapLink("Лицензия", "/licenziya/", "/assets/icons/shield-check.svg"),
            SiteMapLink("Фотогалерея", "/galereya/", "/assets/icons/sun.svg"),
            SiteMapLink("Частые вопросы", "/voprosy/", "/assets/icons/chat-circle.svg"),
        ),
    )


def _info_section() -> SiteMapSection:
    return SiteMapSection(
        id="info",
        title="Разделы сайта",
        icon="/assets/icons/article.svg",
        links=(
            SiteMapLink("Цены", "/ceny/", "/assets/icons/currency-rub.svg"),
            SiteMapLink("Отзывы", "/otzyvy/", "/assets/icons/star.svg"),
            SiteMapLink("Контакты", "/kontakty/", "/assets/icons/map-pin.svg"),
        ),
    )


def _legal_section() -> SiteMapSection:
    return SiteMapSection(
        id="legal",
        title="Правовая информация",
        icon="/assets/icons/file-text.svg",
        links=(
            SiteMapLink(
                "Политика конфиденциальности",
                "/politika-konfidencialnosti/",
                "/assets/icons/shield-check.svg",
            ),
            SiteMapLink(
                "Согласие на обработку персональных данных",
                "/soglasie/",
                "/assets/icons/clipboard-text.svg",
            ),
        ),
    )


def _services_section(catalog: PageCatalog) -> SiteMapSection:
    groups: list[SiteMapGroup] = []

    for page in catalog.pages:
        if page["kind"] != "silo-root":
            continue
        depth = page["url"].count("/")
        children = [
            SiteMapLink(child["name"], child["url"], DEFAULT_ICON)
            for child in catalog.pages
            if child["kind"] == "child"
            and child["url"].startswith(page["url"])
            and child["url"].count("/") == depth + 1
        ]
        groups.append(
            SiteMapGroup(
                title=page["name"],
                url=page["url"],
                icon=SILO_ICONS.get(page["url"], DEFAULT_ICON),
                links=tuple(children),
                geo_blocks=_geo_blocks_for_silo(catalog, page["url"]),
            )
        )

    return SiteMapSection(
        id="services",
        title="Услуги",
        icon="/assets/icons/first-aid-kit.svg",
        groups=tuple(groups),
    )


def _geo_blocks_for_silo(catalog: PageCatalog, silo_url: str) -> tuple[SiteMapGeoBlock, ...]:
    by_kind: dict[str, list[SiteMapLink]] = {kind: [] for kind in GEO_KIND_ORDER}

    for page in catalog.pages:
        kind = page["kind"]
        if kind not in by_kind:
            continue
        if not page["url"].startswith(silo_url):
            continue
        title = _geo_link_title(page)
        by_kind[kind].append(SiteMapLink(title, page["url"], GEO_ICON))

    blocks: list[SiteMapGeoBlock] = []
    for kind in GEO_KIND_ORDER:
        links = by_kind[kind]
        if not links:
            continue
        links.sort(key=lambda item: item.title.casefold())
        blocks.append(SiteMapGeoBlock(GEO_BLOCK_TITLES[kind], tuple(links)))
    return tuple(blocks)


def _geo_link_title(page: dict) -> str:
    if page["kind"] == "geo-hub":
        return page["name"]
    geo_name = (page.get("geo_name") or "").strip()
    if geo_name:
        return geo_name
    return page["name"]
