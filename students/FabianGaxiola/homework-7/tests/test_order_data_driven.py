"""Parameterized comparison suite using the shared CSV records."""

import pytest
from data_loaders import load_order_cases
from order_calculator import Order

COMPARISON_CASES = load_order_cases()[:10]


@pytest.mark.parametrize("case", COMPARISON_CASES, ids=lambda case: case["test_name"])
def test_order_case_matches_external_expected_values(case):
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance_km"], case["is_express"])
    actual = order.calculate_total()

    assert actual == pytest.approx(
        {
            "subtotal": case["expected_subtotal"],
            "discount": case["expected_discount"],
            "tax": case["expected_tax"],
            "shipping": case["expected_shipping"],
            "total": case["expected_total"],
        },
        abs=0.001,
    )
