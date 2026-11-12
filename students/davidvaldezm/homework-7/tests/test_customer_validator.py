"""Test customer validation with fixed dates and external JSON inputs."""

from datetime import date

import pytest

from src.customer_validator import validate_customer
from tests.data_loader import json_cases


@pytest.mark.parametrize("case", json_cases("customer_validation.json"))
def test_customer_validation(case):
    """Check both validity and the complete ordered error list."""
    assert (
        validate_customer(case["customer"], today=date.fromisoformat(case["as_of"]))
        == case["expected"]
    )
