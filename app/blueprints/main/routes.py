from flask import Blueprint, Response, render_template, request

from app.data.clinic_contacts import get_clinic_contacts
from app.services.catalog import get_catalog
from app.services.info_pages import INFO_PAGES

main_bp = Blueprint("main", __name__)

HOME_TITLE = "Нова клиник — наркологическая клиника | Помощь 24/7"
HOME_DESCRIPTION = (
    "Наркологическая клиника «Нова клиник»: вызов врача на дом, детоксикация, "
    "стационар и сопровождение восстановления. Круглосуточно, конфиденциально, "
    "с понятной стоимостью до начала помощи."
)


@main_bp.route("/")
def home():
    return render_template(
        "pages/home.html",
        meta_title=HOME_TITLE,
        meta_description=HOME_DESCRIPTION,
        canonical=_canonical("/"),
    )


@main_bp.route("/<slug>/")
def info_page(slug):
    page = INFO_PAGES.get(slug)
    if page is None:
        return render_template(
            "errors/404.html",
            meta_title="Страница не найдена — Нова клиник",
            meta_description="Запрошенной страницы нет на сайте Нова клиник.",
            canonical=None,
        ), 404

    meta_title = f"{page['title']} — Нова клиник"
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

    return render_template(
        "pages/info.html",
        page=page,
        meta_title=meta_title,
        meta_description=meta_description,
        canonical=canonical,
    )


@main_bp.route("/sitemap.xml")
def sitemap():
    urls = ["/"] + [f"/{slug}/" for slug in INFO_PAGES] + get_catalog().public_urls()
    host = request.host_url.rstrip("/")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{host}{path}</loc>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return Response("\n".join(lines) + "\n", mimetype="application/xml")


def _canonical(path: str) -> str:
    return request.host_url.rstrip("/") + path
