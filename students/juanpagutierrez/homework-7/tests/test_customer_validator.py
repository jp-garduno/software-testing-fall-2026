"""Data-driven tests for the customer validator (Part 2).

The cases live in test_data/customer_validation.json. Each one carries its
own reference date so expiration checks give the same answer on any day.
"""

from collections import Counter
from datetime import date

import pytest

from src.customer_validator import is_valid_card_number, luhn_check, validate_customer
from src.data_loader import load_customer_cases

CUSTOMER_CASES = load_customer_cases()

# Minimum number of cases per category the assignment asks for.
REQUIRED_PER_CATEGORY = {
    "valid": 3, "invalid_email": 4, "invalid_phone": 4, "invalid_address": 5, "invalid_card": 8,
    "multiple_errors": 6,
}


@pytest.mark.parametrize("case", CUSTOMER_CASES, ids=lambda case: case.test_name)
def test_customer_validation(case):
    result = validate_customer(case.customer, case.reference_date)

    assert result["is_valid"] is case.expected_valid, f"{case.test_name}: {case.description}"
    assert result["errors"] == case.expected_errors


@pytest.mark.parametrize("category,minimum", REQUIRED_PER_CATEGORY.items())
def test_data_file_meets_minimum_cases_per_category(category, minimum):
    assert Counter(case.category for case in CUSTOMER_CASES)[category] >= minimum


def test_data_file_has_at_least_30_cases():
    assert len(CUSTOMER_CASES) >= 30


@pytest.mark.parametrize("number,valid", [
    ("4532015112830366", True),
    ("79927398713", True),
    ("0", True),
    ("79927398710", False),
    ("4532015112830367", False),
    ("", False),
    ("12a4", False),
])
def test_luhn_check(number, valid):
    assert luhn_check(number) is valid


@pytest.mark.parametrize("number,valid", [
    ("4222222222222", True),
    ("4111 1111 1111 1111", True),
    ("6011-1111-1111-1117", True),
    (None, False),
    (4111111111111111, False),
])
def test_card_number_lengths_and_types(number, valid):
    assert is_valid_card_number(number) is valid


def test_expiration_defaults_to_today():
    customer = CUSTOMER_CASES[0].customer
    far_future = {**customer, "credit_card": {**customer["credit_card"], "expiration": f"12/{date.today().year + 5}"}}
    assert validate_customer(far_future)["is_valid"] is True


def test_non_string_fields_are_rejected_not_crashed():
    customer = {
        "email": 42,
        "phone": 5551234567,
        "billing_address": {"street": "1 A St", "city": 7, "state": "NY", "zip": 10001},
        "credit_card": {"number": "4532015112830366", "expiration": 122030, "cvv": 123},
    }
    assert validate_customer(customer, date(2026, 6, 15))["errors"] == [
        "Invalid email format", "Invalid phone format", "Invalid city", "Invalid ZIP code",
        "Invalid expiration date format", "Invalid CVV",
    ]
