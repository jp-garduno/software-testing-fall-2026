"""Ten explicit, hardcoded tests for a fair comparison with CSV parameterization."""

from order_calculator import Order


def test_simple_one():
    """One item without discounts."""
    order = Order([{"name": "Sample product", "price": 10, "quantity": 1, "weight": 0}])
    order.set_shipping(0)
    assert order.calculate_total() == {
        "subtotal": 10,
        "discount": 0,
        "tax": 0.8,
        "shipping": 0,
        "total": 10.8,
    }


def test_simple_quantity():
    """Quantity multiplies the unit price."""
    order = Order(
        [{"name": "Sample product", "price": 12.5, "quantity": 2, "weight": 0}]
    )
    order.set_shipping(0)
    assert order.calculate_total() == {
        "subtotal": 25,
        "discount": 0,
        "tax": 2,
        "shipping": 0,
        "total": 27,
    }


def test_simple_empty():
    """An empty order has zero total at zero distance."""
    order = Order([])
    order.set_shipping(0)
    assert order.calculate_total() == {
        "subtotal": 0,
        "discount": 0,
        "tax": 0,
        "shipping": 0,
        "total": 0,
    }


def test_save10_at_50():
    """The SAVE10 threshold is exclusive."""
    order = Order([{"name": "Sample product", "price": 50, "quantity": 1, "weight": 0}])
    order.apply_discount("SAVE10")
    order.set_shipping(0)
    assert order.calculate_total() == {
        "subtotal": 50,
        "discount": 0,
        "tax": 4,
        "shipping": 0,
        "total": 54,
    }


def test_save10_above_50():
    """SAVE10 applies just above fifty."""
    order = Order(
        [{"name": "Sample product", "price": 50.01, "quantity": 1, "weight": 0}]
    )
    order.apply_discount("SAVE10")
    order.set_shipping(0)
    assert order.calculate_total() == {
        "subtotal": 50.01,
        "discount": 5,
        "tax": 3.6,
        "shipping": 0,
        "total": 48.61,
    }


def test_save20_at_100():
    """SAVE20 does not apply at exactly one hundred."""
    order = Order(
        [{"name": "Sample product", "price": 100, "quantity": 1, "weight": 0}]
    )
    order.apply_discount("SAVE20")
    order.set_shipping(0)
    assert order.calculate_total() == {
        "subtotal": 100,
        "discount": 0,
        "tax": 8,
        "shipping": 0,
        "total": 108,
    }


def test_save20_above_100():
    """SAVE20 applies one cent above the threshold."""
    order = Order(
        [{"name": "Sample product", "price": 100.01, "quantity": 1, "weight": 0}]
    )
    order.apply_discount("SAVE20")
    order.set_shipping(0)
    assert order.calculate_total() == {
        "subtotal": 100.01,
        "discount": 20,
        "tax": 6.4,
        "shipping": 0,
        "total": 86.41,
    }


def test_save10_below_50():
    """SAVE10 is rejected below the threshold."""
    order = Order(
        [{"name": "Sample product", "price": 49.99, "quantity": 1, "weight": 0}]
    )
    order.apply_discount("SAVE10")
    order.set_shipping(0)
    assert order.calculate_total() == {
        "subtotal": 49.99,
        "discount": 0,
        "tax": 4,
        "shipping": 0,
        "total": 53.99,
    }


def test_newuser_eligible():
    """A new customer's first order receives fifteen percent."""
    order = Order(
        [{"name": "Sample product", "price": 80, "quantity": 1, "weight": 0}], "new"
    )
    order.apply_discount("NEWUSER")
    order.set_shipping(0)
    assert order.calculate_total() == {
        "subtotal": 80,
        "discount": 12,
        "tax": 5.44,
        "shipping": 0,
        "total": 73.44,
    }


def test_newuser_returning():
    """Regular customers cannot reuse NEWUSER."""
    order = Order([{"name": "Sample product", "price": 80, "quantity": 1, "weight": 0}])
    order.apply_discount("NEWUSER")
    order.set_shipping(0)
    assert order.calculate_total() == {
        "subtotal": 80,
        "discount": 0,
        "tax": 6.4,
        "shipping": 0,
        "total": 86.4,
    }
