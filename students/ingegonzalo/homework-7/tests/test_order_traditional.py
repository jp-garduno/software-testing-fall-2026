"""Version TRADICIONAL: 10 tests con datos hardcodeados."""
import pytest

from order_calculator import Order


def test_simple_single_item():
    order = Order([{"name": "Item1", "price": 50, "quantity": 1, "weight": 0}])
    order.set_shipping(0, False)
    assert order.calculate_total() == pytest.approx(
        {"subtotal": 50.0, "discount": 0.0, "tax": 4.0, "shipping": 0.0, "total": 54.0}, abs=0.01)


def test_simple_multiple_items():
    order = Order([{"name": "A", "price": 10, "quantity": 2, "weight": 0},
                   {"name": "B", "price": 5, "quantity": 3, "weight": 0}])
    order.set_shipping(0, False)
    assert order.calculate_total() == pytest.approx(
        {"subtotal": 35.0, "discount": 0.0, "tax": 2.8, "shipping": 0.0, "total": 37.8}, abs=0.01)


def test_save10_at_threshold():
    order = Order([{"name": "Item", "price": 50, "quantity": 1, "weight": 0}])
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)
    assert order.calculate_total() == pytest.approx(
        {"subtotal": 50.0, "discount": 5.0, "tax": 3.6, "shipping": 0.0, "total": 48.6}, abs=0.01)


def test_save10_below_minimum():
    order = Order([{"name": "Item", "price": 49.99, "quantity": 1, "weight": 0}])
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)
    assert order.calculate_total() == pytest.approx(
        {"subtotal": 49.99, "discount": 0.0, "tax": 4.0, "shipping": 0.0, "total": 53.99}, abs=0.01)


def test_save20_at_threshold():
    order = Order([{"name": "Item", "price": 100, "quantity": 1, "weight": 0}])
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)
    assert order.calculate_total() == pytest.approx(
        {"subtotal": 100.0, "discount": 20.0, "tax": 6.4, "shipping": 0.0, "total": 86.4}, abs=0.01)


def test_invalid_code():
    order = Order([{"name": "Item", "price": 80, "quantity": 1, "weight": 0}])
    order.apply_discount("BOGUS")
    order.set_shipping(0, False)
    assert order.calculate_total() == pytest.approx(
        {"subtotal": 80.0, "discount": 0.0, "tax": 6.4, "shipping": 0.0, "total": 86.4}, abs=0.01)


def test_tax_rounding_up():
    order = Order([{"name": "Item", "price": 19.99, "quantity": 3, "weight": 0}])
    order.set_shipping(0, False)
    assert order.calculate_total() == pytest.approx(
        {"subtotal": 59.97, "discount": 0.0, "tax": 4.8, "shipping": 0.0, "total": 64.77}, abs=0.01)


def test_ship_weight_and_distance():
    order = Order([{"name": "Item", "price": 20, "quantity": 1, "weight": 2}])
    order.set_shipping(50, False)
    assert order.calculate_total() == pytest.approx(
        {"subtotal": 20.0, "discount": 0.0, "tax": 1.6, "shipping": 6.0, "total": 27.6}, abs=0.01)


def test_ship_express():
    order = Order([{"name": "Item", "price": 20, "quantity": 1, "weight": 2}])
    order.set_shipping(50, True)
    assert order.calculate_total() == pytest.approx(
        {"subtotal": 20.0, "discount": 0.0, "tax": 1.6, "shipping": 9.0, "total": 30.6}, abs=0.01)


def test_complex_save10_express():
    order = Order([{"name": "Laptop", "price": 500, "quantity": 1, "weight": 2},
                   {"name": "Mouse", "price": 25, "quantity": 2, "weight": 0.2}])
    order.apply_discount("SAVE10")
    order.set_shipping(300, True)
    assert order.calculate_total() == pytest.approx(
        {"subtotal": 550.0, "discount": 55.0, "tax": 39.6, "shipping": 46.8, "total": 581.4}, abs=0.01)