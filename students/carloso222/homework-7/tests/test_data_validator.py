"""Bonus C: the data validator finds bad rows/fields and reports line numbers."""

import json
from pathlib import Path

import pytest
from src.data_validator import format_report, validate_all
from src.orders_csv_check import REQUIRED_COLUMNS, validate_orders_csv
from tests.data_loader import TEST_DATA_DIR

HEADER = ",".join(REQUIRED_COLUMNS)
GOOD_ROW = (
    'ok_row,"[{""name"": ""A"", ""price"": 5, ""quantity"": 1, ""weight"": 0}]",'
    "regular,NONE,0,false,5.00,0.00,0.40,0.00,5.40"
)


def _write(tmp_path: Path, name: str, content: str) -> Path:
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return path


def _csv(tmp_path: Path, *rows: str) -> Path:
    return _write(tmp_path, "orders.csv", "\n".join([HEADER, *rows]) + "\n")


def test_validate_all_real_test_data_has_no_issues():
    assert validate_all(TEST_DATA_DIR) == []


def test_validate_orders_csv_valid_file_returns_no_issues(tmp_path):
    assert validate_orders_csv(_csv(tmp_path, GOOD_ROW)) == []


def test_validate_orders_csv_missing_column_reports_line_one(tmp_path):
    path = _write(tmp_path, "orders.csv", "test_name,items\nx,[]\n")

    issues = validate_orders_csv(path)

    assert (issues[0].line, "missing required columns" in issues[0].message) == (
        1,
        True,
    )


def test_validate_orders_csv_bad_number_reports_row_line(tmp_path):
    bad = GOOD_ROW.replace("ok_row", "bad_row").replace("5.40", "abc")

    issues = validate_orders_csv(_csv(tmp_path, GOOD_ROW, bad))

    assert [(i.line, i.message) for i in issues] == [
        (3, "expected_total must be a number")
    ]


def test_validate_orders_csv_empty_field_reports_each_empty_column(tmp_path):
    row = GOOD_ROW.replace("regular", "")

    issues = validate_orders_csv(_csv(tmp_path, row))

    assert [i.message for i in issues] == ["customer_type is empty"]


@pytest.mark.parametrize(
    "row, message",
    [
        (
            GOOD_ROW.replace("regular", "vip"),
            "customer_type must be 'new' or 'regular'",
        ),
        (GOOD_ROW.replace("false", "yes"), "is_express must be 'true' or 'false'"),
        ('bad,"not json",regular,NONE,0,false,1,1,1,1,1', "items is not valid JSON"),
    ],
    ids=["customer_type", "is_express", "items_json"],
)
def test_validate_orders_csv_invalid_values_are_reported(tmp_path, row, message):
    issues = validate_orders_csv(_csv(tmp_path, row))

    assert message in issues[0].message


def test_validate_orders_csv_items_wrong_types_are_reported_per_field(tmp_path):
    items = json.dumps(
        [{"name": 1, "price": "x", "quantity": 1.5, "weight": None}, "str"]
    ).replace('"', '""')
    row = f'bad,"{items}",regular,NONE,0,false,1,1,1,1,1'

    messages = [i.message for i in validate_orders_csv(_csv(tmp_path, row))]

    assert len(messages) == 5 and "items[1] must be an object" in messages


def test_validate_orders_csv_items_not_a_list_is_reported(tmp_path):
    row = 'bad,"{}",regular,NONE,0,false,1,1,1,1,1'

    assert (
        validate_orders_csv(_csv(tmp_path, row))[0].message
        == "items must be a JSON list"
    )


def test_validate_orders_csv_duplicate_test_name_is_reported(tmp_path):
    issues = validate_orders_csv(_csv(tmp_path, GOOD_ROW, GOOD_ROW))

    assert [(i.line, "duplicate" in i.message) for i in issues] == [(3, True)]


def _data_dir(tmp_path: Path, customers: str, workflows: str) -> Path:
    (tmp_path / "order_calculations.csv").write_text(
        HEADER + "\n" + GOOD_ROW + "\n", encoding="utf-8"
    )
    (tmp_path / "customer_validation.json").write_text(customers, encoding="utf-8")
    (tmp_path / "order_workflows.json").write_text(workflows, encoding="utf-8")
    return tmp_path


GOOD_CUSTOMERS = '[\n  {"test_name": "a", "customer": {}, "expected": {"is_valid": false, "errors": []}}\n]'
GOOD_WORKFLOWS = (
    '{"reference_date": "2026-01-15", "workflows": [\n'
    '  {"name": "w", "steps": [{"action": "process_payment", "expected": {}}]}\n]}'
)


def test_validate_all_minimal_valid_directory_has_no_issues(tmp_path):
    assert validate_all(_data_dir(tmp_path, GOOD_CUSTOMERS, GOOD_WORKFLOWS)) == []


def test_validate_all_missing_files_are_reported(tmp_path):
    messages = [str(i) for i in validate_all(tmp_path)]

    assert messages == [
        "customer_validation.json:0: required data file not found",
        "order_workflows.json:0: required data file not found",
        "order_calculations.csv:0: required data file not found",
    ]


def test_validate_customers_json_bad_case_reports_line_number(tmp_path):
    customers = (
        '[\n  {"test_name": "ok", "customer": {}, "expected": {"is_valid": true, "errors": []}},\n'
        '  {"test_name": "", "customer": 5, "expected": {"is_valid": "yes", "errors": [1]}}\n]'
    )

    issues = validate_all(_data_dir(tmp_path, customers, GOOD_WORKFLOWS))

    assert {i.line for i in issues} == {3} and len(issues) == 4


def test_validate_customers_json_missing_expected_and_non_object_case(tmp_path):
    customers = '[\n  {"test_name": "a", "customer": {}},\n  7\n]'

    messages = [
        str(i) for i in validate_all(_data_dir(tmp_path, customers, GOOD_WORKFLOWS))
    ]

    assert messages == [
        "customer_validation.json:2: item #1: expected must be an object",
        "customer_validation.json:3: item #2: case must be an object",
    ]


def test_validate_json_syntax_error_reports_line(tmp_path):
    issues = validate_all(_data_dir(tmp_path, '[\n  {"a": }\n]', GOOD_WORKFLOWS))

    assert (issues[0].line, issues[0].message.startswith("invalid JSON")) == (2, True)


def test_validate_customers_json_top_level_not_list_is_reported(tmp_path):
    issues = validate_all(_data_dir(tmp_path, '{"a": 1}', GOOD_WORKFLOWS))

    assert issues[0].message == "top level must be a list of cases"


def test_validate_workflows_json_bad_steps_are_reported(tmp_path):
    workflows = (
        '{"reference_date": 5, "workflows": [\n'
        '  {"name": "w", "steps": [{"action": "fly", "expected": {}}, {"action": "create_order", "expected": 1}, 3]},\n'
        '  {"name": "", "steps": []},\n'
        '  "x"\n]}'
    )

    messages = [
        str(i) for i in validate_all(_data_dir(tmp_path, GOOD_CUSTOMERS, workflows))
    ]

    assert len(messages) == 8 and any(
        "steps[0].action must be one of" in m for m in messages
    )
    assert "order_workflows.json:4: item #3: workflow must be an object" in messages
    assert (
        "order_workflows.json:1: reference_date must be a string (YYYY-MM-DD)"
        in messages
    )


def test_validate_workflows_json_top_level_shape_is_reported(tmp_path):
    issues = validate_all(_data_dir(tmp_path, GOOD_CUSTOMERS, "[]"))

    assert issues[0].message == "top level must be an object with a 'workflows' list"


def test_format_report_lists_each_issue_with_file_and_line(tmp_path):
    report = format_report(validate_all(tmp_path))

    assert report.splitlines()[0] == "3 problem(s) found in the test data files:"
    assert "  customer_validation.json:0: required data file not found" in report


def test_validate_workflows_json_syntax_error_reports_line(tmp_path):
    issues = validate_all(_data_dir(tmp_path, GOOD_CUSTOMERS, '{\n  "workflows": [\n'))

    assert (issues[0].file, issues[0].line) == ("order_workflows.json", 3)
