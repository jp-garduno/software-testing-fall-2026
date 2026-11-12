"""Tests for the test-data validator and loaders (Bonus option C).

Broken copies of the data files are written to a temporary directory and the
validator must point at the right line and field for each problem.
"""

import json

import pytest

from src.data_loader import DataFileError, load_customer_cases, load_order_cases, load_workflows
from src.data_validation import (DATA_DIR, DataIssue, main, validate_customer_json, validate_order_csv,
                                 validate_workflows_json)

HEADER = ("test_name,category,items,customer_type,discount_code,distance_km,is_express,"
          "expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total,expected_error")
GOOD_ROW = "ok,simple,\"[{'name':'A','price':10,'quantity':1,'weight':0}]\",regular,NONE,0,false,10,0,0.80,0,10.80,"


def write(tmp_path, name, content):
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return path


def issue_summary(issues):
    return [(issue.line, issue.field) for issue in issues]


@pytest.mark.parametrize("validator,file_name", [
    (validate_order_csv, "order_calculations.csv"),
    (validate_order_csv, "order_comparison.csv"),
    (validate_order_csv, "generated_orders.csv"),
    (validate_customer_json, "customer_validation.json"),
    (validate_workflows_json, "order_workflows.json"),
])
def test_shipped_data_files_are_valid(validator, file_name):
    issues = validator(DATA_DIR / file_name)
    assert not issues, issues


@pytest.mark.parametrize("bad_row,field", [
    (GOOD_ROW, "test_name"),
    (",simple,[],regular,NONE,0,false,0,0,0,0,0,", "test_name"),
    ("b,weird,[],regular,NONE,0,false,0,0,0,0,0,", "category"),
    ("b,simple,not json,regular,NONE,0,false,0,0,0,0,0,", "items"),
    ("b,simple,{},regular,NONE,0,false,0,0,0,0,0,", "items"),
    ("b,simple,[1],regular,NONE,0,false,0,0,0,0,0,", "items"),
    ("b,simple,\"[{'name':'A','price':'x','quantity':1}]\",regular,NONE,0,false,0,0,0,0,0,", "items"),
    ("b,simple,[],vip,NONE,0,false,0,0,0,0,0,", "customer_type"),
    ("b,simple,[],regular,,0,false,0,0,0,0,0,", "discount_code"),
    ("b,simple,[],regular,NONE,far,false,0,0,0,0,0,", "distance_km"),
    ("b,simple,[],regular,NONE,0,yes,0,0,0,0,0,", "is_express"),
    ("b,simple,[],regular,NONE,0,false,abc,0,0,0,0,", "expected_subtotal"),
    ("b,simple,[],regular,NONE,0,false,10,0,0.80,0,99,", "expected_total"),
    ("b,simple,[],regular,NONE,0,false,10,,,,,boom", "expected_subtotal"),
    ("b,simple,[],regular,NONE,0,false", "row"),
])
def test_order_csv_issue_points_at_line_and_field(tmp_path, bad_row, field):
    path = write(tmp_path, "orders.csv", f"{HEADER}\n{GOOD_ROW}\n{bad_row}\n")
    issues = validate_order_csv(path)
    assert (3, field) in issue_summary(issues)
    assert all(issue.line == 3 for issue in issues)


def test_order_csv_missing_column(tmp_path):
    path = write(tmp_path, "orders.csv", "test_name,items\nx,[]\n")
    assert issue_summary(validate_order_csv(path)) == [(1, "header")]


def customer_case(**overrides):
    case = {"test_name": "c", "category": "valid", "reference_date": "2026-01-01", "customer": {},
            "expected": {"is_valid": True, "errors": []}}
    case.update(overrides)
    return case


@pytest.mark.parametrize("bad_case,field", [
    (customer_case(test_name=""), "test_name"),
    (customer_case(test_name="first"), "test_name"),
    (customer_case(category="other"), "category"),
    (customer_case(reference_date="15/06/2026"), "reference_date"),
    (customer_case(customer=[]), "customer"),
    (customer_case(expected=None), "expected"),
    (customer_case(expected={"is_valid": "yes", "errors": []}), "expected.is_valid"),
    (customer_case(expected={"is_valid": False, "errors": "boom"}), "expected.errors"),
    (customer_case(expected={"is_valid": True, "errors": ["Invalid CVV"]}), "expected"),
    ("not an object", "case"),
])
def test_customer_json_issue_points_at_case_line(tmp_path, bad_case, field):
    first = customer_case(test_name="first")
    path = write(tmp_path, "customers.json", json.dumps([first, bad_case], indent=2))
    # Line 1 is "[", then the first case, then the bad one.
    bad_line = 1 + len(json.dumps(first, indent=2).splitlines()) + 1
    assert (bad_line, field) in issue_summary(validate_customer_json(path))


def test_customer_json_syntax_error_reports_line(tmp_path):
    path = write(tmp_path, "customers.json", '[\n  {"test_name": "a",\n  oops\n]')
    assert issue_summary(validate_customer_json(path)) == [(3, "json")]


def test_customer_json_must_be_a_list(tmp_path):
    path = write(tmp_path, "customers.json", '{"cases": []}')
    assert issue_summary(validate_customer_json(path)) == [(1, "root")]


def workflow_file(tmp_path, workflows, reference_date="2026-06-15"):
    return write(tmp_path, "workflows.json",
                 json.dumps({"reference_date": reference_date, "workflows": workflows}, indent=2))


GOOD_STEP = {"action": "calculate_total", "data": {}, "expected": {"status": "error"}}


@pytest.mark.parametrize("workflows,field", [
    ([{"name": "a", "steps": [GOOD_STEP]}, {"name": "a", "steps": [GOOD_STEP]}], "name"),
    ([{"steps": [GOOD_STEP]}], "name"),
    ([{"name": "a", "steps": []}], "steps"),
    ([{"name": "a", "steps": [{"action": "fly", "expected": {"x": 1}}]}], "action"),
    ([{"name": "a", "steps": [{"action": "calculate_total", "data": [], "expected": {"x": 1}}]}], "data"),
    ([{"name": "a", "steps": [{"action": "calculate_total", "expected": {}}]}], "expected"),
    ([{"name": "a", "steps": ["step"]}], "step"),
    (["workflow"], "workflow"),
])
def test_workflow_json_issues(tmp_path, workflows, field):
    assert field in [issue.field for issue in validate_workflows_json(workflow_file(tmp_path, workflows))]


def test_workflow_step_issue_has_the_step_line(tmp_path):
    bad_step = {"action": "fly", "expected": {"x": 1}}
    path = workflow_file(tmp_path, [{"name": "a", "steps": [GOOD_STEP, bad_step]}])
    step_line = path.read_text(encoding="utf-8").splitlines().index('          "action": "fly",')
    assert issue_summary(validate_workflows_json(path)) == [(step_line, "action")]


@pytest.mark.parametrize("content,field", [
    ('{"workflows": []}', "workflows"),
    ("[]", "workflows"),
    ("{", "json"),
])
def test_workflow_file_structure(tmp_path, content, field):
    assert [issue.field for issue in validate_workflows_json(write(tmp_path, "w.json", content))] == [field]


def test_workflow_reference_date_checked(tmp_path):
    path = workflow_file(tmp_path, [{"name": "a", "steps": [GOOD_STEP]}], reference_date="tomorrow")
    assert issue_summary(validate_workflows_json(path)) == [(1, "reference_date")]


def test_loaders_refuse_invalid_files(tmp_path):
    bad_row = "b,simple,[],regular,NONE,0,yes,0,0,0,0,0,"
    with pytest.raises(DataFileError, match=r"orders.csv:3: \[is_express\]"):
        load_order_cases(write(tmp_path, "orders.csv", f"{HEADER}\n{GOOD_ROW}\n{bad_row}\n"))
    with pytest.raises(DataFileError):
        load_customer_cases(write(tmp_path, "c.json", "{}"))
    with pytest.raises(DataFileError):
        load_workflows(write(tmp_path, "w.json", "[]"))


def test_load_order_cases_by_category():
    assert {case.category for case in load_order_cases(category="tax")} == {"tax"}


def test_customer_case_without_reference_date(tmp_path):
    case = customer_case()
    del case["reference_date"]
    assert load_customer_cases(write(tmp_path, "c.json", json.dumps([case])))[0].reference_date is None


def test_issue_string_format():
    assert str(DataIssue("f.csv", 7, "items", "bad")) == "f.csv:7: [items] bad"


def test_main_reports_every_file(tmp_path, capsys):
    for name in ("order_calculations.csv", "customer_validation.json", "order_workflows.json"):
        write(tmp_path, name, (DATA_DIR / name).read_text(encoding="utf-8"))
    assert main(tmp_path) == 0
    write(tmp_path, "order_workflows.json", "[]")
    assert main(tmp_path) == 1
    output = capsys.readouterr().out
    assert "BAD order_workflows.json: 1 issue(s)" in output
    assert "order_workflows.json:1: [workflows]" in output
