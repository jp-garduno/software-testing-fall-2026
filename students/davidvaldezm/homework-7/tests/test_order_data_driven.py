"""Run the same ten order breakdown checks using external CSV cases."""

import pytest

from src.order_calculator import Order
from tests.data_loader import order_cases
from tests.data_schemas import MONEY_FIELDS


@pytest.mark.parametrize("case", order_cases("order_comparison.csv"))
def test_order_breakdown(case):
    """Check the coupon result and all five amounts for each order."""
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"] is not None:
        assert order.apply_discount(case["discount_code"]) is case["discount_applied"]
    order.set_shipping(case["distance_km"], case["is_express"])
    assert order.calculate_total() == {
        key: case[f"expected_{key}"] for key in MONEY_FIELDS
    }
