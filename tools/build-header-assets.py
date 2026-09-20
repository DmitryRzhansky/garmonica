from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from PIL import Image

ROOT = Path(r"C:\Users\User\Desktop\garmonica")
SRC_LOGO = ROOT / "assets" / "images" / "logo.png"
OUT_MARK = ROOT / "assets" / "images" / "logo-mark.png"
ARCH = Path(
    r"C:\profilactica.clinic\wp-content\themes\zxxrc\assets\data\services-architecture.json"
)
OUT_MENU = ROOT / "assets" / "data" / "services-menu.json"


def crop_logo_mark() -> None:
    im = Image.open(SRC_LOGO).convert("RGBA")
    width, height = im.size
    pixels = im.load()

    def row_density(y: int) -> float:
        non = 0
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a > 20 and not (r > 245 and g > 245 and b > 245):
                non += 1
        return non / width

    # Icon ends at the white gap before title (~570).
    crop_top = 100
    crop_bottom = 570

    xs: list[int] = []
    for y in range(crop_top, crop_bottom):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a > 20 and not (r > 245 and g > 245 and b > 245):
                xs.append(x)

    left, right = min(xs), max(xs)
    pad = 24
    box = (
        max(0, left - pad),
        max(0, crop_top - pad),
        min(width, right + pad),
        crop_bottom,
    )
    icon = im.crop(box)

    side = max(icon.size) + 16
    canvas = Image.new("RGBA", (side, side), (255, 255, 255, 255))
    ox = (side - icon.size[0]) // 2
    oy = (side - icon.size[1]) // 2
    canvas.paste(icon, (ox, oy))
    canvas.save(OUT_MARK, optimize=True)

    for size in (256, 128, 64):
        canvas.resize((size, size), Image.Resampling.LANCZOS).save(
            ROOT / "assets" / "images" / f"logo-mark-{size}.png",
            optimize=True,
        )

    print("logo-mark saved", OUT_MARK, canvas.size, "box", box)


def silo_of(url: str, by_url: dict) -> str | None:
    current = url
    for _ in range(20):
        page = by_url.get(current)
        if not page:
            return None
        if page.get("kind") == "silo":
            return page["url"]
        current = page.get("parent")
    return None


def build_full_menu() -> None:
    data = json.loads(ARCH.read_text(encoding="utf-8"))
    silos = [page for page in data["pages"] if page.get("kind") == "silo"]
    services = [page for page in data["pages"] if page.get("kind") == "service"]
    by_url = {page["url"]: page for page in data["pages"]}
    link_to_silo = {silo["url"]: silo for silo in silos}
    title_to_silo = {silo["title"]: silo for silo in silos}

    groups: dict[str, list] = defaultdict(list)
    for service in services:
        parent_silo = silo_of(service["url"], by_url)
        if parent_silo:
            groups[parent_silo].append(service)

    menu = []
    for item in data["menu"]:
        link = item.get("link") or ""
        silo = link_to_silo.get(link) or title_to_silo.get(item["parent"])
        if not silo:
            menu.append(
                {
                    "parent": item["parent"],
                    "link": "#prices",
                    "child": [
                        {"title": child["title"], "link": "#prices"}
                        for child in item.get("child") or []
                    ],
                }
            )
            continue

        kids = groups.get(silo["url"], [])
        curated_titles = [child["title"] for child in item.get("child") or []]
        by_title = {kid["title"]: kid for kid in kids}
        ordered = []
        seen: set[str] = set()
        for title in curated_titles:
            if title in by_title:
                ordered.append(by_title[title])
                seen.add(title)
        ordered.extend(
            sorted(
                [kid for kid in kids if kid["title"] not in seen],
                key=lambda kid: kid["title"],
            )
        )
        menu.append(
            {
                "parent": item["parent"],
                "link": "#prices",
                "child": [
                    {"title": kid["title"], "link": "#prices"} for kid in ordered
                ],
            }
        )

    OUT_MENU.parent.mkdir(parents=True, exist_ok=True)
    OUT_MENU.write_text(
        json.dumps(menu, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    js_path = ROOT / "assets" / "js" / "data" / "services-menu.js"
    js_path.parent.mkdir(parents=True, exist_ok=True)
    js_path.write_text(
        "export const servicesMenu = "
        + json.dumps(menu, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )

    total = sum(len(item["child"]) for item in menu)
    print("menu cats", len(menu), "services", total)
    print("js module", js_path)
    for item in menu:
        print(f"  {item['parent']}: {len(item['child'])}")


if __name__ == "__main__":
    crop_logo_mark()
    build_full_menu()
