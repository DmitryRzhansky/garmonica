"""Offer / OfferCatalog helpers for the published price list."""

from __future__ import annotations

import re
from typing import Any

from app.data.prices import get_price_groups

_PRICE_NUMBER = re.compile(r"(\d[\d\s]*)")


def _digits(chunk: str) -> int | None:
    match = _PRICE_NUMBER.search(chunk)
    if not match:
        return None
    return int(match.group(1).replace(" ", "").replace("\u00a0", ""))


def price_spec_from_label(price_label: str, unit: str | None) -> dict[str, Any] | None:
    """Map visible price strings to Schema.org price fields without inventing amounts."""
    raw = price_label.replace("\u00a0", " ").strip()
    lowered = raw.lower()
    if "по запросу" in lowered:
        return {
            "@type": "Offer",
            "description": raw,
            "availability": "https://schema.org/InStoreOnly",
        }

    currency = "RUB"
    working = raw.replace("₽", "").strip()
    is_from = working.lower().startswith("от ")
    if is_from:
        working = working[3:].strip()

    # Range: "8 000–10 000" or "от 15 000–20 000"
    if "–" in working or "—" in working:
        separator = "–" if "–" in working else "—"
        left, right = working.split(separator, 1)
        min_price = _digits(left)
        max_price = _digits(right)
        if min_price is None or max_price is None:
            return None
        spec: dict[str, Any] = {
            "@type": "UnitPriceSpecification",
            "priceCurrency": currency,
            "minPrice": min_price,
            "maxPrice": max_price,
        }
        if unit:
            spec["unitText"] = unit
        offer: dict[str, Any] = {
            "@type": "Offer",
            "priceCurrency": currency,
            "priceSpecification": spec,
        }
        if is_from:
            offer["description"] = raw
        return offer

    amount = _digits(working)
    if amount is None:
        return None

    if is_from or unit:
        spec = {
            "@type": "UnitPriceSpecification",
            "priceCurrency": currency,
            "price": amount if not is_from else None,
            "minPrice": amount if is_from else None,
        }
        if unit:
            spec["unitText"] = unit
        # prune None keys below
        spec = {k: v for k, v in spec.items() if v is not None}
        return {
            "@type": "Offer",
            "priceCurrency": currency,
            "priceSpecification": spec,
            "description": raw if is_from else None,
        }

    return {
        "@type": "Offer",
        "price": amount,
        "priceCurrency": currency,
    }


def build_offer_catalog(host: str, page_url: str) -> dict[str, Any]:
    groups = get_price_groups()
    group_nodes: list[dict[str, Any]] = []
    for group in groups:
        offers: list[dict[str, Any]] = []
        for index, row in enumerate(group["rows"], 1):
            offer = price_spec_from_label(row["price"], row.get("unit"))
            if offer is None:
                continue
            offer["@id"] = f"{page_url}#offer-{group['id']}-{index}"
            offer["name"] = row["name"]
            if row.get("includes"):
                offer["description"] = row["includes"]
            # Keep visible "от …" wording when present
            if row["price"].replace("\u00a0", " ").strip().lower().startswith("от "):
                offer["description"] = (
                    f"{row['includes']}. {row['price']}"
                    if row.get("includes")
                    else row["price"]
                )
            elif "по запросу" in row["price"].lower():
                offer["description"] = (
                    f"{row['includes']}. {row['price']}"
                    if row.get("includes")
                    else row["price"]
                )
            offer["url"] = page_url
            offers.append({k: v for k, v in offer.items() if v is not None})
        if not offers:
            continue
        group_nodes.append(
            {
                "@type": "OfferCatalog",
                "@id": f"{page_url}#price-group-{group['id']}",
                "name": group["title"],
                "itemListElement": offers,
            }
        )

    return {
        "@type": "OfferCatalog",
        "@id": f"{page_url}#offer-catalog",
        "name": "Цены",
        "url": page_url,
        "provider": {"@id": f"{host}/#clinic"},
        "itemListElement": group_nodes,
    }
