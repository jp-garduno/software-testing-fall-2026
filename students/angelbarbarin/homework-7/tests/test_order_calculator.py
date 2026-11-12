"""Data-driven tests for the order calculator (part 1).

Every case lives in test_data/order_calculations.csv; this file only knows how to run one.
Adding a scenario means adding a CSV row - no Python changes.
"""

from pathlib import Path

import pytest

from data_files import load_order_cases
from order_calculator import InvalidOrderError, Order

DATA_FILE = Path(__file__).resolve().parent.parent / "test_data" / "order_calculations.csv"
CASES = load_order_cases(DATA_FILE)
VALID_CASES = [case for case in CASES if case["expected_error"] is None]
ERROR_CASES = [case for case in CASES if case["expected_error"] is not None]


def build_order(case):
    """Create the order exactly as a customer would: items, discount code, then shipping."""
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance_km"], case["is_express"])
    return order


@pytest.mark.parametrize("case", VALID_CASES, ids=[case["test_name"] for case in VALID_CASES])
def test_order_calculation(case):
    result = build_order(case).calculate_total()

    for component in ("subtotal", "discount", "tax", "shipping", "total"):
        assert result[component] == pytest.approx(
            case["expected"][component], abs=0.005
        ), f"{case['test_name']}: {component} expected {case['expected'][component]}, got {result[component]}"


@pytest.mark.parametrize("case", ERROR_CASES, ids=[case["test_name"] for case in ERROR_CASES])
def test_order_rejects_invalid_data(case):
    with pytest.raises(InvalidOrderError, match=case["expected_error"]):
        build_order(case)


@pytest.mark.parametrize("case", VALID_CASES, ids=[case["test_name"] for case in VALID_CASES])
def test_individual_methods_match_breakdown(case):
    """calculate_subtotal/discount/tax/shipping must agree with calculate_total."""
    order = build_order(case)
    breakdown = order.calculate_total()

    assert order.calculate_subtotal() == breakdown["subtotal"]
    assert order.calculate_discount() == breakdown["discount"]
    assert order.calculate_tax() == breakdown["tax"]
    assert order.calculate_shipping() == breakdown["shipping"]


def test_data_file_meets_minimum_case_counts():
    """The assignment asks for 25+ cases and minimums per category."""
    minimums = {"simple": 3, "discount": 5, "tax": 4, "shipping": 6, "complex": 7}
    assert len(CASES) >= 25
    for category, minimum in minimums.items():
        assert sum(case["category"] == category for case in CASES) >= minimum, category


# --------------------------------------------------------------------------- #
# apply_discount return values and input validation (small inline tables)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "subtotal_price,customer_type,code,applied",
    [
        (50.00, "regular", "SAVE10", True),
        (49.99, "regular", "SAVE10", False),
        (100.00, "regular", "SAVE20", True),
        (99.99, "regular", "SAVE20", False),
        (1.00, "regular", "FREESHIP", True),
        (1.00, "new", "NEWUSER", True),
        (1.00, "regular", "NEWUSER", False),
        (80.00, "regular", " save10 ", True),
        (80.00, "regular", "SAVE30", False),
        (80.00, "regular", "", False),
        (80.00, "regular", None, False),
    ],
)
def test_apply_discount_return_value(subtotal_price, customer_type, code, applied):
    order = Order([{"name": "Item", "price": subtotal_price, "quantity": 1, "weight": 1}], customer_type)
    assert order.apply_discount(code) is applied


def test_invalid_code_keeps_previous_valid_code():
    order = Order([{"name": "Item", "price": 120, "quantity": 1, "weight": 1}])
    order.apply_discount("SAVE20")

    assert order.apply_discount("BOGUS") is False
    assert order.discount_code == "SAVE20"


@pytest.mark.parametrize(
    "items,customer_type,message",
    [
        ([], "vip", "Invalid customer type"),
        ("not a list", "regular", "Items must be a list"),
        (["laptop"], "regular", "Each item must be an object"),
        ([{"name": " ", "price": 1, "quantity": 1, "weight": 1}], "regular", "name is required"),
        ([{"name": "A", "price": "10", "quantity": 1, "weight": 1}], "regular", "price must be a number"),
        ([{"name": "A", "price": True, "quantity": 1, "weight": 1}], "regular", "price must be a number"),
        ([{"name": "A", "price": 1, "quantity": 1.5, "weight": 1}], "regular", "quantity must be a whole number"),
        ([{"name": "A", "price": 1, "quantity": True, "weight": 1}], "regular", "quantity must be a whole number"),
    ],
)
def test_invalid_order_input_is_rejected(items, customer_type, message):
    with pytest.raises(InvalidOrderError, match=message):
        Order(items, customer_type)


@pytest.mark.parametrize("distance", ["10", None, True])
def test_set_shipping_rejects_non_numeric_distance(distance):
    order = Order([{"name": "A", "price": 1, "quantity": 1, "weight": 1}])
    with pytest.raises(InvalidOrderError, match="Distance must be a number"):
        order.set_shipping(distance)


def test_item_defaults_quantity_one_and_weight_zero():
    order = Order([{"name": "Gift card", "price": 25}])
    order.set_shipping(10)

    assert order.calculate_subtotal() == 25.0
    assert order.calculate_shipping() == 5.0  # 4.00 base + 0 kg + 10 km x 0.10
