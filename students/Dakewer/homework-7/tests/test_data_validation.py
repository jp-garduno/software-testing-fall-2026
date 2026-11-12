"""Tests for the test-data validator (bonus Option C)."""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from validate_test_data import (  # noqa: E402
    validate_all, validate_customers_json, validate_orders_csv, validate_workflows_json,
)

DATA = ROOT / "test_data"


def test_shipped_data_is_valid():
    assert validate_all(DATA) == []


def test_bad_csv_rows_are_reported_with_line_numbers(tmp_path):
    source = (DATA / "order_calculations.csv").read_text().splitlines()
    bad = source[:3] + [source[3].replace(",regular,", ",vip,", 1)]
    bad[2] = bad[2].replace(",false,", ",maybe,", 1)
    target = tmp_path / "order_calculations.csv"
    target.write_text("\n".join(bad) + "\n")
    problems = validate_orders_csv(target)
    assert any(p.startswith("order_calculations.csv:3:") and "is_express" in p for p in problems)
    assert any(p.startswith("order_calculations.csv:4:") and "customer_type" in p for p in problems)


def test_csv_missing_column_and_duplicates(tmp_path):
    target = tmp_path / "a.csv"
    target.write_text("test_name,items\nx,[]\n")
    assert "missing columns" in validate_orders_csv(target)[0]

    lines = (DATA / "comparison_cases.csv").read_text().splitlines()
    target.write_text("\n".join(lines[:2] + [lines[1]]) + "\n")
    assert any("duplicate" in p for p in validate_orders_csv(target))


def test_csv_bad_items_and_numbers(tmp_path):
    header = (DATA / "comparison_cases.csv").read_text().splitlines()[0]
    target = tmp_path / "b.csv"
    target.write_text(header + "\nbad,not-json,regular,NONE,x,false,1,1,1,1,1,\n")
    problems = validate_orders_csv(target)
    assert any("distance_km is not a number" in p for p in problems)
    assert any("items must be" in p for p in problems)


def test_customer_json_problems(tmp_path):
    cases = json.loads((DATA / "customer_validation.json").read_text())
    cases[0]["expected"]["is_valid"] = False  # contradicts empty error list
    cases[1]["expected"]["errors"] = "oops"
    del cases[2]["category"]
    cases.append(dict(cases[3]))  # duplicate name
    target = tmp_path / "customer_validation.json"
    target.write_text(json.dumps(cases, indent=2))
    text = "\n".join(validate_customers_json(target))
    for fragment in ("contradicts", "must be a list", "missing 'category'", "duplicate"):
        assert fragment in text
    assert ":" in text.splitlines()[0]  # includes a line number


def test_invalid_json_reports_line(tmp_path):
    target = tmp_path / "order_workflows.json"
    target.write_text('{\n  "workflows": [\n')
    assert "invalid JSON" in validate_workflows_json(target)[0]
    assert "invalid JSON" in validate_customers_json(target)[0]


def test_workflow_problems(tmp_path):
    spec = {"reference_date": "01/02/2025", "workflows": [
        {"name": "w", "steps": [{"action": "fly", "expected": 5}]},
        {"name": "empty", "steps": []},
    ]}
    target = tmp_path / "order_workflows.json"
    target.write_text(json.dumps(spec, indent=2))
    text = "\n".join(validate_workflows_json(target))
    for fragment in ("reference_date", "unknown action", "'expected' object", "no steps"):
        assert fragment in text


def test_generator_output_is_valid_and_reproducible(tmp_path):
    from generate_orders import generate
    assert generate(5) == generate(5)
    shutil.copy(DATA / "customer_validation.json", tmp_path)
    shutil.copy(DATA / "order_workflows.json", tmp_path)
    import csv
    from generate_orders import HEADER
    with open(tmp_path / "generated_orders.csv", "w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(HEADER)
        writer.writerows(generate(20))
    assert validate_all(tmp_path) == []
