"""
Test suite for Order Calculator using data-driven testing with CSV.
"""

import os
import csv
import json
import pytest
from src.order_calculator import Order


def load_order_test_data():
    """Load test cases from CSV file using robust absolute path resolution."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, "test_data", "order_calculations.csv")

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
    load_order_test_data(),
    ids=lambda val: val if isinstance(val, str) and len(val) < 40 else "",
)
def test_order_calculation(test_name, items, customer_type, discount_code,
                           distance, is_express, exp_subtotal, exp_discount,
                           exp_tax, exp_shipping, exp_total):
    """Data-driven test for order calculations from CSV."""
    order = Order(items, customer_type)

    if discount_code:
        applied = order.apply_discount(discount_code)
        if exp_discount > 0:
            assert applied is True, f"{test_name}: Discount '{discount_code}' should have been applied"

    order.set_shipping(distance, is_express)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(exp_subtotal, abs=0.02), f"{test_name}: Subtotal mismatch"
    assert result["discount"] == pytest.approx(exp_discount, abs=0.02), f"{test_name}: Discount mismatch"
    assert result["tax"] == pytest.approx(exp_tax, abs=0.02), f"{test_name}: Tax mismatch"
    assert result["shipping"] == pytest.approx(exp_shipping, abs=0.02), f"{test_name}: Shipping mismatch"
    assert result["total"] == pytest.approx(exp_total, abs=0.02), f"{test_name}: Total mismatch"


def test_order_validation_invalid_customer_type():
    """Ensure invalid customer_type raises ValueError."""
    with pytest.raises(ValueError, match="Invalid customer type"):
        Order([], customer_type="vip")


def test_order_validation_negative_item_values():
    """Ensure negative price, quantity, or weight raise ValueError."""
    with pytest.raises(ValueError, match="Negative price"):
        Order([{"name": "Bad", "price": -5.0, "quantity": 1, "weight": 1.0}])

    with pytest.raises(ValueError, match="Negative quantity"):
        Order([{"name": "Bad", "price": 10.0, "quantity": -1, "weight": 1.0}])

    with pytest.raises(ValueError, match="Negative weight"):
        Order([{"name": "Bad", "price": 10.0, "quantity": 1, "weight": -0.5}])


def test_order_validation_negative_distance():
    """Ensure negative distance raises ValueError."""
    order = Order([])
    with pytest.raises(ValueError, match="Distance cannot be negative"):
        order.set_shipping(-10.0)

