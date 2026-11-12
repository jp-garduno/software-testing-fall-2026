import pytest

from data_loader import load_order_cases, run_order_case

CASES = load_order_cases(filename="generated_orders.csv")


@pytest.mark.parametrize("case", CASES)
def test_generated_order_regression(case):
    assert run_order_case(case) == pytest.approx(case["expected"], abs=0.01)


def test_generated_has_100_orders():
    assert len(CASES) == 100