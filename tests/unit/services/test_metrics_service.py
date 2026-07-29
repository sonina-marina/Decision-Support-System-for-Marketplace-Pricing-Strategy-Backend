from datetime import datetime
import pytest
from unittest.mock import AsyncMock

from src.db.models.metrics import Metrics
from src.db.models.product import Product
from src.schemas.metric import MetricsResult, ProductCalculationData
from src.schemas.metrics import MetricsView
from src.services.exceptions import MetricsNotFoundError, ProductNotFoundError
from src.services.metrics import MetricsService
from src.db.repositories.metrics import MetricsRepository
from src.db.repositories.product import ProductRepository

# --------- Fixture ---------

@pytest.fixture
def metrics_repo():
    return AsyncMock(spec=MetricsRepository)


@pytest.fixture
def product_repo():
    return AsyncMock(spec=ProductRepository)


@pytest.fixture
def service(metrics_repo, product_repo):
    return MetricsService(metrics_repo, product_repo)


@pytest.fixture
def metric():
    return Metrics(
        id=1,
        product_id=1,
        conversion=0.2,
        cac=10,
        required_cpa=2,
        ltc=100,
        cm=50,
        ltv=150,
        product_roi=0.35,
        calculated_at=datetime.now(),
    )


@pytest.fixture
def product():
    return Product(
        id=1,
        store_id=1,
        item_number=123456,
        name="Phone",
        category="Electronics",

        price=1000,
        cogs=600,
        commission=10,
        acquiring=2,
        tax=6,

        views=1000,
        target_actions=100,
        buyers=20,

        ad_costs=200,

        inbound_logistic=10,
        direct_logistic=15,
        reverse_logistic=5,

        return_rate=0.05,
        defect_rate=0.01,

        avg_storage=3,
        avg_packaging=2,

        sales=20,
    )


@pytest.fixture
def metrics_result():
    return MetricsResult(
        conversion=0.2,
        cac=10,
        required_cpa=2,
        ltc=100,
        cm=50,
        ltv=150,
        product_roi=50,
    )

# --------- create ---------


@pytest.mark.asyncio
async def test_calculate_metrics_success(
    service,
    product_repo,
    metrics_repo,
    product
):

    product_repo.get_full_product_by_id.return_value = product

    result = await service.calculate_metrics(product.id)

    metrics_repo.save.assert_called_once()

    assert result.conversion > 0
    assert result.cm > 0


@pytest.mark.asyncio
async def test_calculate_metrics_product_not_found(
    service,
    product_repo,
    metrics_repo,
):

    product_repo.get_full_product_by_id.return_value = None

    with pytest.raises(ProductNotFoundError):
        await service.calculate_metrics(1)

    metrics_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_calculate_metrics_for_custom_product(
    service,
    metrics_repo,
    product,
):

    result = await service.calculate_metrics_for_custom_product(
        ProductCalculationData.model_validate(product, from_attributes=True)    )

    metrics_repo.save.assert_called_once()

    assert isinstance(result, MetricsView)

    assert result.conversion > 0
    assert result.cac > 0
    assert result.cm > 0


# --------- get_by_id ---------

@pytest.mark.asyncio
async def test_get_by_id_success(
    service,
    metrics_repo,
    metric,
):

    metrics_repo.get_by_id.return_value = metric

    result = await service.get_by_id(metric.id)

    metrics_repo.get_by_id.assert_called_once_with(metric.id)

    assert result.id == metric.id
    assert result.cm == metric.cm


@pytest.mark.asyncio
async def test_get_by_id_not_found(
    service,
    metrics_repo,
):

    metrics_repo.get_by_id.return_value = None

    with pytest.raises(MetricsNotFoundError):
        await service.get_by_id(1)
