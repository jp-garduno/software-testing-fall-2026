"""Data-driven version of the same 10 scenarios as test_order_traditional.py.

The scenarios are picked by name from test_data/order_calculations.csv, so the
data lives in the file and the test logic is written once.
"""

import pytest

from data_loader import load_order_cases
from order_calculator import Order

SCENARIOS = [
    "simple_single_item",
    "save10_at_exact_minimum",
    "save10_below_minimum",
    "save20_at_exact_minimum",
    "invalid_code_ignored",
    "newuser_for_new_customer",
    "shipping_weight_and_distance",
    "shipping_express_weight_and_distance",
    "shipping_free_with_freeship",
    "complex_multi_item_discount_shipping",
]
BY_NAME = {case["test_name"]: case for case in load_order_cases()}


@pytest.mark.parametrize("name", SCENARIOS)
def test_order_scenario(name):
    case = BY_NAME[name]
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance"], case["is_express"])
    result = order.calculate_total()
    for key, expected in case["expected"].items():
        assert result[key] == pytest.approx(expected, abs=0.005)
