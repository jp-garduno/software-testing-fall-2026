"""Data-driven tests for customer validation (part 2).

Cases come from test_data/customer_validation.json. The whole error list is compared, so a
case also proves the validator does not report extra or misplaced errors.
"""

from collections import Counter
from datetime import date
from pathlib import Path

import pytest

from customer_validator import luhn_checksum_ok, validate_customer
from data_files import load_customer_cases

DATA_FILE = Path(__file__).resolve().parent.parent / "test_data" / "customer_validation.json"
CASES = load_customer_cases(DATA_FILE)


@pytest.mark.parametrize("case", CASES, ids=[case["test_name"] for case in CASES])
def test_customer_validation(case, reference_date):
    today = date.fromisoformat(case["today"]) if "today" in case else reference_date

    result = validate_customer(case["customer"], today)

    assert result.is_valid is case["expected"]["is_valid"]
    assert result.errors == case["expected"]["errors"]


def test_data_file_meets_minimum_case_counts():
    minimums = {
        "valid": 3,
        "invalid_email": 4,
        "invalid_phone": 4,
        "invalid_address": 5,
        "invalid_card": 8,
        "multiple_errors": 6,
    }
    counts = Counter(case["category"] for case in CASES)
    assert len(CASES) >= 30
    for category, minimum in minimums.items():
        assert counts[category] >= minimum, category


@pytest.mark.parametrize(
    "number,expected",
    [
        ("4532015112830366", True),
        ("4532015112830367", False),
        ("79927398713", True),  # textbook Luhn example
        ("0", True),
    ],
)
def test_luhn_checksum(number, expected):
    assert luhn_checksum_ok(number) is expected


@pytest.mark.parametrize("customer", [None, "john@example.com", []])
def test_non_dict_customer_reports_every_section_missing(customer, reference_date):
    result = validate_customer(customer, reference_date)
    assert result.errors == [
        "Email is required",
        "Phone is required",
        "Billing address is required",
        "Credit card is required",
    ]


def test_default_today_is_used_when_not_given():
    customer = CASES[0]["customer"]  # expires 12/2028
    assert validate_customer(customer).is_valid
