from flask import Blueprint, abort, render_template, request

from app.data.clinic_contacts import get_clinic_contacts
from app.data.doctors import get_doctor_by_slug
from app.data.field_service import get_field_service_context, resolve_field_service_base
from app.data.license import get_clinic_license
from app.data.service_credits import get_service_credits
from app.data.service_doctors import get_service_doctors
from app.data.prices import get_price_groups
from app.data.service_facility import (
    get_service_facility,
    should_show_field_service,
    should_show_service_facility,
)
from app.data.service_legal import get_service_legal
from app.data.service_reviews import get_service_review_stats, get_service_reviews
from app.services.catalog import get_catalog, has_banned_segment, normalize_url
from app.services.seo.presentation import price_groups_for

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

    show_facility = should_show_service_facility(view.url)
    facility = None
    if show_facility:
        facility = get_service_facility()
        if view.seo.facility_title:
            facility = {**facility, "title": view.seo.facility_title}

    return render_template(
        "pages/service.html",
        page=view,
        meta_title=view.meta_title,
        meta_description=view.meta_description,
        canonical=request.host_url.rstrip("/") + view.url,
        review_sources=get_service_reviews(),
        review_stats=get_service_review_stats(),
        service_doctors=get_service_doctors(),
        call_form_doctor=get_doctor_by_slug("antipov-dmitriy-evgenevich"),
        field_service=(
            get_field_service_context(resolve_field_service_base(view.url))
            if should_show_field_service(view.url)
            else None
        ),
        service_facility=facility,
        service_faq={
            "title": view.seo.faq_title,
            "questions": [{"ask": ask, "answer": answer} for ask, answer in view.seo.faq_items],
        },
        price_groups=get_price_groups(
            price_groups_for(view.seo.service_url, view.seo.presentation)
        ),
        clinic_contacts=get_clinic_contacts(),
        clinic_license=get_clinic_license(),
        service_legal=get_service_legal(),
        service_credits=get_service_credits(),
    )
