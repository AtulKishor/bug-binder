import time
from dataclasses import dataclass

import pytest
from django.contrib.auth.models import User

from tests.pages.login_page import LoginPage
from tests.pages.signup_page import SignupPage


@dataclass(frozen=True)
class AuthData:
    username: str
    email: str
    password: str

    def ensure_user_exists(self):
        if not User.objects.filter(username=self.username).exists():
            User.objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password,
            )


@pytest.fixture(scope="module")
def auth_data():
    # Shared credentials and persistence helpers for auth tests.
    return AuthData(
        username="test_user",
        email="test@example.com",
        password="test@123",
    )


@pytest.mark.django_db
def test_signup(page, live_server, auth_data):
    signup = SignupPage(page, live_server)
    signup.open()
    signup.signup(auth_data.username, auth_data.email, auth_data.password)

    if page.locator("#signup-error").is_visible():
        user_exists = User.objects.filter(username=auth_data.username).exists()
        assert user_exists, "Error message should be visible for existing username"
        return

    signup.fill_additional_details(
        "Test User dev1",
        "1234567890",
        "Test Organization",
        "pallavijainy",
        "Pallavi jany",
    )
    assert page.locator("#user-image").is_visible(), "User github profile should be visible after signing up and filling details"


@pytest.mark.django_db
def test_login(page, live_server, auth_data):
    # pytest-django rolls back DB changes after each test, so recreate test user if needed.
    auth_data.ensure_user_exists()

    login = LoginPage(page, live_server)
    login.open()
    login.login(auth_data.email, auth_data.password)

    assert page.get_by_role("heading", name="Dashboard").is_visible(), f"Login error: {page.locator('#login-error').text_content()}"


@pytest.mark.django_db
def test_logout(page, live_server, auth_data):
    # pytest-django rolls back DB changes after each test, so recreate test user if needed.
    auth_data.ensure_user_exists()

    page.goto(live_server.url)
    login = LoginPage(page, live_server)
    login.login(auth_data.email, auth_data.password)

    page.get_by_role("link", name="exit_to_app Logout").nth(1).click()

    assert (
        page.locator("#nav-mobile").get_by_role("link", name="Login account_box").is_visible()
    ), "Login screen should be visible after logging out"


# TODO: Add tests for forgot password and reset password functionality
