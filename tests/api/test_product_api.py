from datetime import datetime
import pytest
from unittest.mock import AsyncMock

from src.main import app
from src.api.dependencies import get_product_service
from src.schemas.metrics import MetricsView
from src.schemas.product import ProductDetailedView, ProductView
from src.services.product import ProductService


@pytest.fixture
def product_service():
    service = AsyncMock(spec=ProductService)

    app.dependency_overrides[get_product_service] = lambda: service

    yield service

    app.dependency_overrides.pop(get_product_service, None)


# --------- create ---------

def test_create_product(client, product_service):

    product_service.create.return_value = ProductView(
        id=1,
        item_number=123456,
        name="Phone",
        category="Electronics",
        price=1000.0,
    )

    response = client.post(
        "/api/v1/products/",
        json={
            "storeId": 1,
            "itemNumber": 123456,
            "name": "Phone",
            "category": "Electronics",
            "price": 1000,
            "cogs": 500,
            "commission": 10,
            "acquiring": 2,
            "tax": 6,
            "views": 1000,
            "targetActions": 100,
            "buyers": 50,
            "adCosts": 300,
            "inboundLogistic": 20,
            "directLogistic": 15,
            "reverseLogistic": 10,
            "returnRate": 0.05,
            "defectRate": 0.01,
            "avgStorage": 5,
            "avgPackaging": 3,
            "sales": 60,
        },
    )

    assert response.status_code == 200

    product_service.create.assert_awaited_once()

    data = response.json()

    assert data["id"] == 1
    assert data["itemNumber"] == 123456
    assert data["name"] == "Phone"


# --------- get_by_id ---------

def test_get_product_by_id(client, product_service):

    product_service.get_by_id.return_value = ProductView(
        id=1,
        item_number=123456,
        name="Phone",
        category="Electronics",
        price=1000,
    )

    response = client.get("/api/v1/products/?id=1")

    assert response.status_code == 200

    product_service.get_by_id.assert_awaited_once_with(1)

    assert response.json()["id"] == 1
    assert response.json()["name"] == "Phone"


# --------- update ---------

def test_update_product(client, product_service):

    product_service.update.return_value = ProductView(
        id=1,
        item_number=123456,
        name="Samsung",
        category="Electronics",
        price=1200,
    )

    response = client.put(
        "/api/v1/products/",
        json={
            "id": 1,
            "name": "Samsung",
            "category": "Electronics",
            "price": 1200,
            "cogs": 600,
            "commission": 10,
            "acquiring": 2,
            "tax": 6,
            "views": 1000,
            "targetActions": 100,
            "buyers": 50,
            "adCosts": 300,
            "inboundLogistic": 20,
            "directLogistic": 15,
            "reverseLogistic": 10,
            "returnRate": 0.05,
            "defectRate": 0.01,
            "avgStorage": 5,
            "avgPackaging": 3,
            "sales": 60,
        },
    )

    assert response.status_code == 200

    product_service.update.assert_awaited_once()

    assert response.json()["name"] == "Samsung"

# ---------- delete ----------

def test_delete_product(client, product_service):

    product_service.delete.return_value = None

    response = client.delete(
        "/api/v1/products/",
        params={"id": 1},
    )

    assert response.status_code == 200

    product_service.delete.assert_awaited_once_with(1)


# --------- product_with_metrics --------

def test_get_product_with_metrics(client, product_service):

    product_service.get_product_with_metric_by_id.return_value = ProductDetailedView(
        id=1,
        store_id=1,
        item_number=123456,
        name="iPhone",
        category="Electronics",
        price=1000,
        cogs=500,
        commission=10,
        acquiring=2,
        tax=6,
        views=1000,
        target_actions=100,
        buyers=50,
        ad_costs=300,
        inbound_logistic=20,
        direct_logistic=15,
        reverse_logistic=10,
        return_rate=0.05,
        defect_rate=0.01,
        avg_storage=5,
        avg_packaging=3,
        sales=60,
        metrics=[
            MetricsView(
                id=1,
                conversion=0.1,
                cac=6,
                required_cpa=3,
                ltc=650,
                cm=350,
                ltv=420,
                product_roi=53.8,
                calculated_at=datetime.now(),
            )
        ],
    )

    response = client.get(
        "/api/v1/products/metrics",
        params={"id": 1},
    )

    assert response.status_code == 200

    product_service.get_product_with_metric_by_id.assert_awaited_once_with(1)

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "iPhone"

    assert len(data["metrics"]) == 1

    assert data["metrics"][0]["conversion"] == 0.1
    assert data["metrics"][0]["cm"] == 350
