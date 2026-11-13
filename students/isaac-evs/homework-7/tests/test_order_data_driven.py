"""Data-driven version of the same 10 order tests; the scenarios live in test_data/comparison_orders.csv."""

import pytest
from data_loader import COMPONENTS, DATA_DIR, load_order_cases, run_order_case


@pytest.mark.parametrize("case", load_order_cases(DATA_DIR / "comparison_orders.csv"))
def test_order_calculation(case):
    result = run_order_case(case)
    for component in COMPONENTS:
        assert result[component] == pytest.approx(case["expected"][component], abs=0.005)
