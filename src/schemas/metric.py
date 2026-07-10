from pydantic import BaseModel


class ProductCalculationData(BaseModel):
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


class MetricsResult(BaseModel):
    conversion: float
    cac: float
    required_cpa: float

    ltc: float
    cm: float
    ltv: float
    product_roi: float
