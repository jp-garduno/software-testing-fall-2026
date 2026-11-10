"""Part 3: Data-driven version of the 10 comparison order tests loaded from CSV."""

import csv
import json
from pathlib import Path
import pytest
from order_calculator import Order

CSV_PATH = Path(__file__).resolve().parent.parent / "test_data" / "order_calculations.csv"
COMPARISON_TEST_NAMES = {
    "simple_single_item",
    "simple_two_quantities",
    "discount_save10_at_threshold",
    "discount_save10_below_min",
    "discount_save20_at_threshold",
    "discount_newuser_valid",
    "discount_invalid_code",
    "shipping_express_multiplier",
    "shipping_freeship_code",
    "complex_three_items_save20_exp",
}


def load_comparison_cases():
    """Load the 10 comparison test cases from the external CSV file."""
    with CSV_PATH.open("r", encoding="utf-8") as csv_file:
        return [
            row
            for row in csv.DictReader(csv_file)
            if row["test_name"] in COMPARISON_TEST_NAMES
        ]


CASES = load_comparison_cases()


@pytest.mark.parametrize("case", CASES, ids=[c["test_name"] for c in CASES])
def test_order_data_driven_comparison(case):
    """Execute the 10 comparison scenarios using parameterized external CSV data."""
    order = Order(json.loads(case["items"]), case["customer_type"])
    if case["discount_code"] != "NONE":
        order.apply_discount(case["discount_code"])
    order.set_shipping(float(case["distance_km"]), case["is_express"] == "true")
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(float(case["expected_subtotal"]))
    assert result["discount"] == pytest.approx(float(case["expected_discount"]))
    assert result["tax"] == pytest.approx(float(case["expected_tax"]))
    assert result["shipping"] == pytest.approx(float(case["expected_shipping"]))
    assert result["total"] == pytest.approx(float(case["expected_total"]))
