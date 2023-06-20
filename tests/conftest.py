import pytest
from rest_framework.test import APIClient

from tests.users.factories import UserFactory


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture
def active_user():
    return UserFactory()


@pytest.fixture
def admin_user():
    return UserFactory(is_superuser=True)
