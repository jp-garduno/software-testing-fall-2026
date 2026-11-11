"""State changes and malformed API inputs beyond the required datasets."""

from datetime import date
from pathlib import Path
from unittest.mock import Mock

import pytest

from customer_validator import validate_customer, valid_expiration
from data_loader import load_customers
from order_calculator import Order, nonnegative
from order_processor import OrderProcessor


@pytest.mark.parametrize("value", [None, "1", True, float("nan"), float("inf"), -1])
def test_numeric_inputs_must_be_finite_nonnegative_numbers(value):
    """Reject wrong types as well as values outside the numeric domain."""
    with pytest.raises(ValueError):
        nonnegative(value)


@pytest.mark.parametrize(
    "items",
    [
        None,
        [None],
        [{}],
        [{"name": "", "price": 1, "quantity": 1, "weight": 0}],
        [{"name": "x", "price": 1, "quantity": 1.5, "weight": 0}],
        [{"name": "x", "price": 1, "quantity": True, "weight": 0}],
    ],
)
def test_reject_malformed_items(items):
    """An invalid catalog item is never accepted as a valid order."""
    with pytest.raises(ValueError):
        Order(items)


def test_replacing_discount_never_stacks_previous_code():
    """An ineligible replacement clears a previously selected discount."""
    order = Order([{"name": "x", "price": 60, "quantity": 1, "weight": 1}])
    assert order.apply_discount("SAVE10") is True
    assert order.calculate_discount() == 6
    assert order.apply_discount("SAVE20") is False
    assert order.calculate_discount() == 0
    assert order.apply_discount(None) is False


def test_shipping_requires_boolean_service():
    """Do not treat the string 'false' as express truthiness."""
    with pytest.raises(ValueError):
        Order([]).set_shipping(10, "false")


def test_customer_missing_nested_fields_reports_all_errors():
    """Absent dictionaries produce field diagnostics instead of exceptions."""
    assert validate_customer({}, date(2026, 11, 10)) == {
        "is_valid": False,
        "errors": [
            "Invalid email format",
            "Invalid phone format",
            "Invalid billing street",
            "Invalid billing city",
            "Invalid billing state",
            "Invalid billing zip",
            "Invalid credit card number",
            "Invalid credit card expiration",
            "Invalid credit card CVV",
        ],
    }
    assert validate_customer(None) == {
        "is_valid": False,
        "errors": ["Invalid customer"],
    }


def test_expiration_boundary_includes_current_month():
    """Month comparison does not expire a card at the start of its month."""
    assert valid_expiration("11/2026", date(2026, 11, 30)) is True
    assert valid_expiration("10/2026", date(2026, 11, 1)) is False


def test_uncreated_order_cannot_be_charged():
    """No payment call occurs before an order exists."""
    payment = Mock()
    processor = OrderProcessor(payment, date(2026, 11, 10), "test")
    with pytest.raises(ValueError, match="Order not created"):
        processor.pay()
    payment.assert_not_called()


def test_create_order_without_optional_shipping_or_coupon():
    """Default order settings are usable after validating a customer."""
    customer = load_customers(
        Path(__file__).resolve().parents[1] / "test_data/customer_validation.json"
    )[0]["customer"]
    processor = OrderProcessor(Mock(), date(2026, 11, 10), "default")
    assert processor.validate(customer)["is_valid"] is True
    assert processor.create({"items": []}) == {"status": "created"}
    assert processor.total() == {
        "subtotal": 0,
        "discount": 0,
        "tax": 0,
        "shipping": 0,
        "total": 0,
    }
