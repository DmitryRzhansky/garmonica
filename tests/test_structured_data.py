"""JSON-LD structured data: coverage, validity, content regression."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import pytest

from app import create_app
from app.data.faq_page import get_faq_page
from app.services.catalog import get_catalog
from app.services.info_pages import INFO_PAGES

LD_RE = re.compile(
    r"<script\b[^>]*type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>",
    re.DOTALL | re.IGNORECASE,
)
LD_STRIP_RE = re.compile(
    r"\s*<script\b[^>]*type=[\"']application/ld\+json[\"'][^>]*>.*?</script>",
    re.DOTALL | re.IGNORECASE,
)

FIXTURE = Path(__file__).parent / "fixtures" / "html_content_fingerprints.json"


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def public_urls() -> list[str]:
    return ["/"] + [f"/{slug}/" for slug in INFO_PAGES] + get_catalog().public_urls()


def extract_graphs(html: str) -> list[dict]:
    graphs = []
    for match in LD_RE.finditer(html):
        payload = json.loads(match.group(1))
        if isinstance(payload, dict) and "@graph" in payload:
            graphs.append(payload)
        else:
            graphs.append(payload)
    return graphs


def graph_nodes(html: str) -> list[dict]:
    nodes: list[dict] = []
    for payload in extract_graphs(html):
        if isinstance(payload, dict) and "@graph" in payload:
            nodes.extend(payload["@graph"])
        elif isinstance(payload, list):
            nodes.extend(payload)
        else:
            nodes.append(payload)
    return nodes


def types_of(nodes: list[dict]) -> set[str]:
    found: set[str] = set()
    for node in nodes:
        value = node.get("@type")
        if isinstance(value, list):
            found.update(value)
        elif value:
            found.add(value)
    return found


def test_public_url_count():
    urls = public_urls()
    assert len(urls) == 1513
    kinds = Counter(page["kind"] for page in get_catalog().pages)
    assert kinds == {
        "structural": 1,
        "silo-root": 12,
        "child": 138,
        "geo-hub": 10,
        "metro": 860,
        "okrug": 60,
        "city": 420,
    }
    assert len(INFO_PAGES) == 11


@pytest.mark.parametrize(
    ("url", "required_types"),
    [
        ("/", {"WebSite", "WebPage", "MedicalClinic"}),
        ("/uslugi/", {"CollectionPage", "ItemList", "MedicalClinic", "FAQPage"}),
        ("/uslugi/narkolog-na-dom/", {"WebPage", "Service", "MedicalClinic", "FAQPage", "BreadcrumbList"}),
        ("/uslugi/narkolog-na-dom/aeroport/", {"WebPage", "Service", "MedicalClinic", "FAQPage", "BreadcrumbList"}),
        ("/uslugi/narkolog-na-dom/cao/", {"WebPage", "Service", "MedicalClinic", "FAQPage", "BreadcrumbList"}),
        (
            "/uslugi/narkolog-na-dom/moskovskaya-oblast/balashiha/",
            {"WebPage", "Service", "MedicalClinic", "FAQPage", "BreadcrumbList"},
        ),
        ("/uslugi/narkolog-na-dom/moskovskaya-oblast/", {"WebPage", "Service", "MedicalClinic", "FAQPage"}),
        ("/voprosy/", {"FAQPage", "MedicalClinic", "BreadcrumbList"}),
        ("/otzyvy/", {"CollectionPage", "ItemList", "MedicalClinic"}),
        ("/vrachi/", {"CollectionPage", "ItemList", "Person", "MedicalClinic"}),
        ("/ceny/", {"CollectionPage", "OfferCatalog", "MedicalClinic"}),
        ("/o-klinike/", {"AboutPage", "MedicalClinic"}),
        ("/kontakty/", {"ContactPage", "MedicalClinic"}),
        ("/licenziya/", {"WebPage", "MedicalClinic"}),
        ("/galereya/", {"ImageGallery", "ImageObject", "MedicalClinic"}),
        ("/karta-sajta/", {"CollectionPage", "ItemList", "MedicalClinic"}),
        ("/politika-konfidencialnosti/", {"WebPage", "MedicalClinic"}),
        ("/soglasie/", {"WebPage", "MedicalClinic"}),
    ],
)
def test_representative_page_types(client, url, required_types):
    response = client.get(url)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    nodes = graph_nodes(html)
    assert types_of(nodes) >= required_types
    assert len(extract_graphs(html)) == 1


def test_stable_clinic_id_and_no_self_serving_ratings(client):
    html = client.get("/").get_data(as_text=True)
    nodes = graph_nodes(html)
    clinic = next(n for n in nodes if n.get("@type") == "MedicalClinic")
    assert clinic["@id"].endswith("/#clinic")
    assert clinic["name"] == "Нова"
    assert clinic["legalName"] == "ООО «НикаПроМЕД»"
    assert clinic["taxID"] == "9715492100"
    assert "aggregateRating" not in clinic
    assert "review" not in clinic

    reviews_html = client.get("/otzyvy/").get_data(as_text=True)
    review_nodes = graph_nodes(reviews_html)
    assert "Review" not in types_of(review_nodes)
    assert "AggregateRating" not in types_of(review_nodes)
    clinic_on_reviews = next(n for n in review_nodes if n.get("@type") == "MedicalClinic")
    assert "aggregateRating" not in clinic_on_reviews
    assert "review" not in clinic_on_reviews


def test_geo_area_served_not_a_branch(client):
    html = client.get("/uslugi/narkolog-na-dom/aeroport/").get_data(as_text=True)
    service = next(n for n in graph_nodes(html) if n.get("@type") == "Service")
    assert service["areaServed"]["@type"] == "Place"
    assert "метро" in service["areaServed"]["name"]
    assert "address" not in service["areaServed"]
    assert "geo" not in service["areaServed"]


def test_faq_matches_visible_questions(client):
    page = get_faq_page()
    html = client.get("/voprosy/").get_data(as_text=True)
    faq = next(n for n in graph_nodes(html) if n.get("@type") == "FAQPage")
    entities = faq["mainEntity"]
    assert len(entities) == len(page["questions"])
    for entity, item in zip(entities, page["questions"], strict=True):
        assert entity["name"] == item["ask"]
        assert entity["acceptedAnswer"]["text"] == item["answer"]

    service_html = client.get("/uslugi/narkolog-na-dom/").get_data(as_text=True)
    assert service_html.count('"@type": "Question"') == 10
    assert service_html.count("FAQPage") == 1


def test_prices_preserve_from_and_on_request(client):
    html = client.get("/ceny/").get_data(as_text=True)
    nodes = graph_nodes(html)
    offers = [n for n in nodes if n.get("@type") == "OfferCatalog"]
    assert offers
    serialized = json.dumps(nodes, ensure_ascii=False)
    assert "minPrice" in serialized
    assert "по запросу" in serialized or "InStoreOnly" in serialized
    assert "Product" not in types_of(nodes)


def test_doctors_are_person_not_physician(client):
    nodes = graph_nodes(client.get("/vrachi/").get_data(as_text=True))
    people = [n for n in nodes if n.get("@type") == "Person"]
    assert len(people) == 4
    assert "Physician" not in types_of(nodes)
    for person in people:
        assert "image" not in person
        assert person["worksFor"]["@id"].endswith("/#clinic")


def test_404_has_no_json_ld(client):
    response = client.get("/no-such-page-for-schema/")
    assert response.status_code == 404
    html = response.get_data(as_text=True)
    assert "application/ld+json" not in html


def test_all_public_pages_have_valid_unique_json_ld(client):
    clinic_ids = set()
    page_ids = set()
    failures: list[str] = []

    for url in public_urls():
        response = client.get(url)
        if response.status_code != 200:
            failures.append(f"{url}: status {response.status_code}")
            continue
        html = response.get_data(as_text=True)
        scripts = LD_RE.findall(html)
        if len(scripts) != 1:
            failures.append(f"{url}: expected 1 JSON-LD script, got {len(scripts)}")
            continue
        try:
            payload = json.loads(scripts[0])
        except json.JSONDecodeError as exc:
            failures.append(f"{url}: invalid JSON ({exc})")
            continue
        if not isinstance(payload, dict) or "@graph" not in payload:
            failures.append(f"{url}: missing @graph")
            continue
        nodes = payload["@graph"]
        ids = [n.get("@id") for n in nodes if n.get("@id")]
        if len(ids) != len(set(ids)):
            failures.append(f"{url}: duplicate @id in graph")
        clinic = next((n for n in nodes if n.get("@type") == "MedicalClinic"), None)
        if clinic is None:
            failures.append(f"{url}: missing MedicalClinic")
        else:
            clinic_ids.add(clinic["@id"])
        page_node = next(
            (
                n
                for n in nodes
                if n.get("@id")
                and n.get("@type")
                in {
                    "WebPage",
                    "CollectionPage",
                    "AboutPage",
                    "ContactPage",
                    "FAQPage",
                    "ImageGallery",
                }
            ),
            None,
        )
        if page_node is None:
            failures.append(f"{url}: missing page entity")
        else:
            if page_node["@id"] in page_ids:
                failures.append(f"{url}: page @id reused: {page_node['@id']}")
            page_ids.add(page_node["@id"])
            canonical = re.search(r'rel="canonical" href="([^"]+)"', html)
            if canonical and page_node.get("url"):
                if page_node["url"] != canonical.group(1):
                    failures.append(
                        f"{url}: page url {page_node['url']} != canonical {canonical.group(1)}"
                    )
        if "aggregateRating" in html.lower() and '"aggregateRating"' in html:
            failures.append(f"{url}: unexpected aggregateRating")

    assert not failures, "\n".join(failures[:40])
    assert len(clinic_ids) == 1
    assert len(page_ids) == 1513


def test_html_content_unchanged_except_json_ld(client):
    baseline = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert baseline["count"] == 1513
    mismatches: list[str] = []
    for url, meta in baseline["urls"].items():
        response = client.get(url)
        assert response.status_code == 200, url
        stripped = LD_STRIP_RE.sub("", response.get_data(as_text=True))
        digest = hashlib.sha256(stripped.encode("utf-8")).hexdigest()
        if digest != meta["sha256"]:
            mismatches.append(f"{url}: content changed outside JSON-LD")
    assert not mismatches, "\n".join(mismatches[:30])
