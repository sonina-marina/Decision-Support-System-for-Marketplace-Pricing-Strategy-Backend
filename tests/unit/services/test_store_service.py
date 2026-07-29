import pytest
from unittest.mock import AsyncMock

from sqlalchemy.exc import IntegrityError

from src.db.models.store import Store
from src.db.repositories.store import StoreRepository
from src.schemas.store import StoreCreate, StoreUpdate
from src.services.exceptions import StoreAlreadyExistsError, StoreNotFoundError
from src.services.store import StoreService


# --------- Fixtures ---------

@pytest.fixture
def repo():
    return AsyncMock(spec=StoreRepository)


@pytest.fixture
def service(repo):
    return StoreService(repo)


@pytest.fixture
def store():
    return Store(
        id=1,
        user_id=1,
        name="Temp Store",
        is_deleted=False
    )


# --------- create ---------

@pytest.mark.asyncio
async def test_create_success(service, repo, store):

    schema = StoreCreate(
        user_id=1,
        name="Temp Store"
    )

    repo.get_store_by_user_id.return_value = []
    repo.save.return_value = store
    repo.get_by_id.return_value = store

    result = await service.create(schema)

    repo.get_store_by_user_id.assert_called_once_with(schema.user_id)
    repo.save.assert_called_once()
    repo.get_by_id.assert_called_once_with(store.id)

    assert result.id == store.id
    assert result.name == store.name


@pytest.mark.asyncio
async def test_crete_store_already_exist(service, repo, store):
    
    schema = StoreCreate(
        user_id=1,
        name="Temp Store"
    )

    repo.get_store_by_user_id.return_value = [store]

    with pytest.raises(StoreAlreadyExistsError):
        await service.create(schema)

    repo.save.assert_not_called()


# --------- get_by_id ---------

@pytest.mark.asyncio
async def test_get_by_id_success(service, repo, store):

    repo.get_by_id.return_value = store

    result = await service.get_by_id(store.id)

    repo.get_by_id.assert_called_once_with(store.id)

    assert result.id == store.id
    assert result.name == "Temp Store"


@pytest.mark.asyncio
async def test_get_by_id_not_found(service, repo, store):

    repo.get_by_id.return_value = None

    with pytest.raises(StoreNotFoundError):
        await service.get_by_id(store.id)


# --------- get_all ---------

@pytest.mark.asyncio
async def test_get_all(service, repo):

    stores = [
        Store(
            id=1,
            user_id=1,
            name="Temp Store 1",
            is_deleted=False
        ),
        Store(
            id=2,
            user_id=2,
            name="Temp Store 2",
            is_deleted=False
        ),
    ]

    repo.get_all.return_value = stores

    result = await service.get_all()

    repo.get_all.assert_called_once()

    assert result.count == 2
    assert result.items[0].name == "Temp Store 1"
    assert result.items[1].name == "Temp Store 2"


# --------- get_store_by_user_id ---------

@pytest.mark.asyncio
async def test_store_by_user_id(service, repo):

    stores = [
        Store(
            id=1,
            user_id=1,
            name="Temp Store 1",
            is_deleted=False
        ),
        Store(
            id=2,
            user_id=1,
            name="Temp Store 2",
            is_deleted=False
        ),
    ]

    repo.get_all.return_value = stores

    result = await service.get_all()

    repo.get_all.assert_called_once()

    assert result.count == 2
    assert result.items[0].name == "Temp Store 1"
    assert result.items[1].name == "Temp Store 2"


# --------- delete ---------

@pytest.mark.asyncio
async def test_delete_success(service, repo, store):

    repo.get_by_id.return_value = store

    await service.delete(store.id)

    repo.get_by_id.assert_called_once_with(store.id)
    repo.delete.assert_called_once_with(store)


@pytest.mark.asyncio
async def test_delete_not_found(service, repo):

    repo.get_by_id.return_value = None

    with pytest.raises(StoreNotFoundError):
        await service.delete(1)

    repo.delete.assert_not_called()


# --------- update ---------

@pytest.mark.asyncio
async def test_update_success(service, repo, store):

    schema = StoreUpdate(
        id=1,
        name="New Name"
    )

    repo.get_by_id.return_value = store
    repo.save.return_value = store

    result = await service.update(schema)

    repo.save.assert_called_once()

    assert store.name == "New Name"
    assert result.id == store.id


@pytest.mark.asyncio
async def test_update_not_found(service, repo):

    schema = StoreUpdate(
        id=1,
        name="New Name"
    )
    
    repo.get_by_id.return_value = None

    with pytest.raises(StoreNotFoundError):
        await service.update(schema)

    repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_update_store_already_exists(service, repo, store):

    schema = StoreUpdate(
        id=1,
        name="New Name"
    )

    repo.get_by_id.return_value = store

    repo.save.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception("duplicate info")
    )

    with pytest.raises(StoreAlreadyExistsError):
        await service.update(schema)

