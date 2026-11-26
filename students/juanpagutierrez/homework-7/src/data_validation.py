"""Validation of the test data files themselves (Bonus option C).

A typo in a data file should fail loudly with the place to fix, not show up as
a confusing assertion error in a test. Each ``validate_*`` function returns a
list of ``DataIssue`` objects, each one pointing at a line of the file; an
empty list means the file is usable.

Run ``python -m src.data_validation`` to check every file in ``test_data/``.
"""

import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple

DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"

ORDER_COLUMNS = (
    "test_name", "category", "items", "customer_type", "discount_code", "distance_km", "is_express",
    "expected_subtotal", "expected_discount", "expected_tax", "expected_shipping", "expected_total",
    "expected_error",
)
EXPECTED_AMOUNTS = ORDER_COLUMNS[7:12]
ORDER_CATEGORIES = ("simple", "discount", "tax", "shipping", "complex", "generated")
ITEM_FIELDS = ("name", "price", "quantity", "weight")

CUSTOMER_CATEGORIES = ("valid", "invalid_email", "invalid_phone", "invalid_address", "invalid_card", "multiple_errors")
WORKFLOW_ACTIONS = (
    "validate_customer", "create_order", "apply_discount", "calculate_total", "process_payment",
    "generate_confirmation",
)
WORKFLOWS_KEY = re.compile(r'"workflows"\s*:\s*\[')
STEPS_KEY = re.compile(r'"steps"\s*:\s*\[')


@dataclass(frozen=True)
class DataIssue:
    """One problem found in a data file."""

    file: str
    line: int
    field: str
    message: str

    def __str__(self) -> str:
        return f"{self.file}:{self.line}: [{self.field}] {self.message}"


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _parse_float(text: str) -> Optional[float]:
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def _is_iso_date(text: Any) -> bool:
    try:
        date.fromisoformat(text)
    except (TypeError, ValueError):
        return False
    return True


def _line_of(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def _array_elements(text: str, start: int) -> List[Tuple[int, Any]]:
    """Decode the JSON array whose "[" is at ``start``, keeping each element's offset."""
    decoder = json.JSONDecoder()
    whitespace = re.compile(r"\s*")
    elements = []
    position = whitespace.match(text, start + 1).end()
    while text[position] != "]":
        value, end = decoder.raw_decode(text, position)
        elements.append((position, value))
        position = whitespace.match(text, end).end()
        if text[position] == ",":
            position = whitespace.match(text, position + 1).end()
    return elements


# ---------------------------------------------------------------------------
# order_calculations.csv
# ---------------------------------------------------------------------------

def _item_issues(raw: str) -> List[str]:
    try:
        items = json.loads(raw.replace("'", '"'))
    except json.JSONDecodeError as error:
        return [f"items is not valid JSON: {error.msg}"]
    if not isinstance(items, list):
        return ["items must be a list"]
    problems = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            problems.append(f"item {index} must be an object")
            continue
        missing = [name for name in ITEM_FIELDS if name not in item]
        if missing:
            problems.append(f"item {index} is missing {', '.join(missing)}")
        problems.extend(f"item {index} {name} must be a number"
                        for name in ITEM_FIELDS[1:] if name in item and not _is_number(item[name]))
    return problems


def _order_row_issues(row: dict, seen: set) -> Iterable[Tuple[str, str]]:
    name = row["test_name"].strip()
    if not name:
        yield "test_name", "test_name is empty"
    elif name in seen:
        yield "test_name", f"duplicate test_name '{name}'"
    seen.add(name)
    if row["category"] not in ORDER_CATEGORIES:
        yield "category", f"unknown category '{row['category']}'"
    for problem in _item_issues(row["items"]):
        yield "items", problem
    if row["customer_type"] not in ("new", "regular"):
        yield "customer_type", f"must be 'new' or 'regular', got '{row['customer_type']}'"
    if not row["discount_code"].strip():
        yield "discount_code", "use NONE instead of an empty discount code"
    if _parse_float(row["distance_km"]) is None:
        yield "distance_km", f"'{row['distance_km']}' is not a number"
    if row["is_express"] not in ("true", "false"):
        yield "is_express", f"must be 'true' or 'false', got '{row['is_express']}'"
    yield from _expected_amount_issues(row)


def _expected_amount_issues(row: dict) -> Iterable[Tuple[str, str]]:
    if row["expected_error"].strip():
        for column in EXPECTED_AMOUNTS:
            if row[column].strip():
                yield column, "must be empty when expected_error is set"
        return
    amounts = {}
    for column in EXPECTED_AMOUNTS:
        amounts[column] = _parse_float(row[column])
        if amounts[column] is None:
            yield column, f"'{row[column]}' is not a number"
    if None not in amounts.values():
        computed = (amounts["expected_subtotal"] - amounts["expected_discount"]
                    + amounts["expected_tax"] + amounts["expected_shipping"])
        if abs(computed - amounts["expected_total"]) > 0.005:
            yield "expected_total", f"parts add up to {computed:.2f}, not {amounts['expected_total']:.2f}"


def validate_order_csv(path: Path) -> List[DataIssue]:
    """Check the order calculation CSV: columns, types and that each total adds up."""
    name = Path(path).name
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in ORDER_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            return [DataIssue(name, 1, "header", f"missing columns: {', '.join(missing)}")]
        issues, seen = [], set()
        for row in reader:
            if None in row or None in row.values():
                issues.append(DataIssue(name, reader.line_num, "row", "wrong number of columns"))
                continue
            issues.extend(DataIssue(name, reader.line_num, field, message)
                          for field, message in _order_row_issues(row, seen))
    return issues


# ---------------------------------------------------------------------------
# customer_validation.json
# ---------------------------------------------------------------------------

def _customer_case_issues(case: Any, seen: set) -> Iterable[Tuple[str, str]]:
    if not isinstance(case, dict):
        yield "case", "each test case must be an object"
        return
    name = case.get("test_name")
    if not isinstance(name, str) or not name:
        yield "test_name", "test_name is missing"
    elif name in seen:
        yield "test_name", f"duplicate test_name '{name}'"
    seen.add(name)
    if case.get("category") not in CUSTOMER_CATEGORIES:
        yield "category", f"unknown category '{case.get('category')}'"
    if "reference_date" in case and not _is_iso_date(case["reference_date"]):
        yield "reference_date", "must be an ISO date (YYYY-MM-DD)"
    if not isinstance(case.get("customer"), dict):
        yield "customer", "customer must be an object"
    expected = case.get("expected")
    if not isinstance(expected, dict):
        yield "expected", "expected must be an object"
        return
    if not isinstance(expected.get("is_valid"), bool):
        yield "expected.is_valid", "must be true or false"
    errors = expected.get("errors")
    if not isinstance(errors, list) or not all(isinstance(error, str) for error in errors):
        yield "expected.errors", "must be a list of strings"
    elif isinstance(expected.get("is_valid"), bool) and expected["is_valid"] == bool(errors):
        yield "expected", "is_valid must be true exactly when errors is empty"


def _load_json(path: Path) -> Tuple[str, Any, Optional[DataIssue]]:
    text = Path(path).read_text(encoding="utf-8")
    try:
        return text, json.loads(text), None
    except json.JSONDecodeError as error:
        return text, None, DataIssue(Path(path).name, error.lineno, "json", error.msg)


def validate_customer_json(path: Path) -> List[DataIssue]:
    """Check the customer validation JSON: required keys, types and consistency."""
    name = Path(path).name
    text, data, syntax_error = _load_json(path)
    if syntax_error:
        return [syntax_error]
    if not isinstance(data, list):
        return [DataIssue(name, 1, "root", "the file must contain a list of test cases")]
    issues, seen = [], set()
    for position, case in _array_elements(text, text.index("[")):
        line = _line_of(text, position)
        issues.extend(DataIssue(name, line, field, message) for field, message in _customer_case_issues(case, seen))
    return issues


# ---------------------------------------------------------------------------
# order_workflows.json
# ---------------------------------------------------------------------------

def _step_issues(step: Any) -> Iterable[Tuple[str, str]]:
    if not isinstance(step, dict):
        yield "step", "each step must be an object"
        return
    if step.get("action") not in WORKFLOW_ACTIONS:
        yield "action", f"unknown action '{step.get('action')}'"
    if not isinstance(step.get("data", {}), dict):
        yield "data", "data must be an object"
    if not isinstance(step.get("expected"), dict) or not step["expected"]:
        yield "expected", "expected must be a non-empty object"


def _workflow_issues(text: str, position: int, workflow: Any, seen: set) -> Iterable[Tuple[int, str, str]]:
    line = _line_of(text, position)
    if not isinstance(workflow, dict):
        yield line, "workflow", "each workflow must be an object"
        return
    name = workflow.get("name")
    if not isinstance(name, str) or not name:
        yield line, "name", "workflow name is missing"
    elif name in seen:
        yield line, "name", f"duplicate workflow name '{name}'"
    seen.add(name)
    if not isinstance(workflow.get("steps"), list) or not workflow["steps"]:
        yield line, "steps", "steps must be a non-empty list"
        return
    steps_start = STEPS_KEY.search(text, position).end() - 1
    for step_position, step in _array_elements(text, steps_start):
        for field, message in _step_issues(step):
            yield _line_of(text, step_position), field, message


def validate_workflows_json(path: Path) -> List[DataIssue]:
    """Check the workflow JSON: workflow names, step actions and expectations."""
    name = Path(path).name
    text, data, syntax_error = _load_json(path)
    if syntax_error:
        return [syntax_error]
    if not isinstance(data, dict) or not isinstance(data.get("workflows"), list) or not data["workflows"]:
        return [DataIssue(name, 1, "workflows", "the file must contain a non-empty 'workflows' list")]
    issues = []
    if "reference_date" in data and not _is_iso_date(data["reference_date"]):
        issues.append(DataIssue(name, 1, "reference_date", "must be an ISO date (YYYY-MM-DD)"))
    start = WORKFLOWS_KEY.search(text).end() - 1
    seen: set = set()
    for position, workflow in _array_elements(text, start):
        issues.extend(DataIssue(name, line, field, message)
                      for line, field, message in _workflow_issues(text, position, workflow, seen))
    return issues


VALIDATORS = {
    "order_calculations.csv": validate_order_csv,
    "customer_validation.json": validate_customer_json,
    "order_workflows.json": validate_workflows_json,
}


def main(data_dir: Path = DATA_DIR) -> int:
    """Validate every known data file and print a report. Returns the exit code."""
    issues = []
    for file_name, validator in VALIDATORS.items():
        file_issues = validator(Path(data_dir) / file_name)
        print(f"{'OK ' if not file_issues else 'BAD'} {file_name}: {len(file_issues)} issue(s)")
        issues.extend(file_issues)
    for issue in issues:
        print(f"  {issue}")
    return 1 if issues else 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
