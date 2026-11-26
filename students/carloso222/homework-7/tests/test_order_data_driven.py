"""Part 3 - DATA-DRIVEN version: the same 10 scenarios as test_order_traditional.py, loaded from the CSV."""

import pytest
from tests.data_loader import calculate_case, load_order_cases

SCENARIOS = [
    "simple_single_item",
    "discount_save10_above_min",
    "discount_save10_at_threshold_rejected",
    "discount_save20_above_min",
    "discount_invalid_code",
    "discount_newuser_new_customer",
    "tax_rounds_up_small_amount",
    "shipping_weight_and_distance",
    "shipping_express_multiplier",
    "shipping_freeship_code",
]


@pytest.mark.parametrize("case", load_order_cases(names=SCENARIOS))
def test_order_scenario_from_csv_returns_expected_breakdown(case):
    result = calculate_case(case)

    assert result == pytest.approx(case["expected"], abs=0.005)
