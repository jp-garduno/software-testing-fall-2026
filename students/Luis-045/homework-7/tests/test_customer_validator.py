"""Check customer validation against the independent JSON expectations."""

import json
from datetime import date
from pathlib import Path

import pytest

from src.customer_validator import validate_customer

DATA_PATH = (
    Path(__file__).resolve().parents[1] / "test_data" / "customer_validation.json"
)
with DATA_PATH.open(encoding="utf-8") as file:
    DATA = json.load(file)
REFERENCE_DATE = date(2026, 11, 10)


@pytest.mark.parametrize(
    "case",
    DATA,
    ids=lambda case: case["test_name"],
)
def test_customer_validation(case):
    """Compare validity and the full, ordered list of errors."""
    assert validate_customer(case["customer"], today=REFERENCE_DATE) == case["expected"]
