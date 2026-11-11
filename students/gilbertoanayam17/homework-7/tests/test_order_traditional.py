"""Part 3, traditional version: ten order tests, each with its data written in the code.

test_order_data_driven.py runs these same ten scenarios from a CSV file.
"""

from order_calculator import Order


def test_simple_single_item():
    order = Order([{"name": "Ebook", "price": 20, "quantity": 1, "weight": 0}], "regular")
    order.set_shipping(0, False)

    assert order.calculate_total() == {
        "subtotal": 20.00,
        "discount": 0.00,
        "tax": 1.60,
        "shipping": 0.00,
        "total": 21.60,
    }


def test_simple_multiple_items():
    items = [
        {"name": "Software License", "price": 29.99, "quantity": 1, "weight": 0},
        {"name": "Song", "price": 1.29, "quantity": 3, "weight": 0},
    ]
    order = Order(items, "regular")
    order.set_shipping(0, False)

    assert order.calculate_total() == {
        "subtotal": 33.86,
        "discount": 0.00,
        "tax": 2.71,
        "shipping": 0.00,
        "total": 36.57,
    }


def test_discount_save10_at_minimum():
    order = Order([{"name": "Backpack", "price": 50, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)

    assert order.calculate_total() == {
        "subtotal": 50.00,
        "discount": 5.00,
        "tax": 3.60,
        "shipping": 0.00,
        "total": 48.60,
    }


def test_discount_save20_below_minimum():
    order = Order([{"name": "Office Chair", "price": 99.99, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)

    assert order.calculate_total() == {
        "subtotal": 99.99,
        "discount": 0.00,
        "tax": 8.00,
        "shipping": 0.00,
        "total": 107.99,
    }


def test_discount_invalid_code():
    order = Order([{"name": "Keyboard", "price": 80, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SUMMER2019")
    order.set_shipping(0, False)

    assert order.calculate_total() == {
        "subtotal": 80.00,
        "discount": 0.00,
        "tax": 6.40,
        "shipping": 0.00,
        "total": 86.40,
    }


def test_tax_after_newuser_discount():
    order = Order([{"name": "Starter Kit", "price": 40, "quantity": 1, "weight": 0}], "new")
    order.apply_discount("NEWUSER")
    order.set_shipping(0, False)

    assert order.calculate_total() == {
        "subtotal": 40.00,
        "discount": 6.00,
        "tax": 2.72,
        "shipping": 0.00,
        "total": 36.72,
    }


def test_shipping_weight_and_distance_standard():
    order = Order([{"name": "Toaster", "price": 40, "quantity": 1, "weight": 4}], "regular")
    order.set_shipping(30, False)

    assert order.calculate_total() == {
        "subtotal": 40.00,
        "discount": 0.00,
        "tax": 3.20,
        "shipping": 5.00,
        "total": 48.20,
    }


def test_shipping_weight_and_distance_express():
    order = Order([{"name": "Toaster", "price": 40, "quantity": 1, "weight": 4}], "regular")
    order.set_shipping(30, True)

    assert order.calculate_total() == {
        "subtotal": 40.00,
        "discount": 0.00,
        "tax": 3.20,
        "shipping": 7.50,
        "total": 50.70,
    }


def test_shipping_freeship_code():
    order = Order([{"name": "Bookshelf", "price": 150, "quantity": 1, "weight": 20}], "regular")
    order.apply_discount("FREESHIP")
    order.set_shipping(500, True)

    assert order.calculate_total() == {
        "subtotal": 150.00,
        "discount": 0.00,
        "tax": 12.00,
        "shipping": 0.00,
        "total": 162.00,
    }


def test_complex_multi_item_save20_express():
    items = [
        {"name": "Laptop", "price": 899.99, "quantity": 1, "weight": 2.2},
        {"name": "Mouse", "price": 25.5, "quantity": 2, "weight": 0.1},
        {"name": "Laptop Bag", "price": 45, "quantity": 1, "weight": 0.8},
    ]
    order = Order(items, "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(250, True)

    assert order.calculate_total() == {
        "subtotal": 995.99,
        "discount": 199.20,
        "tax": 63.74,
        "shipping": 39.90,
        "total": 900.43,
    }
