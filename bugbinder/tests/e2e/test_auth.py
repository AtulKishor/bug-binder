import time

import pytest
from django.contrib.auth.models import User

from tests.pages.login_page import LoginPage
from tests.pages.signup_page import SignupPage


@pytest.mark.django_db
def test_signup(page, live_server, test_user):
    signup = SignupPage(page, live_server)
    signup.open()
    signup.signup(test_user.username, test_user.email, test_user.password)

    if page.locator("#signup-error").is_visible():
        user_exists = User.objects.filter(username=test_user.username).exists()
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
def test_login(page, live_server, test_user, shared_users):
    # pytest-django rolls back DB changes after each test, so recreate test user if needed.
    shared_users.ensure_exists(test_user)

    login = LoginPage(page, live_server)
    login.open()
    login.login(test_user.email, test_user.password)

    assert page.get_by_role("heading", name="Dashboard").is_visible(), f"Login error: {page.locator('#login-error').text_content()}"


@pytest.mark.django_db
def test_logout(page, live_server, test_user, shared_users):
    # pytest-django rolls back DB changes after each test, so recreate test_user if needed.
    shared_users.ensure_exists(test_user)

    page.goto(live_server.url)
    login = LoginPage(page, live_server)
    login.login(test_user.email, test_user.password)

    page.get_by_role("link", name="exit_to_app Logout").nth(1).click()

    assert (
        page.locator("#nav-mobile").get_by_role("link", name="Login account_box").is_visible()
    ), "Login screen should be visible after logging out"


@pytest.mark.django_db
def test_reset_password(page, live_server, test_user, shared_users):
    # pytest-django rolls back DB changes after each test, so recreate test_user if needed.
    shared_users.ensure_exists(test_user)

    page.goto(live_server.url)
    login = LoginPage(page, live_server)
    login.login(test_user.email, test_user.password)
    login.reset_password(test_user.password, "test@1234")

    assert page.get_by_role("link", name="Change Password").is_visible(), "Change Password link should be visible after saving password"
    