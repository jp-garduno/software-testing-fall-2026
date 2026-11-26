"""Customer validator tests: 37 cases from customer_validation.json plus unit tests for the rules."""

from datetime import date

import pytest
from src import validation_rules as rules
from src.customer_validator import validate_customer
from tests.data_loader import REFERENCE_DATE, load_customer_cases


@pytest.mark.parametrize("case", load_customer_cases())
def test_validate_customer_from_json_returns_expected_result(case):
    result = validate_customer(case["customer"], today=REFERENCE_DATE)

    assert result == case["expected"]


def test_validate_customer_non_dict_input_reports_all_errors():
    result = validate_customer(None, today=REFERENCE_DATE)

    assert (result["is_valid"], len(result["errors"])) == (False, 9)


def test_validate_customer_without_today_uses_real_date_and_rejects_year_2000_card():
    customer = {
        "credit_card": {
            "number": "4111111111111111",
            "expiration": "01/2000",
            "cvv": "123",
        }
    }

    result = validate_customer(customer)

    assert "Credit card expired" in result["errors"]


def test_validate_customer_non_dict_sections_are_treated_as_missing():
    result = validate_customer(
        {"billing_address": "x", "credit_card": 5}, today=REFERENCE_DATE
    )

    assert (
        "Invalid street address" in result["errors"]
        and "Invalid credit card number" in result["errors"]
    )


@pytest.mark.parametrize("value", [None, 123, ["a@b.com"]])
def test_rules_non_string_values_are_invalid(value):
    checks = [
        rules.is_valid_email,
        rules.is_valid_phone,
        rules.is_non_empty_text,
        rules.is_valid_state,
        rules.is_valid_zip,
        rules.is_valid_card_number,
        rules.is_valid_cvv,
    ]

    assert not any(check(value) for check in checks)


def test_rules_email_consecutive_dots_is_invalid():
    assert rules.is_valid_email("john..doe@example.com") is False


@pytest.mark.parametrize(
    "number, expected", [("4111111111111111", True), ("4111111111111112", False)]
)
def test_luhn_check_known_numbers_returns_expected(number, expected):
    assert rules.luhn_check(number) is expected


def test_parse_expiration_valid_value_returns_month_and_year():
    assert rules.parse_expiration("03/2031") == (3, 2031)


def test_parse_expiration_non_string_returns_none():
    assert rules.parse_expiration(None) is None


@pytest.mark.parametrize(
    "month, year, expected",
    [(1, 2026, False), (12, 2025, True), (2, 2026, False), (1, 2027, False)],
)
def test_is_expired_relative_to_january_2026(month, year, expected):
    assert rules.is_expired(month, year, date(2026, 1, 31)) is expected
