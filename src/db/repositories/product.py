from typing import Generic

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.models.product import Product
from src.db.repositories.base import BaseRepository


class ProductRepository(
    BaseRepository[Product]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(Product, session)


    async def get_product_by_store_id(
        self,
        store_id: int
    ) -> list[Product]:
        
        stmt = (
            select(Product)
            .where(Product.store_id == store_id)
        )

        result = await self.session.execute(stmt)

        return self.exclude_deleted_from_list(list(result.scalars().all()))


    async def get_product_by_item_number(
        self,
        item_number: int
    ) -> Product | None:

        stmt = (
            select(Product)
            .where(Product.item_number == item_number)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


    async def get_full_product_by_id(
        self,
        id
    ) -> Product | None:

        product = await self.get_by_id(
            id, 
            options=[
                selectinload(Product.metrics)
            ]
        )

        return self.exclude_deleted(product)
