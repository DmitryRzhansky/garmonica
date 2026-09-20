# -*- coding: utf-8 -*-
"""Generate services mega-menu HTML into index.html and rewrite classic scripts."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"C:\Users\User\Desktop\garmonica")
MENU = json.loads((ROOT / "assets" / "data" / "services-menu.json").read_text(encoding="utf-8"))

CAT_ICONS = [
    ("нарколог", "ambulance.svg"),
    ("алкогол", "first-aid.svg"),
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


def desktop_html() -> str:
    cats = []
    panels = []
    search_items = []

    for index, item in enumerate(MENU):
        icon = cat_icon(item["parent"])
        active = " is-active" if index == 0 else ""
        cats.append(
            f"""                  <li>
                    <button class="services-menu__cat{active}" type="button" data-services-cat="{index}">
                      <img class="services-menu__cat-icon" src="assets/icons/{icon}" alt="" width="16" height="16" decoding="async">
                      <span>{esc(item["parent"])}</span>
                    </button>
                  </li>"""
        )

        links = []
        for child in item.get("child") or []:
            search_items.append(
                f'                  <li data-services-search-item hidden><a href="{esc(child["link"])}">{esc(child["title"])}</a></li>'
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

    return f"""    <div class="services-menu" id="services-menu" data-services-menu-panel>
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
          <img class="services-menu__clear-icon" src="assets/icons/x.svg" alt="" width="13" height="13" decoding="async">
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


def mobile_html() -> str:
    blocks = [
        '          <p class="mobile-menu__services-title">Услуги</p>',
    ]
    for item in MENU:
        links = [
            f'              <a href="{esc(item["link"])}" data-menu-close>Все услуги раздела</a>'
        ]
        for child in item.get("child") or []:
            links.append(
                f'              <a href="{esc(child["link"])}" data-menu-close>{esc(child["title"])}</a>'
            )
        blocks.append(
            f"""          <div class="mobile-menu__accordion" data-mobile-accordion>
            <button class="mobile-menu__accordion-btn" type="button" data-mobile-accordion-btn aria-expanded="false">
              {esc(item["parent"])}
            </button>
            <div class="mobile-menu__accordion-panel">
{chr(10).join(links)}
            </div>
          </div>"""
        )
    return "\n".join(blocks)


def patch_index() -> None:
    path = ROOT / "index.html"
    html = path.read_text(encoding="utf-8")

    desktop = desktop_html()
    html = re.sub(
        r'<div class="services-menu" id="services-menu" data-services-menu-panel>.*?</div>\s*(?=<div\s+class="mobile-menu")',
        desktop + "\n\n    ",
        html,
        count=1,
        flags=re.S,
    )

    # If empty self-closing style tag was used
    if 'data-services-menu-panel></div>' in html and "services-menu__toolbar" not in html:
        html = html.replace(
            '<div class="services-menu" id="services-menu" data-services-menu-panel></div>',
            desktop,
            1,
        )

    mobile = mobile_html()
    html = re.sub(
        r'<div data-services-menu-mobile></div>',
        f'<div data-services-menu-mobile>\n{mobile}\n          </div>',
        html,
        count=1,
    )

    html = re.sub(
        r'<script type="module" src="assets/js/main\.js[^"]*"></script>',
        """<script src="assets/js/modules/menu.js" defer></script>
    <script src="assets/js/modules/services-menu.js" defer></script>
    <script src="assets/js/modules/contact-form.js" defer></script>
    <script src="assets/js/modules/reviews.js" defer></script>
    <script src="assets/js/main.js" defer></script>""",
        html,
        count=1,
    )

    path.write_text(html, encoding="utf-8")
    print("patched index.html")


if __name__ == "__main__":
    patch_index()
