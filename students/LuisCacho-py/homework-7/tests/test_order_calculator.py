"""Data-driven tests for Order calculator using CSV test data."""

import csv
import json
from pathlib import Path
import pytest
from order_calculator import Order

BASE_DIR = Path(__file__).resolve().parent.parent
ORDER_CSV_PATH = BASE_DIR / "test_data" / "order_calculations.csv"


def load_order_test_data():
    """Load order calculation test cases from CSV."""
    test_data = []
    with ORDER_CSV_PATH.open("r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            items = json.loads(row["items"].replace("'", '"'))
            test_data.append(
                (
                    row["test_name"],
                    items,
                    row["customer_type"],
                    row["discount_code"] if row["discount_code"] != "NONE" else None,
                    float(row["distance_km"]),
                    row["is_express"].lower() == "true",
                    float(row["expected_subtotal"]),
                    float(row["expected_discount"]),
                    float(row["expected_tax"]),
                    float(row["expected_shipping"]),
                    float(row["expected_total"]),
                )
            )
    return test_data


ORDER_TEST_CASES = load_order_test_data()


@pytest.mark.parametrize(
    "test_name,items,customer_type,discount_code,distance,is_express,"
    "exp_subtotal,exp_discount,exp_tax,exp_shipping,exp_total",
    ORDER_TEST_CASES,
    ids=[case[0] for case in ORDER_TEST_CASES],
)
def test_order_calculation(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    test_name,
    items,
    customer_type,
    discount_code,
    distance,
    is_express,
    exp_subtotal,
    exp_discount,
    exp_tax,
    exp_shipping,
    exp_total,
):
    """Verify subtotal, discount, tax, shipping, and total for each CSV test case."""
    order = Order(items, customer_type)

    if discount_code:
        order.apply_discount(discount_code)

    order.set_shipping(distance, is_express)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(exp_subtotal, abs=1e-2), f"{test_name}: Subtotal mismatch"
    assert result["discount"] == pytest.approx(exp_discount, abs=1e-2), f"{test_name}: Discount mismatch"
    assert result["tax"] == pytest.approx(exp_tax, abs=1e-2), f"{test_name}: Tax mismatch"
    assert result["shipping"] == pytest.approx(exp_shipping, abs=1e-2), f"{test_name}: Shipping mismatch"
    assert result["total"] == pytest.approx(exp_total, abs=1e-2), f"{test_name}: Total mismatch"


def test_order_discount_state_changes():
    """Verify edge cases when discount state or items change after applying a code."""
    order = Order(None, "regular")
    assert order.calculate_subtotal() == 0.0
    assert order.apply_discount("") is False

    # Manually set discount_code to test defensive branches in calculate_discount
    order.items = [{"name": "Item", "price": 30.0, "quantity": 1, "weight": 1.0}]
    order.discount_code = "SAVE10"
    assert order.calculate_discount() == 0.0

    order.discount_code = "NEWUSER"
    assert order.calculate_discount() == 0.0
