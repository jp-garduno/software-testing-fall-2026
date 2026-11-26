"""Part 3: Traditional (non-parameterized) order tests with hardcoded test data."""

import pytest
from order_calculator import Order


def test_traditional_01_simple_single_item():
    """Test 1: Simple single item order without discount or shipping."""
    order = Order([{"name": "Book", "price": 25.0, "quantity": 1, "weight": 0.0}], "regular")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(25.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(2.00)
    assert result["shipping"] == pytest.approx(0.00)
    assert result["total"] == pytest.approx(27.00)


def test_traditional_02_simple_two_quantities():
    """Test 2: Single item with multiple quantities without shipping."""
    order = Order([{"name": "Notebook", "price": 15.0, "quantity": 3, "weight": 0.0}], "regular")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(45.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(3.60)
    assert result["shipping"] == pytest.approx(0.00)
    assert result["total"] == pytest.approx(48.60)


def test_traditional_03_save10_at_threshold():
    """Test 3: SAVE10 discount applied at exact $50 threshold."""
    order = Order([{"name": "Item1", "price": 50.0, "quantity": 1, "weight": 1.0}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(10, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00)
    assert result["discount"] == pytest.approx(5.00)
    assert result["tax"] == pytest.approx(3.60)
    assert result["shipping"] == pytest.approx(1.50)
    assert result["total"] == pytest.approx(50.10)


def test_traditional_04_save10_below_minimum():
    """Test 4: SAVE10 discount rejected below $50 minimum."""
    order = Order([{"name": "Item1", "price": 49.99, "quantity": 1, "weight": 1.0}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(10, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(49.99)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(4.00)
    assert result["shipping"] == pytest.approx(1.50)
    assert result["total"] == pytest.approx(55.49)


def test_traditional_05_save20_at_threshold():
    """Test 5: SAVE20 discount applied at exact $100 threshold."""
    order = Order([{"name": "Item1", "price": 100.0, "quantity": 1, "weight": 2.0}], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(10, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(100.00)
    assert result["discount"] == pytest.approx(20.00)
    assert result["tax"] == pytest.approx(6.40)
    assert result["shipping"] == pytest.approx(2.00)
    assert result["total"] == pytest.approx(88.40)


def test_traditional_06_newuser_valid():
    """Test 6: NEWUSER 15% discount applied for a new customer."""
    order = Order([{"name": "StarterKit", "price": 40.0, "quantity": 1, "weight": 1.0}], "new")
    order.apply_discount("NEWUSER")
    order.set_shipping(5, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(40.00)
    assert result["discount"] == pytest.approx(6.00)
    assert result["tax"] == pytest.approx(2.72)
    assert result["shipping"] == pytest.approx(1.00)
    assert result["total"] == pytest.approx(37.72)


def test_traditional_07_invalid_discount_code():
    """Test 7: Invalid discount code ignored on regular order."""
    order = Order([{"name": "Item1", "price": 80.0, "quantity": 1, "weight": 1.0}], "regular")
    order.apply_discount("EXPIRED50")
    order.set_shipping(10, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(80.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(6.40)
    assert result["shipping"] == pytest.approx(1.50)
    assert result["total"] == pytest.approx(87.90)


def test_traditional_08_express_shipping_multiplier():
    """Test 8: Express shipping applies 1.5x multiplier to base shipping."""
    order = Order([{"name": "Monitor", "price": 200.0, "quantity": 1, "weight": 4.0}], "regular")
    order.set_shipping(20, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(200.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(16.00)
    assert result["shipping"] == pytest.approx(6.00)
    assert result["total"] == pytest.approx(222.00)


def test_traditional_09_freeship_code():
    """Test 9: FREESHIP code sets shipping cost to zero even with express."""
    order = Order([{"name": "Chair", "price": 180.0, "quantity": 1, "weight": 15.0}], "regular")
    order.apply_discount("FREESHIP")
    order.set_shipping(100, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(180.00)
    assert result["discount"] == pytest.approx(0.00)
    assert result["tax"] == pytest.approx(14.40)
    assert result["shipping"] == pytest.approx(0.00)
    assert result["total"] == pytest.approx(194.40)


def test_traditional_10_complex_multi_item_order():
    """Test 10: Complex multi-item order with SAVE20 and express shipping."""
    items = [
        {"name": "Laptop", "price": 800.0, "quantity": 1, "weight": 2.0},
        {"name": "Stand", "price": 40.0, "quantity": 1, "weight": 1.0},
        {"name": "Adapter", "price": 20.0, "quantity": 2, "weight": 0.2},
    ]
    order = Order(items, "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(40, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(880.00)
    assert result["discount"] == pytest.approx(176.00)
    assert result["tax"] == pytest.approx(56.32)
    assert result["shipping"] == pytest.approx(8.55)
    assert result["total"] == pytest.approx(768.87)
