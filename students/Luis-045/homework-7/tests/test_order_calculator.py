"""Check the complete order breakdown and error cases defined in the CSV."""

from pathlib import Path
from runpy import run_path

import pytest
from test_order_data_driven import ORDER_CASES, configure_order

from src.order_calculator import Order


@pytest.mark.parametrize("case", ORDER_CASES, ids=lambda case: case.name)
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


@pytest.mark.parametrize(
    ("items", "customer_type", "message"),
    [
        ([], "vip", "customer_type must be new or regular"),
        ({"name": "Book"}, "regular", "items must be a list"),
        (["Book"], "regular", "each item must be an object"),
        (
            [{"name": " ", "price": 25, "quantity": 1, "weight": 1}],
            "regular",
            "item name must be a non-empty string",
        ),
        (
            [{"name": "Book", "price": True, "quantity": 1, "weight": 1}],
            "regular",
            "price must be a finite non-negative number",
        ),
    ],
    ids=[
        "unknown_customer_type",
        "items_not_list",
        "item_not_object",
        "blank_name",
        "boolean_price",
    ],
)
def test_invalid_order_inputs(items, customer_type, message):
    """Reject malformed customer types and item data."""
    with pytest.raises(ValueError, match=message):
        Order(items, customer_type)


def test_invalid_express_flag_preserves_shipping():
    """Reject non-boolean express flags without changing shipping."""
    order = Order([{"name": "Book", "price": 25, "quantity": 1, "weight": 2}])
    order.set_shipping(10)

    with pytest.raises(ValueError, match="is_express must be a boolean"):
        order.set_shipping(40, is_express="false")

    assert order.calculate_shipping() == 2.0


def test_order_module_supports_direct_loading(monkeypatch):
    """Load the module with src on the import path and use its checkout."""
    src = Path(__file__).resolve().parents[1] / "src"
    monkeypatch.syspath_prepend(str(src))

    module = run_path(str(src / "order_calculator.py"))
    checkout = module["Checkout"]("direct")
    assert checkout.validate_customer({})["valid"] is False
