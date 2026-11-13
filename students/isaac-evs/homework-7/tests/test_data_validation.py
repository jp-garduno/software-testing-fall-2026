"""Tests for the data file validator (bonus option C) and for the shipped data files themselves."""

import json

import pytest
from data_loader import CUSTOMER_JSON, DATA_DIR, ORDER_CSV, WORKFLOW_JSON

from data_validator import (
    Problem,
    check_minimum_counts,
    validate_customer_json,
    validate_order_csv,
    validate_workflow_json,
)

HEADER = (
    "test_name,category,items,customer_type,discount_code,distance_km,is_express,"
    "expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total,expected_error\n"
)
GOOD_ITEMS = '"[{""name"": ""A"", ""price"": 10, ""quantity"": 1, ""weight"": 1}]"'
GOOD_ROW = f"ok_case,simple,{GOOD_ITEMS},regular,NONE,0,false,10.00,0.00,0.80,0.50,11.30,\n"


def write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


# --- the shipped data files must be clean and large enough -------------------------------------


@pytest.mark.parametrize(
    "validator, path",
    [
        (validate_order_csv, ORDER_CSV),
        (validate_order_csv, DATA_DIR / "comparison_orders.csv"),
        (validate_customer_json, CUSTOMER_JSON),
        (validate_workflow_json, WORKFLOW_JSON),
    ],
    ids=["orders", "comparison_orders", "customers", "workflows"],
)
def test_shipped_data_files_have_no_problems(validator, path):
    assert [str(problem) for problem in validator(path)] == []


def test_shipped_data_files_meet_the_minimum_case_counts():
    assert len(check_minimum_counts(ORDER_CSV, CUSTOMER_JSON, WORKFLOW_JSON)) == 0


# --- order CSV ---------------------------------------------------------------------------------


def test_a_well_formed_csv_row_passes(tmp_path):
    assert len(validate_order_csv(write(tmp_path, "ok.csv", HEADER + GOOD_ROW))) == 0


def test_missing_columns_are_reported(tmp_path):
    problems = validate_order_csv(write(tmp_path, "bad.csv", "test_name,items\nx,y\n"))
    assert len(problems) == 1 and "missing columns" in problems[0].message


@pytest.mark.parametrize(
    "row, expected_message",
    [
        ("x,simple,not json,regular,NONE,0,false,1,1,1,1,1,\n", "not valid JSON"),
        (f"x,simple,{GOOD_ITEMS},regular,NONE,far,false,1,1,1,1,1,\n", "distance_km must be a number"),
        (f"x,simple,{GOOD_ITEMS},regular,NONE,0,maybe,1,1,1,1,1,\n", "is_express must be true or false"),
        (f"x,simple,{GOOD_ITEMS},regular,NONE,0,false,1,1,abc,1,1,\n", "expected_tax must be a number"),
        (f"x,simple,{GOOD_ITEMS},,NONE,0,false,1,1,1,1,1,\n", "customer_type is required"),
        (f"x,simple,{GOOD_ITEMS},regular,NONE,0,false,1,1,1,1,1,boom\n", "must be empty when expected_error is set"),
        ('x,simple,"{}",regular,NONE,0,false,1,1,1,1,1,\n', "items must be a JSON list"),
        ('x,simple,"[1]",regular,NONE,0,false,1,1,1,1,1,\n', "item 1 must be an object"),
        ('x,simple,"[{}]",regular,NONE,0,false,1,1,1,1,1,\n', "item 1 needs a name of the right type"),
    ],
)
def test_bad_csv_rows_are_reported_with_their_line_number(tmp_path, row, expected_message):
    path = write(tmp_path, "bad.csv", HEADER + GOOD_ROW + row)
    problems = validate_order_csv(path)
    assert problems and all(problem.line == 3 for problem in problems)
    assert any(expected_message in problem.message for problem in problems)


def test_duplicate_csv_test_names_point_back_to_the_first_line(tmp_path):
    problems = validate_order_csv(write(tmp_path, "dup.csv", HEADER + GOOD_ROW + GOOD_ROW))
    assert [(p.line, "first used on line 2" in p.message) for p in problems] == [(3, True)]


# --- customer JSON -----------------------------------------------------------------------------


def customer_case(**overrides):
    case = {"test_name": "c1", "category": "valid", "customer": {}, "expected": {"is_valid": True, "errors": []}}
    case.update(overrides)
    return case


def write_json(tmp_path, data):
    return write(tmp_path, "data.json", json.dumps(data, indent=2))


def test_a_well_formed_customer_file_passes(tmp_path):
    assert len(validate_customer_json(write_json(tmp_path, [customer_case()]))) == 0


def test_invalid_json_is_reported_with_its_line(tmp_path):
    problems = validate_customer_json(write(tmp_path, "broken.json", '[\n  {"test_name": "a",\n]'))
    assert len(problems) == 1 and problems[0].line == 3 and "invalid JSON" in problems[0].message


def test_top_level_must_be_a_list(tmp_path):
    problems = validate_customer_json(write_json(tmp_path, {"a": 1}))
    assert "must be a list" in problems[0].message


@pytest.mark.parametrize(
    "overrides, expected_message",
    [
        ({"customer": "x"}, "customer must be an object"),
        ({"category": 5}, "category must be a string"),
        ({"expected": {"is_valid": "yes", "errors": []}}, "is_valid must be true or false"),
        ({"expected": {"is_valid": True, "errors": "none"}}, "errors must be a list"),
        ({"expected": {"is_valid": True, "errors": ["boom"]}}, "contradicts"),
    ],
)
def test_bad_customer_cases_are_reported_on_the_line_of_their_name(tmp_path, overrides, expected_message):
    path = write_json(tmp_path, [customer_case(test_name="first"), customer_case(test_name="second", **overrides)])
    problems = validate_customer_json(path)
    assert problems and all(problem.test_name == "second" for problem in problems)
    assert any(expected_message in problem.message for problem in problems)
    lines = path.read_text(encoding="utf-8").splitlines()
    assert problems[0].line == next(number for number, text in enumerate(lines, 1) if '"second"' in text)


def test_duplicate_customer_names_are_reported(tmp_path):
    problems = validate_customer_json(write_json(tmp_path, [customer_case(), customer_case()]))
    assert [problem.message for problem in problems] == ["duplicate test_name"]


def test_non_object_customer_case_is_reported(tmp_path):
    problems = validate_customer_json(write_json(tmp_path, ["nope"]))
    assert problems[0].message == "case must be an object"


def test_blank_customer_test_name_is_reported(tmp_path):
    problems = validate_customer_json(write_json(tmp_path, [customer_case(test_name="")]))
    assert "non-empty string" in problems[0].message


# --- workflow JSON -----------------------------------------------------------------------------


def workflow_file(steps, customers=None):
    return {"customers": customers or {}, "workflows": [{"name": "flow", "steps": steps}]}


def test_a_well_formed_workflow_file_passes(tmp_path):
    steps = [{"action": "calculate_total", "expected": {"total": 1}}]
    assert len(validate_workflow_json(write_json(tmp_path, workflow_file(steps)))) == 0


@pytest.mark.parametrize(
    "step, expected_message",
    [
        ({"action": "teleport", "expected": {}}, "unknown action"),
        ({"action": "calculate_total"}, "expected must be an object"),
        ({"action": "validate_customer", "data": {"customer": "ghost"}, "expected": {}}, "unknown customer"),
    ],
)
def test_bad_workflow_steps_are_reported(tmp_path, step, expected_message):
    problems = validate_workflow_json(write_json(tmp_path, workflow_file([step])))
    assert any(expected_message in problem.message for problem in problems)


def test_workflow_without_steps_is_reported(tmp_path):
    problems = validate_workflow_json(write_json(tmp_path, workflow_file([])))
    assert "non-empty list of steps" in problems[0].message


def test_workflows_must_be_a_list(tmp_path):
    assert "workflows must be a list" in validate_workflow_json(write_json(tmp_path, {"workflows": 1}))[0].message


def test_broken_workflow_json_is_reported(tmp_path):
    problems = validate_workflow_json(write(tmp_path, "broken.json", "{"))
    assert "invalid JSON" in problems[0].message


# --- minimum counts and Problem formatting ----------------------------------------------------


def test_small_data_files_are_reported_as_shortfalls(tmp_path):
    csv_path = write(tmp_path, "small.csv", HEADER + GOOD_ROW)
    customers = write_json(tmp_path, [customer_case()])
    flows = write(tmp_path, "flows.json", json.dumps(workflow_file([])))
    shortfalls = check_minimum_counts(csv_path, customers, flows)
    assert "order cases: 1 < 25" in shortfalls
    assert "customer cases: 1 < 30" in shortfalls
    assert "workflows: 1 < 3" in shortfalls


def test_problem_string_includes_line_and_name():
    assert str(Problem(7, "case_a", "boom")) == "line 7 [case_a]: boom"
    assert str(Problem(2, "", "boom")) == "line 2: boom"
