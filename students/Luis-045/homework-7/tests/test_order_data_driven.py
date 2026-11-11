"""The same ten comparison scenarios loaded from the order CSV."""

import pytest

from .data_cases import configure_order, load_order_cases

COMPARISON_CASES = [case for case in load_order_cases() if case.comparison]


@pytest.mark.parametrize("case", COMPARISON_CASES, ids=lambda case: case.name)
def test_order_from_data(case):
    """Check the coupon result and all five amounts for each selected order."""
    assert configure_order(case).calculate_total() == case.expected
