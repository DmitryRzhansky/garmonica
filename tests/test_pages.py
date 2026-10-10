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

    assert len(urls) == 1501
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
    assert "Психонаркологическая клиника — Нова" in html
    assert 'href="/uslugi/narkolog-na-dom/"' in html
    assert 'href="/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/"' in html
    assert 'href="/vrachi/"' in html
    assert "/uslugi/pomoshch-rodstvennikam/" not in html
    assert "/uslugi/diagnostika/" not in html
    assert "/uslugi/vosstanovitelnaya-terapiya/" not in html
    assert "Запись к специалисту" not in html
    assert "Виды оказываемых медицинских услуг" not in html
    assert "Лицензия и коды услуг" not in html
    assert "Наши лицензии и документы" not in html
    assert 'id="service-licenses-title"' in html
    assert 'id="guidelines-title"' in html
    assert "license-extract-page-1.png" in html
    assert "sanitary-conclusion" not in html
    assert "Цены на наши услуги" in html
    assert "4-местная палата" in html
    assert "prices-tab-stationary" in html
    assert "prices-tab-labs" in html
    assert "Анализ «Дионарк»" in html
    assert "Как проходит обращение" not in html
    assert "Отзывы о клинике «Нова»" in html
    assert "reviews-stats" in html
    assert "Л041-01137-77/01838787" in html
    assert "9715492100" in html.split("site-footer", 1)[-1]
    assert 'hero-header__meta-value">г. Москва, ул. Люблинская, д. 46' in html
    assert 'mobile-menu__detail">г. Москва, ул. Люблинская, д. 46' in html
    assert 'mailto:novaklinika111@yandex.ru' in html
    assert 'mailto:info@nova-clinic.ru' not in html
    assert "Профсоюзная" not in html


def test_narkolog_keeps_written_hero(client):
    response = client.get("/uslugi/narkolog-na-dom/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "<title>Вызов нарколога на дом в Москве — Нова</title>" in html
    assert "Вызов нарколога на дом в" in html
    assert "Москве и области" in html
    assert "Врач приедет на адрес" in html
    assert "Антипов Дмитрий Евгеньевич" in html
    assert "от 5&nbsp;000&nbsp;₽" in html


def test_service_pages_share_layout_blocks(client):
    urls = [
        "/uslugi/narkolog-na-dom/",
        "/uslugi/vyvod-iz-zapoya/na-domu/",
        "/uslugi/kodirovanie/",
        "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/",
        "/uslugi/narkologicheskaya-pomosh/",
    ]
    markers = (
        'id="service-price-title"',
        'id="service-payment-title"',
        'id="service-diff-title"',
        'id="service-reviews-title"',
        'id="service-doctors-title"',
        'id="service-licenses-title"',
        'id="guidelines-title"',
        'id="service-faq-title"',
        'id="service-request-title"',
        "service-legal",
        "article-credits",
    )
    field_service_urls = {
        "/uslugi/narkolog-na-dom/",
        "/uslugi/vyvod-iz-zapoya/na-domu/",
        "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/",
    }

    for url in urls:
        response = client.get(url)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        for marker in markers:
            assert marker in html, f"{marker} missing on {url}"
        if url in field_service_urls:
            assert 'id="field-service-title"' in html, f"field service missing on {url}"
        else:
            assert 'id="field-service-title"' not in html, f"field service should be absent on {url}"


def test_service_facility_on_clinic_and_hubs_not_on_home(client):
    with_facility = [
        "/uslugi/lechenie-alkogolizma/",
        "/uslugi/lechenie-alkogolizma/v-stacionare/",
        "/uslugi/kodirovanie/v-klinike/",
        "/uslugi/narkologicheskaya-pomosh/stacionar/",
        "/uslugi/narkologicheskaya-pomosh/",
        "/uslugi/psihiatriya/stacionar/",
    ]
    without_facility = [
        "/uslugi/narkolog-na-dom/",
        "/uslugi/vyvod-iz-zapoya/na-domu/",
        "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/",
        "/uslugi/reabilitaciya/",
        "/uslugi/psihiatriya/psihiatr-na-dom/",
    ]

    for url in with_facility:
        html = client.get(url).get_data(as_text=True)
        assert 'id="service-facility-title"' in html, f"facility missing on {url}"
        assert "Где будет находиться пациент" in html
        assert "Люблинская" in html
        assert 'id="field-service-title"' not in html, f"field service should be absent on {url}"

    for url in without_facility:
        html = client.get(url).get_data(as_text=True)
        assert 'id="service-facility-title"' not in html, f"facility should be absent on {url}"
        if url != "/uslugi/reabilitaciya/":
            assert 'id="field-service-title"' in html, f"field service missing on {url}"


def test_geo_pages_change_heading_and_keep_doctor(client):
    metro = client.get("/uslugi/narkolog-na-dom/aeroport/")
    city = client.get("/uslugi/narkolog-na-dom/moskovskaya-oblast/balashiha/")

    assert metro.status_code == 200
    assert city.status_code == 200
    metro_html = metro.get_data(as_text=True)
    city_html = city.get_data(as_text=True)
    assert "метро Аэропорт" in metro_html
    assert "Балашиха" in city_html
    assert "Антипов Дмитрий Евгеньевич" in metro_html
    assert "Антипов Дмитрий Евгеньевич" in city_html
    assert 'rel="canonical" href="http://localhost/uslugi/narkolog-na-dom/aeroport/"' in metro_html


def test_geo_hub_uses_v_moskovskoy_oblasti_wording(client):
    response = client.get("/uslugi/narkolog-na-dom/moskovskaya-oblast/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "<title>Нарколог на дом в Московской области — Нова</title>" in html
    assert "Нарколог на дом в" in html
    assert "Московской области" in html
    assert "Нарколог на дом — Московская область" not in html
    assert "Московская область" not in html.split("site-footer", 1)[0]

    catalog = get_catalog()
    for page in catalog.pages:
        if page["kind"] != "geo-hub":
            continue
        assert page["name"].endswith(" в Московской области")
        assert "— Московская область" not in page["name"]
        view = catalog.view(page["url"])
        assert view is not None
        assert view.h1_before.endswith(" в")
        assert view.h1_accent == "Московской области"


def test_removed_and_help_sections_are_missing(client):
    assert client.get("/uslugi/pomoshch-rodstvennikam/").status_code == 404
    assert client.get("/uslugi/diagnostika/").status_code == 404
    assert client.get("/uslugi/vosstanovitelnaya-terapiya/").status_code == 404
    assert client.get("/pomoshch/").status_code == 404
    assert client.get("/pomosh/").status_code == 404


def test_license_page(client):
    response = client.get("/licenziya/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "lp-head__title" in html
    assert "Лицензия" in html
    assert "Л041-01137-77/01838787" in html
    assert "ООО «НикаПроМЕД»" in html
    assert "9715492100" in html
    assert "1247700585186" in html
    assert "Люблинская" in html
    assert "Марьиной Рощи" in html
    assert "license-extract-page-1.png" in html
    assert "license-extract-page-3.png" in html
    assert "sanitary-conclusion" not in html
    assert "Вавилова" not in html
    assert "00918432" not in html
    assert "info-page__title" not in html
    assert "/assets/docs/license-L041-01137-77-01838787.pdf" in html


def test_about_clinic_page(client):
    response = client.get("/o-klinike/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "ca-hero__title" in html
    assert "О клинике" in html
    assert "Стационар и амбулаторный приём" in html
    assert "Анонимность и конфиденциальность" in html
    assert "Врачи с опытом стационарной работы" in html
    assert "Л041-01137-77/01838787" in html


def test_doctors_page(client):
    response = client.get("/vrachi/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "dp-head__title" in html
    assert "Наши врачи" in html
    assert "Антипов Дмитрий Евгеньевич" in html
    assert "Сычев Артемий Валерьевич" in html
    assert "Мищерекова Кристина Дмитриевна" in html
    assert "Поплевченков Константин Николаевич" in html
    assert "Доктор медицинских наук" in html
    assert "dp-card__avatar-icon" in html
    assert "/assets/icons/phosphor/" in html


def test_prices_page(client):
    response = client.get("/ceny/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "pp-head__title" in html
    assert "Цены" in html
    assert "pp-head__lead" not in html
    assert "pp-head__actions" not in html
    assert "pp-notes" not in html
    assert "Стационар" in html
    assert "4-местная палата" in html
    assert "от 12" in html
    assert "VIP-палата" in html
    assert "prices__service-icon-wrap" in html
    assert "Консультация психиатра" in html
    assert "Сосудистая терапия" in html
    assert "Анализы для госпитализации" in html
    assert "Информированное сопровождение" in html
    assert "Нова" in html


def test_faq_page(client):
    response = client.get("/voprosy/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "fq-head__title" in html
    assert "Частые вопросы" in html
    assert "Узнает ли работодатель" in html
    assert "Паспорт всё равно просят" in html
    assert "не хочет лечиться" in html
    assert "ограничивают телефон" in html
    assert "подростков" in html
    assert "Капельница на дому" in html
    assert "снова сорвался" in html
    assert "только поговорить" in html
    assert "Родственникам расскажете" in html
    assert "Когда звонить 103" in html
    assert '"@type": "FAQPage"' in html
    assert "Развёрнутые ответы на вопросы" not in html
    assert "info-page__title" not in html


def test_gallery_page(client):
    response = client.get("/galereya/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "gp-head__title" in html
    assert "Фотогалерея" in html
    assert "service-facility--page" in html
    assert "Общая палата" in html
    assert "Палата комфорт / VIP" in html
    assert "Осмотр и диагностика" in html
    assert "Санузел" in html
    assert "Общая зона" in html
    assert "/assets/images/service-facility/ward-shared.webp" in html
    assert "service-facility__facts" not in html
    assert "Здесь будет фотогалерея" not in html
    assert "info-page__title" not in html


def test_reviews_page(client):
    response = client.get("/otzyvy/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "rp-head__title" in html
    assert "Отзывы" in html
    assert "reviews--page" in html
    assert "reviews-stats" in html
    assert "Яндекс" in html
    assert "2ГИС" in html
    assert "Google" in html
    assert "data-reviews" in html
    assert "Здесь будет отдельная лента отзывов" not in html
    assert "info-page__title" not in html
    assert 'id="service-reviews-title"' not in html


def test_contacts_page(client):
    response = client.get("/kontakty/")
    html = response.get_data(as_text=True)
    main_html = html.split("site-footer", 1)[0]
    if 'id="top"' in main_html:
        main_html = main_html.split('id="top"', 1)[1]

    assert response.status_code == 200
    assert "cp-head__title" in html
    assert "Контакты" in html
    assert "+7 (495) 120-45-67" in main_html
    assert "tel:+74951204567" in main_html
    assert "novaklinika111@yandex.ru" in main_html
    assert "Люблинская" in main_html
    assert "Круглосуточно 24/7" in main_html
    assert "Телеграм" in main_html
    assert "Ватсап" in main_html
    assert "Макс" in main_html
    assert "ВКонтакте" in main_html
    assert "9715492100" in main_html
    assert "1247700585186" in main_html
    assert "Л041-01137-77/01838787" in main_html
    assert "Марьиной Рощи" in main_html
    assert "map-widget" in main_html
    assert "Профсоюзная" not in main_html
    assert "info-page__title" not in html


def test_remaining_site_pages(client):
    pages = {
        "/politika-konfidencialnosti/": "Политика конфиденциальности",
        "/soglasie/": "Согласие на обработку персональных данных",
    }

    for path, title in pages.items():
        response = client.get(path)
        assert response.status_code == 200
        assert f"<h1 class=\"info-page__title\">{title}</h1>" in response.get_data(as_text=True)

    for removed in ("/blog/", "/kejsy/", "/dogovor/", "/garantiya/"):
        assert client.get(removed).status_code == 404

    home = client.get("/").get_data(as_text=True)
    assert 'href="/ceny/"' in home
    assert 'href="/otzyvy/"' in home
    assert 'href="/kontakty/"' in home
    assert 'href="/o-klinike/"' in home
    assert 'href="/blog/"' not in home
    assert 'href="/kejsy/"' not in home
    assert 'href="/dogovor/"' not in home
    assert 'href="/garantiya/"' not in home
    assert 'href="/soglasie/"' in home
    assert 'href="/karta-sajta/"' in home
    assert "Карта сайта" in home
    assert home.index('href="/karta-sajta/"') < home.index("site-footer__legal")


def test_html_site_map_page(client):
    response = client.get("/karta-sajta/")
    html = response.get_data(as_text=True)
    main_html = html.split("site-footer", 1)[0]

    assert response.status_code == 200
    assert '<h1 class="sm-head__title">Карта сайта</h1>' in html
    assert "sm-jump" not in html
    assert "Все основные разделы" not in html
    assert "Каталог услуг" not in html
    assert 'href="/blog/"' not in html
    assert 'href="/kejsy/"' not in html
    assert 'href="/dogovor/"' not in html
    assert 'href="/garantiya/"' not in html
    assert 'href="/uslugi/narkologicheskaya-pomosh/"' in html
    assert 'href="/uslugi/narkolog-na-dom/moskovskaya-oblast/"' in html
    assert 'href="/uslugi/narkolog-na-dom/aeroport/"' in html
    assert 'href="/uslugi/lechenie-alkogolizma/moskovskaya-oblast/"' in html
    assert 'href="/vrachi/"' in main_html
    assert 'href="/ceny/"' in main_html
    assert 'href="/soglasie/"' in html
    assert "/assets/icons/heartbeat.svg" in html
    assert "sm-group" in html
    assert "sm-geo" in html


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
    assert "http://localhost/karta-sajta/" in body
    assert "pomoshch-rodstvennikam" not in body
    assert "/pomoshch/" not in body
    assert "/pomosh/" not in body
