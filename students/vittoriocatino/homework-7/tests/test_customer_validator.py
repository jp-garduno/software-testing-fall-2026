"""Validate whole error lists, including multiple simultaneous field errors."""

from datetime import date
from pathlib import Path

import pytest

from customer_validator import validate_customer
from data_loader import load_customers

DATA = Path(__file__).resolve().parents[1] / "test_data/customer_validation.json"


@pytest.mark.parametrize(
    "case", load_customers(DATA), ids=lambda case: case["test_name"]
)
def test_customer_validation(case):
    """Freeze the reference month to keep expiration cases deterministic."""
    assert (
        validate_customer(case["customer"], today=date(2026, 11, 10))
        == case["expected"]
    )
