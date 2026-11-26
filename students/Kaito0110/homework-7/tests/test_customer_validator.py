"""Data-driven tests for Customer Validator using JSON test data."""

import json
from pathlib import Path

import pytest

from src.customer_validator import (
    validate_billing_address,
    validate_credit_card,
    validate_customer,
    validate_email,
    validate_phone,
)

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "test_data" / "customer_validation.json"


def load_customer_validation_data():
    """Load customer validation test cases from JSON."""
    with JSON_PATH.open("r", encoding="utf-8") as handle:
        cases = json.load(handle)
    return [
        (case["test_name"], case["customer"], case["expected"])
        for case in cases
    ]


@pytest.mark.parametrize(
    "test_name,customer_data,expected",
    load_customer_validation_data(),
    ids=lambda val: val if isinstance(val, str) else "",
)
def test_customer_validation_from_json(test_name, customer_data, expected):
    """Validate customer payload against expected validity and error list."""
    result = validate_customer(
        customer_data, reference_year=2025, reference_month=1
    )

    assert (
        result["is_valid"] == expected["is_valid"]
    ), f"{test_name}: is_valid mismatch"
    assert (
        result["errors"] == expected["errors"]
    ), f"{test_name}: errors mismatch"


def test_validator_handles_non_dict_and_non_string_inputs():
    """Verify defensive handling of non-dict payloads and non-string fields."""
    assert validate_email(None) is False
    assert validate_phone(1234567890) is False

    addr_ok, addr_errors = validate_billing_address(None)
    assert addr_ok is False
    assert addr_errors == ["Invalid billing address"]

    card_ok, card_errors = validate_credit_card("not-a-dict")
    assert card_ok is False
    assert card_errors == ["Invalid credit card information"]

    customer_res = validate_customer("invalid-payload")  # type: ignore[arg-type]
    assert customer_res == {
        "is_valid": False,
        "errors": ["Invalid customer payload"],
    }
