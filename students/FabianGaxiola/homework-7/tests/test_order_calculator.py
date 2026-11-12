"""Data-driven and boundary tests for order pricing."""

import pytest
from data_loaders import load_order_cases
from order_calculator import Order

ORDER_CASES = load_order_cases()


@pytest.mark.parametrize("case", ORDER_CASES, ids=lambda case: case["test_name"])
def test_order_totals_from_csv(case):
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"] is not None:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance_km"], case["is_express"])

    result = order.calculate_total()
    for field in ("subtotal", "discount", "tax", "shipping", "total"):
        expected = case[f"expected_{field}"]
        assert result[field] == pytest.approx(
            expected, abs=0.001
        ), f"{case['test_name']}: {field} differs"


@pytest.mark.parametrize(
    ("subtotal", "customer_type", "code", "valid", "discount"),
    [
        (50, "regular", "SAVE10", False, 0),
        (50.01, "regular", "SAVE10", True, 5),
        (100, "regular", "SAVE20", False, 0),
        (100.01, "regular", "SAVE20", True, 20),
        (20, "regular", "NEWUSER", False, 0),
        (20, "new", "NEWUSER", True, 3),
        (10, "regular", "UNKNOWN", False, 0),
    ],
)
def test_discount_code_rules(subtotal, customer_type, code, valid, discount):
    order = Order(
        [{"name": "item", "price": subtotal, "quantity": 1, "weight": 0}],
        customer_type,
    )
    assert order.apply_discount(code) is valid
    assert float(order.calculate_discount()) == pytest.approx(discount)


def test_invalid_discount_clears_previously_applied_code():
    order = Order([{"name": "item", "price": 80, "quantity": 1, "weight": 0}])
    assert order.apply_discount("SAVE10")
    assert not order.apply_discount("EXPIRED")
    assert order.calculate_discount() == 0


def test_non_string_discount_code_is_rejected():
    order = Order([{"name": "item", "price": 80, "quantity": 1, "weight": 0}])
    assert not order.apply_discount(123)


@pytest.mark.parametrize(
    "items",
    [
        [],
        [None],
        [{"name": "item", "price": -1, "quantity": 1, "weight": 0}],
        [{"name": "item", "price": True, "quantity": 1, "weight": 0}],
        [{"name": "item", "price": "not-a-price", "quantity": 1, "weight": 0}],
        [{"name": " ", "price": 1, "quantity": 1, "weight": 0}],
        [{"name": "item", "price": 1, "quantity": -1, "weight": 0}],
        [{"name": "item", "price": 1, "quantity": True, "weight": 0}],
        [{"name": "item", "price": 1, "quantity": 1, "weight": -1}],
        [{"name": "item", "price": float("nan"), "quantity": 1, "weight": 0}],
        [{"name": "item", "price": 1, "quantity": 1.5, "weight": 0}],
    ],
)
def test_invalid_order_items_are_rejected(items):
    with pytest.raises(ValueError):
        Order(items)


@pytest.mark.parametrize("distance", [-1, float("nan"), float("inf")])
def test_invalid_shipping_distance_is_rejected(distance):
    order = Order([{"name": "item", "price": 1, "quantity": 1, "weight": 0}])
    with pytest.raises(ValueError):
        order.set_shipping(distance)


def test_invalid_express_flag_is_rejected():
    order = Order([{"name": "item", "price": 1, "quantity": 1, "weight": 0}])
    with pytest.raises(ValueError, match="is_express"):
        order.set_shipping(0, "yes")


def test_invalid_customer_type_is_rejected():
    with pytest.raises(ValueError, match="customer_type"):
        Order([{"name": "item", "price": 1, "quantity": 1, "weight": 0}], "guest")
