from datetime import datetime
import pytest
from unittest.mock import AsyncMock

from src.api.dependencies import get_metrics_service
from src.main import app
from src.schemas.metrics import MetricsList, MetricsView
from src.services.metrics import MetricsService


@pytest.fixture
def metrics_service():
    service = AsyncMock(spec=MetricsService)

    app.dependency_overrides[get_metrics_service] = lambda: service

    yield service

    app.dependency_overrides.pop(get_metrics_service, None)

    
# --------- calculete ---------

def test_calculate_metrics(client, metrics_service):

    metrics_service.calculate_metrics.return_value = MetricsView(
        id=1,
        conversion=0.1,
        cac=5,
        required_cpa=2,
        ltc=600,
        cm=400,
        ltv=480,
        product_roi=66.7,
        calculated_at=datetime.now(),
    )

    response = client.post(
        "/api/v1/metrics/",
        params={"id": 1},
    )

    assert response.status_code == 200

    metrics_service.calculate_metrics.assert_awaited_once_with(1)

    assert response.json()["cm"] == 400


def test_calculate_custom_metrics(client, metrics_service):

    metrics_service.calculate_metrics_for_custom_product.return_value = MetricsView(
        id=1,
        conversion=0.1,
        cac=5,
        required_cpa=2,
        ltc=600,
        cm=400,
        ltv=480,
        product_roi=66.7,
        calculated_at=datetime.now(),
    )

    response = client.post(
        "/api/v1/metrics/custom",
        json={
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

    metrics_service.calculate_metrics_for_custom_product.assert_awaited_once()

    assert response.json()["productRoi"] == 66.7


# --------- get_metrics_by_id ---------

def test_get_metrics_by_id(client, metrics_service):

    metrics_service.get_by_id.return_value = MetricsView(
        id=1,
        conversion=0.1,
        cac=5,
        required_cpa=2,
        ltc=600,
        cm=400,
        ltv=480,
        product_roi=66.7,
        calculated_at=datetime.now(),
    )

    response = client.get(
        "/api/v1/metrics/",
        params={"id": 1},
    )

    assert response.status_code == 200

    metrics_service.get_by_id.assert_awaited_once_with(1)

    assert response.json()["id"] == 1
    assert response.json()["ltv"] == 480


# --------- get_metrics_by_product_id ---------

def test_get_metrics_by_product_id(client, metrics_service):

    metrics_service.get_metrics_by_product_id.return_value = MetricsList(
        count=2,
        items=[
            MetricsView(
                id=1,
                conversion=0.10,
                cac=5,
                required_cpa=2,
                ltc=600,
                cm=400,
                ltv=480,
                product_roi=66.7,
                calculated_at=datetime.now(),
            ),
            MetricsView(
                id=2,
                conversion=0.12,
                cac=4.8,
                required_cpa=1.9,
                ltc=590,
                cm=410,
                ltv=500,
                product_roi=69.5,
                calculated_at=datetime.now(),
            ),
        ],
    )

    response = client.get(
        "/api/v1/metrics/by_product",
        params={"id": 1},
    )

    assert response.status_code == 200

    metrics_service.get_metrics_by_product_id.assert_awaited_once_with(1)

    data = response.json()

    assert data["count"] == 2
    assert len(data["items"]) == 2

    assert data["items"][0]["id"] == 1
    assert data["items"][0]["cm"] == 400

    assert data["items"][1]["id"] == 2
    assert data["items"][1]["productRoi"] == 69.5
