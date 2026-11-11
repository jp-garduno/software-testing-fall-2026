"""Check the complete order breakdown and error cases defined in the CSV."""

import pytest

from src.order_calculator import Order

from .data_cases import configure_order, load_order_cases


@pytest.mark.parametrize("case", load_order_cases(), ids=lambda case: case.name)
def test_order_calculation(case):
    """Check every amount for accepted orders and the specific error for rejected inputs."""
    if case.error:
        with pytest.raises(ValueError) as error:
            configure_order(case)
        assert str(error.value) == case.error
        return

    order = configure_order(case)
    assert order.calculate_total() == case.expected
    assert order.calculate_subtotal() == case.expected["subtotal"]
    assert order.calculate_discount() == case.expected["discount"]
    assert order.calculate_tax() == case.expected["tax"]
    assert order.calculate_shipping() == case.expected["shipping"]


def test_only_one_valid_discount_can_be_applied():
    """A rejected code preserves the current coupon; an accepted code replaces it."""
    order = Order([{"name": "Book", "price": 50, "quantity": 1, "weight": 2}])
    assert order.apply_discount("SAVE10") is True
    assert order.apply_discount("SAVE20") is False
    assert order.calculate_discount() == 5
    assert order.apply_discount("FREESHIP") is True
    assert order.calculate_total() == {
        "subtotal": 50,
        "discount": 0,
        "tax": 4,
        "shipping": 0,
        "total": 54,
    }
