from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.metrics import Metrics
from src.db.repositories.base import BaseRepository


class MetricsRepository(
    BaseRepository[Metrics]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(Metrics, session)


    async def get_metrics_by_product_id(
        self,
        product_id: int
    ) -> list[Metrics]:
        
        stmt = (
            select(Metrics)
            .where(Metrics.product_id == product_id)
        )

        result = await self.session.execute(stmt)

        return self.exclude_deleted_from_list(list(result.scalars().all()))
