from typing import TypeVar

from pydantic import EmailStr
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


    async def get_user_by_email(
        self,
        email: EmailStr
    ) -> User | None:

        stmt = (
            select(User)
            .where(User.email == email)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
