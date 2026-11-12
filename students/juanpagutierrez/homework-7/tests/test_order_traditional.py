"""Traditional version of the comparison suite (Part 3).

Ten hand-written tests, one per scenario, with the data hardcoded inside each
function. test_order_data_driven.py runs exactly the same ten scenarios from
test_data/order_comparison.csv; COMPARISON_REPORT.md compares the two.
"""

import pytest

from src.order_calculator import Order


def test_simple_single_item():
    order = Order([{"name": "Ebook", "price": 50, "quantity": 1, "weight": 0}], "regular")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(4.00)
    assert result["shipping"] == pytest.approx(0.00)
    assert result["total"] == pytest.approx(54.00)


def test_simple_with_standard_shipping():
    order = Order([{"name": "Item1", "price": 50, "quantity": 1, "weight": 1}], "regular")
    order.set_shipping(10, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(4.00)
    assert result["shipping"] == pytest.approx(1.50)
    assert result["total"] == pytest.approx(55.50)


def test_discount_save10_at_threshold():
    order = Order([{"name": "Headphones", "price": 50, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00)
    assert result["discount"] == pytest.approx(5.00)
    assert result["tax"] == pytest.approx(3.60)
    assert result["shipping"] == pytest.approx(0.00)
    assert result["total"] == pytest.approx(48.60)


def test_discount_save10_below_threshold():
    order = Order([{"name": "Headphones", "price": 49.99, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(49.99)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(4.00)
    assert result["shipping"] == pytest.approx(0.00)
    assert result["total"] == pytest.approx(53.99)


def test_discount_save20_at_threshold():
    order = Order([{"name": "Monitor", "price": 100, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(100.00)
    assert result["discount"] == pytest.approx(20.00)
    assert result["tax"] == pytest.approx(6.40)
    assert result["shipping"] == pytest.approx(0.00)
    assert result["total"] == pytest.approx(86.40)


def test_discount_newuser_new_customer():
    order = Order([{"name": "Backpack", "price": 80, "quantity": 1, "weight": 0}], "new")
    order.apply_discount("NEWUSER")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(80.00)
    assert result["discount"] == pytest.approx(12.00)
    assert result["tax"] == pytest.approx(5.44)
    assert result["shipping"] == pytest.approx(0.00)
    assert result["total"] == pytest.approx(73.44)


def test_discount_invalid_code():
    order = Order([{"name": "Backpack", "price": 80, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("BOGUS50")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(80.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(6.40)
    assert result["shipping"] == pytest.approx(0.00)
    assert result["total"] == pytest.approx(86.40)


def test_tax_after_discount():
    order = Order([{"name": "Speaker", "price": 123.45, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(123.45)
    assert result["discount"] == pytest.approx(24.69)
    assert result["tax"] == pytest.approx(7.90)
    assert result["shipping"] == pytest.approx(0.00)
    assert result["total"] == pytest.approx(106.66)


def test_shipping_express_multiplier():
    order = Order([{"name": "Plant", "price": 10, "quantity": 2, "weight": 2.5}], "regular")
    order.set_shipping(120, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(20.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(1.60)
    assert result["shipping"] == pytest.approx(21.75)
    assert result["total"] == pytest.approx(43.35)


def test_shipping_freeship_code():
    order = Order([{"name": "Rug", "price": 20, "quantity": 1, "weight": 5}], "regular")
    order.apply_discount("FREESHIP")
    order.set_shipping(200, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(20.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(1.60)
    assert result["shipping"] == pytest.approx(0.00)
    assert result["total"] == pytest.approx(21.60)
