"""Bonus C: validate the test data files before the suite runs.

Every problem is reported with a line number (CSV: the row's line; JSON: the
line where the offending case starts), e.g. ``order_calculations.csv:7: ...``.

Usage:  python src/data_validator.py        (validates all files in test_data/)
"""

import csv
import json
import re
import sys
from pathlib import Path
from typing import List

CSV_COLUMNS = [
    "test_name",
    "items",
    "customer_type",
    "discount_code",
    "distance_km",
    "is_express",
    "expected_subtotal",
    "expected_discount",
    "expected_tax",
    "expected_shipping",
    "expected_total",
]
NUMERIC_COLUMNS = [c for c in CSV_COLUMNS if c.startswith("expected_")] + ["distance_km"]
ITEM_FIELDS = {"name": str, "price": (int, float), "quantity": (int, float), "weight": (int, float)}


def validate_order_csv(path) -> List[str]:
    """Check header, required fields, data types and item structure of a CSV."""
    path = Path(path)
    problems: List[str] = []
    tag = path.name
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in CSV_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            return [f"{tag}:1: missing columns {missing}"]
        seen = set()
        for row in reader:
            line = reader.line_num
            for column in CSV_COLUMNS:
                if row.get(column) in (None, ""):
                    problems.append(f"{tag}:{line}: empty value for '{column}'")
            name = row["test_name"]
            if name in seen:
                problems.append(f"{tag}:{line}: duplicate test_name '{name}'")
            seen.add(name)
            if row["customer_type"] not in ("new", "regular"):
                problems.append(f"{tag}:{line}: customer_type must be new|regular")
            if row["is_express"] not in ("true", "false"):
                problems.append(f"{tag}:{line}: is_express must be true|false")
            for column in NUMERIC_COLUMNS:
                try:
                    float(row[column])
                except (TypeError, ValueError):
                    problems.append(f"{tag}:{line}: '{column}' is not a number: {row[column]!r}")
            problems.extend(_check_items(tag, line, row["items"]))
    return problems


def _check_items(tag, line, raw) -> List[str]:
    try:
        items = json.loads((raw or "").replace("'", '"'))
    except json.JSONDecodeError:
        return [f"{tag}:{line}: items is not valid JSON"]
    if not isinstance(items, list):
        return [f"{tag}:{line}: items must be a list"]
    problems = []
    for index, item in enumerate(items):
        for field, kind in ITEM_FIELDS.items():
            if (
                not isinstance(item, dict)
                or not isinstance(item.get(field), kind)
                or isinstance(item.get(field), bool)
            ):
                problems.append(f"{tag}:{line}: item {index} has missing/invalid '{field}'")
    return problems


def _line_of(text: str, needle: str) -> int:
    """1-based line number of the first occurrence of ``needle`` (1 if absent)."""
    position = text.find(needle)
    return text.count("\n", 0, position) + 1 if position >= 0 else 1


def validate_customer_json(path) -> List[str]:
    """Check structure of customer_validation.json."""
    path = Path(path)
    tag = path.name
    text = path.read_text(encoding="utf-8")
    try:
        cases = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"{tag}:{exc.lineno}: invalid JSON ({exc.msg})"]
    if not isinstance(cases, list):
        return [f"{tag}:1: top level must be a list"]
    problems = []
    for index, case in enumerate(cases):
        name = case.get("test_name") if isinstance(case, dict) else None
        line = _line_of(text, f'"test_name": "{name}"') if name else 1
        where = f"{tag}:{line}: case #{index} ({name})"
        if not isinstance(case, dict) or not name:
            problems.append(f"{where}: needs a test_name")
            continue
        if "customer" not in case:
            problems.append(f"{where}: missing 'customer'")
        expected = case.get("expected")
        if not isinstance(expected, dict):
            problems.append(f"{where}: missing 'expected'")
            continue
        if not isinstance(expected.get("is_valid"), bool):
            problems.append(f"{where}: expected.is_valid must be a boolean")
        if not isinstance(expected.get("errors"), list):
            problems.append(f"{where}: expected.errors must be a list")
        elif bool(expected["errors"]) == bool(expected.get("is_valid")):
            problems.append(f"{where}: is_valid contradicts the errors list")
        if re.search(r"(^|\W)reference_date", json.dumps(case)) and not re.match(
            r"^\d{4}-\d{2}-\d{2}$", str(case.get("reference_date", ""))
        ):
            problems.append(f"{where}: reference_date must be YYYY-MM-DD")
    return problems


def validate_workflow_json(path) -> List[str]:
    """Check structure of order_workflows.json."""
    path = Path(path)
    tag = path.name
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"{tag}:{exc.lineno}: invalid JSON ({exc.msg})"]
    workflows = data.get("workflows") if isinstance(data, dict) else None
    if not isinstance(workflows, list):
        return [f"{tag}:1: top level needs a 'workflows' list"]
    problems = []
    for workflow in workflows:
        name = workflow.get("name", "?")
        line = _line_of(text, f'"name": "{name}"')
        steps = workflow.get("steps")
        if not isinstance(steps, list) or not steps:
            problems.append(f"{tag}:{line}: workflow '{name}' has no steps")
            continue
        for number, step in enumerate(steps, start=1):
            if "action" not in step or not isinstance(step.get("expected"), dict):
                problems.append(
                    f"{tag}:{line}: workflow '{name}' step {number} needs 'action' and 'expected'"
                )
    return problems


def validate_all(data_dir) -> List[str]:
    """Validate every known file inside ``data_dir``."""
    data_dir = Path(data_dir)
    problems: List[str] = []
    for csv_name in ("order_calculations.csv", "generated_orders.csv"):
        if (data_dir / csv_name).exists():
            problems += validate_order_csv(data_dir / csv_name)
    problems += validate_customer_json(data_dir / "customer_validation.json")
    problems += validate_workflow_json(data_dir / "order_workflows.json")
    return problems


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    data_dir = Path(argv[0]) if argv else Path(__file__).resolve().parent.parent / "test_data"
    problems = validate_all(data_dir)
    for problem in problems:
        print(problem)
    print("test data OK" if not problems else f"{len(problems)} problem(s) found")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
