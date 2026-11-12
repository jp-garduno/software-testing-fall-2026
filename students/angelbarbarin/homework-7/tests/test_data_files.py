"""Tests for the test-data validator (bonus option C).

Each case writes a deliberately broken file to a temporary folder and checks that the
validator reports the right problem on the right line.
"""

import json
from pathlib import Path

import pytest

from data_files import (
    TestDataError,
    load_customer_cases,
    load_order_cases,
    load_workflows,
    main,
    validate_customer_json,
    validate_directory,
    validate_order_csv,
    validate_workflow_json,
)

HEADER = (
    "test_name,category,items,customer_type,discount_code,distance_km,is_express,"
    "expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total,expected_error"
)
GOOD_ITEMS = '"[{""name"":""A"",""price"":10,""quantity"":1,""weight"":1}]"'
GOOD_ROW = f"ok_case,simple,{GOOD_ITEMS},regular,NONE,10,false,10.00,0.00,0.80,5.50,16.30,"
DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"


def write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_real_data_files_are_valid():
    assert not validate_directory(DATA_DIR)


@pytest.mark.parametrize(
    "row,message",
    [
        (GOOD_ROW.replace("ok_case", ""), "test_name is empty"),
        (GOOD_ROW.replace(GOOD_ITEMS, '"[{bad json}]"'), "items is not valid JSON"),
        (GOOD_ROW.replace(GOOD_ITEMS, '"{""name"":""A""}"'), "items must be a JSON list"),
        (GOOD_ROW.replace(GOOD_ITEMS, '"[{""name"":""A"",""price"":10}]"'), "item 0 is missing quantity, weight"),
        (GOOD_ROW.replace("regular", "vip"), "customer_type must be new or regular"),
        (GOOD_ROW.replace("NONE", ""), "discount_code is empty"),
        (GOOD_ROW.replace(",10,false", ",ten,false"), "distance_km is not a number"),
        (GOOD_ROW.replace("false", "yes"), "is_express must be true or false"),
        (GOOD_ROW.replace("16.30", "sixteen"), "expected_total is not a number"),
        (GOOD_ROW + "price cannot be negative", "must leave the expected amounts empty"),
        ("short,row", "wrong number of columns"),
    ],
)
def test_order_csv_problem_is_reported_with_line_number(tmp_path, row, message):
    path = write(tmp_path, "orders.csv", f"{HEADER}\n{GOOD_ROW}\n{row}\n")

    errors = validate_order_csv(path)

    assert any(message in error.message for error in errors), errors
    assert all(error.line == 3 for error in errors)
    assert str(errors[0]).startswith("orders.csv:3: ")


def test_order_csv_missing_column(tmp_path):
    path = write(tmp_path, "orders.csv", "test_name,items\nx,[]\n")
    errors = validate_order_csv(path)
    assert len(errors) == 1 and errors[0].line == 1 and "missing column(s)" in errors[0].message


def test_order_csv_duplicate_names(tmp_path):
    path = write(tmp_path, "orders.csv", f"{HEADER}\n{GOOD_ROW}\n{GOOD_ROW}\n")
    errors = validate_order_csv(path)
    assert [str(error) for error in errors] == ["orders.csv:3: duplicate test_name 'ok_case' (first on line 2)"]


def test_loader_raises_with_all_problems(tmp_path):
    path = write(tmp_path, "orders.csv", f"{HEADER}\n{GOOD_ROW.replace('false', 'maybe')}\n")
    with pytest.raises(TestDataError, match="orders.csv:2: is_express"):
        load_order_cases(path)


CUSTOMER = {"email": "a@b.co"}


@pytest.mark.parametrize(
    "cases,message",
    [
        ({"not": "a list"}, "top level must be a list"),
        ([{"customer": CUSTOMER, "expected": {"is_valid": True, "errors": []}}], "case 0 has no test_name"),
        (
            [{"test_name": "c1", "customer": "x", "expected": {"is_valid": True, "errors": []}}],
            "customer must be an object",
        ),
        (
            [{"test_name": "c1", "customer": CUSTOMER, "expected": {"is_valid": "yes"}}],
            "is_valid must be true or false",
        ),
        (
            [{"test_name": "c1", "customer": CUSTOMER, "expected": {"is_valid": False, "errors": "x"}}],
            "errors must be a list",
        ),
        ([{"test_name": "c1", "customer": CUSTOMER, "expected": {"is_valid": True, "errors": ["E"]}}], "contradicts"),
        (
            [
                {"test_name": "c1", "customer": CUSTOMER, "expected": {"is_valid": True, "errors": []}},
                {"test_name": "c1", "customer": CUSTOMER, "expected": {"is_valid": True, "errors": []}},
            ],
            "duplicate test_name",
        ),
    ],
)
def test_customer_json_problems(tmp_path, cases, message):
    path = write(tmp_path, "customer_validation.json", json.dumps(cases, indent=2))
    errors = validate_customer_json(path)
    assert any(message in error.message for error in errors), errors
    with pytest.raises(TestDataError):
        load_customer_cases(path)


def test_customer_json_reports_line_of_the_bad_case(tmp_path):
    good = {"test_name": "first", "customer": CUSTOMER, "expected": {"is_valid": True, "errors": []}}
    bad = {"test_name": "second", "customer": CUSTOMER, "expected": {"is_valid": True, "errors": ["E"]}}
    path = write(tmp_path, "customer_validation.json", json.dumps([good, bad], indent=2))
    text_lines = path.read_text(encoding="utf-8").splitlines()

    (error,) = validate_customer_json(path)

    assert '"second"' in text_lines[error.line - 1]


def test_invalid_json_syntax_reports_its_line(tmp_path):
    path = write(tmp_path, "customer_validation.json", '[\n  {"test_name": "x",\n  oops\n]')
    (error,) = validate_customer_json(path)
    assert error.line == 3 and "invalid JSON" in error.message


@pytest.mark.parametrize(
    "data,message",
    [
        ([], 'object with a "workflows" list'),
        ({"workflows": [{"steps": []}]}, "workflow 0 has no name"),
        ({"workflows": [{"name": "w", "steps": []}]}, "steps must be a non-empty list"),
        ({"workflows": [{"name": "w", "steps": [{"expected": {}}]}]}, "step 1 has no action"),
        ({"workflows": [{"name": "w", "steps": [{"action": "calculate_total"}]}]}, "step 1 has no expected object"),
    ],
)
def test_workflow_json_problems(tmp_path, data, message):
    path = write(tmp_path, "order_workflows.json", json.dumps(data, indent=2))
    errors = validate_workflow_json(path)
    assert any(message in error.message for error in errors), errors
    with pytest.raises(TestDataError):
        load_workflows(path)


def test_workflow_json_syntax_error(tmp_path):
    path = write(tmp_path, "order_workflows.json", "{")
    assert "invalid JSON" in validate_workflow_json(path)[0].message


def test_validate_directory_combines_every_file(tmp_path):
    write(tmp_path, "orders.csv", f"{HEADER}\n{GOOD_ROW.replace('regular', 'vip')}\n")
    write(tmp_path, "customer_validation.json", "{}")
    write(tmp_path, "order_workflows.json", "[]")
    assert len(validate_directory(tmp_path)) == 3


def test_cli_exit_codes(tmp_path, capsys):
    assert main([str(DATA_DIR)]) == 0
    write(tmp_path, "orders.csv", "bad header\n")
    assert main([str(tmp_path)]) == 1
    assert "1 problem(s) found" in capsys.readouterr().out
