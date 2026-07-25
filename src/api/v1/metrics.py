from fastapi import APIRouter, Depends
from src.schemas.metrics import (MetricsList, MetricsView)
from src.services.metrics import MetricsService
from src.api.dependencies import get_metrics_service


router = APIRouter(prefix='/metricss')


@router.post('/', response_model=MetricsView)
async def calculate_metrics(
    id: int,
    metrics_service: MetricsService = Depends(get_metrics_service)
):

    return await metrics_service.calculate_metrics(id)


@router.get('/', response_model=MetricsView)
async def get_by_id(
    id: int,
    metrics_service: MetricsService = Depends(get_metrics_service)
):

    return await metrics_service.get_by_id(id)
