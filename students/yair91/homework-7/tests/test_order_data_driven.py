"""Data-driven version: the same ten scenarios, one single test.

This is the other half of the Part 3 comparison. The scenarios are picked by
name from order_calculations.csv, so adding an eleventh means adding its name
to the list, not writing another function.
"""

import pytest

from conftest import build_order, order_cases

ONE_CENT = 0.005

SCENARIOS = [
    "simple_single_item",
    "simple_two_products",
    "discount_save10_at_minimum",
    "discount_save10_below_minimum",
    "discount_save20_at_minimum",
    "discount_invalid_code",
    "discount_newuser_for_new_customer",
    "shipping_weight_and_distance",
    "shipping_express_multiplies",
    "shipping_freeship_waives_cost",
]

CASES = [case for case in order_cases() if case["test_name"] in SCENARIOS]


def test_the_ten_scenarios_exist_in_the_csv():
    """If someone renames a CSV row this complains instead of skipping it."""
    assert sorted(case["test_name"] for case in CASES) == sorted(SCENARIOS)


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["test_name"])
def test_order_breakdown(case):
    """The five amounts of every scenario, read from the CSV."""
    breakdown = build_order(case).calculate_total()

    for key, expected in case["expected"].items():
        assert breakdown[key] == pytest.approx(expected, abs=ONE_CENT), f"{key} in {case['test_name']}"
