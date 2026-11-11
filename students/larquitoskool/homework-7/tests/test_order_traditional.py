import pytest
from src.order_calculator import Order

def test_simple_1():
    order = Order([{"name": "A", "price": 10, "quantity": 1, "weight": 2}], "regular")
    order.set_shipping(10, False)
    assert order.calculate_total()['total'] == 12.80

def test_simple_2():
    order = Order([{"name": "B", "price": 20, "quantity": 2, "weight": 1}], "regular")
    order.set_shipping(0, False)
    assert order.calculate_total()['total'] == 44.20

def test_discount_save10():
    order = Order([{"name": "C", "price": 50, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)
    assert order.calculate_total()['total'] == 48.60

def test_discount_save20_fail():
    order = Order([{"name": "D", "price": 99, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)
    assert order.calculate_total()['total'] == 106.92

def test_newuser_valid():
    order = Order([{"name": "E", "price": 100, "quantity": 1, "weight": 0}], "new")
    order.apply_discount("NEWUSER")
    order.set_shipping(0, False)
    assert order.calculate_total()['total'] == 91.80

def test_invalid_code():
    order = Order([{"name": "F", "price": 100, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("FAKE")
    order.set_shipping(0, False)
    assert order.calculate_total()['total'] == 108.00

def test_high_distance():
    order = Order([{"name": "G", "price": 10, "quantity": 1, "weight": 0}], "regular")
    order.set_shipping(100, False)
    assert order.calculate_total()['total'] == 20.80

def test_express_shipping():
    order = Order([{"name": "H", "price": 10, "quantity": 1, "weight": 10}], "regular")
    order.set_shipping(50, True)
    assert order.calculate_total()['total'] == 25.80

def test_free_shipping_code():
    order = Order([{"name": "I", "price": 10, "quantity": 1, "weight": 100}], "regular")
    order.apply_discount("FREESHIP")
    order.set_shipping(1000, True)
    assert order.calculate_total()['total'] == 10.80

def test_complex_order():
    order = Order([{"name": "J", "price": 200, "quantity": 1, "weight": 5}], "new")
    order.apply_discount("NEWUSER")
    order.set_shipping(10, True)
    assert order.calculate_total()['total'] == 188.85