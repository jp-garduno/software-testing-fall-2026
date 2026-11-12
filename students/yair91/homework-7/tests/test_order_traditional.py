"""Traditional version: ten tests without parameterization, data inline.

This is one half of the Part 3 comparison. It covers exactly the same ten
scenarios as test_order_data_driven.py, with the same assertions, so the line
count compares like with like.
"""

import pytest

from order_calculator import Order

ONE_CENT = 0.005


def test_simple_single_item():
    """One article, no discount and no shipping."""
    order = Order([{"name": "Notebook", "price": 25.0, "quantity": 1, "weight": 0.0}], "regular")
    order.set_shipping(0, False)
    breakdown = order.calculate_total()
    assert breakdown["subtotal"] == pytest.approx(25.00, abs=ONE_CENT)
    assert breakdown["discount"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["tax"] == pytest.approx(2.00, abs=ONE_CENT)
    assert breakdown["shipping"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["total"] == pytest.approx(27.00, abs=ONE_CENT)


def test_simple_two_products():
    """Two different products, no discount and no shipping."""
    order = Order(
        [
            {"name": "Pen", "price": 5.0, "quantity": 3, "weight": 0.0},
            {"name": "Folder", "price": 10.0, "quantity": 2, "weight": 0.0},
        ],
        "regular",
    )
    order.set_shipping(0, False)
    breakdown = order.calculate_total()
    assert breakdown["subtotal"] == pytest.approx(35.00, abs=ONE_CENT)
    assert breakdown["discount"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["tax"] == pytest.approx(2.80, abs=ONE_CENT)
    assert breakdown["shipping"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["total"] == pytest.approx(37.80, abs=ONE_CENT)


def test_save10_exactly_at_the_minimum():
    """SAVE10 needs 50; at exactly 50 it is accepted."""
    order = Order([{"name": "Backpack", "price": 50.0, "quantity": 1, "weight": 0.0}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)
    breakdown = order.calculate_total()
    assert breakdown["subtotal"] == pytest.approx(50.00, abs=ONE_CENT)
    assert breakdown["discount"] == pytest.approx(5.00, abs=ONE_CENT)
    assert breakdown["tax"] == pytest.approx(3.60, abs=ONE_CENT)
    assert breakdown["shipping"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["total"] == pytest.approx(48.60, abs=ONE_CENT)


def test_save10_below_the_minimum():
    """One cent below the minimum and the code does not apply."""
    order = Order([{"name": "Backpack", "price": 49.99, "quantity": 1, "weight": 0.0}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)
    breakdown = order.calculate_total()
    assert breakdown["subtotal"] == pytest.approx(49.99, abs=ONE_CENT)
    assert breakdown["discount"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["tax"] == pytest.approx(4.00, abs=ONE_CENT)
    assert breakdown["shipping"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["total"] == pytest.approx(53.99, abs=ONE_CENT)


def test_save20_exactly_at_the_minimum():
    """SAVE20 needs 100; at exactly 100 it is accepted."""
    order = Order([{"name": "Monitor", "price": 100.0, "quantity": 1, "weight": 0.0}], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)
    breakdown = order.calculate_total()
    assert breakdown["subtotal"] == pytest.approx(100.00, abs=ONE_CENT)
    assert breakdown["discount"] == pytest.approx(20.00, abs=ONE_CENT)
    assert breakdown["tax"] == pytest.approx(6.40, abs=ONE_CENT)
    assert breakdown["shipping"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["total"] == pytest.approx(86.40, abs=ONE_CENT)


def test_invalid_code_gives_no_discount():
    """A code that does not exist leaves the order at full price."""
    order = Order([{"name": "Monitor", "price": 100.0, "quantity": 1, "weight": 0.0}], "regular")
    order.apply_discount("SAVE50")
    order.set_shipping(0, False)
    breakdown = order.calculate_total()
    assert breakdown["subtotal"] == pytest.approx(100.00, abs=ONE_CENT)
    assert breakdown["discount"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["tax"] == pytest.approx(8.00, abs=ONE_CENT)
    assert breakdown["shipping"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["total"] == pytest.approx(108.00, abs=ONE_CENT)


def test_newuser_for_a_new_customer():
    """NEWUSER takes 15% off when the customer is new."""
    order = Order([{"name": "Lamp", "price": 40.0, "quantity": 1, "weight": 0.0}], "new")
    order.apply_discount("NEWUSER")
    order.set_shipping(0, False)
    breakdown = order.calculate_total()
    assert breakdown["subtotal"] == pytest.approx(40.00, abs=ONE_CENT)
    assert breakdown["discount"] == pytest.approx(6.00, abs=ONE_CENT)
    assert breakdown["tax"] == pytest.approx(2.72, abs=ONE_CENT)
    assert breakdown["shipping"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["total"] == pytest.approx(36.72, abs=ONE_CENT)


def test_shipping_from_weight_and_distance():
    """Shipping adds weight times 0.50 and distance times 0.10."""
    order = Order([{"name": "Box", "price": 10.0, "quantity": 1, "weight": 3.0}], "regular")
    order.set_shipping(40, False)
    breakdown = order.calculate_total()
    assert breakdown["subtotal"] == pytest.approx(10.00, abs=ONE_CENT)
    assert breakdown["discount"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["tax"] == pytest.approx(0.80, abs=ONE_CENT)
    assert breakdown["shipping"] == pytest.approx(5.50, abs=ONE_CENT)
    assert breakdown["total"] == pytest.approx(16.30, abs=ONE_CENT)


def test_express_multiplies_the_shipping():
    """The same order in express costs 1.5 times the base shipping."""
    order = Order([{"name": "Box", "price": 10.0, "quantity": 1, "weight": 3.0}], "regular")
    order.set_shipping(40, True)
    breakdown = order.calculate_total()
    assert breakdown["subtotal"] == pytest.approx(10.00, abs=ONE_CENT)
    assert breakdown["discount"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["tax"] == pytest.approx(0.80, abs=ONE_CENT)
    assert breakdown["shipping"] == pytest.approx(8.25, abs=ONE_CENT)
    assert breakdown["total"] == pytest.approx(19.05, abs=ONE_CENT)


def test_freeship_waives_the_shipping():
    """FREESHIP zeroes the shipping without touching the price."""
    order = Order([{"name": "Heavy", "price": 10.0, "quantity": 1, "weight": 20.0}], "regular")
    order.apply_discount("FREESHIP")
    order.set_shipping(100, False)
    breakdown = order.calculate_total()
    assert breakdown["subtotal"] == pytest.approx(10.00, abs=ONE_CENT)
    assert breakdown["discount"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["tax"] == pytest.approx(0.80, abs=ONE_CENT)
    assert breakdown["shipping"] == pytest.approx(0.00, abs=ONE_CENT)
    assert breakdown["total"] == pytest.approx(10.80, abs=ONE_CENT)
