from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.dependencies import get_session
from src.db.repositories import (UserRepository, StoreRepository,
                                 ProductRepository, MetricsRepository)
from src.services.auth import AuthService
from src.services.metrics import MetricsService
from src.services.product import ProductService
from src.services.store import StoreService
from src.services.user import UserService


async def get_user_repository(
    session: AsyncSession = Depends(get_session)
) -> UserRepository:

    return UserRepository(session)


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:

    return UserService(user_repository)


async def get_store_repository(
    session: AsyncSession = Depends(get_session)
) -> StoreRepository:

    return StoreRepository(session)


async def get_store_service(
    store_repository: StoreRepository = Depends(get_store_repository)
) -> StoreService:

    return StoreService(store_repository)


async def get_product_repository(
    session: AsyncSession = Depends(get_session)
) -> ProductRepository:

    return ProductRepository(session)


async def get_metrics_repository(
    session: AsyncSession = Depends(get_session)
) -> MetricsRepository:

    return MetricsRepository(session)


async def get_product_service(
    product_repository: ProductRepository = Depends(get_product_repository),
    metrics_repository: MetricsRepository = Depends(get_metrics_repository)
) -> ProductService:

    return ProductService(product_repository, metrics_repository)


async def get_metrics_service(
    metrics_repository: MetricsRepository = Depends(get_metrics_repository),
    product_repository: ProductRepository = Depends(get_product_repository)
) -> MetricsService:

    return MetricsService(metrics_repository, product_repository)


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:

    return AuthService(user_repository)
