"""Bonus option D: the order tests driven by an Excel workbook.

order_calculations.xlsx has one sheet per test category (Simple, Discounts,
Tax, Shipping, Complex). Every row of every sheet is one test.
"""

import pytest

from excel_loader import load_order_workbook
from order_calculator import Order


@pytest.mark.parametrize("case", load_order_workbook("order_calculations.xlsx"))
def test_order_calculation_from_excel(case):
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance_km"], case["is_express"])

    assert order.calculate_total() == case["expected"]
