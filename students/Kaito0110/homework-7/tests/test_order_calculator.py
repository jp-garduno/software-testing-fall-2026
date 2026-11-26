"""Data-driven tests for the Order Calculator using CSV test data."""

import csv
import json
from pathlib import Path

import pytest

from src.data_tools import generate_synthetic_orders_csv, validate_order_csv_file
from src.order_calculator import Order

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "test_data" / "order_calculations.csv"
GENERATED_CSV_PATH = BASE_DIR / "test_data" / "generated_orders.csv"


def load_order_test_data(csv_file: Path = CSV_PATH):
    """Load test data from CSV file."""
    test_data = []
    with csv_file.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            items = json.loads(row["items"].replace("'", '"'))
            test_data.append(
                (
                    row["test_name"],
                    items,
                    row["customer_type"],
                    (
                        row["discount_code"]
                        if row["discount_code"] != "NONE"
                        else None
                    ),
                    float(row["distance_km"]),
                    row["is_express"] == "true",
                    float(row["expected_subtotal"]),
                    float(row["expected_discount"]),
                    float(row["expected_tax"]),
                    float(row["expected_shipping"]),
                    float(row["expected_total"]),
                )
            )
    return test_data


# pylint: disable=too-many-arguments,too-many-positional-arguments
@pytest.mark.parametrize(
    "test_name,items,customer_type,discount_code,distance,is_express,"
    "exp_subtotal,exp_discount,exp_tax,exp_shipping,exp_total",
    load_order_test_data(),
    ids=lambda val: val if isinstance(val, str) and len(val) < 45 else "",
)
def test_order_calculation(
    test_name,
    items,
    customer_type,
    discount_code,
    distance,
    is_express,
    exp_subtotal,
    exp_discount,
    exp_tax,
    exp_shipping,
    exp_total,
):
    """Test order calculations with data loaded from CSV."""
    order = Order(items, customer_type)

    if discount_code:
        order.apply_discount(discount_code)

    order.set_shipping(distance, is_express)
    result = order.calculate_total()

    assert result["subtotal"] == pytest.approx(
        exp_subtotal, abs=1e-2
    ), f"{test_name}: Subtotal mismatch"
    assert result["discount"] == pytest.approx(
        exp_discount, abs=1e-2
    ), f"{test_name}: Discount mismatch"
    assert result["tax"] == pytest.approx(
        exp_tax, abs=1e-2
    ), f"{test_name}: Tax mismatch"
    assert result["shipping"] == pytest.approx(
        exp_shipping, abs=1e-2
    ), f"{test_name}: Shipping mismatch"
    assert result["total"] == pytest.approx(
        exp_total, abs=1e-2
    ), f"{test_name}: Total mismatch"


def test_order_csv_data_file_is_valid():
    """Verify the primary order_calculations.csv passes pre-test validation (Bonus C)."""
    validation = validate_order_csv_file(CSV_PATH)
    assert validation["is_valid"] is True
    assert not validation["errors"]


def test_data_validator_detects_missing_columns_and_invalid_rows(tmp_path):
    """Verify validate_order_csv_file reports exact line numbers for bad rows (Bonus C)."""
    bad_header_csv = tmp_path / "bad_header.csv"
    bad_header_csv.write_text("test_name,items\n", encoding="utf-8")
    res_header = validate_order_csv_file(bad_header_csv)
    assert res_header["is_valid"] is False
    assert res_header["errors"][0]["line"] == 1

    bad_rows_csv = tmp_path / "bad_rows.csv"
    bad_rows_csv.write_text(
        "test_name,items,customer_type,discount_code,distance_km,is_express,"
        "expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total\n"
        ",not_json,regular,NONE,abc,maybe,10,0,0.8,1,11.8\n"
        "not_a_list_row,\"{'a': 1}\",regular,NONE,10,true,10,0,0.8,1,11.8\n",
        encoding="utf-8",
    )
    res_rows = validate_order_csv_file(bad_rows_csv)
    assert res_rows["is_valid"] is False
    assert any(err["line"] == 2 for err in res_rows["errors"])
    assert any(err["line"] == 3 for err in res_rows["errors"])


def test_faker_data_generator_creates_100_valid_orders():
    """Generate 100 synthetic orders with Faker and verify all pass validation (Bonus A)."""
    count = generate_synthetic_orders_csv(GENERATED_CSV_PATH, count=100, seed=42)
    assert count == 100

    validation = validate_order_csv_file(GENERATED_CSV_PATH)
    assert validation["is_valid"] is True

    generated_cases = load_order_test_data(GENERATED_CSV_PATH)
    assert len(generated_cases) == 100

    sample_case = generated_cases[0]
    order = Order(sample_case[1], sample_case[2])
    if sample_case[3]:
        order.apply_discount(sample_case[3])
    order.set_shipping(sample_case[4], sample_case[5])
    totals = order.calculate_total()
    assert totals["total"] == pytest.approx(sample_case[10], abs=1e-2)
