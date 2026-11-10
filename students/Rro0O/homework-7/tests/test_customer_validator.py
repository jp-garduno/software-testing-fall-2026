"""Data-driven tests for customer validation (JSON) plus helper unit tests."""

from datetime import date

import pytest

from customer_validator import (
    ERR_EXP_FORMAT,
    ERR_EXPIRED,
    luhn_check,
    validate_address,
    validate_credit_card,
    validate_customer,
    validate_email,
    validate_expiration,
    validate_phone,
)
from data_loader import case_ids, load_customer_cases, parse_reference_date

CASES = load_customer_cases()


def test_json_has_required_volume():
    assert len(CASES) >= 30
    assert len({c["test_name"] for c in CASES}) == len(CASES), "duplicate test names"


@pytest.mark.parametrize("case", CASES, ids=case_ids(CASES))
def test_customer_validation(case):
    """Each JSON case: validity flag and the exact ordered list of errors."""
    today = parse_reference_date(case.get("reference_date"))
    result = validate_customer(case["customer"], today)
    assert result["is_valid"] == case["expected"]["is_valid"]
    assert result["errors"] == case["expected"]["errors"]


# ---- helper-level unit tests ------------------------------------------
@pytest.mark.parametrize("email", ["a@b.co", "first.last+tag@sub.example.org"])
def test_validate_email_accepts(email):
    assert validate_email(email)


@pytest.mark.parametrize("email", [None, 5, "a@b", "@b.com", "a b@c.com", "a@@b.com"])
def test_validate_email_rejects(email):
    assert not validate_email(email)


def test_validate_phone():
    assert validate_phone("(555) 123-4567")
    assert not validate_phone(None)
    assert not validate_phone("(555) 123-45678")


@pytest.mark.parametrize("number", ["4111111111111111", "5500005555555559", "378282246310005"])
def test_luhn_accepts_known_test_numbers(number):
    assert luhn_check(number)


@pytest.mark.parametrize(
    "number", [None, 4111111111111111, "", "abc", "4111111111111112", "0" * 12, "1" * 20]
)
def test_luhn_rejects(number):
    assert not luhn_check(number)


def test_expiration_same_month_valid_and_previous_month_expired():
    today = date(2026, 6, 15)
    assert validate_expiration("06/2026", today) is None
    assert validate_expiration("05/2026", today) == ERR_EXPIRED
    assert validate_expiration("06/2025", today) == ERR_EXPIRED
    assert validate_expiration("1/26", today) == ERR_EXP_FORMAT
    assert validate_expiration(None, today) == ERR_EXP_FORMAT


def test_expiration_defaults_to_real_today():
    assert validate_expiration("12/2999") is None
    assert validate_expiration("01/2000") == ERR_EXPIRED


def test_validate_address_non_dict():
    assert validate_address("nowhere") == ["Missing billing address"]
    assert validate_address({}) == ["Missing billing address"]


def test_validate_credit_card_non_dict():
    assert validate_credit_card(None) == ["Missing credit card"]
    assert validate_credit_card({}) == ["Missing credit card"]


def test_validate_customer_non_dict_reports_everything():
    result = validate_customer(None)
    assert result["is_valid"] is False
    assert result["errors"][0] == "Invalid email format"
    assert "Missing billing address" in result["errors"]
    assert "Missing credit card" in result["errors"]
