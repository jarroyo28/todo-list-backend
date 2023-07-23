import pytest
from rest_framework.test import APIClient

from todo_list_backend.users.models import User
from todo_list_backend.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def unauthenticated_api_client(db):
    return APIClient()


@pytest.fixture
def authenticated_api_client(db, unauthenticated_api_client, user):
    unauthenticated_api_client.force_authenticate(user)
    return unauthenticated_api_client
