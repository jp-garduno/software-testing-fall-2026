"""Part 3 - TRADITIONAL version: 10 tests, no parameterization, every value hardcoded."""

import pytest
from src.order_calculator import Order


def test_order_simple_single_item_returns_subtotal_plus_tax():
    order = Order(
        [{"name": "Item1", "price": 20, "quantity": 1, "weight": 0}], "regular"
    )
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == pytest.approx(
        {
            "subtotal": 20.00,
            "discount": 0.00,
            "tax": 1.60,
            "shipping": 0.00,
            "total": 21.60,
        },
        abs=0.005,
    )


def test_order_save10_above_minimum_applies_ten_percent():
    order = Order(
        [{"name": "Item1", "price": 60, "quantity": 1, "weight": 0}], "regular"
    )
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == pytest.approx(
        {
            "subtotal": 60.00,
            "discount": 6.00,
            "tax": 4.32,
            "shipping": 0.00,
            "total": 58.32,
        },
        abs=0.005,
    )


def test_order_save10_at_threshold_is_rejected():
    order = Order(
        [{"name": "Item1", "price": 50, "quantity": 1, "weight": 0}], "regular"
    )
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == pytest.approx(
        {
            "subtotal": 50.00,
            "discount": 0.00,
            "tax": 4.00,
            "shipping": 0.00,
            "total": 54.00,
        },
        abs=0.005,
    )


def test_order_save20_above_minimum_applies_twenty_percent():
    order = Order(
        [{"name": "Item1", "price": 120, "quantity": 1, "weight": 0}], "regular"
    )
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == pytest.approx(
        {
            "subtotal": 120.00,
            "discount": 24.00,
            "tax": 7.68,
            "shipping": 0.00,
            "total": 103.68,
        },
        abs=0.005,
    )


def test_order_invalid_code_gives_no_discount():
    order = Order(
        [{"name": "Item1", "price": 80, "quantity": 1, "weight": 0}], "regular"
    )
    order.apply_discount("BOGUS")
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == pytest.approx(
        {
            "subtotal": 80.00,
            "discount": 0.00,
            "tax": 6.40,
            "shipping": 0.00,
            "total": 86.40,
        },
        abs=0.005,
    )


def test_order_newuser_code_for_new_customer_gives_fifteen_percent():
    order = Order([{"name": "Item1", "price": 40, "quantity": 1, "weight": 0}], "new")
    order.apply_discount("NEWUSER")
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == pytest.approx(
        {
            "subtotal": 40.00,
            "discount": 6.00,
            "tax": 2.72,
            "shipping": 0.00,
            "total": 36.72,
        },
        abs=0.005,
    )


def test_order_tiny_amount_rounds_tax_up_to_one_cent():
    order = Order(
        [{"name": "Item1", "price": 0.10, "quantity": 1, "weight": 0}], "regular"
    )
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == pytest.approx(
        {
            "subtotal": 0.10,
            "discount": 0.00,
            "tax": 0.01,
            "shipping": 0.00,
            "total": 0.11,
        },
        abs=0.005,
    )


def test_order_weight_and_distance_add_up_standard_shipping():
    order = Order(
        [{"name": "Item1", "price": 10, "quantity": 1, "weight": 2}], "regular"
    )
    order.set_shipping(20, False)

    result = order.calculate_total()

    assert result == pytest.approx(
        {
            "subtotal": 10.00,
            "discount": 0.00,
            "tax": 0.80,
            "shipping": 3.00,
            "total": 13.80,
        },
        abs=0.005,
    )


def test_order_express_shipping_costs_one_and_a_half_times():
    order = Order(
        [{"name": "Item1", "price": 10, "quantity": 1, "weight": 2}], "regular"
    )
    order.set_shipping(20, True)

    result = order.calculate_total()

    assert result == pytest.approx(
        {
            "subtotal": 10.00,
            "discount": 0.00,
            "tax": 0.80,
            "shipping": 4.50,
            "total": 15.30,
        },
        abs=0.005,
    )


def test_order_freeship_code_makes_shipping_free():
    order = Order(
        [{"name": "Item1", "price": 10, "quantity": 1, "weight": 2}], "regular"
    )
    order.apply_discount("FREESHIP")
    order.set_shipping(20, False)

    result = order.calculate_total()

    assert result == pytest.approx(
        {
            "subtotal": 10.00,
            "discount": 0.00,
            "tax": 0.80,
            "shipping": 0.00,
            "total": 10.80,
        },
        abs=0.005,
    )
