"""Order calculator tests, driven by order_calculations.csv.

One CSV row is a complete case: inputs, the five expected amounts and, where
it applies, the error that must be raised. Adding a case means adding a line
to the CSV, without touching this file.
"""

import pytest

from conftest import build_order, order_cases
from order_calculator import Order

CASES = order_cases()
ONE_CENT = 0.005


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["test_name"])
def test_full_order_breakdown(case):
    """Check the five amounts, or the error, of every CSV row."""
    if case["expected_error"]:
        with pytest.raises(ValueError) as error:
            build_order(case)
        assert str(error.value) == case["expected_error"]
        return

    breakdown = build_order(case).calculate_total()

    for key, expected in case["expected"].items():
        assert breakdown[key] == pytest.approx(expected, abs=ONE_CENT), f"{key} in {case['test_name']}"


@pytest.mark.parametrize("case", [c for c in CASES if not c["expected_error"]], ids=lambda c: c["test_name"])
def test_the_total_is_the_sum_of_its_parts(case):
    """subtotal - discount + tax + shipping has to add up to the total."""
    breakdown = build_order(case).calculate_total()
    added = breakdown["subtotal"] - breakdown["discount"] + breakdown["tax"] + breakdown["shipping"]

    assert breakdown["total"] == pytest.approx(added, abs=ONE_CENT)


class TestCsvCoverage:
    """The CSV has to keep meeting what the brief asks for."""

    def test_minimum_number_of_cases(self):
        assert len(CASES) >= 25

    @pytest.mark.parametrize(
        "category,minimum",
        [("simple", 3), ("discount", 5), ("tax", 4), ("shipping", 6), ("complex", 7)],
    )
    def test_minimum_per_category(self, category, minimum):
        assert len([c for c in CASES if c["category"] == category]) >= minimum

    def test_there_are_error_cases(self):
        assert any(c["expected_error"] for c in CASES)


class TestDiscountRules:
    """apply_discount behaviour that the CSV cannot express as an amount."""

    def test_unknown_code_is_rejected(self):
        order = Order([{"name": "X", "price": 100.0, "quantity": 1, "weight": 0.0}])
        assert order.apply_discount("NOPE") is False
        assert order.discount_code is None

    def test_newuser_only_for_new_customers(self):
        new = Order([{"name": "X", "price": 10.0, "quantity": 1, "weight": 0.0}], "new")
        regular = Order([{"name": "X", "price": 10.0, "quantity": 1, "weight": 0.0}], "regular")

        assert new.apply_discount("NEWUSER") is True
        assert regular.apply_discount("NEWUSER") is False

    def test_a_rejected_code_does_not_replace_the_previous_one(self):
        order = Order([{"name": "X", "price": 100.0, "quantity": 1, "weight": 0.0}])
        order.apply_discount("SAVE20")

        assert order.apply_discount("NOPE") is False
        assert order.discount_code == "SAVE20"

    def test_freeship_does_not_discount_the_price(self):
        order = Order([{"name": "X", "price": 100.0, "quantity": 1, "weight": 5.0}])
        order.apply_discount("FREESHIP")
        order.set_shipping(100)

        assert order.calculate_discount() == 0.0
        assert order.calculate_shipping() == 0.0


class TestInvalidInput:
    """What the constructor and set_shipping have to reject."""

    @pytest.mark.parametrize(
        "items,message",
        [
            ("not a list", "items must be a list"),
            ([["not", "a", "dict"]], "each item must be an object"),
            ([{"price": 1.0, "quantity": 1, "weight": 1.0}], "item is missing name"),
            ([{"name": "", "price": 1.0, "quantity": 1, "weight": 1.0}], "item name must be a non-empty string"),
            ([{"name": "X", "price": "1.0", "quantity": 1, "weight": 1.0}], "price must be a number"),
            ([{"name": "X", "price": float("nan"), "quantity": 1, "weight": 1.0}], "price must be a finite number"),
            ([{"name": "X", "price": float("inf"), "quantity": 1, "weight": 1.0}], "price must be a finite number"),
            ([{"name": "X", "price": 1.0, "quantity": 1.5, "weight": 1.0}], "quantity must be a whole number"),
            ([{"name": "X", "price": 1.0, "quantity": True, "weight": 1.0}], "quantity must be a whole number"),
            ([{"name": "X", "price": 1.0, "quantity": 1, "weight": -1.0}], "weight must not be negative"),
        ],
    )
    def test_invalid_items(self, items, message):
        with pytest.raises(ValueError, match=message):
            Order(items)

    def test_invalid_customer_type(self):
        with pytest.raises(ValueError, match="customer_type must be new or regular"):
            Order([], "vip")

    def test_express_must_be_a_boolean(self):
        with pytest.raises(ValueError, match="is_express must be a boolean"):
            Order([]).set_shipping(10, "yes")

    def test_non_numeric_distance(self):
        with pytest.raises(ValueError, match="distance_km must be a number"):
            Order([]).set_shipping("ten")
