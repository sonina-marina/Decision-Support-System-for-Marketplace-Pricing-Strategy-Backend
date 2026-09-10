import pytest

from src.schemas.metric import ProductCalculationData
from src.utils.metric_calculator import MetricCalculator


def test_conversion():

    data = ProductCalculationData(
        price=1000,
        cogs=400,
        commission=10,
        acquiring=2,
        tax=6,
        views=1000,
        target_actions=100,
        buyers=20,
        sales=25,
        ad_costs=5000,
        inbound_logistic=30,
        direct_logistic=40,
        reverse_logistic=50,
        return_rate=0.1,
        defect_rate=0.05,
        avg_storage=15,
        avg_packaging=10
    )

    assert MetricCalculator._calculate_conversion(data) == 0.1
    

def test_conversion_zero_views():

    data = ProductCalculationData(
        price=1000,
        cogs=400,
        commission=10,
        acquiring=2,
        tax=6,
        views=0,
        target_actions=100,
        buyers=20,
        sales=25,
        ad_costs=5000,
        inbound_logistic=30,
        direct_logistic=40,
        reverse_logistic=50,
        return_rate=0.1,
        defect_rate=0.05,
        avg_storage=15,
        avg_packaging=10
    )

    with pytest.raises(ValueError):
        MetricCalculator._calculate_conversion(data)


def test_cac():    

    data = ProductCalculationData(
        price=1000,
        cogs=400,
        commission=10,
        acquiring=2,
        tax=6,
        views=1000,
        target_actions=100,
        buyers=20,
        sales=25,
        ad_costs=5000,
        inbound_logistic=30,
        direct_logistic=40,
        reverse_logistic=50,
        return_rate=0.1,
        defect_rate=0.05,
        avg_storage=15,
        avg_packaging=10
    )

    assert MetricCalculator._calculate_cac(data) == 250
    

def test_cac_zero_byuers():

    data = ProductCalculationData(
        price=1000,
        cogs=400,
        commission=10,
        acquiring=2,
        tax=6,
        views=1000,
        target_actions=100,
        buyers=0,
        sales=25,
        ad_costs=5000,
        inbound_logistic=30,
        direct_logistic=40,
        reverse_logistic=50,
        return_rate=0.1,
        defect_rate=0.05,
        avg_storage=15,
        avg_packaging=10
    )

    with pytest.raises(ValueError):
        MetricCalculator._calculate_cac(data)


def test_required_cpa_negative_digit():

    data = ProductCalculationData(
        price=1000,
        cogs=400,
        commission=10,
        acquiring=2,
        tax=6,
        views=1000,
        target_actions=-1,
        buyers=20,
        sales=25,
        ad_costs=5000,
        inbound_logistic=30,
        direct_logistic=40,
        reverse_logistic=50,
        return_rate=0.1,
        defect_rate=0.05,
        avg_storage=15,
        avg_packaging=10
    )

    with pytest.raises(ValueError):
        MetricCalculator._calculate_required_cpa(data)




def test_ltc():

    data = ProductCalculationData(
        price=1000,
        cogs=400,
        commission=10,
        acquiring=2,
        tax=6,
        views=1000,
        target_actions=100,
        buyers=20,
        sales=25,
        ad_costs=5000,
        inbound_logistic=30,
        direct_logistic=40,
        reverse_logistic=50,
        return_rate=0.1,
        defect_rate=0.05,
        avg_storage=15,
        avg_packaging=10
    )

    assert MetricCalculator._calculate_ltc(data) == 682
    

def test_product_roi_zero():

    with pytest.raises(ValueError):
        MetricCalculator._calculate_product_roi(318, 0)


def test_product_roi():

    result = MetricCalculator._calculate_product_roi(318, 628)

    assert result == pytest.approx(46,627)
