"""Собирает app/data/pages.json из CSV архитектуры profilactica-competitors."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path.home() / "Downloads" / "profilactica-competitors"
OUT_PATH = ROOT / "app" / "data" / "pages.json"

EXCLUDED_SILOS = {
    "Помощь родственникам",
    "Диагностика",
    "Восстановительная терапия",
}
BANNED_SEGMENTS = {"pomosh", "pomoshch"}
MENU_KINDS = {"silo-root", "child", "structural"}


def parent_url(url: str) -> str:
    parts = [part for part in url.strip("/").split("/") if part]
    if len(parts) <= 1:
        return "/"
    return "/" + "/".join(parts[:-1]) + "/"


def banned(url: str) -> bool:
    return any(part in BANNED_SEGMENTS for part in url.strip("/").split("/"))


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


GEO_HUB_OLD_SUFFIX = " — Московская область"
GEO_HUB_NEW_SUFFIX = " в Московской области"


def normalize_geo_hub_name(name: str) -> str:
    if name.endswith(GEO_HUB_OLD_SUFFIX):
        return name[: -len(GEO_HUB_OLD_SUFFIX)] + GEO_HUB_NEW_SUFFIX
    return name


def geo_hub_service_from_name(name: str) -> str:
    for suffix in (GEO_HUB_NEW_SUFFIX, GEO_HUB_OLD_SUFFIX):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    if " — " in name:
        return name.split(" — ", 1)[0]
    return name


def service_heading(page: dict, by_url: dict[str, dict]) -> str:
    if page["kind"] == "geo-hub":
        return geo_hub_service_from_name(page["name"])
    if not page["geo_type"]:
        return page["name"]
    parent = by_url.get(parent_url(page["url"]))
    if parent and parent["kind"] == "geo-hub":
        grandparent = by_url.get(parent_url(parent["url"]))
        if grandparent:
            return grandparent["name"]
    if parent and parent["kind"] != "structural":
        return parent["name"]
    return page["service_name"] or page["name"]


def build_pages(source: Path) -> list[dict]:
    canonical = load_csv(source / "profilactica_canonical_urls.csv")
    geo_rows = load_csv(source / "profilactica_geo_pages.csv")
    geo_by_url = {row["proposed_url"]: row for row in geo_rows}

    pages: list[dict] = []
    for row in canonical:
        url = row["url"]
        if url == "/":
            continue
        if row["silo"] in EXCLUDED_SILOS or banned(url):
            continue
        geo = geo_by_url.get(url, {})
        kind = row["entity_type"]
        name = row["page"]
        if kind == "geo-hub":
            name = normalize_geo_hub_name(name)
        pages.append(
            {
                "url": url,
                "name": name,
                "kind": kind,
                "silo": row["silo"],
                "service_name": geo.get("service_name") or name,
                "geo_name": geo.get("geo_name") or "",
                "geo_type": geo.get("geo_type") or "",
            }
        )

    by_url = {page["url"]: page for page in pages}
    for page in pages:
        page["service_name"] = service_heading(page, by_url)
    return pages


def warn_duplicate_titles(pages: list[dict]) -> None:
    seen: dict[str, str] = {}
    for page in pages:
        if page["kind"] not in MENU_KINDS:
            continue
        previous = seen.get(page["name"])
        if previous and previous != page["url"]:
            raise SystemExit(f"Повторяющееся название: {page['name']} -> {previous} и {page['url']}")
        seen[page["name"]] = page["url"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    pages = build_pages(args.source)
    warn_duplicate_titles(pages)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps({"pages": pages}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"pages {len(pages)} -> {OUT_PATH}")


if __name__ == "__main__":
    main()
