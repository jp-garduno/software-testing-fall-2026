"""Part 3: Traditional (non-parameterized) order tests with hardcoded data."""

# pylint: disable=duplicate-code

import pytest

from src.order_calculator import Order


def test_traditional_01_simple_single_item():
    """Test 1: Simple single item order without discount or shipping."""
    order = Order(
        [{"name": "Notebook", "price": 20.00, "quantity": 1, "weight": 0.0}],
        "regular",
    )
    order.set_shipping(0, False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(20.00, abs=1e-2)
    assert result["discount"] == pytest.approx(0.00, abs=1e-2)
    assert result["tax"] == pytest.approx(1.60, abs=1e-2)
    assert result["shipping"] == pytest.approx(0.00, abs=1e-2)
    assert result["total"] == pytest.approx(21.60, abs=1e-2)


def test_traditional_02_simple_two_items():
    """Test 2: Simple two-item order without discount or shipping."""
    order = Order(
        [
            {"name": "Pen", "price": 5.00, "quantity": 3, "weight": 0.0},
            {"name": "Folder", "price": 10.00, "quantity": 2, "weight": 0.0},
        ],
        "regular",
    )
    order.set_shipping(0, False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(35.00, abs=1e-2)
    assert result["discount"] == pytest.approx(0.00, abs=1e-2)
    assert result["tax"] == pytest.approx(2.80, abs=1e-2)
    assert result["shipping"] == pytest.approx(0.00, abs=1e-2)
    assert result["total"] == pytest.approx(37.80, abs=1e-2)


def test_traditional_03_regular_order_with_shipping():
    """Test 3: Regular order with weight and distance shipping."""
    order = Order(
        [{"name": "Headphones", "price": 50.00, "quantity": 1, "weight": 1.0}],
        "regular",
    )
    order.set_shipping(10, False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(50.00, abs=1e-2)
    assert result["discount"] == pytest.approx(0.00, abs=1e-2)
    assert result["tax"] == pytest.approx(4.00, abs=1e-2)
    assert result["shipping"] == pytest.approx(1.50, abs=1e-2)
    assert result["total"] == pytest.approx(55.50, abs=1e-2)


def test_traditional_04_save10_at_threshold():
    """Test 4: SAVE10 discount applied at $50 threshold."""
    order = Order(
        [{"name": "Keyboard", "price": 50.00, "quantity": 1, "weight": 1.0}],
        "regular",
    )
    order.apply_discount("SAVE10")
    order.set_shipping(10, False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(50.00, abs=1e-2)
    assert result["discount"] == pytest.approx(5.00, abs=1e-2)
    assert result["tax"] == pytest.approx(3.60, abs=1e-2)
    assert result["shipping"] == pytest.approx(1.50, abs=1e-2)
    assert result["total"] == pytest.approx(50.10, abs=1e-2)


def test_traditional_05_save10_below_threshold():
    """Test 5: SAVE10 discount rejected below $50 threshold."""
    order = Order(
        [{"name": "Mouse", "price": 49.99, "quantity": 1, "weight": 0.5}],
        "regular",
    )
    order.apply_discount("SAVE10")
    order.set_shipping(10, False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(49.99, abs=1e-2)
    assert result["discount"] == pytest.approx(0.00, abs=1e-2)
    assert result["tax"] == pytest.approx(4.00, abs=1e-2)
    assert result["shipping"] == pytest.approx(1.25, abs=1e-2)
    assert result["total"] == pytest.approx(55.24, abs=1e-2)


def test_traditional_06_save20_at_threshold():
    """Test 6: SAVE20 discount applied at $100 threshold."""
    order = Order(
        [{"name": "Monitor", "price": 100.00, "quantity": 1, "weight": 4.0}],
        "regular",
    )
    order.apply_discount("SAVE20")
    order.set_shipping(20, False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(100.00, abs=1e-2)
    assert result["discount"] == pytest.approx(20.00, abs=1e-2)
    assert result["tax"] == pytest.approx(6.40, abs=1e-2)
    assert result["shipping"] == pytest.approx(4.00, abs=1e-2)
    assert result["total"] == pytest.approx(90.40, abs=1e-2)


def test_traditional_07_newuser_discount_for_new_customer():
    """Test 7: NEWUSER 15% discount applied for a new customer."""
    order = Order(
        [{"name": "Backpack", "price": 80.00, "quantity": 1, "weight": 1.0}],
        "new",
    )
    order.apply_discount("NEWUSER")
    order.set_shipping(10, False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(80.00, abs=1e-2)
    assert result["discount"] == pytest.approx(12.00, abs=1e-2)
    assert result["tax"] == pytest.approx(5.44, abs=1e-2)
    assert result["shipping"] == pytest.approx(1.50, abs=1e-2)
    assert result["total"] == pytest.approx(74.94, abs=1e-2)


def test_traditional_08_express_shipping_multiplier():
    """Test 8: Express shipping applies 1.5x multiplier."""
    order = Order(
        [{"name": "Camera", "price": 300.00, "quantity": 1, "weight": 2.0}],
        "regular",
    )
    order.set_shipping(30, True)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(300.00, abs=1e-2)
    assert result["discount"] == pytest.approx(0.00, abs=1e-2)
    assert result["tax"] == pytest.approx(24.00, abs=1e-2)
    assert result["shipping"] == pytest.approx(6.00, abs=1e-2)
    assert result["total"] == pytest.approx(330.00, abs=1e-2)


def test_traditional_09_freeship_discount_code():
    """Test 9: FREESHIP discount zeroes out shipping cost."""
    order = Order(
        [{"name": "Shoes", "price": 65.00, "quantity": 1, "weight": 1.5}],
        "regular",
    )
    order.apply_discount("FREESHIP")
    order.set_shipping(40, False)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(65.00, abs=1e-2)
    assert result["discount"] == pytest.approx(0.00, abs=1e-2)
    assert result["tax"] == pytest.approx(5.20, abs=1e-2)
    assert result["shipping"] == pytest.approx(0.00, abs=1e-2)
    assert result["total"] == pytest.approx(70.20, abs=1e-2)


def test_traditional_10_complex_multi_item_express_save20():
    """Test 10: Complex multi-item order with SAVE20 and express shipping."""
    order = Order(
        [
            {"name": "Laptop", "price": 800.00, "quantity": 1, "weight": 2.5},
            {"name": "Dock", "price": 150.00, "quantity": 1, "weight": 0.5},
            {"name": "Mouse", "price": 50.00, "quantity": 1, "weight": 0.2},
        ],
        "regular",
    )
    order.apply_discount("SAVE20")
    order.set_shipping(50, True)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(1000.00, abs=1e-2)
    assert result["discount"] == pytest.approx(200.00, abs=1e-2)
    assert result["tax"] == pytest.approx(64.00, abs=1e-2)
    assert result["shipping"] == pytest.approx(9.90, abs=1e-2)
    assert result["total"] == pytest.approx(873.90, abs=1e-2)
