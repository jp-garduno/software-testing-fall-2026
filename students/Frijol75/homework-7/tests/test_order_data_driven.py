"""
Data-Driven Version of the 10 Comparison Tests.

Tests the exact same 10 scenarios as test_order_traditional.py, but loads
the data dynamically from CSV using @pytest.mark.parametrize.
"""

import os
import csv
import json
import pytest
from src.order_calculator import Order


def load_10_comparison_cases():
    """Load the 10 comparison test cases from CSV."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, "test_data", "comparison_10_cases.csv")

    test_data = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items = json.loads(row["items"].replace("'", '"'))
            test_data.append((
                row["test_name"],
                items,
                row["customer_type"],
                row["discount_code"] if row["discount_code"] != "NONE" else None,
                float(row["distance_km"]),
                str(row["is_express"]).strip().lower() == "true",
                float(row["expected_subtotal"]),
                float(row["expected_discount"]),
                float(row["expected_tax"]),
                float(row["expected_shipping"]),
                float(row["expected_total"]),
            ))
    return test_data


@pytest.mark.parametrize(
    "test_name,items,customer_type,discount_code,distance,is_express,"
    "exp_subtotal,exp_discount,exp_tax,exp_shipping,exp_total",
    load_10_comparison_cases(),
    ids=lambda val: val if isinstance(val, str) else "",
)
def test_order_data_driven_comparison(test_name, items, customer_type, discount_code,
                                      distance, is_express, exp_subtotal, exp_discount,
                                      exp_tax, exp_shipping, exp_total):
    """Single parameterized test function replacing 10 traditional test functions."""
    order = Order(items, customer_type)

    if discount_code:
        order.apply_discount(discount_code)

    order.set_shipping(distance, is_express)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(exp_subtotal, abs=0.01)
    assert result["discount"] == pytest.approx(exp_discount, abs=0.01)
    assert result["tax"] == pytest.approx(exp_tax, abs=0.01)
    assert result["shipping"] == pytest.approx(exp_shipping, abs=0.01)
    assert result["total"] == pytest.approx(exp_total, abs=0.01)

