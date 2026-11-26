"""Data-driven tests for the order calculator (cases live in the CSV)."""
import pytest

from data_loader import load_order_cases, run_order_case
from order_calculator import Order


@pytest.mark.parametrize("case", load_order_cases())
def test_order_calculation(case):
    """One test per row of test_data/order_calculations.csv."""
    run_order_case(case)


def test_csv_meets_minimum_case_count():
    assert len(load_order_cases()) >= 25


# --- behaviour that does not fit the CSV shape -------------------------

def test_apply_discount_return_values():
    order = Order([{"name": "A", "price": 60, "quantity": 1, "weight": 0}])
    assert order.apply_discount("SAVE10") is True
    assert order.apply_discount("SAVE20") is False  # below $100 minimum
    assert order.apply_discount("NOPE") is False
    assert order.discount_code == "SAVE10"  # a rejected code keeps the previous one


def test_individual_calculation_methods():
    order = Order([{"name": "A", "price": 25, "quantity": 4, "weight": 1}])
    order.apply_discount("SAVE10")
    order.set_shipping(20, is_express=True)
    assert order.calculate_subtotal() == 100.00
    assert order.calculate_discount() == 10.00
    assert order.calculate_tax() == 7.20
    assert order.calculate_shipping() == 6.00  # (4*0.5 + 20*0.1) * 1.5


@pytest.mark.parametrize("items", [
    "not a list",
    ["not a dict"],
    [{"price": "10", "quantity": 1}],
    [{"price": 10}],
    [{"price": 10, "quantity": 1.5}],
    [{"price": 10, "quantity": True}],
    [{"price": 10, "quantity": 1, "weight": "heavy"}],
])
def test_malformed_items_raise(items):
    with pytest.raises(ValueError):
        Order(items)


def test_unknown_customer_type_raises():
    with pytest.raises(ValueError):
        Order([], customer_type="vip")


@pytest.mark.parametrize("distance", [-1, "far", None])
def test_invalid_distance_raises(distance):
    with pytest.raises(ValueError):
        Order([]).set_shipping(distance)
