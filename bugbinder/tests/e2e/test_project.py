import pytest
from playwright.sync_api import expect
from tests.pages.login_page import LoginPage
from tests.pages.project_page import ProjectPage
from tests.pages.bug_page import BugPage

@pytest.mark.django_db
def test_create_project(page, live_server, test_user, project_creator, project_assignee):
    login = LoginPage(page, live_server)
    login.open()
    login.login(project_creator.username, project_creator.password)

    project = ProjectPage(page, live_server)
    project.create_project("Test Project", "Testing project")
    assert page.get_by_text("Test Project").is_visible()

    # add test_user and project_assignee as a member of the project
    project.add_member(test_user.username)
    project.add_member(project_assignee.username)


@pytest.mark.django_db
def test_create_and_assign_bug(page, live_server, test_user, project_creator, project_assignee, seeded_project):
    login = LoginPage(page, live_server)
    login.open()
    login.login(test_user.username, test_user.password)

    # create a bug in the project to verify project creation
    bug = BugPage(page, live_server)
    steps = ["Step 1: Do this", "Step 2: Do that"]
    bug.create_bug(seeded_project.title, "Test Bug", steps=steps, env="Testing Environment",
                   comment="Testing bug creation. This is a test bug")
    expect(page.get_by_role("heading", name="Test Bug")).to_be_visible()

    # assignment to another user must be done by the project owner
    page.get_by_role("link", name="exit_to_app Logout").nth(1).click()
    login.open()
    login.login(project_creator.username, project_creator.password)
    page.goto(f"{live_server.url}/project/{seeded_project.id}")

    # assign the bug to the assignee user
    bug.assign_bug(project_assignee.username)
    expect(page.locator(f"a[href='/u/{project_assignee.username}']").first).to_be_visible()
    

@pytest.mark.django_db
def test_solve_bug(page, live_server, project_assignee, seeded_assigned_bug):
    login = LoginPage(page, live_server)
    login.open()
    login.login(project_assignee.username, project_assignee.password)

    bug = BugPage(page, live_server)
    bug.solve_bug(message="This is a solution for the bug")
    expect(page.get_by_text(f"Submitted by {project_assignee.username}")).to_be_visible()
