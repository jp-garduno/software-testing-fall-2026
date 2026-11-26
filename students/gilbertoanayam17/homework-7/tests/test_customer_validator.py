"""Part 2: every entry of customer_validation.json is one customer validation test."""

import pytest

from case_loaders import REFERENCE_DATE, load_customer_cases
from customer_validator import validate_customer


@pytest.mark.parametrize("case", load_customer_cases("customer_validation.json"))
def test_customer_validation(case):
    """The verdict and the full, ordered list of error messages must match."""
    result = validate_customer(case["customer"], today=REFERENCE_DATE)

    assert result == case["expected"]
