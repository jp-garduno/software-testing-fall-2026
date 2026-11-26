"""Traditional approach: 10 separate tests, every value hardcoded."""
import pytest

from order_calculator import Order


def test_simple_single_item():
    order = Order([{"name": "Item1", "price": 50, "quantity": 1, "weight": 0}], "regular")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00, abs=0.005)
    assert result["discount"] == pytest.approx(0.00, abs=0.005)
    assert result["tax"] == pytest.approx(4.00, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(54.00, abs=0.005)


def test_discount_save10_at_threshold():
    order = Order([{"name": "Item1", "price": 50, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00, abs=0.005)
    assert result["discount"] == pytest.approx(5.00, abs=0.005)
    assert result["tax"] == pytest.approx(3.60, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(48.60, abs=0.005)


def test_discount_save20_below_min():
    order = Order([{"name": "Item1", "price": 99, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(99.00, abs=0.005)
    assert result["discount"] == pytest.approx(0.00, abs=0.005)
    assert result["tax"] == pytest.approx(7.92, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(106.92, abs=0.005)


def test_discount_newuser_new_customer():
    order = Order([{"name": "Item1", "price": 40, "quantity": 1, "weight": 0}], "new")
    order.apply_discount("NEWUSER")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(40.00, abs=0.005)
    assert result["discount"] == pytest.approx(6.00, abs=0.005)
    assert result["tax"] == pytest.approx(2.72, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(36.72, abs=0.005)


def test_tax_computed_after_discount():
    order = Order([{"name": "Item1", "price": 200, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(200.00, abs=0.005)
    assert result["discount"] == pytest.approx(40.00, abs=0.005)
    assert result["tax"] == pytest.approx(12.80, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(172.80, abs=0.005)


def test_shipping_weight_and_distance():
    order = Order([{"name": "Item1", "price": 50, "quantity": 1, "weight": 1}], "regular")
    order.set_shipping(10, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00, abs=0.005)
    assert result["discount"] == pytest.approx(0.00, abs=0.005)
    assert result["tax"] == pytest.approx(4.00, abs=0.005)
    assert result["shipping"] == pytest.approx(1.50, abs=0.005)
    assert result["total"] == pytest.approx(55.50, abs=0.005)


def test_shipping_express():
    order = Order([{"name": "Item1", "price": 50, "quantity": 1, "weight": 1}], "regular")
    order.set_shipping(10, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00, abs=0.005)
    assert result["discount"] == pytest.approx(0.00, abs=0.005)
    assert result["tax"] == pytest.approx(4.00, abs=0.005)
    assert result["shipping"] == pytest.approx(2.25, abs=0.005)
    assert result["total"] == pytest.approx(56.25, abs=0.005)


def test_shipping_freeship_code():
    order = Order([{"name": "Item1", "price": 50, "quantity": 1, "weight": 5}], "regular")
    order.apply_discount("FREESHIP")
    order.set_shipping(100, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(50.00, abs=0.005)
    assert result["discount"] == pytest.approx(0.00, abs=0.005)
    assert result["tax"] == pytest.approx(4.00, abs=0.005)
    assert result["shipping"] == pytest.approx(0.00, abs=0.005)
    assert result["total"] == pytest.approx(54.00, abs=0.005)


def test_complex_multi_item_save10_shipping():
    order = Order([
        {"name": "Item1", "price": 25, "quantity": 2, "weight": 1.5},
        {"name": "Item2", "price": 40, "quantity": 1, "weight": 3},
    ], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(30, False)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(90.00, abs=0.005)
    assert result["discount"] == pytest.approx(9.00, abs=0.005)
    assert result["tax"] == pytest.approx(6.48, abs=0.005)
    assert result["shipping"] == pytest.approx(6.00, abs=0.005)
    assert result["total"] == pytest.approx(93.48, abs=0.005)


def test_complex_save20_express():
    order = Order([
        {"name": "Item1", "price": 60, "quantity": 2, "weight": 2.5},
        {"name": "Item2", "price": 35, "quantity": 1, "weight": 1},
    ], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(120, True)
    result = order.calculate_total()
    assert result["subtotal"] == pytest.approx(155.00, abs=0.005)
    assert result["discount"] == pytest.approx(31.00, abs=0.005)
    assert result["tax"] == pytest.approx(9.92, abs=0.005)
    assert result["shipping"] == pytest.approx(22.50, abs=0.005)
    assert result["total"] == pytest.approx(156.42, abs=0.005)
