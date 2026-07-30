import pytest
from unittest.mock import AsyncMock

from src.enums import UserRole
from src.services.user import UserService
from src.db.repositories import UserRepository
from src.db.models.user import User
from src.schemas.user import (UserCreate,
                              UserUpdateFullname,
                              UserUpdatePassword)
from src.services.exceptions import (UserAlreadyExistsError,
                                     UserNotFoundError)


# ---------- Fixtures ----------

@pytest.fixture
def repo():
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def service(repo):
    return UserService(repo)


@pytest.fixture
def user():
    return User(
        id=1,
        fullname="John Doe",
        email="john@mail.com",
        hash_password="123",
        role='SELLER',
    )


# ---------- create ----------

@pytest.mark.asyncio
async def test_create_success(service, repo, user):

    schema = UserCreate(
        fullname="John Doe",
        email="john@mail.com",
        password="password",
        role=UserRole.SELLER,
    )

    repo.get_user_by_email.return_value = None
    repo.save.return_value = user
    repo.get_by_id.return_value = user

    result = await service.create(schema)

    repo.get_user_by_email.assert_called_once_with(schema.email)
    repo.save.assert_called_once()
    repo.get_by_id.assert_called_once_with(user.id)

    assert result.id == user.id
    assert result.fullname == user.fullname
    assert result.email == user.email


@pytest.mark.asyncio
async def test_create_user_already_exists(service, repo, user):

    schema = UserCreate(
        fullname="John Doe",
        email="john@mail.com",
        password="password",
        role=UserRole.SELLER,
    )

    repo.get_user_by_email.return_value = user

    with pytest.raises(UserAlreadyExistsError):
        await service.create(schema)

    repo.save.assert_not_called()


# ---------- get_by_id ----------

@pytest.mark.asyncio
async def test_get_by_id_success(service, repo, user):

    repo.get_by_id.return_value = user

    result = await service.get_by_id(user.id)

    repo.get_by_id.assert_called_once_with(user.id)

    assert result.id == 1
    assert result.fullname == "John Doe"


@pytest.mark.asyncio
async def test_get_by_id_not_found(service, repo, user):

    repo.get_by_id.return_value = None

    with pytest.raises(UserNotFoundError):
        await service.get_by_id(user.id)


# ---------- get_all ----------

@pytest.mark.asyncio
async def test_get_all(service, repo):

    users = [
        User(
            id=1,
            fullname="Ivan",
            email="ivan@test.com",
            hash_password="123",
            role=UserRole.SELLER,
        ),
        User(
            id=2,
            fullname="Anna",
            email="anna@test.com",
            hash_password="456",
            role=UserRole.SELLER,
        ),
    ]

    repo.get_all.return_value = users

    result = await service.get_all()

    repo.get_all.assert_called_once()

    assert result.count == 2
    assert len(result.items) == 2
    assert result.items[0].fullname == "Ivan"
    assert result.items[1].fullname == "Anna"


# ---------- delete ----------

@pytest.mark.asyncio
async def test_delete_success(service, repo, user):

    repo.get_by_id.return_value = user

    await service.delete(user.id)

    repo.get_by_id.assert_called_once_with(user.id)
    repo.delete.assert_called_once_with(user)


@pytest.mark.asyncio
async def test_delete_not_found(service, repo):

    repo.get_by_id.return_value = None

    with pytest.raises(UserNotFoundError):
        await service.delete(1)

    repo.delete.assert_not_called()


# ---------- change_fullname ----------

@pytest.mark.asyncio
async def test_change_fullname(service, repo, user):

    schema = UserUpdateFullname(
        id=1,
        new_fullname="New Name",
    )

    repo.get_by_id.return_value = user
    repo.save.return_value = user

    result = await service.change_fullname(schema)

    repo.save.assert_called_once()

    assert result.fullname == "New Name"


# ---------- change_password ----------

@pytest.mark.asyncio
async def test_change_password(service, repo, user):

    schema = UserUpdatePassword(
        id=1,
        new_password="new_password",
    )

    repo.get_by_id.return_value = user
    repo.save.return_value = user

    result = await service.change_password(schema)

    repo.save.assert_called_once()

    assert user.hash_password == "new_password"
    assert result.id == user.id
