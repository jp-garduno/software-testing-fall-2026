import pytest

from tests.order_cases import build_order, order_params
from tools.data_files import TEST_DATA_DIR, load_order_cases

CASES = load_order_cases(TEST_DATA_DIR / "order_comparison.csv")


@pytest.mark.parametrize("case", order_params(CASES))
def test_calculate_total_returns_expected_breakdown(case):
    assert build_order(case).calculate_total() == case.expected
