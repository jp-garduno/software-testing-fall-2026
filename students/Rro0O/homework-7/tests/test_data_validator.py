"""Bonus C tests: the data validator reports problems with line numbers."""

import json

from data_loader import DATA_DIR
from data_validator import (
    main,
    validate_all,
    validate_customer_json,
    validate_order_csv,
    validate_workflow_json,
)

HEADER = (
    "test_name,items,customer_type,discount_code,distance_km,is_express,"
    "expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total\n"
)
GOOD_ROW = (
    "ok,\"[{'name':'A','price':1,'quantity':1,'weight':0}]\",regular,NONE,0,false,1,0,0.08,0,1.08\n"
)


def write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_committed_data_is_valid():
    assert validate_all(DATA_DIR) == []


def test_csv_good_file(tmp_path):
    assert validate_order_csv(write(tmp_path, "a.csv", HEADER + GOOD_ROW)) == []


def test_csv_missing_columns(tmp_path):
    problems = validate_order_csv(write(tmp_path, "a.csv", "test_name,items\nx,y\n"))
    assert len(problems) == 1 and problems[0].startswith("a.csv:1: missing columns")


def test_csv_reports_line_numbers_for_each_problem(tmp_path):
    bad_number = "n1,\"[{'name':'A','price':1,'quantity':1,'weight':0}]\",regular,NONE,far,false,1,0,0.08,0,1.08\n"
    bad_type = (
        "n2,\"[{'name':'A','price':1,'quantity':1,'weight':0}]\",vip,NONE,0,maybe,1,0,0.08,0,1.08\n"
    )
    empty = "n3,,regular,NONE,0,false,1,0,0.08,0,1.08\n"
    duplicate = GOOD_ROW
    path = write(tmp_path, "a.csv", HEADER + GOOD_ROW + bad_number + bad_type + empty + duplicate)
    problems = validate_order_csv(path)
    text = "\n".join(problems)
    assert "a.csv:3: 'distance_km' is not a number" in text
    assert "a.csv:4: customer_type must be new|regular" in text
    assert "a.csv:4: is_express must be true|false" in text
    assert "a.csv:5: empty value for 'items'" in text
    assert "a.csv:6: duplicate test_name 'ok'" in text


def test_csv_item_problems(tmp_path):
    rows = (
        "a,not json,regular,NONE,0,false,1,0,0,0,1\n"
        "b,\"{'name':'A'}\",regular,NONE,0,false,1,0,0,0,1\n"
        "c,\"[{'name':'A','price':'x','quantity':1}]\",regular,NONE,0,false,1,0,0,0,1\n"
    )
    text = "\n".join(validate_order_csv(write(tmp_path, "a.csv", HEADER + rows)))
    assert "a.csv:2: items is not valid JSON" in text
    assert "a.csv:3: items must be a list" in text
    assert "a.csv:4: item 0 has missing/invalid 'price'" in text
    assert "a.csv:4: item 0 has missing/invalid 'weight'" in text


def test_customer_json_problems_have_line_numbers(tmp_path):
    cases = [
        {"test_name": "good", "customer": {}, "expected": {"is_valid": True, "errors": []}},
        {
            "test_name": "contradiction",
            "customer": {},
            "expected": {"is_valid": True, "errors": ["x"]},
        },
        {"test_name": "no_expected", "customer": {}},
        {"test_name": "bad_types", "expected": {"is_valid": "yes", "errors": "none"}},
        {
            "test_name": "bad_date",
            "customer": {},
            "reference_date": "01/01/2026",
            "expected": {"is_valid": True, "errors": []},
        },
        {"customer": {}},
    ]
    path = write(tmp_path, "c.json", json.dumps(cases, indent=2))
    text = "\n".join(validate_customer_json(path))
    assert "contradiction): is_valid contradicts" in text
    assert "no_expected): missing 'expected'" in text
    assert "bad_types): missing 'customer'" in text
    assert "bad_types): expected.is_valid must be a boolean" in text
    assert "bad_types): expected.errors must be a list" in text
    assert "bad_date): reference_date must be YYYY-MM-DD" in text
    assert "needs a test_name" in text
    assert "good" not in text.replace("bad_", "")
    first_line = int(text.splitlines()[0].split(":")[1])
    assert first_line > 1


def test_customer_json_syntax_error_and_wrong_top_level(tmp_path):
    assert "invalid JSON" in validate_customer_json(write(tmp_path, "a.json", "[1,"))[0]
    assert validate_customer_json(write(tmp_path, "b.json", "{}")) == [
        "b.json:1: top level must be a list"
    ]


def test_workflow_json_problems(tmp_path):
    data = {
        "workflows": [
            {"name": "empty", "steps": []},
            {"name": "broken", "steps": [{"action": "x"}]},
            {"name": "fine", "steps": [{"action": "x", "expected": {}}]},
        ]
    }
    text = "\n".join(validate_workflow_json(write(tmp_path, "w.json", json.dumps(data, indent=2))))
    assert "workflow 'empty' has no steps" in text
    assert "workflow 'broken' step 1 needs" in text
    assert "fine" not in text


def test_workflow_json_syntax_error_and_wrong_top_level(tmp_path):
    assert "invalid JSON" in validate_workflow_json(write(tmp_path, "a.json", "{"))[0]
    assert "needs a 'workflows' list" in validate_workflow_json(write(tmp_path, "b.json", "[]"))[0]


def test_main_exit_codes(tmp_path, capsys):
    assert main([str(DATA_DIR)]) == 0
    assert "test data OK" in capsys.readouterr().out
    write(tmp_path, "customer_validation.json", "[")
    write(tmp_path, "order_workflows.json", "{")
    assert main([str(tmp_path)]) == 1
    assert "problem(s) found" in capsys.readouterr().out
