"""Part 1: every row of order_calculations.csv is one test of the order breakdown."""

import pytest

from case_loaders import load_order_csv
from order_calculator import Order


@pytest.mark.parametrize("case", load_order_csv("order_calculations.csv"))
def test_order_calculation(case):
    """Subtotal, discount, tax, shipping and total must match the row to the cent."""
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance_km"], case["is_express"])

    # Exact comparison on purpose: amounts are already rounded to cents, and a
    # tolerance would let a one-cent error through.
    assert order.calculate_total() == case["expected"]
