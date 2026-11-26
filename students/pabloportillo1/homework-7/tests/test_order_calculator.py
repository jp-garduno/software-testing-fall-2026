import re
from datetime import date

import pytest

from src.order_calculator import Order
from tests.order_cases import build_order, order_params
from tools.data_files import TEST_DATA_DIR, load_order_cases

CASES = load_order_cases(TEST_DATA_DIR / "order_calculations.csv")
VALID_CASES = [case for case in CASES if case.expected_error is None]
INVALID_CASES = [case for case in CASES if case.expected_error is not None]


@pytest.mark.parametrize("case", order_params(VALID_CASES))
def test_calculate_total_valid_order_returns_expected_breakdown(case):
    assert build_order(case).calculate_total() == case.expected


@pytest.mark.parametrize("case", order_params(VALID_CASES))
def test_component_methods_valid_order_match_expected_breakdown(case):
    order = build_order(case)

    components = {
        "subtotal": order.calculate_subtotal(),
        "discount": order.calculate_discount(),
        "tax": order.calculate_tax(),
        "shipping": order.calculate_shipping(),
    }

    assert components == {name: case.expected[name] for name in components}


@pytest.mark.parametrize("case", order_params(INVALID_CASES))
def test_build_order_invalid_data_raises_value_error(case):
    with pytest.raises(ValueError, match=re.escape(case.expected_error)):
        build_order(case)


def test_apply_discount_rejected_code_keeps_previous_code():
    order = Order([{"name": "Lamp", "price": 60.0, "quantity": 1, "weight": 0}], order_date=date(2026, 11, 1))
    order.apply_discount("SAVE10")

    accepted = order.apply_discount("SAVE20")

    assert (accepted, order.discount_code) == (False, "SAVE10")
