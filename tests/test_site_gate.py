from app import create_app


def _client(*, protect: bool = True, testing: bool = False):
    app = create_app()
    app.config["TESTING"] = testing
    app.config["SITE_PASSWORD_PROTECT"] = protect
    app.config["SITE_ACCESS_PASSWORD"] = "nova-clinic-test"
    app.config["SECRET_KEY"] = "test-secret"
    return app.test_client()


def test_protected_page_does_not_leak_html_content():
    client = _client(protect=True, testing=False)
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 302
    assert "/login/" in response.headers["Location"]

    login_page = client.get("/login/")
    html = login_page.get_data(as_text=True)

    assert login_page.status_code == 200
    assert "Закрытый доступ" in html
    assert "Психонаркологическая клиника — Нова" not in html
    assert "Наши услуги" not in html
    assert "site-footer" not in html
    assert 'name="robots" content="noindex, nofollow"' in html


def test_wrong_password_keeps_content_locked():
    client = _client(protect=True, testing=False)
    login_page = client.get("/login/")
    csrf = _extract_csrf(login_page.get_data(as_text=True))

    response = client.post(
        "/login/",
        data={"password": "wrong", "csrf_token": csrf, "next": "/"},
        follow_redirects=False,
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Неверный пароль" in html

    blocked = client.get("/", follow_redirects=False)
    assert blocked.status_code == 302
    assert "/login/" in blocked.headers["Location"]


def test_correct_password_unlocks_html():
    client = _client(protect=True, testing=False)
    login_page = client.get("/login/")
    csrf = _extract_csrf(login_page.get_data(as_text=True))

    unlock = client.post(
        "/login/",
        data={"password": "nova-clinic-test", "csrf_token": csrf, "next": "/"},
        follow_redirects=False,
    )
    assert unlock.status_code == 302
    assert unlock.headers["Location"].endswith("/")

    home = client.get("/")
    html = home.get_data(as_text=True)

    assert home.status_code == 200
    assert "Психонаркологическая клиника — Нова" in html
    assert "Наши услуги" in html


def test_testing_mode_bypasses_gate():
    client = _client(protect=True, testing=True)
    response = client.get("/")

    assert response.status_code == 200
    assert "Психонаркологическая клиника — Нова" in response.get_data(as_text=True)


def test_open_redirect_is_blocked():
    client = _client(protect=True, testing=False)
    login_page = client.get("/login/")
    csrf = _extract_csrf(login_page.get_data(as_text=True))

    unlock = client.post(
        "/login/",
        data={
            "password": "nova-clinic-test",
            "csrf_token": csrf,
            "next": "https://evil.example/",
        },
        follow_redirects=False,
    )

    assert unlock.status_code == 302
    assert unlock.headers["Location"].endswith("/")


def _extract_csrf(html: str) -> str:
    marker = 'name="csrf_token" value="'
    start = html.index(marker) + len(marker)
    end = html.index('"', start)
    return html[start:end]
