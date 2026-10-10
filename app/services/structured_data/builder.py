"""Build Schema.org @graph payloads per public page type."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from app.data.doctors import get_clinic_doctors
from app.data.faq_page import get_faq_page
from app.data.gallery_page import get_gallery_page
from app.data.home_services import get_home_service_hubs
from app.data.service_reviews import get_service_reviews
from app.services.catalog import get_catalog, normalize_url
from app.services.info_pages import INFO_PAGES
from app.services.site_map import get_site_map
from app.services.structured_data.clinic import (
    absolute_url,
    build_medical_clinic,
    build_website,
    clinic_id,
    website_id,
)
from app.services.structured_data.offers import build_offer_catalog
from app.services.structured_data.serialize import dumps_json_ld, prune_empty

INFO_BREADCRUMBS: dict[str, list[tuple[str, str | None]]] = {
    "o-klinike": [("Главная", "/"), ("О клинике", None)],
    "vrachi": [("Главная", "/"), ("Наши врачи", None)],
    "ceny": [("Главная", "/"), ("Цены", None)],
    "karta-sajta": [("Главная", "/"), ("Карта сайта", None)],
    "voprosy": [("Главная", "/"), ("Частые вопросы", None)],
    "galereya": [("Главная", "/"), ("Фотогалерея", None)],
    "licenziya": [("Главная", "/"), ("Лицензия", None)],
    "otzyvy": [("Главная", "/"), ("Отзывы", None)],
    "kontakty": [("Главная", "/"), ("Контакты", None)],
}

def build_json_ld(request) -> str | None:
    """Return serialized JSON-LD for the current request, or None if not a public page."""
    host = request.host_url.rstrip("/")
    path = request.path
    if not path.endswith("/") and path != "/":
        path = path + "/"

    graph = _graph_for_path(host, path)
    if not graph:
        return None
    payload = prune_empty({"@context": "https://schema.org", "@graph": graph})
    if not payload:
        return None
    return dumps_json_ld(payload)


def _graph_for_path(host: str, path: str) -> list[dict[str, Any]] | None:
    if path == "/":
        return _home_graph(host)

    if path.startswith("/uslugi"):
        return _service_graph(host, path)

    slug = path.strip("/")
    if slug in INFO_PAGES:
        return _info_graph(host, slug)

    return None


def _home_graph(host: str) -> list[dict[str, Any]]:
    page_id = f"{host}/"
    clinic = build_medical_clinic(host)
    website = build_website(host)
    hubs = get_home_service_hubs()
    item_list = {
        "@type": "ItemList",
        "@id": f"{page_id}#services",
        "name": "Наши услуги",
        "numberOfItems": len(hubs),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": hub["name"],
                "url": absolute_url(host, hub["url"]),
                "description": hub["text"],
            }
            for index, hub in enumerate(hubs, 1)
        ],
    }
    webpage = {
        "@type": "WebPage",
        "@id": page_id,
        "url": page_id,
        "name": "Нова — клиника психиатрии и наркологии | Помощь 24/7",
        "description": (
            "Клиника психиатрии и наркологии «Нова»: вызов врача на дом, детоксикация, "
            "стационар и сопровождение восстановления. Круглосуточно, конфиденциально, "
            "с понятной стоимостью до начала помощи."
        ),
        "inLanguage": "ru-RU",
        "isPartOf": {"@id": website_id(host)},
        "about": {"@id": clinic_id(host)},
        "mainEntity": {"@id": clinic_id(host)},
        "hasPart": {"@id": item_list["@id"]},
    }
    return [clinic, website, webpage, item_list]


def _service_graph(host: str, path: str) -> list[dict[str, Any]] | None:
    catalog = get_catalog()
    url = normalize_url(path)
    view = catalog.view(url)
    if view is None:
        return None

    page_id = absolute_url(host, view.url)
    clinic = build_medical_clinic(host)
    website = build_website(host)
    graph: list[dict[str, Any]] = [clinic, website]

    breadcrumbs = _breadcrumb_list(host, [(c.name, c.url) for c in view.breadcrumbs], page_id)
    if breadcrumbs:
        graph.append(breadcrumbs)

    kind = catalog.get(view.url).get("kind")
    page_meta = {
        "url": page_id,
        "name": view.seo.h1,
        "description": view.meta_description,
        "inLanguage": "ru-RU",
        "isPartOf": {"@id": website_id(host)},
        "about": {"@id": clinic_id(host)},
        "breadcrumb": {"@id": f"{page_id}#breadcrumb"} if breadcrumbs else None,
    }

    faq_items = [(ask, answer) for ask, answer in view.seo.faq_items]
    faq_ref = {"@id": f"{page_id}#faq"} if faq_items else None

    if kind == "structural":
        silo_roots = [p for p in catalog.pages if p["kind"] == "silo-root"]
        item_list = {
            "@type": "ItemList",
            "@id": f"{page_id}#itemlist",
            "name": view.name,
            "numberOfItems": len(silo_roots),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": index,
                    "name": page["name"],
                    "url": absolute_url(host, page["url"]),
                }
                for index, page in enumerate(silo_roots, 1)
            ],
        }
        webpage = {
            "@type": "CollectionPage",
            "@id": page_id,
            **page_meta,
            "mainEntity": {"@id": item_list["@id"]},
            "hasPart": faq_ref,
        }
        graph.extend([webpage, item_list])
    else:
        page_row = catalog.get(view.url) or {}
        service = _service_entity(host, page_id, view, page_row)
        webpage = {
            "@type": "WebPage",
            "@id": page_id,
            **page_meta,
            "mainEntity": {"@id": service["@id"]},
            "hasPart": faq_ref,
        }
        graph.extend([webpage, service])

    if faq_items:
        graph.append(_faq_page(page_id, faq_items))

    return graph


def _service_entity(host: str, page_id: str, view, page: dict) -> dict[str, Any]:
    service: dict[str, Any] = {
        "@type": "Service",
        "@id": f"{page_id}#service",
        "name": view.seo.h1,
        "description": view.meta_description,
        "url": page_id,
        "serviceType": page.get("service_name") or view.name,
        "provider": {"@id": clinic_id(host)},
    }
    area = _area_served(page)
    if area:
        service["areaServed"] = area
    return service


def _area_served(page: dict) -> dict[str, Any] | None:
    kind = page.get("kind") or ""
    geo_name = (page.get("geo_name") or "").strip()
    if kind == "metro" and geo_name:
        return {
            "@type": "Place",
            "name": f"станция метро {geo_name}",
            "containedInPlace": {
                "@type": "City",
                "name": "Москва",
            },
        }
    if kind == "okrug" and geo_name:
        return {
            "@type": "AdministrativeArea",
            "name": geo_name,
            "containedInPlace": {
                "@type": "City",
                "name": "Москва",
            },
        }
    if kind == "city" and geo_name:
        return {
            "@type": "City",
            "name": geo_name,
            "containedInPlace": {
                "@type": "AdministrativeArea",
                "name": "Московской области",
            },
        }
    if kind == "geo-hub":
        # Use the same wording as the published H1 accent («Московской области»).
        return {
            "@type": "AdministrativeArea",
            "name": "Московской области",
        }
    # Non-geo service pages: clinic operates in Moscow (published positioning).
    if kind in {"silo-root", "child"}:
        return {
            "@type": "City",
            "name": "Москва",
        }
    return None


def _info_graph(host: str, slug: str) -> list[dict[str, Any]]:
    page = INFO_PAGES[slug]
    page_id = absolute_url(host, f"/{slug}/")
    clinic = build_medical_clinic(host)
    website = build_website(host)
    graph: list[dict[str, Any]] = [clinic, website]

    crumbs = INFO_BREADCRUMBS.get(slug)
    breadcrumbs = None
    if crumbs:
        breadcrumbs = _breadcrumb_list(host, crumbs, page_id)
        graph.append(breadcrumbs)

    base_page = {
        "@id": page_id,
        "url": page_id,
        "name": page["title"],
        "description": page["description"],
        "inLanguage": "ru-RU",
        "isPartOf": {"@id": website_id(host)},
        "about": {"@id": clinic_id(host)},
        "breadcrumb": {"@id": f"{page_id}#breadcrumb"} if breadcrumbs else None,
    }

    if slug == "o-klinike":
        graph.append(
            {
                "@type": "AboutPage",
                **base_page,
                "mainEntity": {"@id": clinic_id(host)},
            }
        )
        return graph

    if slug == "kontakty":
        graph.append(
            {
                "@type": "ContactPage",
                **base_page,
                "mainEntity": {"@id": clinic_id(host)},
            }
        )
        return graph

    if slug == "voprosy":
        faq = get_faq_page()
        questions = [(item["ask"], item["answer"]) for item in faq["questions"]]
        # FAQPage is the document type (WebPage subtype) — do not also emit WebPage.
        faq_node = _faq_page(page_id, questions, is_document=True)
        faq_node.update({k: v for k, v in base_page.items() if k != "@id"})
        faq_node["@id"] = page_id
        graph.append(faq_node)
        return graph

    if slug == "vrachi":
        people, item_list = _doctors_list(host, page_id)
        graph.append(
            {
                "@type": "CollectionPage",
                **base_page,
                "mainEntity": {"@id": item_list["@id"]},
            }
        )
        graph.append(item_list)
        graph.extend(people)
        return graph

    if slug == "ceny":
        catalog = build_offer_catalog(host, page_id)
        graph.append(
            {
                "@type": "CollectionPage",
                **base_page,
                "mainEntity": {"@id": catalog["@id"]},
            }
        )
        graph.append(catalog)
        return graph

    if slug == "otzyvy":
        item_list = _reviews_item_list(page_id)
        graph.append(
            {
                "@type": "CollectionPage",
                **base_page,
                "mainEntity": {"@id": item_list["@id"]},
            }
        )
        graph.append(item_list)
        return graph

    if slug == "galereya":
        images, item_list = _gallery_list(host, page_id)
        graph.append(
            {
                "@type": "ImageGallery",
                **base_page,
                "mainEntity": {"@id": item_list["@id"]},
            }
        )
        graph.append(item_list)
        graph.extend(images)
        return graph

    if slug == "licenziya":
        graph.append(
            {
                "@type": "WebPage",
                **base_page,
                "mainEntity": {"@id": clinic_id(host)},
            }
        )
        return graph

    if slug == "karta-sajta":
        item_list = _sitemap_item_list(host, page_id)
        graph.append(
            {
                "@type": "CollectionPage",
                **base_page,
                "mainEntity": {"@id": item_list["@id"]},
            }
        )
        graph.append(item_list)
        return graph

    # Legal stubs and any other info pages.
    graph.append({"@type": "WebPage", **base_page})
    return graph


def _breadcrumb_list(
    host: str,
    crumbs: list[tuple[str, str | None]],
    page_id: str,
) -> dict[str, Any] | None:
    if len(crumbs) < 2:
        return None
    elements = []
    for position, (name, path) in enumerate(crumbs, 1):
        item: dict[str, Any] = {
            "@type": "ListItem",
            "position": position,
            "name": name,
        }
        is_last = position == len(crumbs)
        if path and not is_last:
            item["item"] = absolute_url(host, path)
        elif is_last:
            # Last crumb is the current page; item optional per Google docs.
            pass
        elements.append(item)
    return {
        "@type": "BreadcrumbList",
        "@id": f"{page_id}#breadcrumb",
        "itemListElement": elements,
    }


def _faq_page(
    page_id: str,
    items: list[tuple[str, str]],
    *,
    is_document: bool = False,
) -> dict[str, Any]:
    entity_id = page_id if is_document else f"{page_id}#faq"
    return {
        "@type": "FAQPage",
        "@id": entity_id,
        "url": page_id if is_document else None,
        "mainEntity": [
            {
                "@type": "Question",
                "@id": f"{entity_id}/q/{index}",
                "name": ask,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answer,
                },
            }
            for index, (ask, answer) in enumerate(items, 1)
        ],
    }


def _doctors_list(host: str, page_id: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    doctors = get_clinic_doctors()
    people: list[dict[str, Any]] = []
    elements: list[dict[str, Any]] = []
    for index, doctor in enumerate(doctors, 1):
        person_id = f"{page_id}#{doctor['slug']}"
        credentials: list[dict[str, Any]] = []
        if doctor.get("degree"):
            credentials.append(
                {
                    "@type": "EducationalOccupationalCredential",
                    "credentialCategory": "degree",
                    "name": doctor["degree"],
                }
            )
        for cert in doctor.get("certificates") or []:
            credentials.append(
                {
                    "@type": "EducationalOccupationalCredential",
                    "credentialCategory": "certificate",
                    "name": cert,
                }
            )
        # jobTitle: published role; specialty text goes into description, not Physician type.
        description_parts = [doctor.get("lead") or ""]
        if doctor.get("specialty"):
            description_parts.append(doctor["specialty"])
        if doctor.get("experience"):
            description_parts.append(f"Опыт: {doctor['experience']}")
        person = {
            "@type": "Person",
            "@id": person_id,
            "name": doctor["name"],
            "jobTitle": doctor["role"],
            "description": ". ".join(part for part in description_parts if part),
            "worksFor": {"@id": clinic_id(host)},
            "url": page_id,
            "hasCredential": credentials or None,
        }
        people.append(person)
        elements.append(
            {
                "@type": "ListItem",
                "position": index,
                "item": {"@id": person_id},
            }
        )
    item_list = {
        "@type": "ItemList",
        "@id": f"{page_id}#itemlist",
        "name": "Наши врачи",
        "numberOfItems": len(people),
        "itemListElement": elements,
    }
    return people, item_list


def _reviews_item_list(page_id: str) -> dict[str, Any]:
    """Neutral collection of published review texts without rating claims.

    Individual Review / AggregateRating on MedicalClinic are omitted: dates lack
    a year, third-party aggregate scores must not become clinic AggregateRating,
    and self-serving LocalBusiness review stars are ineligible for Google.
    """
    elements: list[dict[str, Any]] = []
    position = 0
    for source in get_service_reviews():
        for review in source.get("reviews") or []:
            position += 1
            work_id = f"{page_id}#review-{source['id']}-{position}"
            elements.append(
                {
                    "@type": "ListItem",
                    "position": position,
                    "item": {
                        "@type": "CreativeWork",
                        "@id": work_id,
                        "author": {
                            "@type": "Person",
                            "name": review["name"],
                        },
                        "text": review["text"],
                        "about": {"@id": clinic_id(_host_from_page_id(page_id))},
                        "isPartOf": {
                            "@type": "CreativeWork",
                            "name": source["label"],
                        },
                    },
                }
            )
    return {
        "@type": "ItemList",
        "@id": f"{page_id}#itemlist",
        "name": "Отзывы",
        "numberOfItems": len(elements),
        "itemListElement": elements,
    }


def _host_from_page_id(page_id: str) -> str:
    parsed = urlparse(page_id)
    return f"{parsed.scheme}://{parsed.netloc}"


def _gallery_list(
    host: str, page_id: str
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    photos = get_gallery_page()["photos"]
    images: list[dict[str, Any]] = []
    elements: list[dict[str, Any]] = []
    for index, photo in enumerate(photos, 1):
        image_id = f"{page_id}#image-{index}"
        image = {
            "@type": "ImageObject",
            "@id": image_id,
            "contentUrl": absolute_url(host, photo["src"]),
            "url": absolute_url(host, photo["src"]),
            "name": photo.get("title") or photo.get("alt") or f"Фото {index}",
            "description": photo.get("alt") or photo.get("text"),
            "caption": photo.get("text"),
        }
        images.append(image)
        elements.append(
            {
                "@type": "ListItem",
                "position": index,
                "item": {"@id": image_id},
            }
        )
    item_list = {
        "@type": "ItemList",
        "@id": f"{page_id}#itemlist",
        "name": "Фотогалерея",
        "numberOfItems": len(images),
        "itemListElement": elements,
    }
    return images, item_list


def _sitemap_item_list(host: str, page_id: str) -> dict[str, Any]:
    elements: list[dict[str, Any]] = []
    position = 0
    for section in get_site_map():
        position += 1
        elements.append(
            {
                "@type": "ListItem",
                "position": position,
                "name": section.title,
            }
        )
        for link in section.links:
            position += 1
            elements.append(
                {
                    "@type": "ListItem",
                    "position": position,
                    "name": link.title,
                    "url": absolute_url(host, link.url),
                }
            )
        for group in section.groups:
            position += 1
            elements.append(
                {
                    "@type": "ListItem",
                    "position": position,
                    "name": group.title,
                    "url": absolute_url(host, group.url),
                }
            )
    return {
        "@type": "ItemList",
        "@id": f"{page_id}#itemlist",
        "name": "Карта сайта",
        "numberOfItems": len(elements),
        "itemListElement": elements,
    }
