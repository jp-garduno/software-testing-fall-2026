"""Bonus A: Faker-based generator of 100 valid orders saved to CSV."""

import pytest
from src.data_validator import validate_all
from src.order_generator import generate_order_rows, write_orders_csv
from src.orders_csv_check import validate_orders_csv
from tests.data_loader import TEST_DATA_DIR, calculate_case, load_order_cases


def test_generate_order_rows_default_count_is_100():
    assert len(generate_order_rows()) == 100


def test_generate_order_rows_same_seed_is_reproducible():
    assert generate_order_rows(10, seed=7) == generate_order_rows(10, seed=7)


def test_generate_order_rows_newuser_only_for_new_customers():
    rows = generate_order_rows(200, seed=1)

    assert all(
        r["customer_type"] == "new" for r in rows if r["discount_code"] == "NEWUSER"
    )


def test_write_orders_csv_output_passes_data_validation(tmp_path):
    path = write_orders_csv(generate_order_rows(20), tmp_path / "generated.csv")

    assert validate_orders_csv(path) == []


def test_committed_generated_orders_csv_has_100_rows_and_passes_validation():
    path = TEST_DATA_DIR / "generated_orders.csv"

    assert (
        len(path.read_text(encoding="utf-8").splitlines()) - 1,
        validate_all(TEST_DATA_DIR),
    ) == (100, [])


@pytest.mark.parametrize("case", load_order_cases("generated_orders.csv"))
def test_generated_order_through_order_matches_expected_breakdown(case):
    result = calculate_case(case)

    assert result == pytest.approx(case["expected"], abs=0.005)
