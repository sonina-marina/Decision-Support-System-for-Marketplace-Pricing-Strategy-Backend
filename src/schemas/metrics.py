from datetime import datetime
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class MetricsBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True
    )


class MetricsView(MetricsBaseModel):
    id: int
    #product_id: int
    conversion: float
    cac: float
    required_cpa:float
    ltc: float
    cm: float
    ltv: float
    product_roi: float
    calculated_at: datetime


class MetricsList(MetricsBaseModel):
    count: int
    items: list[MetricsView]
