"""Regression tests over 100 orders generated with Faker (bonus option A).

The file is produced by tools/generate_orders.py with a fixed seed; its expected amounts come
from an independent oracle in that script. The test code is the same loop as part 1, which is
the point of data-driven testing: 100 more scenarios, zero new test logic.
"""

from pathlib import Path

import pytest

from data_files import load_order_cases
from order_calculator import Order

CASES = load_order_cases(Path(__file__).resolve().parent.parent / "test_data" / "generated_orders.csv")


@pytest.mark.parametrize("case", CASES, ids=[case["test_name"] for case in CASES])
def test_generated_order(case):
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance_km"], case["is_express"])

    assert order.calculate_total() == pytest.approx(case["expected"], abs=0.005)


def test_generator_produced_one_hundred_orders():
    assert len(CASES) == 100
