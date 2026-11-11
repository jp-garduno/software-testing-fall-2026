"""Check customer validation against the independent JSON expectations."""

from datetime import date

import pytest

from src.customer_validator import validate_customer

from .data_cases import load_json_cases

REFERENCE_DATE = date(2026, 11, 10)


@pytest.mark.parametrize(
    "case",
    load_json_cases("customer_validation.json"),
    ids=lambda case: case["test_name"],
)
def test_customer_validation(case):
    """Compare validity and the full, ordered list of errors."""
    assert validate_customer(case["customer"], today=REFERENCE_DATE) == case["expected"]
