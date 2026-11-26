"""Data-driven tests for Order (CSV) plus unit tests for its edge cases."""

import pytest

from data_loader import case_ids, load_order_cases
from order_calculator import Order

CASES = load_order_cases()


def build_order(case):
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance"], case["is_express"])
    return order


def test_csv_has_required_volume():
    assert len(CASES) >= 25
    assert len({c["test_name"] for c in CASES}) == len(CASES), "duplicate test names"


@pytest.mark.parametrize("case", CASES, ids=case_ids(CASES))
def test_order_calculation(case):
    """Every CSV row: all five components of the breakdown must match."""
    result = build_order(case).calculate_total()
    for key, expected in case["expected"].items():
        assert result[key] == pytest.approx(
            expected, abs=0.005
        ), f"{case['test_name']}: {key} mismatch"


@pytest.mark.parametrize("case", CASES, ids=case_ids(CASES))
def test_individual_methods_match_breakdown(case):
    """The per-component methods must agree with calculate_total."""
    order = build_order(case)
    total = order.calculate_total()
    assert order.calculate_subtotal() == total["subtotal"]
    assert order.calculate_discount() == total["discount"]
    assert order.calculate_tax() == total["tax"]
    assert order.calculate_shipping() == total["shipping"]


# ---- behaviours that cannot be expressed in the CSV ------------------
ITEM = {"name": "X", "price": 60, "quantity": 1, "weight": 1}


def test_apply_discount_returns_true_for_valid_code():
    assert Order([ITEM]).apply_discount("SAVE10") is True


@pytest.mark.parametrize("code", ["SAVE20", "NOPE", "", "save10"])
def test_apply_discount_returns_false_for_rejected_code(code):
    order = Order([ITEM])
    assert order.apply_discount(code) is False
    assert order.discount_code is None


def test_newuser_rejected_for_regular_customer():
    assert Order([ITEM], "regular").apply_discount("NEWUSER") is False


def test_rejected_code_keeps_previous_valid_code():
    order = Order([ITEM])
    order.apply_discount("SAVE10")
    order.apply_discount("BOGUS")
    assert order.discount_code == "SAVE10"


def test_negative_price_raises():
    with pytest.raises(ValueError, match="negative price"):
        Order([{"name": "Bad", "price": -1, "quantity": 1, "weight": 0}]).calculate_subtotal()


def test_negative_quantity_raises():
    with pytest.raises(ValueError, match="negative quantity"):
        Order([{"name": "Bad", "price": 1, "quantity": -2, "weight": 0}]).calculate_total()


def test_negative_weight_raises():
    order = Order([{"name": "Bad", "price": 1, "quantity": 1, "weight": -1}])
    with pytest.raises(ValueError, match="negative weight"):
        order.calculate_shipping()


def test_negative_distance_raises():
    with pytest.raises(ValueError, match="distance"):
        Order([ITEM]).set_shipping(-5)


def test_missing_weight_defaults_to_zero():
    order = Order([{"name": "NoWeight", "price": 10, "quantity": 2}])
    order.set_shipping(10)
    assert order.calculate_shipping() == 1.0


def test_total_is_sum_of_components():
    order = Order([{"name": "A", "price": 33.33, "quantity": 3, "weight": 0.7}], "new")
    order.apply_discount("NEWUSER")
    order.set_shipping(17.5, True)
    r = order.calculate_total()
    assert r["total"] == pytest.approx(
        r["subtotal"] - r["discount"] + r["tax"] + r["shipping"], abs=0.005
    )
