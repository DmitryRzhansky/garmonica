"""Review and AggregateRating entities for MedicalClinic."""

from __future__ import annotations

from typing import Any

from app.data.service_reviews import (
    SERVICE_REVIEW_STATS,
    iter_service_review_items,
    parse_review_date_iso,
)
from app.services.structured_data.clinic import absolute_url, clinic_id


def review_id(host: str, source_id: str, position: int) -> str:
    """Stable @id shared across pages (canonical reviews URL + fragment)."""
    return f"{absolute_url(host, '/otzyvy/')}#review-{source_id}-{position}"


def build_review_entities(host: str) -> list[dict[str, Any]]:
    clinic_ref = {"@id": clinic_id(host)}
    entities: list[dict[str, Any]] = []
    position = 0
    for source, review in iter_service_review_items():
        position += 1
        entity: dict[str, Any] = {
            "@type": "Review",
            "@id": review_id(host, source["id"], position),
            "author": {
                "@type": "Person",
                "name": review["name"],
            },
            "reviewBody": review["text"],
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": review["rating"],
                "bestRating": 5,
                "worstRating": 1,
            },
            "itemReviewed": clinic_ref,
            "publisher": {
                "@type": "Organization",
                "name": source["label"],
            },
        }
        iso_date = parse_review_date_iso(review.get("date") or "")
        if iso_date:
            entity["datePublished"] = iso_date
        entities.append(entity)
    return entities


def build_aggregate_rating() -> dict[str, Any]:
    """AggregateRating matching the visible multi-platform stats block."""
    stats = SERVICE_REVIEW_STATS
    rating_value = float(str(stats["score"]).replace(",", "."))
    return {
        "@type": "AggregateRating",
        "ratingValue": rating_value,
        "bestRating": 5,
        "worstRating": 1,
        "ratingCount": stats["reviews_total"],
        "reviewCount": stats["reviews_total"],
    }


def attach_reviews_to_clinic(
    clinic: dict[str, Any],
    host: str,
    reviews: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Add aggregateRating + review refs onto the shared MedicalClinic entity."""
    reviews = reviews if reviews is not None else build_review_entities(host)
    clinic = dict(clinic)
    clinic["aggregateRating"] = build_aggregate_rating()
    clinic["review"] = [{"@id": item["@id"]} for item in reviews]
    return clinic


def build_reviews_item_list(host: str, page_id: str, reviews: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "@type": "ItemList",
        "@id": f"{page_id}#itemlist",
        "name": "Отзывы",
        "numberOfItems": len(reviews),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "item": {"@id": review["@id"]},
            }
            for index, review in enumerate(reviews, 1)
        ],
    }
