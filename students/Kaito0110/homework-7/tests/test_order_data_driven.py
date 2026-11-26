"""Part 3: Data-driven version of the 10 comparison order tests."""

# pylint: disable=duplicate-code

from pathlib import Path

import pytest

from src.order_calculator import Order
from tests.test_order_calculator import load_order_test_data

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "test_data" / "order_calculations.csv"

COMPARISON_TEST_NAMES = {
    "simple_single_item_zero_distance",
    "simple_two_items_zero_shipping",
    "simple_regular_order_with_shipping",
    "discount_save10_at_min_threshold",
    "discount_save10_below_threshold",
    "discount_save20_at_min_threshold",
    "discount_newuser_valid_for_new_customer",
    "shipping_express_multiplier_applied",
    "shipping_freeship_code_standard",
    "complex_multi_item_express_save20",
}


def load_ten_comparison_cases():
    """Filter the 10 benchmark cases from the shared CSV dataset."""
    return [
        case
        for case in load_order_test_data(CSV_PATH)
        if case[0] in COMPARISON_TEST_NAMES
    ]


# pylint: disable=too-many-arguments,too-many-positional-arguments
@pytest.mark.parametrize(
    "test_name,items,customer_type,discount_code,distance,is_express,"
    "exp_subtotal,exp_discount,exp_tax,exp_shipping,exp_total",
    load_ten_comparison_cases(),
    ids=lambda val: val if isinstance(val, str) else "",
)
def test_order_data_driven_ten_cases(
    test_name,
    items,
    customer_type,
    discount_code,
    distance,
    is_express,
    exp_subtotal,
    exp_discount,
    exp_tax,
    exp_shipping,
    exp_total,
):
    """Run the 10 benchmark order test cases via parameterization."""
    order = Order(items, customer_type)
    if discount_code:
        order.apply_discount(discount_code)
    order.set_shipping(distance, is_express)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(exp_subtotal, abs=1e-2), test_name
    assert result["discount"] == pytest.approx(exp_discount, abs=1e-2), test_name
    assert result["tax"] == pytest.approx(exp_tax, abs=1e-2), test_name
    assert result["shipping"] == pytest.approx(exp_shipping, abs=1e-2), test_name
    assert result["total"] == pytest.approx(exp_total, abs=1e-2), test_name
