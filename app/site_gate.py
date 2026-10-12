"""Site-wide password gate: HTML pages are not rendered until unlocked."""

from __future__ import annotations

import secrets
from urllib.parse import urlparse

from flask import (
    current_app,
    redirect,
    request,
    session,
    url_for,
)

SESSION_UNLOCK_KEY = "site_access_ok"
SESSION_CSRF_KEY = "site_gate_csrf"
EXEMPT_ENDPOINTS = frozenset({"static", "main.site_login"})


def is_site_unlocked() -> bool:
    return bool(session.get(SESSION_UNLOCK_KEY))


def unlock_site() -> None:
    session[SESSION_UNLOCK_KEY] = True
    session.permanent = True


def gate_csrf_token() -> str:
    token = session.get(SESSION_CSRF_KEY)
    if not token:
        token = secrets.token_hex(16)
        session[SESSION_CSRF_KEY] = token
    return token


def validate_gate_csrf(token: str | None) -> bool:
    expected = session.get(SESSION_CSRF_KEY)
    if not expected or not token:
        return False
    return secrets.compare_digest(expected, token)


def safe_next_url(raw: str | None) -> str:
    if not raw:
        return "/"
    parsed = urlparse(raw)
    if parsed.scheme or parsed.netloc:
        return "/"
    if not raw.startswith("/") or raw.startswith("//"):
        return "/"
    return raw


def password_matches(candidate: str) -> bool:
    expected = current_app.config.get("SITE_ACCESS_PASSWORD") or ""
    if not expected:
        return False
    return secrets.compare_digest(candidate, expected)


def _request_next_path() -> str:
    path = request.full_path
    if path.endswith("?"):
        path = path[:-1]
    return path or "/"


def register_site_gate(app):
    @app.before_request
    def require_site_password():
        if app.config.get("TESTING"):
            return None
        if not app.config.get("SITE_PASSWORD_PROTECT", True):
            return None
        if request.endpoint in EXEMPT_ENDPOINTS:
            return None
        if is_site_unlocked():
            return None
        return redirect(url_for("main.site_login", next=_request_next_path()))
