"""Traditional version: 10 order tests with every input and expected value hard-coded in the test body."""

import pytest

from order_calculator import Order


def test_simple_single_item_no_shipping():
    order = Order(
        [
            {"name": "Item1", "price": 50, "quantity": 1, "weight": 0},
        ],
        "regular",
    )
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00, abs=0.005)
    assert result["discount"] == pytest.approx(0.00, abs=0.005)
    assert result["tax"] == pytest.approx(4.00, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(54.00, abs=0.005)


def test_save10_at_minimum_threshold():
    order = Order(
        [
            {"name": "Item1", "price": 50, "quantity": 1, "weight": 0},
        ],
        "regular",
    )
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00, abs=0.005)
    assert result["discount"] == pytest.approx(5.00, abs=0.005)
    assert result["tax"] == pytest.approx(3.60, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(48.60, abs=0.005)


def test_save20_at_minimum_threshold():
    order = Order(
        [
            {"name": "Item1", "price": 100, "quantity": 1, "weight": 0},
        ],
        "regular",
    )
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(100.00, abs=0.005)
    assert result["discount"] == pytest.approx(20.00, abs=0.005)
    assert result["tax"] == pytest.approx(6.40, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(86.40, abs=0.005)


def test_invalid_code_ignored():
    order = Order(
        [
            {"name": "Item1", "price": 60, "quantity": 1, "weight": 0},
        ],
        "regular",
    )
    order.apply_discount("BOGUS")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(60.00, abs=0.005)
    assert result["discount"] == pytest.approx(0.00, abs=0.005)
    assert result["tax"] == pytest.approx(4.80, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(64.80, abs=0.005)


def test_newuser_for_new_customer():
    order = Order(
        [
            {"name": "Item1", "price": 40, "quantity": 1, "weight": 0},
        ],
        "new",
    )
    order.apply_discount("NEWUSER")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(40.00, abs=0.005)
    assert result["discount"] == pytest.approx(6.00, abs=0.005)
    assert result["tax"] == pytest.approx(2.72, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(36.72, abs=0.005)


def test_tax_is_charged_after_discount():
    order = Order(
        [
            {"name": "Item1", "price": 200, "quantity": 1, "weight": 0},
        ],
        "regular",
    )
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(200.00, abs=0.005)
    assert result["discount"] == pytest.approx(40.00, abs=0.005)
    assert result["tax"] == pytest.approx(12.80, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(172.80, abs=0.005)


def test_shipping_weight_and_distance():
    order = Order(
        [
            {"name": "Item1", "price": 25, "quantity": 2, "weight": 2},
        ],
        "regular",
    )
    order.set_shipping(50, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00, abs=0.005)
    assert result["discount"] == pytest.approx(0.00, abs=0.005)
    assert result["tax"] == pytest.approx(4.00, abs=0.005)
    assert result["shipping"] == pytest.approx(7.00, abs=0.005)
    assert result["total"] == pytest.approx(61.00, abs=0.005)


def test_shipping_express_is_one_and_a_half_times():
    order = Order(
        [
            {"name": "Item1", "price": 25, "quantity": 2, "weight": 2},
        ],
        "regular",
    )
    order.set_shipping(50, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00, abs=0.005)
    assert result["discount"] == pytest.approx(0.00, abs=0.005)
    assert result["tax"] == pytest.approx(4.00, abs=0.005)
    assert result["shipping"] == pytest.approx(10.50, abs=0.005)
    assert result["total"] == pytest.approx(64.50, abs=0.005)


def test_freeship_overrides_express():
    order = Order(
        [
            {"name": "Item1", "price": 25, "quantity": 2, "weight": 2},
        ],
        "regular",
    )
    order.apply_discount("FREESHIP")
    order.set_shipping(50, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00, abs=0.005)
    assert result["discount"] == pytest.approx(0.00, abs=0.005)
    assert result["tax"] == pytest.approx(4.00, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(54.00, abs=0.005)


def test_complex_save20_express_two_items():
    order = Order(
        [
            {"name": "Chair", "price": 60, "quantity": 1, "weight": 5},
            {"name": "Cushion", "price": 25, "quantity": 2, "weight": 1},
        ],
        "regular",
    )
    order.apply_discount("SAVE20")
    order.set_shipping(200, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(110.00, abs=0.005)
    assert result["discount"] == pytest.approx(22.00, abs=0.005)
    assert result["tax"] == pytest.approx(7.04, abs=0.005)
    assert result["shipping"] == pytest.approx(35.25, abs=0.005)
    assert result["total"] == pytest.approx(130.29, abs=0.005)
