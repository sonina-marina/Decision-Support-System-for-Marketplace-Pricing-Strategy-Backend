import pytest
from unittest.mock import AsyncMock

from src.main import app
from src.api.dependencies import get_store_service
from src.services.store import StoreService
from src.schemas.store import StoreView


@pytest.fixture
def store_service():
    service = AsyncMock(spec=StoreService)

    app.dependency_overrides[get_store_service] = lambda: service

    yield service

    app.dependency_overrides.pop(get_store_service, None)


# --------- create ---------

def test_create_store(client, store_service):

    store_service.create.return_value = StoreView(
        id=1,
        name="My Store",
        products=[],
    )

    response = client.post(
        "/api/v1/stores/",
        json={
            "userId": 1,
            "name": "My Store",
        },
    )

    assert response.status_code == 200

    store_service.create.assert_awaited_once()

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "My Store"


# --------- get_by_id ---------

def test_get_store_by_id(client, store_service):

    store_service.get_by_id.return_value = StoreView(
        id=1,
        name="My Store",
        products=[],
    )

    response = client.get("/api/v1/stores/?id=1")

    assert response.status_code == 200

    store_service.get_by_id.assert_awaited_once_with(1)

    assert response.json()["name"] == "My Store"


# --------- update ---------

def test_update_store(client, store_service):

    store_service.update.return_value = StoreView(
        id=1,
        name="New Store",
        products=[],
    )

    response = client.put(
        "/api/v1/stores/",
        json={
            "id": 1,
            "name": "New Store",
        },
    )

    assert response.status_code == 200

    store_service.update.assert_awaited_once()

    assert response.json()["name"] == "New Store"


# ---------- delete ----------

def test_delete_store(client, store_service):

    store_service.delete.return_value = None

    response = client.delete("/api/v1/stores/?id=1")

    assert response.status_code == 200

    store_service.delete.assert_awaited_once_with(1)
