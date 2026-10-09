from flask import Blueprint, abort, render_template, request

from app.data.clinic_contacts import get_clinic_contacts
from app.data.field_service import get_field_service_context
from app.data.service_credits import get_service_credits
from app.data.service_doctors import get_service_doctors
from app.data.service_faq import get_service_faq
from app.data.service_reviews import get_service_review_stats, get_service_reviews
from app.services.catalog import get_catalog, has_banned_segment, normalize_url

services_bp = Blueprint("services", __name__)


@services_bp.route("/uslugi/", defaults={"page_path": ""})
@services_bp.route("/uslugi/<path:page_path>/")
def page(page_path):
    url = "/uslugi/" if not page_path else normalize_url(f"/uslugi/{page_path}")
    if has_banned_segment(url):
        abort(404)
    view = get_catalog().view(url)
    if view is None:
        abort(404)
    field_service = None
    service_faq = None
    clinic_contacts = None
    service_credits = None
    if view.url.startswith("/uslugi/narkolog-na-dom"):
        field_service = get_field_service_context("/uslugi/narkolog-na-dom/")
        service_faq = get_service_faq()
        clinic_contacts = get_clinic_contacts()
        service_credits = get_service_credits()

    return render_template(
        "pages/service.html",
        page=view,
        meta_title=view.meta_title,
        meta_description=view.meta_description,
        canonical=request.host_url.rstrip("/") + view.url,
        review_sources=get_service_reviews(),
        review_stats=get_service_review_stats(),
        service_doctors=get_service_doctors(),
        field_service=field_service,
        service_faq=service_faq,
        clinic_contacts=clinic_contacts,
        service_credits=service_credits,
    )
