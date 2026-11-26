"""The ten comparison scenarios written as separate tests with literal data."""

from src.order_calculator import Order


def test_simple_single_item():
    order = Order(
        [{"name": "Notebook", "price": 25, "quantity": 1, "weight": 0}], "regular"
    )
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 25,
        "discount": 0,
        "tax": 2,
        "shipping": 0,
        "total": 27,
    }


def test_simple_empty_order():
    order = Order([], "regular")
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 0,
        "discount": 0,
        "tax": 0,
        "shipping": 0,
        "total": 0,
    }


def test_discount_save10_at_minimum():
    order = Order(
        [{"name": "Backpack", "price": 50, "quantity": 1, "weight": 0}], "regular"
    )
    assert order.apply_discount("SAVE10") is True
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 50,
        "discount": 5,
        "tax": 3.6,
        "shipping": 0,
        "total": 48.6,
    }


def test_discount_save10_below_minimum():
    order = Order(
        [{"name": "Backpack", "price": 49.99, "quantity": 1, "weight": 0}], "regular"
    )
    assert order.apply_discount("SAVE10") is False
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 49.99,
        "discount": 0,
        "tax": 4,
        "shipping": 0,
        "total": 53.99,
    }


def test_discount_save20_at_minimum():
    order = Order(
        [{"name": "Keyboard", "price": 100, "quantity": 1, "weight": 0}], "regular"
    )
    assert order.apply_discount("SAVE20") is True
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 100,
        "discount": 20,
        "tax": 6.4,
        "shipping": 0,
        "total": 86.4,
    }


def test_discount_unknown_code():
    order = Order(
        [{"name": "Headset", "price": 75, "quantity": 1, "weight": 0}], "regular"
    )
    assert order.apply_discount("NOTACODE") is False
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 75,
        "discount": 0,
        "tax": 6,
        "shipping": 0,
        "total": 81,
    }


def test_discount_newuser_first_order():
    order = Order(
        [{"name": "Coffee maker", "price": 60, "quantity": 1, "weight": 0}], "new"
    )
    assert order.apply_discount("NEWUSER") is True
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 60,
        "discount": 9,
        "tax": 4.08,
        "shipping": 0,
        "total": 55.08,
    }


def test_shipping_express_weight_and_distance():
    order = Order(
        [{"name": "Item1", "price": 50, "quantity": 1, "weight": 1}], "regular"
    )
    order.set_shipping(10, True)
    assert order.calculate_total() == {
        "subtotal": 50,
        "discount": 0,
        "tax": 4,
        "shipping": 2.25,
        "total": 56.25,
    }


def test_shipping_free_overrides_express():
    order = Order(
        [{"name": "Desk lamp", "price": 80, "quantity": 1, "weight": 8}], "regular"
    )
    assert order.apply_discount("FREESHIP") is True
    order.set_shipping(40, True)
    assert order.calculate_total() == {
        "subtotal": 80,
        "discount": 0,
        "tax": 6.4,
        "shipping": 0,
        "total": 86.4,
    }


def test_complex_mixed_express():
    order = Order(
        [
            {"name": "Hiking pack", "price": 40, "quantity": 2, "weight": 1.25},
            {"name": "Bottle", "price": 25, "quantity": 2, "weight": 0.75},
        ],
        "regular",
    )
    assert order.apply_discount("SAVE20") is True
    order.set_shipping(40, True)
    assert order.calculate_total() == {
        "subtotal": 130,
        "discount": 26,
        "tax": 8.32,
        "shipping": 9,
        "total": 121.32,
    }
