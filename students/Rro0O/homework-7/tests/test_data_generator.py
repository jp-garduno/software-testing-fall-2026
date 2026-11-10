"""Bonus A tests: generated orders are valid, reproducible and regression-safe."""

import pytest

from data_generator import generate_orders, main, write_csv
from data_loader import DATA_DIR, case_ids, load_order_cases
from data_validator import validate_order_csv
from order_calculator import Order


def test_generates_requested_number_of_unique_orders():
    rows = generate_orders(100)
    assert len(rows) == 100
    assert len({r["test_name"] for r in rows}) == 100


def test_same_seed_is_reproducible_and_different_seed_differs():
    assert generate_orders(20, seed=1) == generate_orders(20, seed=1)
    assert generate_orders(20, seed=1) != generate_orders(20, seed=2)


def test_generated_csv_passes_validator(tmp_path):
    out = tmp_path / "gen.csv"
    write_csv(out, generate_orders(30))
    assert validate_order_csv(out) == []


def test_main_writes_file(tmp_path, capsys):
    out = tmp_path / "x.csv"
    assert main([str(out), "5", "3"]) == 0
    assert len(load_order_cases(out)) == 5
    assert "wrote 5 orders" in capsys.readouterr().out


GENERATED = load_order_cases(DATA_DIR / "generated_orders.csv")


def test_committed_regression_file_has_100_orders():
    assert len(GENERATED) == 100


@pytest.mark.parametrize("case", GENERATED, ids=case_ids(GENERATED))
def test_generated_order_regression(case):
    """The committed baseline must still match what the calculator returns."""
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance"], case["is_express"])
    result = order.calculate_total()
    for key, expected in case["expected"].items():
        assert result[key] == pytest.approx(expected, abs=0.005)
