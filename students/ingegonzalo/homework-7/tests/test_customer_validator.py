from datetime import date

import pytest

from src.customer_validator import check_expiration, luhn_check, validate_customer
from data_loader import load_customer_cases

FIXED_TODAY = date(2026, 1, 15)  # fecha fija => tests deterministas


@pytest.mark.parametrize("case", load_customer_cases())
def test_customer_validation(case):
    result = validate_customer(case["customer"], today=FIXED_TODAY)
    assert result["is_valid"] == case["expected"]["is_valid"]
    assert result["errors"] == case["expected"]["errors"]


def test_json_has_minimum_cases():
    assert len(load_customer_cases()) >= 30


@pytest.mark.parametrize(
    "number,expected",
    [
        ("4532015112830366", True),
        ("4111111111111111", True),
        ("5500000000000004", True),
        ("378282246310005", True),
        ("4111111111111112", False),
        ("", False),
        ("abcd", False),
    ],
)
def test_luhn_check(number, expected):
    assert luhn_check(number) is expected


def test_card_valid_through_end_of_current_month():
    assert check_expiration("01/2026", FIXED_TODAY) is None
    assert check_expiration("12/2025", FIXED_TODAY) == "Credit card expired"


def test_empty_customer_reports_every_field():
    result = validate_customer({}, today=FIXED_TODAY)
    assert result["is_valid"] is False
    assert len(result["errors"]) == 9


def test_default_today_is_used():
    valid = {
        "email": "a@b.com", "phone": "(555) 123-4567",
        "billing_address": {"street": "1 A St", "city": "X", "state": "CA", "zip": "90001"},
        "credit_card": {"number": "4111111111111111", "expiration": "12/2099", "cvv": "123"},
    }
    assert validate_customer(valid)["is_valid"] is True