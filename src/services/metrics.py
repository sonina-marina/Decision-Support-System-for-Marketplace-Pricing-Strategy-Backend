from src.db.repositories.metrics import MetricsRepository
from src.db.repositories.product import ProductRepository
from src.schemas.metric import ProductCalculationData
from src.schemas.metrics import (MetricsView)
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

        metrics = await self.metrics_repository.save(metrics)

        return MetricsView.model_validate(metrics)


    async def calculate_metrics_for_custom_product(
        self, 
        calc_data: ProductCalculationData
    ) -> MetricsView:

        result = MetricCalculator.calculate(calc_data)

        metrics = Metrics(**result.model_dump())

        metrics = await self.metrics_repository.save(metrics)

        return MetricsView.model_validate(metrics)



    async def get_by_id(self, id: int) -> MetricsView:

        metrics = await self.metrics_repository.get_by_id(id)

        if metrics is None:
            raise MetricsNotFoundError(id) 

        return MetricsView.model_validate(metrics)
