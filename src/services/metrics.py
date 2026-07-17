from src.db.repositories.metrics import MetricsRepository
from src.db.repositories.product import ProductRepository
from src.schemas import metrics
from src.schemas.metric import ProductCalculationData
from src.schemas.metrics import (MetricsList, MetricsView)
from src.services.exceptions import MetricsNotFoundError, ProductNotFoundError
from src.utils.metric_calculator import MetricCalculator
from src.db.models.metrics import Metrics


class MetricsService:
    def __init__(
        self, 
        metrics_repository: MetricsRepository,
        product_repository: ProductRepository
    ):

        self.metrics_repository = metrics_repository
        self.product_repository = product_repository
    
    async def calculate_metrics(self, product_id: int) -> MetricsView:
        
        product = await self.product_repository.get_full_product_by_id(product_id)
        
        if product is None:
            raise ProductNotFoundError(product_id)

        calc_data = ProductCalculationData.model_validate(product) 

        result = MetricCalculator.calculate(calc_data)

        metrics = Metrics(**result.model_dump())

        await self.metrics_repository.save(metrics)

        metrics_view = MetricsView.model_validate(result)

        return metrics_view 


    async def get_by_id(self, id: int) -> MetricsView:

        metrics = await self.metrics_repository.get_by_id(id)

        if metrics is None:
            raise MetricsNotFoundError(id) 

        return MetricsView.model_validate(metrics)


    async def get_all(self) -> MetricsList:

        metrics = await self.metrics_repository.get_all()

        return MetricsList(
            count=len(metrics),
            items=[MetricsView.model_validate(metric) for metric in metrics]
            )
