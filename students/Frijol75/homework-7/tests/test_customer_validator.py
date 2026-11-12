"""
Test suite for Customer Validator using data-driven testing with JSON.
"""

import os
import json
from datetime import date
import pytest
from src.customer_validator import (
    validate_customer,
    validate_email,
    validate_phone,
    validate_address,
    validate_credit_card,
    luhn_check,
)


def load_customer_test_data():
    """Load test cases from customer_validation.json."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, "test_data", "customer_validation.json")

    with open(json_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    return [
        (case["test_name"], case["customer"], case["expected"])
        for case in cases
    ]


@pytest.mark.parametrize(
    "test_name,customer,expected",
    load_customer_test_data(),
    ids=lambda val: val if isinstance(val, str) else "",
)
def test_customer_validation(test_name, customer, expected):
    """Data-driven test evaluating customer validation from JSON."""
    ref_date = date(2026, 11, 1)
    result = validate_customer(customer, today=ref_date)

    assert result["is_valid"] == expected["is_valid"], f"{test_name}: is_valid mismatch"
    assert result["errors"] == expected["errors"], f"{test_name}: errors list mismatch"


def test_customer_validation_edge_cases():
    """Test defensive handling for invalid or null payload inputs."""
    assert validate_customer(None)["is_valid"] is False
    assert validate_customer("not a dict")["is_valid"] is False
    assert validate_email(None) == ["Missing email"]
    assert validate_phone(None) == ["Missing phone"]
    assert validate_address(None) == ["Missing billing address"]
    assert validate_address("invalid") == ["Missing billing address"]
    assert validate_credit_card(None) == ["Missing credit card"]
    assert validate_credit_card("invalid") == ["Missing credit card"]
    assert luhn_check("not_digits") is False

