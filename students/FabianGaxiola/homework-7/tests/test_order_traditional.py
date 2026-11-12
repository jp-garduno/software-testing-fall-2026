"""Ten unparameterized examples for comparison with the CSV-driven suite."""

import pytest
from order_calculator import Order


def _assert_total(items, customer_type, code, shipping, expected):
    order = Order(items, customer_type)
    if code is not None:
        order.apply_discount(code)
    order.set_shipping(*shipping)
    assert order.calculate_total() == pytest.approx(expected, abs=0.001)


def test_simple_single_50():
    _assert_total(
        [{"name": "Notebook", "price": 50, "quantity": 1, "weight": 1}],
        "regular",
        None,
        (10, False),
        {"subtotal": 50, "discount": 0, "tax": 4, "shipping": 1.5, "total": 55.5},
    )


def test_simple_two_items():
    _assert_total(
        [{"name": "Pen pack", "price": 25, "quantity": 2, "weight": 0.5}],
        "regular",
        None,
        (0, False),
        {"subtotal": 50, "discount": 0, "tax": 4, "shipping": 0.5, "total": 54.5},
    )


def test_simple_distance_order():
    _assert_total(
        [{"name": "Headphones", "price": 100, "quantity": 1, "weight": 2}],
        "regular",
        None,
        (25, False),
        {"subtotal": 100, "discount": 0, "tax": 8, "shipping": 3.5, "total": 111.5},
    )


def test_save10_exact_threshold():
    _assert_total(
        [{"name": "Mug", "price": 50, "quantity": 1, "weight": 1}],
        "regular",
        "SAVE10",
        (0, False),
        {"subtotal": 50, "discount": 0, "tax": 4, "shipping": 0.5, "total": 54.5},
    )


def test_save10_over_threshold():
    _assert_total(
        [{"name": "Mug", "price": 50.01, "quantity": 1, "weight": 0}],
        "regular",
        "SAVE10",
        (0, False),
        {"subtotal": 50.01, "discount": 5, "tax": 3.6, "shipping": 0, "total": 48.61},
    )


def test_save20_exact_threshold():
    _assert_total(
        [{"name": "Lamp", "price": 100, "quantity": 1, "weight": 0}],
        "regular",
        "SAVE20",
        (0, False),
        {"subtotal": 100, "discount": 0, "tax": 8, "shipping": 0, "total": 108},
    )


def test_save20_over_threshold():
    _assert_total(
        [{"name": "Lamp", "price": 100.01, "quantity": 1, "weight": 0}],
        "regular",
        "SAVE20",
        (0, False),
        {"subtotal": 100.01, "discount": 20, "tax": 6.4, "shipping": 0, "total": 86.41},
    )


def test_unknown_discount_code():
    _assert_total(
        [{"name": "Cable", "price": 80, "quantity": 1, "weight": 0}],
        "regular",
        "EXPIRED",
        (0, False),
        {"subtotal": 80, "discount": 0, "tax": 6.4, "shipping": 0, "total": 86.4},
    )


def test_newuser_discount_rejected_for_regular_customer():
    _assert_total(
        [{"name": "Book", "price": 20, "quantity": 1, "weight": 0}],
        "regular",
        "NEWUSER",
        (0, False),
        {"subtotal": 20, "discount": 0, "tax": 1.6, "shipping": 0, "total": 21.6},
    )


def test_newuser_discount_applied_to_first_order():
    _assert_total(
        [{"name": "Book", "price": 20, "quantity": 1, "weight": 0}],
        "new",
        "NEWUSER",
        (0, False),
        {"subtotal": 20, "discount": 3, "tax": 1.36, "shipping": 0, "total": 18.36},
    )
