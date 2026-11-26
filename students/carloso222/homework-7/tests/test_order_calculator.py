"""Order calculator tests: the full CSV (data-driven) plus unit tests for rules and error handling."""

import pytest
from src.order_calculator import Order
from tests.data_loader import calculate_case, load_order_cases


@pytest.mark.parametrize("case", load_order_cases())
def test_order_calculation_from_csv_matches_expected_breakdown(case):
    # Arrange: the case comes from test_data/order_calculations.csv
    expected = case["expected"]

    # Act
    result = calculate_case(case)

    # Assert
    assert result == pytest.approx(expected, abs=0.005)


def _item(price=10, quantity=1, weight=0):
    return {"name": "Item", "price": price, "quantity": quantity, "weight": weight}


def test_apply_discount_valid_code_returns_true_and_stores_code():
    order = Order([_item(price=60)])

    applied = order.apply_discount("SAVE10")

    assert (applied, order.discount_code) == (True, "SAVE10")


def test_apply_discount_invalid_code_returns_false_and_keeps_no_code():
    order = Order([_item(price=60)])

    applied = order.apply_discount("NOPE")

    assert (applied, order.discount_code) == (False, None)


def test_apply_discount_non_string_code_returns_false():
    order = Order([_item(price=60)])

    assert order.apply_discount(None) is False


def test_apply_discount_failed_second_code_keeps_first_code():
    order = Order([_item(price=60)])
    order.apply_discount("SAVE10")

    order.apply_discount("SAVE20")

    assert order.discount_code == "SAVE10"


def test_apply_discount_newuser_for_regular_customer_returns_false():
    order = Order([_item(price=60)], customer_type="regular")

    assert order.apply_discount("NEWUSER") is False


def test_calculate_subtotal_multiple_items_returns_sum_of_price_times_quantity():
    order = Order([_item(price=2.50, quantity=4), _item(price=1.25, quantity=2)])

    assert order.calculate_subtotal() == 12.50


def test_calculate_discount_without_code_returns_zero():
    assert Order([_item(price=60)]).calculate_discount() == 0.0


def test_calculate_discount_save10_returns_ten_percent():
    order = Order([_item(price=60)])
    order.apply_discount("SAVE10")

    assert order.calculate_discount() == 6.0


def test_calculate_tax_with_discount_uses_discounted_amount():
    order = Order([_item(price=200)])
    order.apply_discount("SAVE20")

    assert order.calculate_tax() == 12.80


def test_calculate_shipping_default_shipping_is_zero_for_weightless_items():
    assert Order([_item()]).calculate_shipping() == 0.0


def test_calculate_shipping_express_multiplies_base_cost():
    order = Order([_item(weight=2)])
    order.set_shipping(20, is_express=True)

    assert order.calculate_shipping() == 4.50


def test_calculate_shipping_item_without_weight_key_counts_as_weightless():
    order = Order([{"name": "Digital", "price": 5, "quantity": 1}])
    order.set_shipping(10)

    assert order.calculate_shipping() == 1.00


def test_calculate_total_returns_all_breakdown_keys():
    result = Order([_item()]).calculate_total()

    assert sorted(result) == ["discount", "shipping", "subtotal", "tax", "total"]


def test_calculate_total_components_add_up_to_total():
    order = Order([_item(price=33.33, quantity=3, weight=1.7)])
    order.apply_discount("SAVE10")
    order.set_shipping(12.3, is_express=True)

    result = order.calculate_total()

    assert result["subtotal"] - result["discount"] + result["tax"] + result[
        "shipping"
    ] == pytest.approx(result["total"])


@pytest.mark.parametrize(
    "items",
    [
        [_item(price=-1)],
        [_item(quantity=-1)],
        [_item(weight=-0.5)],
    ],
    ids=["negative_price", "negative_quantity", "negative_weight"],
)
def test_order_init_negative_value_raises_value_error(items):
    with pytest.raises(ValueError, match="cannot be negative"):
        Order(items)


@pytest.mark.parametrize(
    "item, message",
    [
        ({"name": "x", "quantity": 1}, "missing 'price'"),
        ({"name": "x", "price": 1}, "missing 'quantity'"),
        ({"name": "x", "price": 1, "quantity": 1.5}, "quantity must be an integer"),
        ({"name": "x", "price": 1, "quantity": True}, "quantity must be an integer"),
    ],
    ids=["no_price", "no_quantity", "float_quantity", "bool_quantity"],
)
def test_order_init_malformed_item_raises_value_error(item, message):
    with pytest.raises(ValueError, match=message):
        Order([item])


def test_order_init_unknown_customer_type_raises_value_error():
    with pytest.raises(ValueError, match="Unknown customer type"):
        Order([_item()], customer_type="vip")


def test_set_shipping_negative_distance_raises_value_error():
    with pytest.raises(ValueError, match="distance cannot be negative"):
        Order([_item()]).set_shipping(-1)


def test_calculate_total_zero_quantity_item_contributes_nothing():
    order = Order([_item(price=100, quantity=0, weight=9), _item(price=10)])

    assert order.calculate_total()["subtotal"] == 10.0
