"""Part 3, data-driven version: the ten scenarios of test_order_traditional.py.

The test logic is written once; the ten scenarios are the rows of
test_data/order_comparison.csv.
"""

import pytest

from case_loaders import load_order_csv
from order_calculator import Order


@pytest.mark.parametrize("case", load_order_csv("order_comparison.csv"))
def test_order_scenario(case):
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance_km"], case["is_express"])

    assert order.calculate_total() == case["expected"]
