"""Bonus tests: Option A (100 generated orders regression) and Option C (Test data validation)."""

import csv
import json
from pathlib import Path
import pytest
from order_calculator import Order
from data_validator import (
    validate_order_csv_file,
    validate_customer_json_file,
    generate_valid_orders,
    save_generated_orders_csv,
)

BASE_DIR = Path(__file__).resolve().parent.parent
TEST_DATA_DIR = BASE_DIR / "test_data"
GENERATED_CSV_PATH = TEST_DATA_DIR / "generated_orders.csv"


def load_generated_orders():
    """Load the 100 programmatically generated orders from CSV."""
    with GENERATED_CSV_PATH.open("r", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


GENERATED_ORDERS = load_generated_orders()


def test_generated_orders_count_and_regression():
    """Verify all 100 generated orders in generated_orders.csv pass calculation checks."""
    assert len(GENERATED_ORDERS) == 100
    for row in GENERATED_ORDERS:
        order = Order(json.loads(row["items"]), row["customer_type"])
        if row["discount_code"] != "NONE":
            order.apply_discount(row["discount_code"])
        order.set_shipping(float(row["distance_km"]), row["is_express"] == "true")
        totals = order.calculate_total()
        assert totals["total"] == pytest.approx(float(row["expected_total"]), abs=1e-2)


def test_generate_and_save_orders_to_tmp(tmp_path):
    """Test programmatic order generator and CSV writer."""
    out_csv = tmp_path / "sample_generated.csv"
    written = save_generated_orders_csv(str(out_csv), count=15, seed=99)
    assert written == 15
    validation = validate_order_csv_file(str(out_csv))
    assert validation["is_valid"] is True
    assert validation["errors"] == []


def test_validate_existing_test_data_files():
    """Verify production CSV and JSON test data files pass schema and type validation."""
    csv_res = validate_order_csv_file(str(TEST_DATA_DIR / "order_calculations.csv"))
    assert csv_res["is_valid"] is True
    assert csv_res["errors"] == []

    json_res = validate_customer_json_file(str(TEST_DATA_DIR / "customer_validation.json"))
    assert json_res["is_valid"] is True
    assert json_res["errors"] == []


def test_validate_order_csv_error_reporting(tmp_path):
    """Verify CSV validator reports missing files, missing columns, and invalid row data with line numbers."""
    missing_res = validate_order_csv_file(str(tmp_path / "nonexistent.csv"))
    assert missing_res["is_valid"] is False
    assert "Line 0" in missing_res["errors"][0]

    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("", encoding="utf-8")
    assert validate_order_csv_file(str(empty_csv))["is_valid"] is False

    bad_header = tmp_path / "bad_header.csv"
    bad_header.write_text("test_name,items\nrow1,[]\n", encoding="utf-8")
    header_res = validate_order_csv_file(str(bad_header))
    assert header_res["is_valid"] is False
    assert "Line 1: Missing required columns" in header_res["errors"][0]

    bad_rows = tmp_path / "bad_rows.csv"
    bad_rows.write_text(
        "test_name,items,customer_type,discount_code,distance_km,is_express,"
        "expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total\n"
        ",not_json,vip,NONE,abc,maybe,10,0,1,1,12\n"
        "row_not_list,{},regular,NONE,10,true,10,0,1,1,12\n",
        encoding="utf-8",
    )
    row_res = validate_order_csv_file(str(bad_rows))
    assert row_res["is_valid"] is False
    assert any("Line 2: Missing test_name" in e for e in row_res["errors"])
    assert any("Line 2: Invalid JSON in items field" in e for e in row_res["errors"])
    assert any("Line 2: Invalid customer_type" in e for e in row_res["errors"])
    assert any("Line 2: is_express must be" in e for e in row_res["errors"])
    assert any("Line 2: Invalid float" in e for e in row_res["errors"])
    assert any("Line 3: items must be a JSON list" in e for e in row_res["errors"])


def test_validate_customer_json_error_reporting(tmp_path):
    """Verify JSON validator reports missing files, syntax errors, and schema violations."""
    assert validate_customer_json_file(str(tmp_path / "missing.json"))["is_valid"] is False

    bad_syntax = tmp_path / "bad_syntax.json"
    bad_syntax.write_text("{broken json", encoding="utf-8")
    syntax_res = validate_customer_json_file(str(bad_syntax))
    assert syntax_res["is_valid"] is False
    assert "Line 1: Invalid JSON" in syntax_res["errors"][0]

    not_list = tmp_path / "not_list.json"
    not_list.write_text('{"a": 1}', encoding="utf-8")
    assert validate_customer_json_file(str(not_list))["is_valid"] is False

    bad_entries = tmp_path / "bad_entries.json"
    bad_entries.write_text(
        json.dumps(
            [
                "not_an_object",
                {"test_name": "missing_fields", "expected": {"is_valid": "yes", "errors": "none"}},
            ]
        ),
        encoding="utf-8",
    )
    entries_res = validate_customer_json_file(str(bad_entries))
    assert entries_res["is_valid"] is False
    assert any("Entry 1: Record must be an object" in e for e in entries_res["errors"])
    assert any("Entry 2: Missing required field 'customer'" in e for e in entries_res["errors"])
    assert any("Entry 2: expected.is_valid must be a boolean" in e for e in entries_res["errors"])
    assert any("Entry 2: expected.errors must be a list" in e for e in entries_res["errors"])


def test_generate_valid_orders_deterministic():
    """Verify generate_valid_orders produces deterministic output for a given seed."""
    batch1 = generate_valid_orders(count=5, seed=7)
    batch2 = generate_valid_orders(count=5, seed=7)
    assert batch1 == batch2
