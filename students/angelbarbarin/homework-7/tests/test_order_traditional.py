"""Traditional version of the comparison suite (part 3).

Ten independent test functions, each with its data written inline. This file exists to be
compared against test_order_data_driven.py, which runs the same ten scenarios from a CSV.
"""

import pytest

from order_calculator import Order


def test_simple_order():
    order = Order([{"name": "Item1", "price": 50, "quantity": 1, "weight": 1}], "regular")
    order.set_shipping(10, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(4.00)
    assert result["shipping"] == pytest.approx(5.50)
    assert result["total"] == pytest.approx(59.50)


def test_save10_at_minimum_threshold():
    order = Order([{"name": "Shoes", "price": 25, "quantity": 2, "weight": 0.8}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(10, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00)
    assert result["discount"] == pytest.approx(5.00)
    assert result["tax"] == pytest.approx(3.60)
    assert result["shipping"] == pytest.approx(5.80)
    assert result["total"] == pytest.approx(54.40)


def test_save10_below_minimum():
    order = Order([{"name": "Shoes", "price": 49.99, "quantity": 1, "weight": 0.8}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(10, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(49.99)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(4.00)
    assert result["shipping"] == pytest.approx(5.40)
    assert result["total"] == pytest.approx(59.39)


def test_save20_at_minimum_threshold():
    order = Order([{"name": "Jacket", "price": 100, "quantity": 1, "weight": 1.2}], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(10, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(100.00)
    assert result["discount"] == pytest.approx(20.00)
    assert result["tax"] == pytest.approx(6.40)
    assert result["shipping"] == pytest.approx(5.60)
    assert result["total"] == pytest.approx(92.00)


def test_newuser_for_new_customer():
    order = Order([{"name": "Headphones", "price": 60, "quantity": 1, "weight": 0.3}], "new")
    order.apply_discount("NEWUSER")
    order.set_shipping(20, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(60.00)
    assert result["discount"] == pytest.approx(9.00)
    assert result["tax"] == pytest.approx(4.08)
    assert result["shipping"] == pytest.approx(6.15)
    assert result["total"] == pytest.approx(61.23)


def test_tax_rounds_up():
    order = Order([{"name": "Book", "price": 10.44, "quantity": 1, "weight": 0.5}], "regular")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(10.44)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(0.84)
    assert result["shipping"] == pytest.approx(4.25)
    assert result["total"] == pytest.approx(15.53)


def test_shipping_express():
    order = Order([{"name": "Vase", "price": 30, "quantity": 1, "weight": 1.5}], "regular")
    order.set_shipping(100, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(30.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(2.40)
    assert result["shipping"] == pytest.approx(22.13)
    assert result["total"] == pytest.approx(54.53)


def test_shipping_freeship_code():
    order = Order([{"name": "Vase", "price": 30, "quantity": 1, "weight": 1.5}], "regular")
    order.apply_discount("FREESHIP")
    order.set_shipping(100, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(30.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(2.40)
    assert result["shipping"] == pytest.approx(0.00)
    assert result["total"] == pytest.approx(32.40)


def test_complex_zero_quantity_item():
    order = Order(
        [
            {"name": "Gift", "price": 20, "quantity": 0, "weight": 1},
            {"name": "Card", "price": 4.5, "quantity": 2, "weight": 0.05},
        ],
        "regular",
    )
    order.set_shipping(8, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(9.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(0.72)
    assert result["shipping"] == pytest.approx(4.85)
    assert result["total"] == pytest.approx(14.57)


def test_complex_cart_save20_express():
    order = Order(
        [
            {"name": "Tablet", "price": 329, "quantity": 1, "weight": 0.5},
            {"name": "Case", "price": 29.99, "quantity": 1, "weight": 0.2},
            {"name": "Charger", "price": 19.99, "quantity": 2, "weight": 0.15},
        ],
        "regular",
    )
    order.apply_discount("SAVE20")
    order.set_shipping(250, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(398.97)
    assert result["discount"] == pytest.approx(79.79)
    assert result["tax"] == pytest.approx(25.53)
    assert result["shipping"] == pytest.approx(44.25)
    assert result["total"] == pytest.approx(388.96)
