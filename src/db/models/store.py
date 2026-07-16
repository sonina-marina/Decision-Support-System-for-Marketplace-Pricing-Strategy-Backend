from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, ForeignKey

from src.db.models.base import Base


class Store(Base):
    __tablename__ = 'stores'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    user: Mapped['User'] = relationship(
        lazy='raise'
    )

    name: Mapped[str] = mapped_column(
        String(100),
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

    products: Mapped[list['Product']]= relationship(
        back_populates='shop',
        cascade='all, delete-orphan',
        lazy='raise'
    )

