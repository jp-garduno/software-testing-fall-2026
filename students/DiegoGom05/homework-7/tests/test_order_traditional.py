"""
Enfoque TRADICIONAL: 10 tests sin parametrizacion.

Cada test tiene sus datos escritos directamente en el codigo.
Son los mismos 10 casos que test_order_data_driven.py, para poder compararlos.
"""

import os
import sys

import pytest

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from order_calculator import Order  # noqa: E402


def test_simple_single_item():
    order = Order([{"name": "Book", "price": 50, "quantity": 1, "weight": 0}], "regular")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(4.00, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(54.00, abs=0.01)


def test_simple_multiple_items():
    order = Order([
        {"name": "Mug", "price": 10, "quantity": 2, "weight": 0},
        {"name": "Card", "price": 5.25, "quantity": 3, "weight": 0},
    ], "regular")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(35.75, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(2.86, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(38.61, abs=0.01)


def test_discount_save10_at_threshold():
    order = Order([{"name": "Shoes", "price": 50, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00, abs=0.01)
    assert result["discount"] == pytest.approx(5.00, abs=0.01)
    assert result["tax"] == pytest.approx(3.60, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(48.60, abs=0.01)


def test_discount_save20_below_min():
    order = Order([{"name": "Jacket", "price": 99.99, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(99.99, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(8.00, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(107.99, abs=0.01)


def test_discount_invalid_code():
    order = Order([{"name": "Hat", "price": 80, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("BOGUS99")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(80.00, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(6.40, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(86.40, abs=0.01)


def test_discount_newuser_new_customer():
    order = Order([{"name": "Lamp", "price": 40, "quantity": 1, "weight": 0}], "new")
    order.apply_discount("NEWUSER")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(40.00, abs=0.01)
    assert result["discount"] == pytest.approx(6.00, abs=0.01)
    assert result["tax"] == pytest.approx(2.72, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(36.72, abs=0.01)


def test_tax_rounding_decimals():
    order = Order([{"name": "Game", "price": 19.99, "quantity": 3, "weight": 0}], "regular")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(59.97, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(4.80, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(64.77, abs=0.01)


def test_shipping_express():
    order = Order([{"name": "Phone", "price": 300, "quantity": 1, "weight": 2}], "regular")
    order.set_shipping(30, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(300.00, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(24.00, abs=0.01)
    assert result["shipping"] == pytest.approx(6.00, abs=0.01)
    assert result["total"] == pytest.approx(330.00, abs=0.01)


def test_shipping_freeship_code():
    order = Order([{"name": "TV", "price": 400, "quantity": 1, "weight": 5}], "regular")
    order.apply_discount("FREESHIP")
    order.set_shipping(100, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(400.00, abs=0.01)
    assert result["discount"] == pytest.approx(0.00, abs=0.01)
    assert result["tax"] == pytest.approx(32.00, abs=0.01)
    assert result["shipping"] == pytest.approx(0.00, abs=0.01)
    assert result["total"] == pytest.approx(432.00, abs=0.01)


def test_complex_multi_item_save20_express():
    order = Order([
        {"name": "Laptop", "price": 80, "quantity": 1, "weight": 2},
        {"name": "Mouse", "price": 15, "quantity": 2, "weight": 0.2},
        {"name": "Bag", "price": 30, "quantity": 1, "weight": 1},
    ], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(40, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(140.00, abs=0.01)
    assert result["discount"] == pytest.approx(28.00, abs=0.01)
    assert result["tax"] == pytest.approx(8.96, abs=0.01)
    assert result["shipping"] == pytest.approx(8.55, abs=0.01)
    assert result["total"] == pytest.approx(129.51, abs=0.01)
