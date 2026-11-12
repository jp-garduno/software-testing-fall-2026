"""Data-driven tests for the order calculator (Part 1).

The cases live in test_data/order_calculations.csv; this file only knows how
to run one. Cases with an ``expected_error`` must raise ValueError, every
other case must produce the expected breakdown to the cent.
"""

from collections import Counter
from datetime import date

import pytest

from src.data_loader import load_order_cases
from src.order_calculator import Order

ORDER_CASES = load_order_cases()
PRICED_CASES = [case for case in ORDER_CASES if case.expected_error is None]
ERROR_CASES = [case for case in ORDER_CASES if case.expected_error is not None]

# Minimum number of cases per category the assignment asks for.
REQUIRED_PER_CATEGORY = {"simple": 3, "discount": 5, "tax": 4, "shipping": 6, "complex": 7}


def build_order(case):
    """Create, discount and ship an order the way a checkout would."""
    order = Order(case.items, case.customer_type)
    if case.discount_code:
        order.apply_discount(case.discount_code)
    order.set_shipping(case.distance_km, case.is_express)
    return order


@pytest.mark.parametrize("case", PRICED_CASES, ids=lambda case: case.test_name)
def test_order_calculation(case):
    result = build_order(case).calculate_total()

    for component, expected in case.expected.items():
        assert result[component] == pytest.approx(expected, abs=0.001), \
            f"{case.test_name}: {component} is {result[component]}, expected {expected}"


@pytest.mark.parametrize("case", PRICED_CASES, ids=lambda case: case.test_name)
def test_individual_calculations_match_breakdown(case):
    order = build_order(case)

    assert order.calculate_subtotal() == pytest.approx(case.expected["subtotal"], abs=0.001)
    assert order.calculate_discount() == pytest.approx(case.expected["discount"], abs=0.001)
    assert order.calculate_tax() == pytest.approx(case.expected["tax"], abs=0.001)
    assert order.calculate_shipping() == pytest.approx(case.expected["shipping"], abs=0.001)


@pytest.mark.parametrize("case", ERROR_CASES, ids=lambda case: case.test_name)
def test_invalid_order_is_rejected(case):
    with pytest.raises(ValueError, match=case.expected_error):
        build_order(case)


@pytest.mark.parametrize("category,minimum", REQUIRED_PER_CATEGORY.items())
def test_data_file_meets_minimum_cases_per_category(category, minimum):
    assert Counter(case.category for case in ORDER_CASES)[category] >= minimum


def test_data_file_has_at_least_25_cases():
    assert len(ORDER_CASES) >= 25


# The return value of apply_discount is not visible in the CSV breakdown, so it
# gets its own table: (code, subtotal, customer_type, accepted).
DISCOUNT_ACCEPTANCE = [
    ("SAVE10", 50, "regular", True),
    ("SAVE10", 49.99, "regular", False),
    ("SAVE20", 100, "regular", True),
    ("SAVE20", 99.99, "regular", False),
    ("FREESHIP", 1, "regular", True),
    ("NEWUSER", 10, "new", True),
    ("NEWUSER", 10, "regular", False),
    ("  save20 ", 150, "regular", True),
    ("BOGUS", 500, "regular", False),
    ("", 500, "regular", False),
    (None, 500, "regular", False),
]


@pytest.mark.parametrize("code,subtotal,customer_type,accepted", DISCOUNT_ACCEPTANCE)
def test_apply_discount_return_value(code, subtotal, customer_type, accepted):
    order = Order([{"name": "Thing", "price": subtotal, "quantity": 1, "weight": 0}], customer_type)
    assert order.apply_discount(code) is accepted


@pytest.mark.parametrize("on_date,accepted", [
    (date(2025, 8, 31), True),
    (date(2025, 9, 1), False),
])
def test_campaign_code_is_valid_through_its_expiration_day(on_date, accepted):
    order = Order([{"name": "Thing", "price": 20, "quantity": 1, "weight": 0}])
    assert order.apply_discount("SUMMER25", on_date) is accepted


def test_rejected_code_keeps_previous_discount():
    order = Order([{"name": "Thing", "price": 120, "quantity": 1, "weight": 0}])
    order.apply_discount("SAVE20")
    order.apply_discount("BOGUS")
    assert order.discount_code == "SAVE20"


def test_accepted_code_replaces_previous_one():
    order = Order([{"name": "Thing", "price": 120, "quantity": 1, "weight": 0}])
    order.apply_discount("SAVE20")
    order.apply_discount("FREESHIP")
    assert order.calculate_total()["discount"] == 0


@pytest.mark.parametrize("items,customer_type,message", [
    ([{"name": "A", "price": 1, "quantity": 1}], "regular", "missing fields: weight"),
    ([{"name": "A", "price": "10", "quantity": 1, "weight": 0}], "regular", "price must be a number"),
    ([{"name": "A", "price": True, "quantity": 1, "weight": 0}], "regular", "price must be a number"),
    ([], "vip", "Unknown customer type"),
])
def test_malformed_order_raises(items, customer_type, message):
    with pytest.raises(ValueError, match=message):
        Order(items, customer_type)
