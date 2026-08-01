from fastapi import APIRouter, Depends
from src.core.auth.dependencies import get_current_user, require_role
from src.enums import UserRole
from src.schemas.metric import ProductCalculationData
from src.schemas.metrics import (MetricsList, MetricsView)
from src.services.metrics import MetricsService
from src.api.dependencies import get_metrics_service


router = APIRouter(prefix='/metrics')


@router.post('/', response_model=MetricsView)
async def calculate_metrics(
    id: int,
    metrics_service: MetricsService = Depends(get_metrics_service),
    user=Depends(
        require_role(UserRole.SELLER)
    )
):

    return await metrics_service.calculate_metrics(id)


@router.post('/custom', response_model=MetricsView)
async def calculate_metrics_for_custom_product(
    product_info: ProductCalculationData,
    metrics_service: MetricsService = Depends(get_metrics_service),
    user=Depends(
        get_current_user
    )
):

    return await metrics_service.calculate_metrics_for_custom_product(product_info)


@router.get('/', response_model=MetricsView)
async def get_by_id(
    id: int,
    metrics_service: MetricsService = Depends(get_metrics_service),
    user=Depends(
        get_current_user
    )
):

    return await metrics_service.get_by_id(id)


@router.get('/by_product', response_model=MetricsList)
async def get_metrics_by_product_id(
    id: int,
    metrics_service: MetricsService = Depends(get_metrics_service),
    user=Depends(
        get_current_user
    )
):

    return await metrics_service.get_metrics_by_product_id(id)
