"""Shared helpers: load order test cases from CSV and run one case.

Keeping the CSV parsing and the assertions here (and out of the test
modules) is what lets the data-driven test files stay tiny.
"""
import csv
import json
from pathlib import Path

import pytest

from order_calculator import Order

DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"
MONEY_TOLERANCE = 0.005  # half a cent; the CSV values are exact to the cent


def load_order_cases(filename="order_calculations.csv"):
    """Return a list of ``pytest.param`` rows, one per CSV record."""
    cases = []
    with open(DATA_DIR / filename, newline="") as handle:
        for row in csv.DictReader(handle):
            code = row["discount_code"]
            cases.append(pytest.param(
                {
                    "items": json.loads(row["items"]),
                    "customer_type": row["customer_type"],
                    "discount_code": None if code == "NONE" else code,
                    "distance": float(row["distance_km"]),
                    "is_express": row["is_express"] == "true",
                    "expected": {key: float(row[f"expected_{key}"]) for key in
                                 ("subtotal", "discount", "tax", "shipping", "total")},
                    "expected_error": row.get("expected_error") or "",
                },
                id=row["test_name"],
            ))
    return cases


def run_order_case(case):
    """Build the order described by ``case`` and check every component."""
    if case["expected_error"]:
        with pytest.raises(ValueError):
            Order(case["items"], case["customer_type"])
        return

    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance"], case["is_express"])
    result = order.calculate_total()

    for key, expected in case["expected"].items():
        assert result[key] == pytest.approx(expected, abs=MONEY_TOLERANCE), \
            f"{key} mismatch: got {result[key]}, expected {expected}"
