"""Data-driven tests for customer validation using JSON test data."""

import json
from pathlib import Path
import pytest
from customer_validator import (
    validate_customer,
    validate_email,
    validate_phone,
    validate_luhn,
    validate_expiration,
    validate_cvv,
)

BASE_DIR = Path(__file__).resolve().parent.parent
CUSTOMER_JSON_PATH = BASE_DIR / "test_data" / "customer_validation.json"


def load_customer_test_data():
    """Load customer validation test cases from JSON."""
    raw_data = json.loads(CUSTOMER_JSON_PATH.read_text(encoding="utf-8"))
    return [
        (entry["test_name"], entry["customer"], entry["expected"])
        for entry in raw_data
    ]


CUSTOMER_TEST_CASES = load_customer_test_data()


@pytest.mark.parametrize(
    "test_name,customer,expected",
    CUSTOMER_TEST_CASES,
    ids=[case[0] for case in CUSTOMER_TEST_CASES],
)
def test_customer_validation_from_json(test_name, customer, expected):
    """Test customer validation against JSON dataset."""
    result = validate_customer(customer)
    assert result["is_valid"] is expected["is_valid"], f"{test_name}: is_valid mismatch"
    for expected_err in expected["errors"]:
        assert expected_err in result["errors"], f"{test_name}: missing error '{expected_err}'"
    assert len(result["errors"]) == len(expected["errors"]), f"{test_name}: error count mismatch"


@pytest.mark.parametrize(
    "func,invalid_value",
    [
        (validate_email, None),
        (validate_phone, 1234567890),
        (validate_luhn, None),
        (validate_expiration, None),
        (validate_cvv, 123),
    ],
    ids=["email_none", "phone_int", "luhn_none", "expiration_none", "cvv_int"],
)
def test_validator_non_string_inputs(func, invalid_value):
    """Verify individual validators return False on non-string types."""
    assert func(invalid_value) is False


def test_validate_customer_non_dict():
    """Verify validate_customer handles non-dict input gracefully."""
    result = validate_customer(None)
    assert result == {"is_valid": False, "errors": ["Invalid customer data"]}
