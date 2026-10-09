from flask import Blueprint, abort, render_template, request

from app.data.service_reviews import get_service_reviews
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
    return render_template(
        "pages/service.html",
        page=view,
        meta_title=view.meta_title,
        meta_description=view.meta_description,
        canonical=request.host_url.rstrip("/") + view.url,
        review_sources=get_service_reviews(),
    )
