import pytest

from fastapi.testclient import TestClient

from src.core.auth.dependencies import get_current_user
from src.enums import UserRole
from src.main import app


@pytest.fixture
def fake_user():
    return {
        "id": 1,
        "email": "admin@mail.com",
        "role": UserRole.SELLER,
    }


@pytest.fixture(autouse=True)
def override_auth(fake_user):

    app.dependency_overrides[get_current_user] = lambda: fake_user

    yield

    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
