from dataclasses import dataclass

import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@dataclass(frozen=True)
class TestUserData:
    username: str
    email: str
    password: str


class SharedUsers:
    def __init__(self):
        self.test_user = TestUserData(
            username="test_user",
            email="test@example.com",
            password="test@123",
        )
        self.project_creator = TestUserData(
            username="creator_user",
            email="creator@example.com",
            password="pass123",
        )
        self.project_assignee = TestUserData(
            username="assignee_user",
            email="assignee@example.com",
            password="pass123",
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
        return user


@pytest.fixture(scope="session")
def shared_users():
    return SharedUsers()


@pytest.fixture(scope="session")
def session_project_users(django_db_setup, django_db_blocker, shared_users):
    with django_db_blocker.unblock():
        shared_users.ensure_exists(shared_users.project_creator)
        shared_users.ensure_exists(shared_users.project_assignee)
    return shared_users


@pytest.fixture
def test_user(shared_users):
    return shared_users.test_user


@pytest.fixture
def project_creator(session_project_users):
    return session_project_users.project_creator


@pytest.fixture
def project_assignee(session_project_users):
    return session_project_users.project_assignee


@pytest.fixture(autouse=True)
def clean_browser_context(context):
    context.clear_cookies()
    yield
