import typo.repositories.user as user_repo
import pytest


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def register(client, username, email, password, confirm=""):
    if not confirm:
        confirm = password
    return client.post('/register', data=dict(
        username=username,
        email=email,
        password=password,
        confirm=password
    ), follow_redirects=True)


def test_login_if_user_dont_exist(client):
    resp = login(client, "test", "test")

    assert resp.status_code == 400
    assert "Invalid username or password." in resp.get_data(as_text=True)


def test_login_valid(client, application):
    with application.app_context():
        user_repo.create_user("test", "test@ema.il", "test")

    resp = login(client, "test", "test")
    assert resp.status_code == 200


def test_register_valid(client):
    resp = register(client, "test", "test@ema.il", "test")

    assert resp.status_code == 200


@pytest.mark.parametrize("args,expected_message", [
    (("duplicate", "unique@ema.il"), "Username &#34;duplicate&#34; is taken."),
    (("unique", "duplicate@ema.il"), "Email &#34;duplicate@ema.il&#34; is taken."),
], ids=["username", "email"])
def test_register_duplicate(client, application, args, expected_message):
    with application.app_context():
        user_repo.create_user("duplicate", "duplicate@ema.il", "password")

    resp = register(client, *args, password="password")
    assert resp.status_code == 400
    assert expected_message in resp.get_data(as_text=True)


@pytest.mark.parametrize("args", [
    pytest.param(
        ("", "", ""), id="empty-all"
    ),
    pytest.param(
        ("user", "user@email", ""), id="empty-password"
    ),
    pytest.param(
        ("user", "", "password"), id="empty-email"
    ),
    pytest.param(
        ("", "user@email", "passowrd"), id="empty-username"
    ),
    pytest.param(
        ("aa", "user@email", "short"), id="short-username"
    ),
    pytest.param(
        ("username", "e@ema.il", "password"), id="short-email"
    ),
    pytest.param(
        ("username", "user@email", ""), id="short-password"
    ),
    pytest.param(
        ("username", "useremail", "password"), id="invalid-email"
    ),
    pytest.param(
        ("user", "user@email", "password", "pass"), id="invalid-password-confirm"
    ),
])
def test_register_invalid_input(client, application, args, expected_message):
    with application.app_context():
        user_repo.create_user("test", "test@ema.il", "test")

    resp = login(client, "test", "test")
    assert resp.status_code == 200
    assert expected_message in resp.get_data(as_text=True)


def test_logout_if_user_dont_auth(client):
    resp = logout(client)

    assert resp.status_code == 200


def test_logout_if_user_auth(client, application):
    with application.app_context():
        user_repo.create_user("test", "test@ema.il", "test")

    login(client, "test", "test")

    resp = logout(client)

    assert resp.status_code == 200
