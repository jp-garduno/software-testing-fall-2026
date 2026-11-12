"""Customer validation cases loaded from JSON."""

from datetime import date

import pytest
from customer_validator import validate_customer
from data_loaders import load_customer_cases


@pytest.mark.parametrize(
    "case", load_customer_cases(), ids=lambda case: case["test_name"]
)
def test_customer_validation_from_json(case):
    result = validate_customer(case["customer"], today=date(2026, 11, 11))
    assert result == case["expected"]


def test_expiration_is_valid_through_the_last_day_of_the_expiration_month():
    case = {
        "email": "alex@example.com",
        "phone": "(555) 123-4567",
        "billing_address": {
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
        },
        "credit_card": {
            "number": "4111111111111111",
            "expiration": "11/2026",
            "cvv": "123",
        },
    }
    assert validate_customer(case, today=date(2026, 11, 30)) == {
        "is_valid": True,
        "errors": [],
    }


def test_non_string_expiration_is_invalid():
    customer = load_customer_cases()[0]["customer"]
    customer["credit_card"]["expiration"] = None
    result = validate_customer(customer, today=date(2026, 11, 11))
    assert result == {
        "is_valid": False,
        "errors": ["Invalid credit card expiration"],
    }


def test_invalid_top_level_values_return_validation_errors():
    result = validate_customer(None, today=date(2026, 11, 11))
    assert result == {
        "is_valid": False,
        "errors": [
            "Invalid email format",
            "Invalid phone format",
            "Invalid billing address",
            "Invalid credit card",
        ],
    }
