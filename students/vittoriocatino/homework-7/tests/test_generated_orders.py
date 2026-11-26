"""Execute every generated order as a regression test, not merely create data."""

import json
from pathlib import Path

import pytest

from data_loader import MONEY_FIELDS, load_orders
from order_calculator import Order


@pytest.mark.parametrize(
    "case",
    load_orders(Path(__file__).resolve().parents[1] / "test_data/generated_orders.csv"),
    ids=lambda case: case["test_name"],
)
def test_generated_order(case):
    """Assert all independently calculated monetary components."""
    order = Order(json.loads(case["items"]))
    order.set_shipping(float(case["distance_km"]), case["is_express"] == "true")
    assert order.calculate_total() == {
        field: float(case[f"expected_{field}"]) for field in MONEY_FIELDS
    }
