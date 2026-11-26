"""Data-driven version of the comparison suite (part 3).

The same ten scenarios as test_order_traditional.py, read from test_data/comparison_orders.csv
and run by a single parametrized test.
"""

from pathlib import Path

import pytest

from data_files import load_order_cases
from order_calculator import Order

CASES = load_order_cases(Path(__file__).resolve().parent.parent / "test_data" / "comparison_orders.csv")


@pytest.mark.parametrize("case", CASES, ids=[case["test_name"] for case in CASES])
def test_order(case):
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance_km"], case["is_express"])

    assert order.calculate_total() == pytest.approx(case["expected"])
