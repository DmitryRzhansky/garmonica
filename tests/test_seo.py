import pytest

from app import create_app
from app.services.catalog import get_catalog
from app.services.seo.geo_forms import CITY_LOCATIVE
from app.services.seo.phrases import PHRASES
from app.services.seo.presentation import price_groups_for, price_tab_for

BANNED = ("аноним", "круглосуточ", "₽", "30–60", "8 000", "12 000", "5 000", "24/7", "полная аноним")


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_every_page_has_distinct_title_and_h1_and_ten_faq():
    catalog = get_catalog()
    titles = []
    for page in catalog.pages:
        seo = catalog.view(page["url"]).seo
        assert seo.service_url in PHRASES
        assert seo.meta_title and seo.meta_description and seo.h1 and seo.lead
        assert seo.meta_title != seo.h1
        assert seo.meta_description != seo.lead
        assert "Текст страницы будет дополнен" not in seo.meta_description
        assert len(seo.faq_items) == 10
        asks = [ask for ask, _ in seo.faq_items]
        assert len(set(asks)) == 10
        assert all(ask.strip() and answer.strip() for ask, answer in seo.faq_items)
        for word in BANNED:
            assert word not in seo.meta_description
            assert word not in seo.lead
        assert "анонимно" not in seo.h1
        assert "₽" not in seo.h1
        titles.append(seo.meta_title)
        if page["kind"] == "city":
            assert seo.h1_accent == CITY_LOCATIVE[page["geo_name"]]
    assert len(titles) == len(set(titles)) == 1501


def test_home_city_and_psych_titles():
    catalog = get_catalog()
    himki = catalog.view("/uslugi/narkolog-na-dom/moskovskaya-oblast/himki/").seo
    assert himki.h1 == "Нарколог на дом в Химках"
    assert himki.meta_title == "Нарколог на дом в Химках — анонимно, выезд 30–60 минут, от 8 000 ₽"
    accents = {
        page["geo_name"]: catalog.view(page["url"]).seo.h1_accent
        for page in catalog.pages
        if page["url"].startswith("/uslugi/narkolog-na-dom/moskovskaya-oblast/")
        and page["geo_name"] in {"Люберцы", "Щёлково", "Химки"}
    }
    assert accents["Люберцы"] == "Люберцах"
    assert accents["Щёлково"] == "Щёлкове"
    assert accents["Химки"] == "Химках"
    depression = catalog.view("/uslugi/psihiatriya/rasstrojstva-nastroeniya/depressiya/").seo
    assert depression.meta_title == "Помощь при депрессии — анонимно, приём в клинике, 8 000 ₽"
    anorexia = catalog.view("/uslugi/psihiatriya/rasstrojstva-pishchevogo-povedeniya/anoreksiya/").seo
    assert anorexia.h1 == "Лечение нервной анорексии"
    assert "капельниц" not in depression.lead.lower()
    assert "выезд нарколога" not in depression.meta_description.lower()
    coding = catalog.view("/uslugi/kodirovanie/").seo
    assert "запой" not in coding.meta_title.lower()
    assert "не выводит из запоя" in coding.meta_description or "не заменяет" in coding.meta_description
    rehab = catalog.view("/uslugi/reabilitaciya/alkogolizm/").seo
    assert "партн" not in rehab.meta_title.lower()
    assert "партн" not in rehab.meta_description.lower()


def test_cluster_blocks_render(client):
    depression = client.get("/uslugi/psihiatriya/rasstrojstva-nastroeniya/depressiya/")
    html = depression.get_data(as_text=True)
    assert depression.status_code == 200
    assert 'id="service-facility-title"' in html
    assert "Клиника на Люблинской, 46" in html
    assert 'id="field-service-title"' not in html
    assert "Записаться на приём" in html
    assert "Вызвать врача на дом" not in html
    assert "Бригада в вашем районе" not in html
    assert "Стоимость выезда" not in html
    assert html.count("<h1") == 1

    psychologist = client.get("/uslugi/psihoterapiya-i-psihologiya/psiholog/")
    psych_html = psychologist.get_data(as_text=True)
    assert 'id="service-facility-title"' in psych_html
    assert 'id="field-service-title"' not in psych_html
    assert "Записаться на приём" in psych_html

    home = client.get("/uslugi/psihiatriya/psihiatr-na-dom/")
    home_html = home.get_data(as_text=True)
    assert 'id="field-service-title"' in home_html
    assert 'id="service-facility-title"' not in home_html
    assert "Вызвать врача на дом" in home_html

    rehab = client.get("/uslugi/reabilitaciya/")
    rehab_html = rehab.get_data(as_text=True)
    assert 'id="field-service-title"' not in rehab_html
    assert 'id="service-facility-title"' not in rehab_html
    assert "партнёрск" not in rehab_html.lower()
    assert "партнерск" not in rehab_html.lower()

    inpatient = client.get("/uslugi/vyvod-iz-zapoya/v-stacionare/")
    inpatient_html = inpatient.get_data(as_text=True)
    assert "Где будет находиться пациент" in inpatient_html
    assert "Заявка на госпитализацию" in inpatient_html
    inpatient_seo = get_catalog().view("/uslugi/vyvod-iz-zapoya/v-stacionare/").seo
    assert "капельниц" not in inpatient_seo.lead.lower()
    assert "на дом" not in inpatient_seo.meta_description.lower()


def test_price_groups_for_clusters():
    assert price_groups_for("/uslugi/narkolog-na-dom/", "home") == (
        "consultations",
        "procedures",
    )
    assert price_tab_for("/uslugi/narkolog-na-dom/", "home") == "consultations"
    assert price_groups_for("/uslugi/kapelnitsy/", "home") == (
        "procedures",
        "consultations",
    )
    assert price_tab_for("/uslugi/kapelnitsy/", "home") == "procedures"
    assert price_groups_for("/uslugi/lechenie-alkogolizma/v-stacionare/", "inpatient") == (
        "stationary",
        "consultations",
        "labs",
        "support",
    )
    assert price_tab_for("/uslugi/lechenie-alkogolizma/v-stacionare/", "inpatient") == "stationary"
    assert price_groups_for("/uslugi/kodirovanie/", "coding") == ("consultations",)
    assert price_groups_for("/uslugi/", "catalog") == (
        "stationary",
        "consultations",
        "procedures",
        "labs",
        "support",
    )


def test_sample_pages_return_200(client):
    catalog = get_catalog()
    urls = [
        "/uslugi/",
        "/uslugi/narkolog-na-dom/aeroport/",
        "/uslugi/narkolog-na-dom/cao/",
        "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/",
        "/uslugi/kodirovanie/metod-dovzhenko/",
        "/uslugi/psihiatriya/stacionar/",
        "/uslugi/lechenie-narkomanii/mefedron/",
        "/uslugi/reabilitaciya/moskovskaya-oblast/",
    ]
    for url in urls:
        response = client.get(url)
        assert response.status_code == 200, url
        html = response.get_data(as_text=True)
        assert html.count("<h1") == 1
        assert "FAQPage" in html
        assert html.count('"@type": "Question"') == 10
    assert len(catalog.pages) == 1501
