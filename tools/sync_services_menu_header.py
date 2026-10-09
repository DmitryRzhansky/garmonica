# -*- coding: utf-8 -*-
"""Sync mega-menu JSON into header.html (desktop + mobile services blocks)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENU_PATH = ROOT / "app" / "static" / "data" / "services-menu.json"
JS_PATH = ROOT / "app" / "static" / "js" / "data" / "services-menu.js"
HEADER = ROOT / "app" / "templates" / "components" / "header.html"

CAT_ICONS = [
    ("нарколог на дом", "ambulance.svg"),
    ("вывод из запоя", "first-aid.svg"),
    ("нарколог", "ambulance.svg"),
    ("алкогол", "first-aid.svg"),
    ("капельниц", "first-aid-kit.svg"),
    ("раскодир", "lock.svg"),
    ("кодирован", "syringe.svg"),
    ("наркоман", "syringe.svg"),
    ("зависимост", "heartbeat.svg"),
    ("реабилит", "leaf.svg"),
    ("психиатр", "users.svg"),
    ("психотерап", "chat-circle.svg"),
    ("психолог", "chat-circle.svg"),
    ("родственник", "house.svg"),
    ("диагност", "plus.svg"),
    ("восстанов", "sun.svg"),
]


def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def cat_icon(title: str) -> str:
    low = title.lower()
    for needle, icon in CAT_ICONS:
        if needle in low:
            return icon
    return "first-aid.svg"


def desktop_html(menu: list[dict]) -> str:
    cats: list[str] = []
    panels: list[str] = []
    search_items: list[str] = []

    for index, item in enumerate(menu):
        icon = cat_icon(item["parent"])
        active = " is-active" if index == 0 else ""
        cats.append(
            f"""                  <li>
                    <button class="services-menu__cat{active}" type="button" data-services-cat="{index}">
                      <img class="services-menu__cat-icon" src="/assets/icons/{icon}" alt="" width="16" height="16" decoding="async">
                      <span>{esc(item["parent"])}</span>
                    </button>
                  </li>"""
        )

        links: list[str] = []
        for child in item.get("child") or []:
            search_items.append(
                f'                  <li data-services-search-item hidden>'
                f'<a href="{esc(child["link"])}">{esc(child["title"])}</a></li>'
            )
            links.append(
                f'                    <li><a href="{esc(child["link"])}">{esc(child["title"])}</a></li>'
            )

        panels.append(
            f"""                <div class="services-menu__panel{active}" data-services-panel="{index}">
                  <ul class="services-menu__panel-list" role="list">
{chr(10).join(links)}
                  </ul>
                </div>"""
        )

    return f"""            <div class="services-menu" id="services-menu" data-services-menu-panel>
      <div class="services-menu__toolbar">
        <form class="services-menu__search" action="#" method="get" data-services-search-form>
          <label class="services-menu__search-field">
            <span class="visually-hidden">Поиск услуги</span>
            <svg class="services-menu__search-icon" aria-hidden="true" width="14" height="14" viewBox="0 0 256 256" fill="currentColor">
              <path d="M229.66,218.34l-50.07-50.06a88.11,88.11,0,1,0-11.31,11.31l50.06,50.07a8,8,0,0,0,11.32-11.32ZM40,112a72,72,0,1,1,72,72A72.08,72.08,0,0,1,40,112Z"/>
            </svg>
            <input class="services-menu__search-input" type="search" placeholder="Поиск услуги" autocomplete="off" data-services-search>
          </label>
        </form>
        <button class="services-menu__clear" type="button" data-services-clear>
          <img class="services-menu__clear-icon" src="/assets/icons/x.svg" alt="" width="13" height="13" decoding="async">
          <span>Очистить</span>
        </button>
      </div>
      <div class="services-menu__results" data-services-results hidden>
        <span class="services-menu__results-title">Результаты поиска</span>
        <ul class="services-menu__results-list" role="list" data-services-results-list>
{chr(10).join(search_items)}
        </ul>
        <p class="services-menu__empty" data-services-empty hidden>Ничего не найдено</p>
      </div>
      <div class="services-menu__layout" data-services-layout>
        <ul class="services-menu__cats" role="list">
{chr(10).join(cats)}
        </ul>
        <div class="services-menu__panels">
{chr(10).join(panels)}
        </div>
      </div>
    </div>"""


def mobile_html(menu: list[dict]) -> str:
    categories: list[str] = []
    for item in menu:
        links = [
            f'                <a href="{esc(item["link"])}" data-menu-close>Все услуги раздела</a>'
        ]
        for child in item.get("child") or []:
            links.append(
                f'                <a href="{esc(child["link"])}" data-menu-close>{esc(child["title"])}</a>'
            )
        categories.append(
            f"""            <div class="mobile-menu__accordion mobile-menu__accordion--nested" data-mobile-accordion>
              <button class="mobile-menu__accordion-btn" type="button" data-mobile-accordion-btn aria-expanded="false">
                {esc(item["parent"])}
              </button>
              <div class="mobile-menu__accordion-panel">
{chr(10).join(links)}
              </div>
            </div>"""
        )

    return f"""          <div data-services-menu-mobile>
          <div class="mobile-menu__accordion mobile-menu__accordion--services" data-mobile-accordion>
            <button class="mobile-menu__accordion-btn" type="button" data-mobile-accordion-btn aria-expanded="false">
              Услуги
            </button>
            <div class="mobile-menu__accordion-panel mobile-menu__accordion-panel--services">
{chr(10).join(categories)}
            </div>
            </div>
          </div>"""


DRUGS = [
    ("esperal", "Эспераль"),
    ("akvilong", "Аквилонг"),
    ("algominal", "Алгоминал"),
    ("disulfiram", "Дисульфирам"),
    ("naltrekson", "Налтрексон"),
    ("vivitrol", "Вивитрол"),
    ("torpedo", "Торпедо"),
]


def rebuild_menu(menu: list[dict]) -> list[dict]:
    """Promote priority tabs and enrich coding/decoding drug lists."""
    by_parent = {item["parent"]: item for item in menu}

    nark_help = by_parent.get("Наркологическая помощь")
    if nark_help:
        nark_help["child"] = [
            child
            for child in nark_help["child"]
            if child["title"] != "Нарколог на дом"
        ]

    alk = by_parent.get("Лечение алкоголизма")
    if alk:
        alk["child"] = [
            child
            for child in alk["child"]
            if not child["title"].startswith("Вывод из запоя")
        ]
        mo_alk = {
            "title": "Лечение алкоголизма в Московской области",
            "link": "/uslugi/lechenie-alkogolizma/moskovskaya-oblast/",
        }
        alk["child"] = [c for c in alk["child"] if c["link"] != mo_alk["link"] and "по городам МО" not in c["title"]]
        alk["child"].insert(0, mo_alk)

    nark = by_parent.get("Лечение наркомании")
    if nark:
        mo_nark = {
            "title": "Лечение наркомании в Московской области",
            "link": "/uslugi/lechenie-narkomanii/moskovskaya-oblast/",
        }
        nark["child"] = [
            c for c in nark["child"] if c["link"] != mo_nark["link"] and "по городам МО" not in c["title"]
        ]
        nark["child"].insert(0, mo_nark)

    rehab = by_parent.get("Реабилитация зависимых")
    if rehab:
        mo_rehab = {
            "title": "Реабилитация зависимых в Московской области",
            "link": "/uslugi/reabilitaciya/moskovskaya-oblast/",
        }
        rehab["child"] = [
            c for c in rehab["child"] if c["link"] != mo_rehab["link"] and "по городам МО" not in c["title"]
        ]
        rehab["child"].insert(0, mo_rehab)

    coding = by_parent.get("Кодирование")
    if coding:
        for child in coding["child"]:
            for slug, name in DRUGS:
                if child["link"] == f"/uslugi/kodirovanie/preparaty/{slug}/":
                    child["title"] = f"Кодирование {name}"
        mo_code = {
            "title": "Кодирование на дому в Московской области",
            "link": "/uslugi/kodirovanie/na-domu/moskovskaya-oblast/",
        }
        if not any(c["link"] == mo_code["link"] for c in coding["child"]):
            insert_at = next(
                (i + 1 for i, c in enumerate(coding["child"]) if c["title"] == "Кодирование на дому"),
                len(coding["child"]),
            )
            coding["child"].insert(insert_at, mo_code)

    kap = by_parent.get("Капельницы")
    if kap:
        mo_kap = {
            "title": "Капельница на дому в Московской области",
            "link": "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/moskovskaya-oblast/",
        }
        if not any(c["link"] == mo_kap["link"] for c in kap["child"]):
            insert_at = next(
                (
                    i + 1
                    for i, c in enumerate(kap["child"])
                    if c["title"] in {"Капельница на дому", "Капельница от запоя", "Капельница от алкоголя"}
                ),
                len(kap["child"]),
            )
            kap["child"].insert(insert_at, mo_kap)

    decoding = by_parent.get("Раскодирование")
    if decoding:
        decoding["child"] = [
            {"title": "Раскодирование", "link": "/uslugi/kodirovanie/raskodirovanie/"}
        ] + [
            {
                "title": f"Раскодирование от {name}",
                "link": f"/uslugi/kodirovanie/raskodirovanie/{slug}/",
            }
            for slug, name in DRUGS
        ]

    priority = [
        {
            "parent": "Нарколог на дом",
            "link": "/uslugi/narkolog-na-dom/",
            "child": [
                {"title": "Нарколог на дом", "link": "/uslugi/narkolog-na-dom/"},
                {
                    "title": "Нарколог на дом в Московской области",
                    "link": "/uslugi/narkolog-na-dom/moskovskaya-oblast/",
                },
            ],
        },
        {
            "parent": "Вывод из запоя на дому",
            "link": "/uslugi/vyvod-iz-zapoya/na-domu/",
            "child": [
                {"title": "Вывод из запоя на дому", "link": "/uslugi/vyvod-iz-zapoya/na-domu/"},
                {
                    "title": "Вывод из запоя на дому в Московской области",
                    "link": "/uslugi/vyvod-iz-zapoya/na-domu/moskovskaya-oblast/",
                },
                {"title": "Вывод из запоя", "link": "/uslugi/vyvod-iz-zapoya/"},
                {
                    "title": "Вывод из запоя в стационаре",
                    "link": "/uslugi/vyvod-iz-zapoya/v-stacionare/",
                },
            ],
        },
    ]

    # Keep coding/decoding near the top after priority tabs.
    rest_order = [
        "Кодирование",
        "Раскодирование",
        "Наркологическая помощь",
        "Лечение алкоголизма",
        "Капельницы",
        "Лечение наркомании",
        "Другие зависимости",
        "Реабилитация зависимых",
        "Психиатрическая помощь",
        "Психотерапия и психология",
    ]
    rest = []
    for name in rest_order:
        item = by_parent.get(name)
        if item:
            rest.append(item)

    for item in menu:
        if item["parent"] not in {p["parent"] for p in priority} and item not in rest:
            rest.append(item)

    return priority + rest


def strip_header_extra_nav(text: str) -> str:
    # Keep about dropdown hooks; remove only coding/decoding/priority tabs.
    if 'data-nav-dropdown' not in text.split("О клинике", 1)[0][-200:]:
        text = text.replace(
            'class="hero-header__nav-item hero-header__nav-item--about"',
            'class="hero-header__nav-item hero-header__nav-item--about hero-header__nav-item--dropdown" data-nav-dropdown',
            1,
        )

    text = re.sub(
        r'\n              <li class="hero-header__nav-item hero-header__nav-item--dropdown" data-nav-dropdown>.*?'
        r'<li class="hero-header__nav-item hero-header__nav-item--priority">.*?'
        r'</li>\n\n              <li class="hero-header__nav-item">\n'
        r'                <a class="hero-header__nav-link" href="/ceny/">Цены</a>',
        '\n              <li class="hero-header__nav-item">\n'
        '                <a class="hero-header__nav-link" href="/ceny/">Цены</a>',
        text,
        count=1,
        flags=re.S,
    )

    text = text.replace(
        'class="hero-header__nav-item hero-header__nav-item--secondary"',
        'class="hero-header__nav-item"',
    )

    # Remove mobile priority blocks inserted earlier.
    text = re.sub(
        r'\n          <ul class="mobile-menu__list mobile-menu__list--priority" role="list">.*?'
        r'(?=          <ul class="mobile-menu__list" role="list">)',
        "\n",
        text,
        count=1,
        flags=re.S,
    )

    return text


def main() -> None:
    menu = rebuild_menu(json.loads(MENU_PATH.read_text(encoding="utf-8")))
    MENU_PATH.write_text(json.dumps(menu, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    JS_PATH.write_text(
        "export const servicesMenu = " + json.dumps(menu, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )

    text = HEADER.read_text(encoding="utf-8")
    text = strip_header_extra_nav(text)

    desktop = desktop_html(menu)
    text, n_desk = re.subn(
        r'<div class="services-menu" id="services-menu" data-services-menu-panel>.*?</div>\s*'
        r'(?=<div\s+class="mobile-menu"|<div\n\s+class="mobile-menu")',
        desktop + "\n\n    ",
        text,
        count=1,
        flags=re.S,
    )
    if n_desk != 1:
        raise SystemExit(f"desktop mega-menu replace failed: {n_desk}")

    mobile = mobile_html(menu)
    text, n_mob = re.subn(
        r'<div data-services-menu-mobile>.*?</div>\s*(?=<ul class="mobile-menu__list")',
        mobile + "\n\n          ",
        text,
        count=1,
        flags=re.S,
    )
    if n_mob != 1:
        raise SystemExit(f"mobile services replace failed: {n_mob}")

    HEADER.write_text(text, encoding="utf-8")
    print("synced", len(menu), "categories")
    for item in menu:
        print(f"  {item['parent']}: {len(item['child'])}")


if __name__ == "__main__":
    main()
