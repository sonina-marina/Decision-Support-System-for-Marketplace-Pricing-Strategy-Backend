from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func

from src.db.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        String(40),
        nullable=False
    )

    fullname: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    hash_password: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now(),
        nullable=False
    )

    is_deleted: Mapped[bool] = mapped_column(
      default=False  
    )

    stores: Mapped[list['Store']]= relationship(
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='raise'
    )
