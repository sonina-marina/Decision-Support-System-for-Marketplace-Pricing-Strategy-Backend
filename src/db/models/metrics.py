from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.base import Base


class Metrics(Base):
    __tablename__ = 'metrics'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        nullable=False
    )

    product: Mapped['Product'] = relationship(
        lazy='raise'
    )

    conversion: Mapped[float] = mapped_column(
        nullable=False
    )

    cac: Mapped[float] = mapped_column(
        nullable=False
    )

    required_cpa: Mapped[float] = mapped_column(
        nullable=False
    )

    ltc: Mapped[float] = mapped_column(
        nullable=False
    )

    cm: Mapped[float] = mapped_column(
        nullable=False
    )

    ltv: Mapped[float] = mapped_column(
        nullable=False
    )

    product_roi: Mapped[float] = mapped_column(
        nullable=False
    )

    calculated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now(),
        nullable=False
    )
