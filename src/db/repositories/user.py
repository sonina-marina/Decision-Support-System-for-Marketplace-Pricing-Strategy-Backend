from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.repositories.base import BaseRepository, ModelType
from src.db.models.user import User

ModelType = TypeVar('ModelType')

class UserRepository(
    BaseRepository[User]
):
    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(User, session)


    async def get_user_password_hash(
        self,
        id: int
    ) -> str:

        stmt = (
            select(User.hash_password)
            .where(User.id == id)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one()
