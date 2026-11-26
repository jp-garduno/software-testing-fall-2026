"""Data-driven version of the comparison suite (Part 3).

The same ten scenarios as test_order_traditional.py, read from
test_data/order_comparison.csv and run by one parameterized test.
"""

import pytest

from src.data_loader import load_order_cases
from src.data_validation import DATA_DIR
from src.order_calculator import Order


@pytest.mark.parametrize("case", load_order_cases(DATA_DIR / "order_comparison.csv"), ids=lambda case: case.test_name)
def test_order_total(case):
    order = Order(case.items, case.customer_type)
    if case.discount_code:
        order.apply_discount(case.discount_code)
    order.set_shipping(case.distance_km, case.is_express)
    result = order.calculate_total()
    for component, expected in case.expected.items():
        assert result[component] == pytest.approx(expected), f"{case.test_name}: {component}"
