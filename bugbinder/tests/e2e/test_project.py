import pytest
from playwright.sync_api import expect
from tests.pages.login_page import LoginPage
from tests.pages.project_page import ProjectPage
from tests.pages.bug_page import BugPage

@pytest.mark.django_db
def test_create_project(page, live_server, project_creator):
    login = LoginPage(page, live_server)
    login.open()
    login.login(project_creator.username, project_creator.password)

    project = ProjectPage(page, live_server)
    project.create_project("Test Project", "Testing project")
    assert page.get_by_text("Test Project").is_visible()
    
    # create a bug in the project to verify project creation
    bug = BugPage(page, live_server)
    steps = ["Step 1: Do this", "Step 2: Do that"]
    bug.create_bug("Test Project", "Test Bug", steps=steps, 
                   comment="Testing bug creation. This is a test bug")
    expect(page.get_by_role("heading", name="Test Bug")).to_be_visible()
