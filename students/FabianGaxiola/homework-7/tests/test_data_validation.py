"""Tests for preflight checks on external data files."""

from pathlib import Path

from data_loaders import DATA_DIR
from data_validation import validate_customer_json, validate_order_csv


def test_committed_csv_and_json_data_are_well_formed():
    assert not validate_order_csv(DATA_DIR / "order_calculations.csv")
    assert not validate_customer_json(DATA_DIR / "customer_validation.json")


def test_csv_validation_reports_physical_line_numbers(tmp_path: Path):
    csv_path = tmp_path / "bad_orders.csv"
    csv_path.write_text(
        "test_name,items,customer_type,discount_code,distance_km,is_express,"
        "expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total\n"
        'bad_case,"not-json",regular,NONE,0,false,1,0,0.08,0,1.08\n',
        encoding="utf-8",
    )

    errors = validate_order_csv(csv_path)
    assert any(error.startswith("line 2: invalid items JSON") for error in errors)


def test_json_syntax_errors_include_line_number(tmp_path: Path):
    json_path = tmp_path / "bad_customers.json"
    json_path.write_text('[\n  {"test_name": "broken",}\n]', encoding="utf-8")

    errors = validate_customer_json(json_path)
    assert errors and errors[0].startswith("line 2: invalid JSON")


def test_csv_validator_reports_header_and_schema_errors(tmp_path: Path):
    empty_path = tmp_path / "empty.csv"
    empty_path.write_text("", encoding="utf-8")
    assert validate_order_csv(empty_path) == ["line 1: missing CSV header"]

    incomplete_path = tmp_path / "incomplete.csv"
    incomplete_path.write_text("test_name\ncase\n", encoding="utf-8")
    errors = validate_order_csv(incomplete_path)
    assert any(error.startswith("line 1: missing columns") for error in errors)
    assert any(
        error.startswith("line 2: items must be a JSON array") for error in errors
    )


def test_csv_validator_checks_item_shapes_types_and_extra_fields(tmp_path: Path):
    csv_path = tmp_path / "bad_rows.csv"
    header = (
        "test_name,items,customer_type,discount_code,distance_km,is_express,"
        "expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total\n"
    )
    csv_path.write_text(
        header
        + "empty_items,[],regular,NONE,0,false,0,0,0,0,0\n"
        + 'bad_item,"[{}]",regular,NONE,not-number,maybe,NaN,0,0,0,0\n'
        + 'extra_field,"[{}]",regular,NONE,0,false,0,0,0,0,0,extra\n',
        encoding="utf-8",
    )

    errors = validate_order_csv(csv_path)
    assert any("line 2: items must be a non-empty array" in error for error in errors)
    assert any("line 3: each item needs" in error for error in errors)
    assert any(
        "line 3: distance_km must be a finite number" in error for error in errors
    )
    assert any("line 3: is_express must be true or false" in error for error in errors)
    assert any(
        "line 3: expected_subtotal must be a finite number" in error for error in errors
    )
    assert any("line 4: unexpected extra CSV fields" in error for error in errors)


def test_customer_json_validator_checks_record_shapes(tmp_path: Path):
    json_path = tmp_path / "bad_customers.json"
    json_path.write_text(
        '[null, {}, {"test_name":"bad","customer":[],"expected":{"is_valid":true,"errors":"bad"}},'
        '{"test_name":"bad-expected","customer":null,"expected":{"is_valid":"yes"}}]',
        encoding="utf-8",
    )

    errors = validate_customer_json(json_path)
    assert any(error.startswith("record 1: expected an object") for error in errors)
    assert any(error.startswith("record 2: test_name is required") for error in errors)
    assert any(
        "record 3: customer must be an object or null" in error for error in errors
    )
    assert any(
        "record 3: expected.errors must be a string array" in error for error in errors
    )
    assert any(
        "record 4: expected.is_valid must be a boolean" in error for error in errors
    )


def test_customer_json_validator_requires_an_array(tmp_path: Path):
    json_path = tmp_path / "not_array.json"
    json_path.write_text('{"test_name":"not-an-array"}', encoding="utf-8")
    assert validate_customer_json(json_path) == ["record 1: expected a JSON array"]
