"""Validation of the external test data files, reporting problems with line numbers."""

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

ORDER_COLUMNS = (
    "test_name",
    "category",
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
    "expected_error",
)
EXPECTED_COLUMNS = ORDER_COLUMNS[7:12]
ITEM_FIELDS = {"name": str, "price": (int, float), "quantity": (int, float), "weight": (int, float)}
WORKFLOW_ACTIONS = (
    "validate_customer",
    "create_order",
    "apply_discount",
    "set_shipping",
    "calculate_total",
    "process_payment",
    "generate_confirmation",
)
MIN_ORDER_CASES = {"simple": 3, "discount": 5, "tax": 4, "shipping": 6}
MIN_COMPLEX_AND_ERROR_CASES = 7
MIN_TOTAL_ORDER_CASES = 25
MIN_CUSTOMER_CASES = 30
MIN_WORKFLOWS = 3


@dataclass(frozen=True)
class Problem:
    """A single problem found in a data file."""

    line: int
    test_name: str
    message: str

    def __str__(self):
        label = f" [{self.test_name}]" if self.test_name else ""
        return f"line {self.line}{label}: {self.message}"


def _is_number(text):
    try:
        float(text)
        return True
    except ValueError:
        return False


def _check_items(items_text):
    """Return a message if the items cell is not a JSON list of well-formed items, else None."""
    try:
        items = json.loads(items_text)
    except json.JSONDecodeError as error:
        return f"items is not valid JSON ({error.msg})"
    if not isinstance(items, list):
        return "items must be a JSON list"
    for position, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return f"item {position} must be an object"
        for field, kinds in ITEM_FIELDS.items():
            if not isinstance(item.get(field), kinds) or isinstance(item.get(field), bool):
                return f"item {position} needs a {field} of the right type"
    return None


def _check_order_row(row):
    """Return the list of messages describing what is wrong with one order CSV row."""
    messages = []
    for column in ("test_name", "category", "customer_type", "discount_code"):
        if not (row.get(column) or "").strip():
            messages.append(f"{column} is required")
    items_message = _check_items(row.get("items") or "")
    if items_message:
        messages.append(items_message)
    if not _is_number(row.get("distance_km") or ""):
        messages.append("distance_km must be a number")
    if (row.get("is_express") or "").strip() not in ("true", "false"):
        messages.append("is_express must be true or false")
    has_error = bool((row.get("expected_error") or "").strip())
    for column in EXPECTED_COLUMNS:
        value = (row.get(column) or "").strip()
        if has_error and value:
            messages.append(f"{column} must be empty when expected_error is set")
        elif not has_error and not _is_number(value):
            messages.append(f"{column} must be a number")
    return messages


def validate_order_csv(path) -> List[Problem]:
    """Check the order calculation CSV: header, required fields, types and duplicate names."""
    problems: List[Problem] = []
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in ORDER_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            return [Problem(1, "", f"missing columns: {', '.join(missing)}")]
        seen = {}
        for row in reader:
            line = reader.line_num
            name = (row.get("test_name") or "").strip()
            problems.extend(Problem(line, name, message) for message in _check_order_row(row))
            if name in seen:
                problems.append(Problem(line, name, f"duplicate test_name (first used on line {seen[name]})"))
            seen.setdefault(name, line)
    return problems


def _line_of(text, name):
    """Line number where a case with this test_name is declared in a JSON text (1 if not found)."""
    match = re.search(rf'"test_name":\s*{re.escape(json.dumps(name))}', text)
    return text.count("\n", 0, match.start()) + 1 if match else 1


def _check_customer_case(case):
    messages = []
    if not isinstance(case.get("test_name"), str) or not case["test_name"]:
        messages.append("test_name must be a non-empty string")
    if not isinstance(case.get("category"), str):
        messages.append("category must be a string")
    if not isinstance(case.get("customer"), dict):
        messages.append("customer must be an object")
    expected = case.get("expected")
    if not isinstance(expected, dict) or not isinstance(expected.get("is_valid"), bool):
        messages.append("expected.is_valid must be true or false")
    elif not isinstance(expected.get("errors"), list):
        messages.append("expected.errors must be a list")
    elif expected["is_valid"] != (expected["errors"] == []):
        messages.append("expected.is_valid contradicts expected.errors")
    return messages


def validate_customer_json(path) -> List[Problem]:
    """Check the customer validation JSON: structure, types, consistency and duplicate names."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        cases = json.loads(text)
    except json.JSONDecodeError as error:
        return [Problem(error.lineno, "", f"invalid JSON: {error.msg}")]
    if not isinstance(cases, list):
        return [Problem(1, "", "top level must be a list of cases")]
    problems, seen = [], set()
    for case in cases:
        name = case.get("test_name", "") if isinstance(case, dict) else ""
        line = _line_of(text, name) if name else 1
        messages = _check_customer_case(case) if isinstance(case, dict) else ["case must be an object"]
        if name in seen:
            messages.append("duplicate test_name")
        seen.add(name)
        problems.extend(Problem(line, name, message) for message in messages)
    return problems


def validate_workflow_json(path) -> List[Problem]:
    """Check the workflow JSON: customers, workflow names, known actions and expected results."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        return [Problem(error.lineno, "", f"invalid JSON: {error.msg}")]
    problems = []
    customers = data.get("customers", {}) if isinstance(data, dict) else {}
    workflows = data.get("workflows") if isinstance(data, dict) else None
    if not isinstance(workflows, list):
        return [Problem(1, "", "workflows must be a list")]
    for flow in workflows:
        name = flow.get("name", "") if isinstance(flow, dict) else ""
        line = text.count("\n", 0, text.find(json.dumps(name))) + 1 if name and json.dumps(name) in text else 1
        steps = flow.get("steps") if isinstance(flow, dict) else None
        if not name or not isinstance(steps, list) or not steps:
            problems.append(Problem(line, name, "workflow needs a name and a non-empty list of steps"))
            continue
        for number, step in enumerate(steps, start=1):
            if step.get("action") not in WORKFLOW_ACTIONS:
                problems.append(Problem(line, name, f"step {number}: unknown action {step.get('action')!r}"))
            if not isinstance(step.get("expected"), dict):
                problems.append(Problem(line, name, f"step {number}: expected must be an object"))
            reference = (step.get("data") or {}).get("customer")
            if reference is not None and reference not in customers:
                problems.append(Problem(line, name, f"step {number}: unknown customer {reference!r}"))
    return problems


def check_minimum_counts(order_csv, customer_json, workflow_json) -> List[str]:
    """Check the data files contain at least the number of cases the assignment requires."""
    with open(order_csv, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    shortfalls = []
    if len(rows) < MIN_TOTAL_ORDER_CASES:
        shortfalls.append(f"order cases: {len(rows)} < {MIN_TOTAL_ORDER_CASES}")
    for category, minimum in MIN_ORDER_CASES.items():
        count = sum(1 for row in rows if row["category"] == category)
        if count < minimum:
            shortfalls.append(f"{category} order cases: {count} < {minimum}")
    others = sum(1 for row in rows if row["category"] in ("complex", "error"))
    if others < MIN_COMPLEX_AND_ERROR_CASES:
        shortfalls.append(f"complex/edge order cases: {others} < {MIN_COMPLEX_AND_ERROR_CASES}")
    customers = json.loads(Path(customer_json).read_text(encoding="utf-8"))
    if len(customers) < MIN_CUSTOMER_CASES:
        shortfalls.append(f"customer cases: {len(customers)} < {MIN_CUSTOMER_CASES}")
    flows = json.loads(Path(workflow_json).read_text(encoding="utf-8"))["workflows"]
    if len(flows) < MIN_WORKFLOWS:
        shortfalls.append(f"workflows: {len(flows)} < {MIN_WORKFLOWS}")
    return shortfalls
