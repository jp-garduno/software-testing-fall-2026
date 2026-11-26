"""Tests for the Faker data generator (Bonus option A).

test_generated_order_regression is the golden-master check: the 100 orders in
test_data/generated_orders.csv were priced when the file was generated, and
must still be priced the same way today.
"""

from datetime import date

import pytest

from src.customer_validator import validate_customer
from src.data_generator import generate_customers, generate_orders, write_orders_csv
from src.data_loader import load_order_cases
from src.data_validation import DATA_DIR, validate_order_csv
from src.order_calculator import Order

GENERATED_CASES = load_order_cases(DATA_DIR / "generated_orders.csv")


@pytest.mark.parametrize("case", GENERATED_CASES, ids=lambda case: case.test_name)
def test_generated_order_regression(case):
    order = Order(case.items, case.customer_type)
    if case.discount_code:
        order.apply_discount(case.discount_code)
    order.set_shipping(case.distance_km, case.is_express)
    assert order.calculate_total() == pytest.approx(case.expected, abs=0.001)


def test_regression_file_has_100_orders():
    assert len(GENERATED_CASES) == 100


@pytest.mark.parametrize("case", GENERATED_CASES, ids=lambda case: case.test_name)
def test_generated_order_invariants(case):
    """Properties that hold for any order, independent of how it was priced."""
    expected = case.expected
    net = expected["subtotal"] - expected["discount"]
    assert expected["tax"] == pytest.approx(net * 0.08, abs=0.006)
    assert 0 <= expected["discount"] <= expected["subtotal"] * 0.20 + 0.005
    if case.discount_code == "FREESHIP":
        assert expected["shipping"] == 0


def test_generation_is_reproducible_with_a_seed():
    assert generate_orders(5, seed=1) == generate_orders(5, seed=1)
    assert generate_orders(5, seed=1) != generate_orders(5, seed=2)


def test_written_csv_passes_data_validation(tmp_path):
    path = tmp_path / "orders.csv"
    write_orders_csv(generate_orders(20, seed=3), path)
    issues = validate_order_csv(path)
    assert not issues, issues
    assert len(load_order_cases(path)) == 20


@pytest.mark.parametrize("seed", range(5))
def test_generated_customers_are_all_valid(seed):
    reference = date(2026, 6, 15)
    for customer in generate_customers(100, seed=seed, today=reference):
        errors = validate_customer(customer, reference)["errors"]
        assert not errors, (customer, errors)
