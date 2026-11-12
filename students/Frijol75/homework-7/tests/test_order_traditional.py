"""
Traditional (Hardcoded) Test Suite for Order Calculator.

Contains 10 independent test functions with hardcoded data and repetitive setup logic.
Used for comparison against the data-driven approach.
"""

import pytest
from src.order_calculator import Order


def test_01_single_item():
    items = [{"name": "Book", "price": 50.0, "quantity": 1, "weight": 0.0}]
    order = Order(items, customer_type="regular")
    order.set_shipping(0.0, is_express=False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(50.00, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(4.00, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(54.00, abs=0.01)


def test_02_multiple_items():
    items = [
        {"name": "Mug", "price": 10.0, "quantity": 2, "weight": 0.0},
        {"name": "Pen", "price": 5.25, "quantity": 3, "weight": 0.0},
    ]
    order = Order(items, customer_type="regular")
    order.set_shipping(0.0, is_express=False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(35.75, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(2.86, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(38.61, abs=0.01)


def test_03_save10_valid():
    items = [{"name": "Headphones", "price": 80.0, "quantity": 1, "weight": 0.0}]
    order = Order(items, customer_type="regular")
    order.apply_discount("SAVE10")
    order.set_shipping(0.0, is_express=False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(80.00, abs=0.01)
    assert result["discount"] == pytest.approx(8.00, abs=0.01)
    assert result["tax"] == pytest.approx(5.76, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(77.76, abs=0.01)


def test_04_save10_below_min():
    items = [{"name": "Mousepad", "price": 45.0, "quantity": 1, "weight": 0.0}]
    order = Order(items, customer_type="regular")
    order.apply_discount("SAVE10")
    order.set_shipping(0.0, is_express=False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(45.00, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(3.60, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(48.60, abs=0.01)


def test_05_save20_valid():
    items = [{"name": "Monitor", "price": 150.0, "quantity": 1, "weight": 0.0}]
    order = Order(items, customer_type="regular")
    order.apply_discount("SAVE20")
    order.set_shipping(0.0, is_express=False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(150.00, abs=0.01)
    assert result["discount"] == pytest.approx(30.00, abs=0.01)
    assert result["tax"] == pytest.approx(9.60, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(129.60, abs=0.01)


def test_06_newuser_valid():
    items = [{"name": "Backpack", "price": 60.0, "quantity": 1, "weight": 0.0}]
    order = Order(items, customer_type="new")
    order.apply_discount("NEWUSER")
    order.set_shipping(0.0, is_express=False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(60.00, abs=0.01)
    assert result["discount"] == pytest.approx(9.00, abs=0.01)
    assert result["tax"] == pytest.approx(4.08, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(55.08, abs=0.01)


def test_07_shipping_standard():
    items = [{"name": "WeightPlate", "price": 30.0, "quantity": 1, "weight": 4.0}]
    order = Order(items, customer_type="regular")
    order.set_shipping(20.0, is_express=False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(30.00, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(2.40, abs=0.01)
    assert result["shipping"] == pytest.approx(4.00, abs=0.01)
    assert result["total"] == pytest.approx(36.40, abs=0.01)


def test_08_shipping_express():
    items = [{"name": "Smartphone", "price": 300.0, "quantity": 1, "weight": 2.0}]
    order = Order(items, customer_type="regular")
    order.set_shipping(30.0, is_express=True)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(300.00, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(24.00, abs=0.01)
    assert result["shipping"] == pytest.approx(6.00, abs=0.01)
    assert result["total"] == pytest.approx(330.00, abs=0.01)


def test_09_freeship_discount():
    items = [{"name": "Microwave", "price": 150.0, "quantity": 1, "weight": 10.0}]
    order = Order(items, customer_type="regular")
    order.apply_discount("FREESHIP")
    order.set_shipping(50.0, is_express=False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(150.00, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(12.00, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(162.00, abs=0.01)


def test_10_complex_combination():
    items = [
        {"name": "Blender", "price": 45.0, "quantity": 1, "weight": 3.0},
        {"name": "Cups", "price": 6.0, "quantity": 4, "weight": 0.25},
    ]
    order = Order(items, customer_type="new")
    order.apply_discount("NEWUSER")
    order.set_shipping(15.0, is_express=True)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(69.00, abs=0.01)
    assert result["discount"] == pytest.approx(10.35, abs=0.01)
    assert result["tax"] == pytest.approx(4.69, abs=0.01)
    assert result["shipping"] == pytest.approx(5.25, abs=0.01)
    assert result["total"] == pytest.approx(68.59, abs=0.01)

