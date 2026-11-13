"""Data-driven tests for the order calculator. Every scenario lives in test_data/order_calculations.csv."""

import re

import pytest

from data_loader import COMPONENTS, load_order_cases, run_order_case
from order_calculator import Order


@pytest.mark.parametrize("case", load_order_cases())
def test_order_calculation(case):
    """Each component of the breakdown matches the value stored in the CSV."""
    result = run_order_case(case)
    for component in COMPONENTS:
        assert result[component] == pytest.approx(case["expected"][component], abs=0.005), f"{component} mismatch"


@pytest.mark.parametrize("case", load_order_cases())
def test_total_is_the_sum_of_its_parts(case):
    """Invariant checked on every data row: total = subtotal - discount + tax + shipping."""
    result = run_order_case(case)
    parts = result["subtotal"] - result["discount"] + result["tax"] + result["shipping"]
    assert result["total"] == pytest.approx(parts, abs=0.005)


@pytest.mark.parametrize("case", load_order_cases(error_cases=True))
def test_invalid_input_is_rejected(case):
    """Rows with an expected_error must raise a ValueError containing that text."""
    with pytest.raises(ValueError, match=re.escape(case["expected_error"])):
        run_order_case(case)


def make_order(price=60.0, customer_type="regular"):
    """A one-item order used by the behaviour tests below."""
    return Order([{"name": "Item", "price": price, "quantity": 1, "weight": 1}], customer_type)


def test_apply_discount_reports_whether_the_code_was_accepted():
    order = make_order()
    assert order.apply_discount("SAVE10") is True
    assert order.apply_discount("NOPE") is False


def test_invalid_code_does_not_remove_a_previously_applied_code():
    order = make_order()
    order.apply_discount("SAVE10")
    order.apply_discount("NOPE")
    assert order.calculate_discount() == 6.0


def test_a_later_valid_code_replaces_the_earlier_one():
    order = make_order(price=120.0)
    order.apply_discount("SAVE10")
    order.apply_discount("SAVE20")
    assert order.calculate_discount() == 24.0


def test_individual_calculations_match_the_breakdown():
    order = make_order(price=100.0)
    order.apply_discount("SAVE20")
    order.set_shipping(40, is_express=True)
    breakdown = order.calculate_total()
    assert (order.calculate_subtotal(), order.calculate_discount(), order.calculate_tax(), order.calculate_shipping()) == (
        breakdown["subtotal"],
        breakdown["discount"],
        breakdown["tax"],
        breakdown["shipping"],
    )


def test_weight_defaults_to_zero_when_missing():
    order = Order([{"name": "Item", "price": 10, "quantity": 1}])
    assert order.calculate_shipping() == 0.0


@pytest.mark.parametrize("bad_price", ["10", None, True])
def test_non_numeric_price_is_rejected(bad_price):
    with pytest.raises(ValueError, match="price must be a number"):
        Order([{"name": "Item", "price": bad_price, "quantity": 1}])


def test_boolean_quantity_is_rejected():
    with pytest.raises(ValueError, match="quantity must be a whole number"):
        Order([{"name": "Item", "price": 10, "quantity": True}])
