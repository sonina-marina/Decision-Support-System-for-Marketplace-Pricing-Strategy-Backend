from typing import Generic, TypeVar

from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

ModelType = TypeVar('ModelType')


class BaseRepository(
    Generic[ModelType]
):
    def __init__(
        self,
        model: type[ModelType],
        session: AsyncSession
    ):

        self.model = model
        self.session = session


    async def get_by_id(
        self,
        id: int,
        options: Sequence[ORMOption] | None = None
    ) -> ModelType | None:

        stmt = (
            select(self.model)
            .where(self.model.id == id)
        )

        if options:
            stmt = stmt.options(*options)

        result = await self.session.execute(stmt)

        return self.exclude_deleted(result.scalar_one_or_none())


    async def get_all(
        self,
        options: Sequence[ORMOption] | None = None
    ) -> list[ModelType]:

        stmt = select(self.model)

        if options:
            stmt = stmt.options(*options)

        result = await self.session.execute(stmt)

        return self.exclude_deleted_from_list(list(result.scalars().all()))


    async def save(
        self,
        entity: ModelType
    ) -> ModelType:

        self.session.add(entity)

        await self.session.flush()

        await self.session.refresh(entity)

        return entity


    async def delete(
        self,
        entity: ModelType
    ) -> None:
        
        if hasattr(entity, "is_deleted"):
            entity.is_deleted = True
        else:
            await self.session.delete(entity)

        await self.session.flush()


    def exclude_deleted_from_list(
        self,
        entities: list[ModelType]
    ) -> list[ModelType]:

        return [
            e for e in entities 
            if not (hasattr(e, "is_deleted") and e.is_deleted)
        ]


    def exclude_deleted(
        self,
        entity: ModelType | None
    ) -> ModelType | None:

        if entity is None or hasattr(entity, "is_deleted") and entity.is_deleted:
            return None

        return entity
