from src.order_calculator import Order


def test_calculate_total_single_item_without_code_adds_only_tax():
    order = Order([{"name": "Notebook", "price": 12.50, "quantity": 1, "weight": 0}], "regular")
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == {"subtotal": 12.50, "discount": 0.00, "tax": 1.00, "shipping": 0.00, "total": 13.50}


def test_calculate_total_save10_at_minimum_order_takes_ten_percent():
    order = Order([{"name": "Headphones", "price": 50.00, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == {"subtotal": 50.00, "discount": 5.00, "tax": 3.60, "shipping": 0.00, "total": 48.60}


def test_calculate_total_save10_below_minimum_order_gives_no_discount():
    order = Order([{"name": "Cable", "price": 49.99, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE10")
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == {"subtotal": 49.99, "discount": 0.00, "tax": 4.00, "shipping": 0.00, "total": 53.99}


def test_calculate_total_save20_at_minimum_order_takes_twenty_percent():
    order = Order([{"name": "Keyboard", "price": 100.00, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("SAVE20")
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == {"subtotal": 100.00, "discount": 20.00, "tax": 6.40, "shipping": 0.00, "total": 86.40}


def test_calculate_total_newuser_for_new_customer_takes_fifteen_percent():
    order = Order([{"name": "Backpack", "price": 40.00, "quantity": 1, "weight": 0}], "new")
    order.apply_discount("NEWUSER")
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == {"subtotal": 40.00, "discount": 6.00, "tax": 2.72, "shipping": 0.00, "total": 36.72}


def test_calculate_total_newuser_for_regular_customer_gives_no_discount():
    order = Order([{"name": "Backpack", "price": 40.00, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("NEWUSER")
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == {"subtotal": 40.00, "discount": 0.00, "tax": 3.20, "shipping": 0.00, "total": 43.20}


def test_calculate_total_unknown_code_gives_no_discount():
    order = Order([{"name": "Lamp", "price": 60.00, "quantity": 1, "weight": 0}], "regular")
    order.apply_discount("BOGUS50")
    order.set_shipping(0, False)

    result = order.calculate_total()

    assert result == {"subtotal": 60.00, "discount": 0.00, "tax": 4.80, "shipping": 0.00, "total": 64.80}


def test_calculate_total_weight_and_distance_add_up_shipping():
    order = Order([{"name": "Chair", "price": 45.00, "quantity": 2, "weight": 7.5}], "regular")
    order.set_shipping(85, False)

    result = order.calculate_total()

    assert result == {"subtotal": 90.00, "discount": 0.00, "tax": 7.20, "shipping": 16.00, "total": 113.20}


def test_calculate_total_express_shipping_costs_half_more():
    order = Order([{"name": "Speaker", "price": 70.00, "quantity": 1, "weight": 3}], "regular")
    order.set_shipping(40, True)

    result = order.calculate_total()

    assert result == {"subtotal": 70.00, "discount": 0.00, "tax": 5.60, "shipping": 8.25, "total": 83.85}


def test_calculate_total_freeship_code_removes_shipping():
    order = Order([{"name": "Rug", "price": 120.00, "quantity": 1, "weight": 12}], "regular")
    order.apply_discount("FREESHIP")
    order.set_shipping(200, False)

    result = order.calculate_total()

    assert result == {"subtotal": 120.00, "discount": 0.00, "tax": 9.60, "shipping": 0.00, "total": 129.60}
