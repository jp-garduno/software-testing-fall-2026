"""Data-driven tests for the customer validator. Scenarios live in test_data/customer_validation.json."""

import pytest
from data_loader import REFERENCE_DATE, case_date, load_customer_cases

from customer_validator import (
    is_valid_cvv,
    is_valid_email,
    luhn_is_valid,
    normalize_card_number,
    validate_customer,
    validate_expiration,
)


@pytest.mark.parametrize("case", load_customer_cases())
def test_customer_validation(case):
    """Validity and the exact list of error messages match the JSON expectation."""
    result = validate_customer(case["customer"], today=case_date(case))
    assert result == case["expected"]


@pytest.mark.parametrize("case", load_customer_cases())
def test_is_valid_is_consistent_with_errors(case):
    """Invariant checked on every data row: a customer is valid exactly when there are no errors."""
    result = validate_customer(case["customer"], today=case_date(case))
    assert result["is_valid"] == (not result["errors"])


@pytest.mark.parametrize("number", ["4111111111111111", "5555555555554444", "378282246310005", "4532015112830366"])
def test_luhn_accepts_known_valid_numbers(number):
    assert luhn_is_valid(number) is True


@pytest.mark.parametrize("number", ["4111111111111112", "1234567890123456", "", "4111x11111111111"])
def test_luhn_rejects_invalid_numbers(number):
    assert luhn_is_valid(number) is False


def test_normalize_card_number_strips_spaces_and_hyphens():
    assert normalize_card_number("4111-1111 1111-1111") == "4111111111111111"


def test_normalize_card_number_ignores_non_strings():
    assert normalize_card_number(4111111111111111) == ""


@pytest.mark.parametrize("value", [None, 123, ["a@b.com"]])
def test_non_string_email_is_invalid(value):
    assert is_valid_email(value) is False


def test_overlong_email_is_invalid():
    assert is_valid_email("a" * 250 + "@example.com") is False


def test_cvv_length_depends_on_the_card_brand():
    assert is_valid_cvv("1234", "378282246310005") is True
    assert is_valid_cvv("123", "4111111111111111") is True
    assert is_valid_cvv("1234", "4111111111111111") is False


def test_non_ascii_digits_are_not_a_valid_cvv():
    assert is_valid_cvv("١٢٣", "4111111111111111") is False


def test_expiration_is_valid_through_the_end_of_its_month():
    assert validate_expiration("06/2026", REFERENCE_DATE) is None
    assert validate_expiration("05/2026", REFERENCE_DATE) == "Credit card expired"


def test_today_defaults_to_the_current_date():
    far_future = {"credit_card": {"number": "4111111111111111", "expiration": "12/2999", "cvv": "123"}}
    assert "Credit card expired" not in validate_customer(far_future)["errors"]
