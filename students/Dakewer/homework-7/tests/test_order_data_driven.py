"""Data-driven approach: the same 10 scenarios, loaded from CSV."""
import pytest

from data_loader import load_order_cases, run_order_case


@pytest.mark.parametrize("case", load_order_cases("comparison_cases.csv"))
def test_order_scenario(case):
    run_order_case(case)
