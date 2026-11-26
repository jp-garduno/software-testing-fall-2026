"""Check calculator behavior using hand-written and generated CSV cases."""

import pytest

from src.order_calculator import Order
from tests.data_loader import order_cases
from tests.order_assertions import assert_order_case


@pytest.mark.parametrize("case", order_cases("order_calculations.csv"))
def test_order_calculation(case):
    """Check every amount, coupon result and expected rejection."""
    assert_order_case(case)


@pytest.mark.parametrize("case", order_cases("generated_orders.csv"))
def test_generated_order(case):
    """Run the seeded regression data through the same calculator assertions."""
    assert_order_case(case)


def test_rejected_replacement_leaves_valid_coupon_in_place():
    """A failed attempt to change the coupon leaves the current total intact."""
    order = Order([{"name": "Book", "price": 75, "quantity": 1, "weight": 1}])
    assert order.apply_discount("SAVE10") is True
    assert order.apply_discount("SAVE20") is False
    assert order.calculate_discount() == 7.50
    assert order.apply_discount("FREESHIP") is True
    assert order.calculate_discount() == 0.00


@pytest.mark.parametrize("distance", [None, float("inf"), float("nan")])
def test_invalid_shipping_distance_preserves_previous_shipping(distance):
    """Reject invalid distance values before changing the shipping state."""
    order = Order([])
    order.set_shipping(10)
    with pytest.raises(
        ValueError, match="distance must be a finite, nonnegative number"
    ):
        order.set_shipping(distance, is_express=True)
    assert order.calculate_shipping() == 1.00


def test_boolean_quantity_is_rejected():
    """Reject a boolean even though Python treats it as an integer subclass."""
    with pytest.raises(ValueError, match="quantity must be a nonnegative integer"):
        Order([{"name": "Pen", "price": 5, "quantity": True, "weight": 1}])
