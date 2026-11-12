"""Data-driven tests for the customer validator (cases live in the JSON)."""
import json
from datetime import date

import pytest

from customer_validator import (
    check_expiration, is_valid_email, luhn_check, validate_customer,
)
from data_loader import DATA_DIR

# Fixed "today" so results never depend on the real date.
REFERENCE_DATE = date(2025, 1, 15)

with open(DATA_DIR / "customer_validation.json") as handle:
    CASES = json.load(handle)


@pytest.mark.parametrize("case", CASES, ids=[c["test_name"] for c in CASES])
def test_customer_validation(case):
    result = validate_customer(case["customer"], today=REFERENCE_DATE)
    assert result["is_valid"] == case["expected"]["is_valid"]
    assert result["errors"] == case["expected"]["errors"]


def test_json_meets_minimum_counts():
    by_category = {}
    for case in CASES:
        by_category[case["category"]] = by_category.get(case["category"], 0) + 1
    assert len(CASES) >= 30
    minimums = {"valid": 3, "email": 4, "phone": 4, "address": 5,
                "credit_card": 8, "multiple": 6}
    for category, minimum in minimums.items():
        assert by_category.get(category, 0) >= minimum, category


# --- unit tests for helpers -------------------------------------------

@pytest.mark.parametrize("number,expected", [
    ("4532015112830366", True),
    ("378282246310005", True),
    ("4532015112830367", False),
    ("", False),
    ("12ab", False),
])
def test_luhn_check(number, expected):
    assert luhn_check(number) is expected


def test_email_with_dash_or_dot_edge_cases():
    assert not is_valid_email(".john@example.com")
    assert not is_valid_email("john.@example.com")
    assert not is_valid_email("john@-example.com")
    assert not is_valid_email(None)
    assert not is_valid_email("a" * 250 + "@example.com")


def test_expiration_month_boundaries():
    assert check_expiration("01/2025", REFERENCE_DATE) is None
    assert check_expiration("12/2024", REFERENCE_DATE) == "Credit card expired"
    assert check_expiration(None, REFERENCE_DATE) == "Invalid expiration date"


def test_expiration_defaults_to_real_today():
    assert check_expiration("01/1999") == "Credit card expired"


def test_non_dict_customer_raises():
    with pytest.raises(ValueError):
        validate_customer(None)


def test_wrong_types_inside_customer_are_invalid_not_crashes():
    result = validate_customer(
        {"email": 5, "phone": None, "billing_address": "home", "credit_card": []},
        today=REFERENCE_DATE,
    )
    assert result["is_valid"] is False
    assert len(result["errors"]) == 9
