"""One pricing contract, expanded from independently reviewed CSV oracles."""

import json
from pathlib import Path

import pytest

from data_loader import MONEY_FIELDS, load_orders
from order_calculator import Order

DATA = Path(__file__).resolve().parents[1] / "test_data"


@pytest.mark.parametrize(
    "case",
    load_orders(DATA / "order_calculations.csv"),
    ids=lambda case: case["test_name"],
)
def test_order_calculation(case):
    """Check all five components, or the explicitly expected validation error."""

    def calculate():
        order = Order(json.loads(case["items"]), case["customer_type"])
        if case["discount_code"] != "NONE":
            order.apply_discount(case["discount_code"])
        order.set_shipping(float(case["distance_km"]), case["is_express"] == "true")
        return order.calculate_total()

    if case["expected_error"]:
        with pytest.raises(ValueError):
            calculate()
    else:
        result = calculate()
        assert set(result) == set(MONEY_FIELDS)
        for field in MONEY_FIELDS:
            assert result[field] == pytest.approx(
                float(case[f"expected_{field}"]), abs=0.000001, rel=0
            ), field
