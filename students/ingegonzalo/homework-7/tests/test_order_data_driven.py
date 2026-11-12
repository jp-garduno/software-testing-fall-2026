"""Version DATA-DRIVEN: los mismos 10 escenarios, datos cargados del CSV."""
import pytest

from data_loader import load_order_cases, run_order_case

SCENARIOS = {
    "simple_single_item", "simple_multiple_items", "save10_at_threshold",
    "save10_below_minimum", "save20_at_threshold", "invalid_code",
    "tax_rounding_up", "ship_weight_and_distance", "ship_express",
    "complex_save10_express",
}


@pytest.mark.parametrize("case", load_order_cases(SCENARIOS))
def test_order_data_driven(case):
    assert run_order_case(case) == pytest.approx(case["expected"], abs=0.01)


def test_all_ten_scenarios_loaded():
    assert len(load_order_cases(SCENARIOS)) == 10