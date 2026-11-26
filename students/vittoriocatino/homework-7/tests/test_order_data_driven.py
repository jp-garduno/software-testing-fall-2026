"""The same ten pricing scenarios as test_order_traditional, loaded from CSV."""

import json
from pathlib import Path

import pytest

from order_calculator import Order
from data_loader import MONEY_FIELDS, load_orders

CASES = load_orders(
    Path(__file__).resolve().parents[1] / "test_data/order_calculations.csv"
)[:10]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["test_name"])
def test_equivalent_order(case):
    """Assert the complete monetary breakdown for each of the ten scenarios."""
    order = Order(json.loads(case["items"]), case["customer_type"])
    if case["discount_code"] != "NONE":
        order.apply_discount(case["discount_code"])
    order.set_shipping(float(case["distance_km"]), case["is_express"] == "true")
    expected = {field: float(case[f"expected_{field}"]) for field in MONEY_FIELDS}
    assert order.calculate_total() == expected
