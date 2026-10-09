import pytest

from app import create_app
from app.services.catalog import get_catalog, has_banned_segment


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_catalog_keeps_service_urls_and_drops_removed_sections():
    catalog = get_catalog()
    urls = set(catalog.public_urls())

    assert len(urls) == 1420
    assert "/uslugi/narkolog-na-dom/" in urls
    assert "/uslugi/narkolog-na-dom/aeroport/" in urls
    assert "/uslugi/narkolog-na-dom/moskovskaya-oblast/balashiha/" in urls
    assert "/uslugi/pomoshch-rodstvennikam/" not in urls
    assert "/uslugi/diagnostika/" not in urls
    assert "/uslugi/vosstanovitelnaya-terapiya/" not in urls
    assert not any(has_banned_segment(url) for url in urls)


def test_menu_aliases_point_at_existing_pages():
    catalog = get_catalog()
    targets = catalog.menu_targets()

    assert targets["Капельница на дому"] == "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/"
    assert targets["Лечение наркомании по городам МО"] == "/uslugi/lechenie-narkomanii/moskovskaya-oblast/"
    assert targets["Метод Шичко"] == "/uslugi/reabilitaciya/"
    assert catalog.get(targets["Капельница от запоя"]) is not None


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Наркологическая помощь при алкогольной и наркотической зависимости" in html
    assert 'href="/uslugi/narkolog-na-dom/"' in html
    assert 'href="/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/"' in html
    assert 'href="/vrachi/"' in html
    assert "/uslugi/pomoshch-rodstvennikam/" not in html
    assert "/uslugi/diagnostika/" not in html
    assert "/uslugi/vosstanovitelnaya-terapiya/" not in html


def test_narkolog_keeps_written_hero(client):
    response = client.get("/uslugi/narkolog-na-dom/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "<title>Вызов нарколога на дом в Москве — Нова клиник</title>" in html
    assert "Вызов нарколога на дом в" in html
    assert "Москве и области" in html
    assert "Врач приедет на адрес" in html
    assert "Солнцев Роман Викторович" in html
    assert "от 5&nbsp;000&nbsp;₽" in html


def test_geo_pages_change_heading_and_keep_doctor(client):
    metro = client.get("/uslugi/narkolog-na-dom/aeroport/")
    city = client.get("/uslugi/narkolog-na-dom/moskovskaya-oblast/balashiha/")

    assert metro.status_code == 200
    assert city.status_code == 200
    metro_html = metro.get_data(as_text=True)
    city_html = city.get_data(as_text=True)
    assert "метро Аэропорт" in metro_html
    assert "Балашиха" in city_html
    assert "Солнцев Роман Викторович" in metro_html
    assert "Солнцев Роман Викторович" in city_html
    assert 'rel="canonical" href="http://localhost/uslugi/narkolog-na-dom/aeroport/"' in metro_html


def test_removed_and_help_sections_are_missing(client):
    assert client.get("/uslugi/pomoshch-rodstvennikam/").status_code == 404
    assert client.get("/uslugi/diagnostika/").status_code == 404
    assert client.get("/uslugi/vosstanovitelnaya-terapiya/").status_code == 404
    assert client.get("/pomoshch/").status_code == 404
    assert client.get("/pomosh/").status_code == 404


def test_info_page(client):
    response = client.get("/licenziya/")

    assert response.status_code == 200
    assert "<h1 class=\"info-page__title\">Лицензия</h1>" in response.get_data(as_text=True)


def test_remaining_site_pages(client):
    pages = {
        "/o-klinike/": "Клиника",
        "/ceny/": "Цены",
        "/otzyvy/": "Отзывы",
        "/kejsy/": "Кейсы",
        "/blog/": "Блог",
        "/kontakty/": "Контакты",
        "/politika-konfidencialnosti/": "Политика конфиденциальности",
        "/soglasie/": "Согласие на обработку персональных данных",
    }

    for path, title in pages.items():
        response = client.get(path)
        assert response.status_code == 200
        assert f"<h1 class=\"info-page__title\">{title}</h1>" in response.get_data(as_text=True)

    home = client.get("/").get_data(as_text=True)
    assert 'href="/ceny/"' in home
    assert 'href="/otzyvy/"' in home
    assert 'href="/kontakty/"' in home
    assert 'href="/o-klinike/"' in home
    assert 'href="/blog/"' in home
    assert 'href="/soglasie/"' in home


def test_sitemap_lists_services_and_skips_removed_sections(client):
    response = client.get("/sitemap.xml")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert response.mimetype == "application/xml"
    assert "http://localhost/uslugi/narkolog-na-dom/" in body
    assert "http://localhost/vrachi/" in body
    assert "http://localhost/ceny/" in body
    assert "http://localhost/kontakty/" in body
    assert "http://localhost/otzyvy/" in body
    assert "pomoshch-rodstvennikam" not in body
    assert "/pomoshch/" not in body
    assert "/pomosh/" not in body
