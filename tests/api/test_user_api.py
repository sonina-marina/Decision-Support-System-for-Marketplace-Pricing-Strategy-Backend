import pytest
from unittest.mock import AsyncMock

from src.enums import UserRole
from src.main import app
from src.api.dependencies import get_user_service
from src.schemas.user import UserView
from src.services.exceptions import ForbiddenError
from src.services.user import UserService


@pytest.fixture
def user_service():
    service = AsyncMock(spec=UserService)

    app.dependency_overrides[get_user_service] = lambda: service

    yield service

    app.dependency_overrides.pop(get_user_service, None)


# --------- create ---------

def test_create_user(client, user_service):

    user_service.create.return_value = UserView(
        id=1,
        email="john@mail.com",
        fullname="John",
        role=UserRole.SELLER,
    )

    response = client.post(
        "/api/v1/users/",
        json={
            "email": "john@mail.com",
            "fullname": "John",
            "password": "password",
            "role": "SELLER",
        },
    )

    assert response.status_code == 200

    user_service.create.assert_awaited_once()

    assert response.json()["id"] == 1
    assert response.json()["email"] == "john@mail.com"


# --------- get_by_id ---------

def test_get_user_by_id(client, user_service):

    user_service.get_by_id.return_value = UserView(
        id=1,
        email="john@mail.com",
        fullname="John",
        role=UserRole.SELLER,
    )

    response = client.get("/api/v1/users/?id=1")

    assert response.status_code == 200

    user_service.get_by_id.assert_awaited_once_with(1)

    data = response.json()

    assert data["id"] == 1
    assert data["email"] == "john@mail.com"
    assert data["fullname"] == "John"


# --------- update ---------

def test_update_fullname(client, user_service):

    user_service.change_fullname.return_value = UserView(
        id=1,
        email="john@mail.com",
        fullname="New Name",
        role=UserRole.SELLER,
    )

    response = client.put(
        "/api/v1/users/update_fullname",
        json={
            "id": 1,
            "newFullname": "New Name",
        },
    )

    assert response.status_code == 200

    user_service.change_fullname.assert_awaited_once()

    data = response.json()

    assert data["fullname"] == "New Name"


# ---------- delete ----------

def test_delete_user(client, user_service):

    with pytest.raises(ForbiddenError):
        client.delete("/api/v1/users/?id=1")

    user_service.delete.assert_not_called()
