from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from src.schemas.metrics import MetricsView


class ProductBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True
    )


class ProductCreate(ProductBaseModel):
    shop_id: int

    item_number: int
    name: str
    category: str
    
    price: float
    cogs: float
    commission: float
    acquiring: float
    tax: float

    views: int
    target_actions: int
    buyers: int

    ad_costs: float

    inbound_logistic: float
    direct_logistic: float
    reverse_logistic: float

    return_rate: float
    defect_rate: float

    avg_storage: float
    avg_packaging: float

    sales: int


class ProductView(ProductBaseModel):
    id: int
    #shop_id: int
    item_number: int
    name: str
    category: str
    price: float


class ProductDetailedView(ProductBaseModel):
    id: int
    shop_id: int

    item_number: int
    name: str
    category: str
    
    price: float
    cogs: float
    commission: float
    acquiring: float
    tax: float

    views: int
    target_actions: int
    buyers: int

    ad_costs: float

    inbound_logistic: float
    direct_logistic: float
    reverse_logistic: float

    return_rate: float
    defect_rate: float

    avg_storage: float
    avg_packaging: float

    sales: int

    metrics: list[MetricsView]


class ProductList(ProductBaseModel):
    count: int
    items: list[ProductView]


class ProductUpdate(ProductBaseModel):
    id: int

    item_number: int
    name: str
    category: str
    
    price: float
    cogs: float
    commission: float
    acquiring: float
    tax: float

    views: int
    target_actions: int
    buyers: int

    ad_costs: float

    inbound_logistic: float
    direct_logistic: float
    reverse_logistic: float

    return_rate: float
    defect_rate: float

    avg_storage: float
    avg_packaging: float

    sales: int
