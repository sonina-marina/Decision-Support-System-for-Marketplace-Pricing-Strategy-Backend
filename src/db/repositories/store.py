from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.db.models.store import Store
from src.db.repositories.base import BaseRepository


class StoreRepository(
    BaseRepository[Store]
):
    def __init__(
        self, 
        session: AsyncSession
    ):
        super().__init__(Store, session)


    async def get_store_by_user_id(
        self,
        user_id: int
    ) -> list[Store]:

        stmt = (
            select(Store)
            .where(Store.user_id == user_id)
        )

        result = await self.session.execute(stmt)

        return self.exclude_deleted_from_list(list(result.scalars().all()))
