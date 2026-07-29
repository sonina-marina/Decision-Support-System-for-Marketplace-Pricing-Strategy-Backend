from datetime import datetime
import pytest
from unittest.mock import AsyncMock

from src.db.models.metrics import Metrics
from src.db.models.product import Product
from src.db.repositories.metrics import MetricsRepository
from src.db.repositories.product import ProductRepository
from src.schemas.product import ProductCreate, ProductUpdate
from src.services.exceptions import ProductAlreadyExistsError, ProductNotFoundError
from src.services.product import ProductService


# --------- Fixture ---------

@pytest.fixture
def prod_repo():
    return AsyncMock(spec=ProductRepository)


@pytest.fixture
def metrics_repo():
    return AsyncMock(spec=MetricsRepository)

@pytest.fixture
def service(prod_repo, metrics_repo):
    return ProductService(prod_repo, metrics_repo)

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


# --------- create ---------

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


@pytest.mark.asyncio
async def test_create_success(service, prod_repo, product):

    schema = ProductCreate(
        store_id=1,

        item_number=123456,
        name="iPhone",
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

    prod_repo.get_product_by_item_number.return_value = None
    prod_repo.save.return_value = product
    prod_repo.get_by_id.return_value = product

    result = await service.create(schema)

    prod_repo.get_product_by_item_number.assert_called_once_with(schema.item_number)
    prod_repo.save.assert_called_once()
    prod_repo.get_by_id.assert_called_once_with(product.id)

    saved_product = prod_repo.save.call_args.args[0]

    assert saved_product.name == schema.name
    assert saved_product.item_number == schema.item_number
    assert saved_product.store_id == schema.store_id

    assert result.id == product.id
    assert result.name == product.name
    assert result.item_number == product.item_number


@pytest.mark.asyncio
async def test_create_product_already_exists(service, prod_repo, product):

    schema = ProductCreate(
        store_id=1,

        item_number=123456,
        name="iPhone",
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

    prod_repo.get_product_by_item_number.return_value = product

    with pytest.raises(ProductAlreadyExistsError):
        await service.create(schema)

    prod_repo.save.assert_not_called()


# --------- get_by_id ---------

@pytest.mark.asyncio
async def test_get_by_id_success(service, prod_repo, product):

    prod_repo.get_by_id.return_value = product

    result = await service.get_by_id(product.id)

    prod_repo.get_by_id.assert_called_once_with(product.id)

    assert result.id == product.id
    assert result.name == product.name


@pytest.mark.asyncio
async def test_get_by_id_not_found(service, prod_repo):

    prod_repo.get_by_id.return_value = None

    with pytest.raises(ProductNotFoundError):
        await service.get_by_id(1)


# --------- get_all ---------

@pytest.mark.asyncio
async def test_get_all(service, prod_repo, product):

    prod_repo.get_all.return_value = [product]

    result = await service.get_all()

    assert result.count == 1
    assert result.items[0].id == product.id



# --------- delete ---------

@pytest.mark.asyncio
async def test_delete_success(service, prod_repo, product):

    prod_repo.get_by_id.return_value = product

    await service.delete(product.id)

    prod_repo.get_by_id.assert_called_once_with(product.id)
    prod_repo.delete.assert_called_once_with(product)


@pytest.mark.asyncio
async def test_delete_not_found(service, prod_repo):

    prod_repo.get_by_id.return_value = None

    with pytest.raises(ProductNotFoundError):
        await service.delete(1)

    prod_repo.delete.assert_not_called()


# --------- update ---------

@pytest.mark.asyncio
async def test_update_success(service, prod_repo, product):

    schema = ProductUpdate(
        id=1,

        name="Samsung",
        category="Phones",

        price=1200,
        cogs=700,
        commission=11,
        acquiring=2,
        tax=6,

        views=2000,
        target_actions=150,
        buyers=30,

        ad_costs=300,

        inbound_logistic=15,
        direct_logistic=20,
        reverse_logistic=6,

        return_rate=0.04,
        defect_rate=0.02,

        avg_storage=4,
        avg_packaging=3,

        sales=30,
    )

    prod_repo.get_by_id.return_value = product
    prod_repo.save.return_value = product

    result = await service.update(schema)

    prod_repo.save.assert_called_once()

    assert result.name == "Samsung"
    assert result.price == 1200


@pytest.mark.asyncio
async def test_update_not_found(service, prod_repo):

    schema = ProductUpdate(
        id=1,

        name="Samsung",
        category="Phones",

        price=1200,
        cogs=700,
        commission=11,
        acquiring=2,
        tax=6,

        views=2000,
        target_actions=150,
        buyers=30,

        ad_costs=300,

        inbound_logistic=15,
        direct_logistic=20,
        reverse_logistic=6,

        return_rate=0.04,
        defect_rate=0.02,

        avg_storage=4,
        avg_packaging=3,

        sales=30,
    )

    prod_repo.get_by_id.return_value = None

    with pytest.raises(ProductNotFoundError):
        await service.update(schema)

    prod_repo.save.assert_not_called()


# --------- get_product_with_metric ---------

@pytest.mark.asyncio
async def test_get_product_with_metric_by_id_success(
    service,
    prod_repo,
    metrics_repo,
    product,
    metric,
):

    prod_repo.get_by_id.return_value = product
    metrics_repo.get_metrics_by_product_id.return_value = [metric]

    result = await service.get_product_with_metric_by_id(product.id)

    prod_repo.get_by_id.assert_called_once_with(product.id)
    metrics_repo.get_metrics_by_product_id.assert_called_once_with(product.id)

    assert result.id == product.id
    assert result.name == product.name

    assert len(result.metrics) == 1

    assert result.metrics[0].id == metric.id
    assert result.metrics[0].conversion == metric.conversion
    assert result.metrics[0].cm == metric.cm


@pytest.mark.asyncio
async def test_get_product_with_metric_by_id_not_found(
    service,
    prod_repo,
    metrics_repo,
):

    prod_repo.get_by_id.return_value = None

    with pytest.raises(ProductNotFoundError):
        await service.get_product_with_metric_by_id(1)

    metrics_repo.get_metrics_by_product_id.assert_not_called()
