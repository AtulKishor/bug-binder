import pytest
from django.contrib.auth.models import User
from tests.pages.login_page import LoginPage
from tests.pages.project_page import ProjectPage

@pytest.mark.django_db
def test_create_project(page, live_server):

    User.objects.create_user(
        username="creator",
        password="pass123"
    )

    login = LoginPage(page, live_server)
    login.open()
    login.login("creator", "pass123")

    project = ProjectPage(page, live_server)
    project.open_create()
    project.create_project("Test Project", "Testing project")

    assert page.locator("text=Test Project").is_visible()
    
