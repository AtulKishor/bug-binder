from dataclasses import dataclass
from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from _profile.models import Profile
from core.models import Project, Task


User = get_user_model()


@dataclass(frozen=True)
class TestUserData:
    username: str
    email: str
    password: str
    name: str
    mobile: str
    office: str
    github: str
    linkedin: str


class SharedUsers:
    def __init__(self):
        self.test_user = TestUserData(
            username="test_user",
            email="test@example.com",
            password="test@123",
            name="Test User",
            mobile="9999999991",
            office="QA",
            github="test-user",
            linkedin="test-user-ln",
        )
        self.project_creator = TestUserData(
            username="creator_user",
            email="creator@example.com",
            password="pass123",
            name="Project Creator",
            mobile="9999999992",
            office="Engineering",
            github="creator-user",
            linkedin="creator-user-ln",
        )
        self.project_assignee = TestUserData(
            username="assignee_user",
            email="assignee@example.com",
            password="pass123",
            name="Project Assignee",
            mobile="9999999993",
            office="Engineering",
            github="assignee-user",
            linkedin="assignee-user-ln",
        )

    def ensure_exists(self, user_data: TestUserData):
        user, created = User.objects.get_or_create(
            username=user_data.username,
            defaults={"email": user_data.email},
        )
        if created or not user.check_password(user_data.password) or user.email != user_data.email:
            user.email = user_data.email
            user.set_password(user_data.password)
            user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.name = user_data.name
        profile.mobile = user_data.mobile
        profile.office = user_data.office
        profile.github = user_data.github
        profile.linkedin = user_data.linkedin
        profile.save()
        return user


@pytest.fixture(scope="session")
def shared_users():
    return SharedUsers()


@pytest.fixture(scope="session")
def session_project_users(django_db_setup, django_db_blocker, shared_users):
    with django_db_blocker.unblock():
        shared_users.ensure_exists(shared_users.test_user)
        shared_users.ensure_exists(shared_users.project_creator)
        shared_users.ensure_exists(shared_users.project_assignee)
    return shared_users


@pytest.fixture(autouse=True)
def ensure_shared_users(request, db, shared_users):
    if request.node.get_closest_marker("django_db") is None:
        return
    shared_users.ensure_exists(shared_users.test_user)
    shared_users.ensure_exists(shared_users.project_creator)
    shared_users.ensure_exists(shared_users.project_assignee)


@pytest.fixture
def test_user(shared_users):
    return shared_users.test_user


@pytest.fixture
def project_creator(session_project_users):
    return session_project_users.project_creator


@pytest.fixture
def project_assignee(session_project_users):
    return session_project_users.project_assignee


@pytest.fixture
def seeded_project(db, shared_users):
    creator = shared_users.ensure_exists(shared_users.project_creator)
    reporter = shared_users.ensure_exists(shared_users.test_user)
    assignee = shared_users.ensure_exists(shared_users.project_assignee)

    project_title = f"Test Project {uuid4().hex[:8]}"
    project, _ = Project.objects.get_or_create(
        owner=creator,
        title=project_title,
        defaults={"description": "Testing project"},
    )
    project.description = "Testing project"
    project.save()
    project.dev.add(creator, reporter, assignee)
    return project


@pytest.fixture
def seeded_assigned_bug(db, shared_users, seeded_project):
    assignee = shared_users.ensure_exists(shared_users.project_assignee)
    task = Task.objects.create(
        title="Seeded Assigned Bug",
        reproduce="Step 1: Open app\nStep 2: Trigger issue",
        environment="Testing Environment",
        comment="Seeded bug for solve flow",
        project=seeded_project,
        dev=assignee,
        assigned=True,
        done=False,
    )
    seeded_project.task.add(task)
    seeded_project.bugs = 0
    seeded_project.assigned = 1
    seeded_project.fixed = 0
    seeded_project.save()
    return task


@pytest.fixture(autouse=True)
def clean_browser_context(context):
    context.clear_cookies()
    yield
