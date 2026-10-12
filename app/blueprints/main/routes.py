from flask import Blueprint, Response, current_app, redirect, render_template, request

from app.data.clinic_contacts import get_clinic_contacts
from app.data.doctors import get_clinic_doctors
from app.data.faq_answerer import get_faq_answerer
from app.data.faq_page import get_faq_page
from app.data.field_service import get_field_service_context
from app.data.gallery_page import get_gallery_page
from app.data.home_services import get_home_service_hubs
from app.data.legal_pages import get_consent_page, get_privacy_policy_page
from app.data.license import get_clinic_license
from app.data.prices import get_price_groups
from app.data.service_doctors import get_service_doctors
from app.data.service_reviews import get_service_review_stats, get_service_reviews
from app.services.catalog import all_public_urls
from app.services.info_pages import INFO_PAGES
from app.services.site_map import get_site_map
from app.site_gate import (
    gate_csrf_token,
    is_site_unlocked,
    password_matches,
    safe_next_url,
    unlock_site,
    validate_gate_csrf,
)

main_bp = Blueprint("main", __name__)

HOME_TITLE = "Нова — клиника психиатрии и наркологии | Помощь 24/7"
HOME_DESCRIPTION = (
    "Клиника психиатрии и наркологии «Нова»: вызов врача на дом, детоксикация, "
    "стационар и сопровождение восстановления. Круглосуточно, конфиденциально, "
    "с понятной стоимостью до начала помощи."
)


@main_bp.route("/login/", methods=["GET", "POST"])
def site_login():
    next_url = safe_next_url(request.values.get("next"))

    if current_app.config.get("TESTING") or not current_app.config.get(
        "SITE_PASSWORD_PROTECT", True
    ):
        return redirect(next_url)

    if is_site_unlocked():
        return redirect(next_url)

    error = None
    if request.method == "POST":
        if not validate_gate_csrf(request.form.get("csrf_token")):
            error = "Сессия устарела. Обновите страницу и попробуйте снова."
        elif password_matches(request.form.get("password") or ""):
            unlock_site()
            return redirect(next_url)
        else:
            error = "Неверный пароль"

    return render_template(
        "pages/site-gate.html",
        error=error,
        next_url=next_url,
        csrf_token=gate_csrf_token(),
        meta_title="Вход — Нова",
        meta_description="Закрытый доступ к тестовой версии сайта клиники Нова.",
    )


@main_bp.route("/")
def home():
    return render_template(
        "pages/home.html",
        meta_title=HOME_TITLE,
        meta_description=HOME_DESCRIPTION,
        canonical=_canonical("/"),
        clinic_license=get_clinic_license(),
        home_service_hubs=get_home_service_hubs(),
        service_doctors=get_service_doctors(),
        field_service=get_field_service_context(),
        price_groups=get_price_groups(),
        review_sources=get_service_reviews(),
        review_stats=get_service_review_stats(),
        faq_answerer=get_faq_answerer(),
    )


@main_bp.route("/<slug>/")
def info_page(slug):
    page = INFO_PAGES.get(slug)
    if page is None:
        return render_template(
            "errors/404.html",
            meta_title="Страница не найдена — Нова",
            meta_description="Запрошенной страницы нет на сайте Нова.",
            canonical=None,
        ), 404

    meta_title = f"{page['title']} — Нова"
    meta_description = page["description"]
    canonical = _canonical(f"/{slug}/")

    if slug == "o-klinike":
        return render_template(
            "pages/about-clinic.html",
            page=page,
            clinic_contacts=get_clinic_contacts(),
            meta_title=meta_title,
            meta_description=meta_description,
            canonical=canonical,
        )

    if slug == "vrachi":
        return render_template(
            "pages/doctors.html",
            page=page,
            doctors=get_clinic_doctors(),
            clinic_contacts=get_clinic_contacts(),
            meta_title=meta_title,
            meta_description=meta_description,
            canonical=canonical,
        )

    if slug == "ceny":
        return render_template(
            "pages/prices.html",
            page=page,
            price_groups=get_price_groups(),
            clinic_contacts=get_clinic_contacts(),
            meta_title=meta_title,
            meta_description=meta_description,
            canonical=canonical,
        )

    if slug == "karta-sajta":
        return render_template(
            "pages/site-map.html",
            page=page,
            site_map=get_site_map(),
            meta_title=meta_title,
            meta_description=meta_description,
            canonical=canonical,
        )

    if slug == "voprosy":
        return render_template(
            "pages/faq.html",
            page=page,
            faq_page=get_faq_page(),
            faq_answerer=get_faq_answerer(),
            clinic_contacts=get_clinic_contacts(),
            meta_title=meta_title,
            meta_description=meta_description,
            canonical=canonical,
        )

    if slug == "galereya":
        return render_template(
            "pages/gallery.html",
            page=page,
            gallery_page=get_gallery_page(),
            clinic_contacts=get_clinic_contacts(),
            meta_title=meta_title,
            meta_description=meta_description,
            canonical=canonical,
        )

    if slug == "licenziya":
        return render_template(
            "pages/license.html",
            page=page,
            clinic_license=get_clinic_license(),
            clinic_contacts=get_clinic_contacts(),
            meta_title=meta_title,
            meta_description=meta_description,
            canonical=canonical,
        )

    if slug == "otzyvy":
        return render_template(
            "pages/reviews.html",
            page=page,
            review_sources=get_service_reviews(),
            review_stats=get_service_review_stats(),
            clinic_contacts=get_clinic_contacts(),
            meta_title=meta_title,
            meta_description=meta_description,
            canonical=canonical,
        )

    if slug == "kontakty":
        return render_template(
            "pages/contacts.html",
            page=page,
            clinic_contacts=get_clinic_contacts(),
            meta_title=meta_title,
            meta_description=meta_description,
            canonical=canonical,
        )

    if slug == "politika-konfidencialnosti":
        legal_page = get_privacy_policy_page()
        return render_template(
            "pages/legal.html",
            page=legal_page,
            meta_title=f"{legal_page['title']} — Нова",
            meta_description=legal_page["description"],
            canonical=canonical,
        )

    if slug == "soglasie":
        legal_page = get_consent_page()
        return render_template(
            "pages/legal.html",
            page=legal_page,
            meta_title=f"{legal_page['title']} — Нова",
            meta_description=legal_page["description"],
            canonical=canonical,
        )

    return render_template(
        "pages/info.html",
        page=page,
        meta_title=meta_title,
        meta_description=meta_description,
        canonical=canonical,
    )


@main_bp.route("/sitemap.xml")
def sitemap():
    host = request.host_url.rstrip("/")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in all_public_urls():
        lines.append("  <url>")
        lines.append(f"    <loc>{host}{path}</loc>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return Response("\n".join(lines) + "\n", mimetype="application/xml")


@main_bp.route("/robots.txt")
def robots():
    host = request.host_url.rstrip("/")
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {host}/sitemap.xml\n"
    )
    return Response(body, mimetype="text/plain")


def _canonical(path: str) -> str:
    return request.host_url.rstrip("/") + path
