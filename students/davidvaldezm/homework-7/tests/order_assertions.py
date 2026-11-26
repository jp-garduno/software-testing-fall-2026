"""Assertions shared by the calculator and generated regression suites."""

import re

import pytest

from src.order_calculator import Order
from tests.data_schemas import MONEY_FIELDS


def assert_order_case(case):
    """Exercise the order from setup through its final breakdown."""
    if case["expected_error"] is not None:
        with pytest.raises(ValueError, match=re.escape(case["expected_error"])):
            order = Order(case["items"], case["customer_type"])
            order.set_shipping(case["distance_km"], case["is_express"])
        return
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"] is not None:
        assert order.apply_discount(case["discount_code"]) is case["discount_applied"]
    order.set_shipping(case["distance_km"], case["is_express"])
    expected = {key: case[f"expected_{key}"] for key in MONEY_FIELDS}
    assert order.calculate_total() == expected
    assert order.calculate_subtotal() == expected["subtotal"]
    assert order.calculate_discount() == expected["discount"]
    assert order.calculate_tax() == expected["tax"]
    assert order.calculate_shipping() == expected["shipping"]
