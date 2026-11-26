import pytest

from src.order_calculator import Order


def build_order(case):
    data = case.order
    order = Order(data.items, data.customer_type, data.order_date)
    if data.discount_code:
        order.apply_discount(data.discount_code)
    order.set_shipping(data.distance_km, data.is_express)
    return order


def order_params(cases):
    return [pytest.param(case, id=case.test_name) for case in cases]
