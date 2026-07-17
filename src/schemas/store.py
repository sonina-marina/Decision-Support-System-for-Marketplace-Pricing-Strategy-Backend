from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from src.schemas.product import ProductView


class StoreBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True
    )


class StoreCreate(StoreBaseModel):
    user_id: int
    name: str


class StoreView(StoreBaseModel):
    id: int
    #user_id: int
    name: str
    products: list[ProductView]


class StoreUpdate(StoreBaseModel):
    id: int
    name: str


class StoreList(StoreBaseModel):
    count: int
    items: list[StoreView]
