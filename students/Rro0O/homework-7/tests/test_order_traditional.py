"""Traditional (non-parameterized) version: 10 tests with hard-coded data.

Compare with test_order_data_driven.py, which covers the same 10 scenarios.
"""

import pytest

from order_calculator import Order


def calc(items, customer_type="regular", code=None, distance=0, express=False):
    order = Order(items, customer_type)
    if code:
        order.apply_discount(code)
    order.set_shipping(distance, express)
    return order.calculate_total()


def check(result, subtotal, discount, tax, shipping, total):
    assert result["subtotal"] == pytest.approx(subtotal, abs=0.005)
    assert result["discount"] == pytest.approx(discount, abs=0.005)
    assert result["tax"] == pytest.approx(tax, abs=0.005)
    assert result["shipping"] == pytest.approx(shipping, abs=0.005)
    assert result["total"] == pytest.approx(total, abs=0.005)


def test_simple_single_item():
    result = calc([{"name": "Item1", "price": 50, "quantity": 1, "weight": 0}])
    check(result, 50.00, 0.00, 4.00, 0.00, 54.00)


def test_save10_at_exact_minimum():
    result = calc([{"name": "Lamp", "price": 50, "quantity": 1, "weight": 0}], code="SAVE10")
    check(result, 50.00, 5.00, 3.60, 0.00, 48.60)


def test_save10_below_minimum():
    result = calc([{"name": "Lamp", "price": 49.99, "quantity": 1, "weight": 0}], code="SAVE10")
    check(result, 49.99, 0.00, 4.00, 0.00, 53.99)


def test_save20_at_exact_minimum():
    result = calc([{"name": "Chair", "price": 100, "quantity": 1, "weight": 0}], code="SAVE20")
    check(result, 100.00, 20.00, 6.40, 0.00, 86.40)


def test_invalid_code_ignored():
    result = calc([{"name": "Desk", "price": 200, "quantity": 1, "weight": 0}], code="BOGUS")
    check(result, 200.00, 0.00, 16.00, 0.00, 216.00)


def test_newuser_for_new_customer():
    result = calc(
        [{"name": "Mug", "price": 20, "quantity": 3, "weight": 0}],
        customer_type="new",
        code="NEWUSER",
    )
    check(result, 60.00, 9.00, 4.08, 0.00, 55.08)


def test_shipping_weight_and_distance():
    result = calc([{"name": "Book", "price": 12, "quantity": 2, "weight": 1.5}], distance=45)
    check(result, 24.00, 0.00, 1.92, 6.00, 31.92)


def test_shipping_express_weight_and_distance():
    result = calc(
        [{"name": "Book", "price": 12, "quantity": 2, "weight": 1.5}], distance=45, express=True
    )
    check(result, 24.00, 0.00, 1.92, 9.00, 34.92)


def test_shipping_free_with_freeship():
    result = calc(
        [{"name": "Anvil", "price": 80, "quantity": 1, "weight": 40}], code="FREESHIP", distance=300
    )
    check(result, 80.00, 0.00, 6.40, 0.00, 86.40)


def test_complex_multi_item_discount_shipping():
    items = [
        {"name": "TV", "price": 399.99, "quantity": 1, "weight": 12},
        {"name": "Cable", "price": 9.5, "quantity": 2, "weight": 0.2},
        {"name": "Mount", "price": 35, "quantity": 1, "weight": 3},
    ]
    result = calc(items, code="SAVE20", distance=250)
    check(result, 453.99, 90.80, 29.06, 32.70, 424.95)
