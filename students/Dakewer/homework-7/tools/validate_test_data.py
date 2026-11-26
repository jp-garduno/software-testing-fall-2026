"""Bonus Option C: validate the test-data files before running the tests.

Usage:  python tools/validate_test_data.py [data_dir]

Checks required fields and data types and reports problems with line
numbers (CSV: the record's first line; JSON: the line of its "test_name"/
"name"). Exit code is 1 when any problem is found.
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from order_processor import ACTIONS  # noqa: E402

ORDER_COLUMNS = ["test_name", "items", "customer_type", "discount_code", "distance_km",
                 "is_express", "expected_subtotal", "expected_discount", "expected_tax",
                 "expected_shipping", "expected_total"]
NUMERIC = ["distance_km", "expected_subtotal", "expected_discount", "expected_tax",
           "expected_shipping", "expected_total"]


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_orders_csv(path):
    path, problems, seen = Path(path), [], set()
    with open(path, newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in ORDER_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            return [f"{path.name}:1: missing columns {missing}"]
        while True:
            start = reader.line_num + 1
            try:
                row = next(reader)
            except StopIteration:
                break

            def bad(message):
                problems.append(f"{path.name}:{start}: {message}")

            name = row["test_name"]
            if not name:
                bad("empty test_name")
            elif name in seen:
                bad(f"duplicate test_name '{name}'")
            seen.add(name)
            if row["customer_type"] not in ("new", "regular"):
                bad(f"customer_type must be new|regular, got '{row['customer_type']}'")
            if row["is_express"] not in ("true", "false"):
                bad(f"is_express must be true|false, got '{row['is_express']}'")
            for column in NUMERIC:
                try:
                    float(row[column])
                except (TypeError, ValueError):
                    bad(f"{column} is not a number: '{row[column]}'")
            try:
                items = json.loads(row["items"])
                assert isinstance(items, list)
                for item in items:
                    assert _is_number(item["price"]) and _is_number(item["quantity"])
                    assert _is_number(item.get("weight", 0))
            except (ValueError, AssertionError, KeyError, TypeError):
                bad("items must be a JSON list of {price, quantity, weight} objects")
    return problems


def _line_of(text, key, name):
    index = text.find(f'"{key}": {json.dumps(name)}')
    return text.count("\n", 0, index) + 1 if index >= 0 else 1


def validate_customers_json(path):
    path = Path(path)
    text = path.read_text()
    try:
        cases = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"{path.name}:{exc.lineno}: invalid JSON ({exc.msg})"]
    problems, seen = [], set()
    for index, case in enumerate(cases):
        name = case.get("test_name", f"#{index}")
        where = f"{path.name}:{_line_of(text, 'test_name', name)}"
        for key in ("test_name", "category", "customer", "expected"):
            if key not in case:
                problems.append(f"{where}: missing '{key}' in {name}")
        if name in seen:
            problems.append(f"{where}: duplicate test_name '{name}'")
        seen.add(name)
        expected = case.get("expected", {})
        if not isinstance(expected.get("is_valid"), bool):
            problems.append(f"{where}: expected.is_valid must be a boolean")
        errors = expected.get("errors")
        if not isinstance(errors, list):
            problems.append(f"{where}: expected.errors must be a list")
        elif isinstance(expected.get("is_valid"), bool) and expected["is_valid"] == bool(errors):
            problems.append(f"{where}: is_valid contradicts the errors list")
    return problems


def validate_workflows_json(path):
    path = Path(path)
    text = path.read_text()
    try:
        spec = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"{path.name}:{exc.lineno}: invalid JSON ({exc.msg})"]
    problems = []
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(spec.get("reference_date", ""))):
        problems.append(f"{path.name}:1: reference_date must be YYYY-MM-DD")
    for workflow in spec.get("workflows", []):
        where = f"{path.name}:{_line_of(text, 'name', workflow.get('name'))}"
        if not workflow.get("steps"):
            problems.append(f"{where}: workflow '{workflow.get('name')}' has no steps")
        for number, step in enumerate(workflow.get("steps", []), 1):
            if step.get("action") not in ACTIONS:
                problems.append(f"{where}: step {number} has unknown action '{step.get('action')}'")
            if not isinstance(step.get("expected"), dict):
                problems.append(f"{where}: step {number} needs an 'expected' object")
    return problems


def validate_all(data_dir):
    data_dir = Path(data_dir)
    problems = []
    for name in ("order_calculations.csv", "comparison_cases.csv", "generated_orders.csv"):
        if (data_dir / name).exists():
            problems += validate_orders_csv(data_dir / name)
    problems += validate_customers_json(data_dir / "customer_validation.json")
    problems += validate_workflows_json(data_dir / "order_workflows.json")
    return problems


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "test_data"
    found = validate_all(target)
    print("\n".join(found) if found else f"OK: all test data in {target} is valid")
    sys.exit(1 if found else 0)
