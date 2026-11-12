"""Ten standalone order tests with hardcoded inputs and expectations."""

from src.order_calculator import Order


def test_simple_single_item():
    """Check simple single item."""
    order = Order(
        [{"name": "Item", "price": 19.99, "quantity": 1, "weight": 0}], "regular"
    )
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 19.99,
        "discount": 0.00,
        "tax": 1.60,
        "shipping": 0.00,
        "total": 21.59,
    }


def test_simple_two_item_lines():
    """Check simple two item lines."""
    order = Order(
        [
            {"name": "Cable", "price": 7.25, "quantity": 3, "weight": 0},
            {"name": "Clip", "price": 1.1, "quantity": 2, "weight": 0},
        ],
        "regular",
    )
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 23.95,
        "discount": 0.00,
        "tax": 1.92,
        "shipping": 0.00,
        "total": 25.87,
    }


def test_discount_save10_exact():
    """Check discount save10 exact."""
    order = Order(
        [{"name": "Item", "price": 50, "quantity": 1, "weight": 0}], "regular"
    )
    assert order.apply_discount("SAVE10") is False
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 50.00,
        "discount": 0.00,
        "tax": 4.00,
        "shipping": 0.00,
        "total": 54.00,
    }


def test_discount_save10_above():
    """Check discount save10 above."""
    order = Order(
        [{"name": "Item", "price": 50.01, "quantity": 1, "weight": 0}], "regular"
    )
    assert order.apply_discount("SAVE10") is True
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 50.01,
        "discount": 5.00,
        "tax": 3.60,
        "shipping": 0.00,
        "total": 48.61,
    }


def test_discount_save20_above():
    """Check discount save20 above."""
    order = Order(
        [{"name": "Item", "price": 100.01, "quantity": 1, "weight": 0}], "regular"
    )
    assert order.apply_discount("SAVE20") is True
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 100.01,
        "discount": 20.00,
        "tax": 6.40,
        "shipping": 0.00,
        "total": 86.41,
    }


def test_discount_new_customer():
    """Check discount new customer."""
    order = Order([{"name": "Item", "price": 40, "quantity": 1, "weight": 0}], "new")
    assert order.apply_discount("NEWUSER") is True
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 40.00,
        "discount": 6.00,
        "tax": 2.72,
        "shipping": 0.00,
        "total": 36.72,
    }


def test_tax_uses_discounted_subtotal():
    """Check tax uses discounted subtotal."""
    order = Order(
        [{"name": "Item", "price": 75, "quantity": 1, "weight": 0}], "regular"
    )
    assert order.apply_discount("SAVE10") is True
    order.set_shipping(0, False)
    assert order.calculate_total() == {
        "subtotal": 75.00,
        "discount": 7.50,
        "tax": 5.40,
        "shipping": 0.00,
        "total": 72.90,
    }


def test_shipping_express():
    """Check shipping express."""
    order = Order(
        [{"name": "Item", "price": 50, "quantity": 1, "weight": 1}], "regular"
    )
    order.set_shipping(10, True)
    assert order.calculate_total() == {
        "subtotal": 50.00,
        "discount": 0.00,
        "tax": 4.00,
        "shipping": 2.25,
        "total": 56.25,
    }


def test_shipping_free_express():
    """Check shipping free express."""
    order = Order(
        [{"name": "Item", "price": 25, "quantity": 1, "weight": 15}], "regular"
    )
    assert order.apply_discount("FREESHIP") is True
    order.set_shipping(200, True)
    assert order.calculate_total() == {
        "subtotal": 25.00,
        "discount": 0.00,
        "tax": 2.00,
        "shipping": 0.00,
        "total": 27.00,
    }


def test_complex_save20_express():
    """Check complex save20 express."""
    order = Order(
        [
            {"name": "Desk", "price": 60, "quantity": 1, "weight": 2.5},
            {"name": "Lamp", "price": 20.5, "quantity": 2, "weight": 1},
        ],
        "regular",
    )
    assert order.apply_discount("SAVE20") is True
    order.set_shipping(15, True)
    assert order.calculate_total() == {
        "subtotal": 101.00,
        "discount": 20.20,
        "tax": 6.46,
        "shipping": 5.63,
        "total": 92.89,
    }
