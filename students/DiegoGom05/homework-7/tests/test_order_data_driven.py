"""
Enfoque DATA-DRIVEN: los mismos 10 tests de test_order_traditional.py,
pero con UNA sola funcion parametrizada y los datos en
test_data/order_calculations.csv.
"""

import csv
import json
import os
import sys

import pytest

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from order_calculator import Order  # noqa: E402

DATA_FILE = os.path.join(BASE_DIR, "test_data", "order_calculations.csv")

# Los 10 casos de la comparacion (mismos que el enfoque tradicional)
COMPARISON_CASES = {
    "simple_single_item", "simple_multiple_items",
    "discount_save10_at_threshold", "discount_save20_below_min",
    "discount_invalid_code", "discount_newuser_new_customer",
    "tax_rounding_decimals", "shipping_express",
    "shipping_freeship_code", "complex_multi_item_save20_express",
}


def load_cases():
    """Lee del CSV solo las filas de la comparacion."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return [
            pytest.param(row, id=row["test_name"])
            for row in csv.DictReader(f)
            if row["test_name"] in COMPARISON_CASES
        ]


@pytest.mark.parametrize("row", load_cases())
def test_order(row):
    items = json.loads(row["items"].replace("'", '"'))
    order = Order(items, row["customer_type"])
    if row["discount_code"] != "NONE":
        order.apply_discount(row["discount_code"])
    order.set_shipping(float(row["distance_km"]), row["is_express"] == "true")
    result = order.calculate_total()

    for field in ("subtotal", "discount", "tax", "shipping", "total"):
        expected = float(row[f"expected_{field}"])
        assert result[field] == pytest.approx(expected, abs=0.01), f"{row['test_name']}: {field}"
