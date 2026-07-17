from datetime import datetime
from sqlalchemy import ForeignKey, func, true
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.base import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    shop_id: Mapped[int] = mapped_column(
        ForeignKey('shops.id'),
        nullable=False
    )

    shop: Mapped['Shop'] = relationship(
        lazy='raise'
    )

    item_number: Mapped[int] = mapped_column(
        nullable=True
    )

    name: Mapped[str] = mapped_column(
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        nullable=True
    )

    price: Mapped[float] = mapped_column(
        nullable=False
    )

    cogs: Mapped[float] = mapped_column(
        nullable=False
    )

    commission: Mapped[float] = mapped_column(
        nullable=False
    ) 

    acquiring: Mapped[float] = mapped_column(
        nullable=False
    ) 

    tax: Mapped[float] = mapped_column(
        nullable=False
    ) 

    views: Mapped[int] = mapped_column(
        nullable=False
    ) 

    target_actions: Mapped[int] = mapped_column(
        nullable=False
    ) 

    buyers: Mapped[int] = mapped_column(
        nullable=False
    ) 

    ad_costs: Mapped[float] = mapped_column(
        nullable=False
    ) 

    inbound_logistic: Mapped[float] = mapped_column(
        nullable=False
    ) 

    direct_logistic: Mapped[float] = mapped_column(
        nullable=False
    ) 

    reverse_logistic: Mapped[float] = mapped_column(
        nullable=False
    ) 

    return_rate: Mapped[float] = mapped_column(
        nullable=False
    ) 

    defect_rate: Mapped[float] = mapped_column(
        nullable=False
    ) 

    avg_storage: Mapped[float] = mapped_column(
        nullable=False
    ) 

    avg_packaging: Mapped[float] = mapped_column(
        nullable=False
    ) 

    sales: Mapped[int] = mapped_column(
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

    metrics: Mapped[list['Metrics']] = relationship(
        back_populates='product',
        cascade='all, delete-orphan',
        lazy='raise'
    )
