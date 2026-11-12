"""Load the test data files, validating every record and reporting problems with their line numbers.

Run ``python -m tools.data_files`` from the homework root to check all files without running the tests.
"""

import csv
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

TEST_DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"

ORDER_COLUMNS = (
    "test_name",
    "category",
    "items",
    "customer_type",
    "discount_code",
    "distance_km",
    "is_express",
    "order_date",
    "expected_subtotal",
    "expected_discount",
    "expected_tax",
    "expected_shipping",
    "expected_total",
    "expected_error",
)
EXPECTED_AMOUNTS = ("subtotal", "discount", "tax", "shipping", "total")
ORDER_CATEGORIES = ("simple", "discount", "tax", "shipping", "complex", "generated")
CUSTOMER_CATEGORIES = ("valid", "email", "phone", "address", "credit_card", "multiple")
WORKFLOW_ACTIONS = ("validate_customer", "create_order", "calculate_total", "process_payment", "generate_confirmation")


class DataFileError(ValueError):
    def __init__(self, problems):
        super().__init__("Invalid test data:\n" + "\n".join(f"  {problem}" for problem in problems))
        self.problems = problems


@dataclass(frozen=True)
class OrderInput:
    items: list
    customer_type: str
    discount_code: str | None
    distance_km: float
    is_express: bool
    order_date: date | None


@dataclass(frozen=True)
class OrderCase:
    test_name: str
    category: str
    order: OrderInput
    expected: dict | None
    expected_error: str | None


@dataclass(frozen=True)
class CustomerCase:
    test_name: str
    category: str
    customer: dict
    is_valid: bool
    errors: list


@dataclass(frozen=True)
class CustomerData:
    reference_date: date
    cases: list


@dataclass(frozen=True)
class WorkflowData:
    reference_date: date
    workflows: list


def load_order_cases(path):
    path = Path(path)
    problems, cases = [], []
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing = [column for column in ORDER_COLUMNS if column not in (reader.fieldnames or ())]
        if missing:
            raise DataFileError([f"{path.name}:1: missing columns: {', '.join(missing)}"])
        for row in reader:
            location = f"{path.name}:{reader.line_num}"
            try:
                cases.append(_order_case(row))
            except ValueError as error:
                problems.append(f"{location}: {error}")
    problems.extend(_duplicate_names(path.name, [case.test_name for case in cases]))
    if problems:
        raise DataFileError(problems)
    return cases


def load_customer_data(path):
    path = Path(path)
    document, lines = _read_json(path, "cases")
    problems = []
    reference_date = _reference_date(document, path, problems)
    cases = []
    for index, raw in enumerate(document.get("cases") or []):
        try:
            cases.append(_customer_case(raw))
        except ValueError as error:
            problems.append(f"{path.name}:{lines[index]}: case {index}: {error}")
    if not cases and not problems:
        problems.append(f"{path.name}:1: 'cases' must be a non-empty list")
    problems.extend(_duplicate_names(path.name, [case.test_name for case in cases]))
    if problems:
        raise DataFileError(problems)
    return CustomerData(reference_date, cases)


def load_workflow_data(path):
    path = Path(path)
    document, lines = _read_json(path, "workflows")
    problems = []
    reference_date = _reference_date(document, path, problems)
    workflows = document.get("workflows") or []
    for index, workflow in enumerate(workflows):
        problems.extend(
            f"{path.name}:{lines[index]}: workflow {index}: {error}" for error in _workflow_errors(workflow)
        )
    if not workflows and not problems:
        problems.append(f"{path.name}:1: 'workflows' must be a non-empty list")
    if not problems:
        problems.extend(_duplicate_names(path.name, [workflow["name"] for workflow in workflows]))
    if problems:
        raise DataFileError(problems)
    return WorkflowData(reference_date, workflows)


def _order_case(row):
    test_name = _required(row, "test_name")
    category = _choice(row, "category", ORDER_CATEGORIES)
    discount_code = _required(row, "discount_code")
    expected_error = row["expected_error"].strip() or None
    items = _items(row["items"], check_values=expected_error is None)
    amounts = {name: row[f"expected_{name}"].strip() for name in EXPECTED_AMOUNTS}
    if expected_error is not None:
        if any(amounts.values()):
            raise ValueError("a row with expected_error must leave the expected amounts empty")
        expected = None
    else:
        expected = {name: _number(row, f"expected_{name}") for name in EXPECTED_AMOUNTS}
        computed = expected["subtotal"] - expected["discount"] + expected["tax"] + expected["shipping"]
        if round(computed, 2) != expected["total"]:
            raise ValueError(f"expected_total {expected['total']} does not add up to {round(computed, 2)}")
    order = OrderInput(
        items=items,
        customer_type=_required(row, "customer_type"),
        discount_code=None if discount_code == "NONE" else discount_code,
        distance_km=_number(row, "distance_km"),
        is_express=_choice(row, "is_express", ("true", "false")) == "true",
        order_date=_optional_date(row["order_date"], "order_date"),
    )
    return OrderCase(test_name, category, order, expected, expected_error)


def _items(raw, check_values):
    try:
        items = json.loads(raw.replace("'", '"'))
    except json.JSONDecodeError as error:
        raise ValueError(f"items is not valid JSON: {error.msg}") from error
    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        raise ValueError("items must be a list of objects")
    if check_values:
        for item in items:
            if not isinstance(item.get("name"), str):
                raise ValueError(f"every item needs a name, got {item!r}")
            for field in ("price", "quantity", "weight"):
                if not isinstance(item.get(field), (int, float)):
                    raise ValueError(f"item {item['name']!r}: {field} must be a number, got {item.get(field)!r}")
    return items


def _required(row, column):
    value = (row[column] or "").strip()
    if not value:
        raise ValueError(f"{column} is required")
    return value


def _choice(row, column, allowed):
    value = _required(row, column)
    if value not in allowed:
        raise ValueError(f"{column} must be one of {', '.join(allowed)}, got {value!r}")
    return value


def _number(row, column):
    value = _required(row, column)
    try:
        return float(value)
    except ValueError as error:
        raise ValueError(f"{column} must be a number, got {value!r}") from error


def _optional_date(value, field):
    if not value or not value.strip():
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError as error:
        raise ValueError(f"{field} must be a YYYY-MM-DD date, got {value!r}") from error


def _duplicate_names(file_name, names):
    seen, problems = set(), []
    for name in names:
        if name in seen:
            problems.append(f"{file_name}: duplicate test name {name!r}")
        seen.add(name)
    return problems


def _read_json(path, list_key):
    text = path.read_text(encoding="utf-8")
    try:
        document = json.loads(text)
    except json.JSONDecodeError as error:
        raise DataFileError([f"{path.name}:{error.lineno}: invalid JSON: {error.msg}"]) from error
    if not isinstance(document, dict) or not isinstance(document.get(list_key), list):
        raise DataFileError([f"{path.name}:1: expected an object with a '{list_key}' list"])
    return document, _element_lines(text, list_key)


def _element_lines(text, list_key):
    decoder = json.JSONDecoder()
    position = text.index("[", text.index(f'"{list_key}"')) + 1
    lines = []
    while True:
        while text[position] in " \t\r\n,":
            position += 1
        if text[position] == "]":
            return lines
        lines.append(text.count("\n", 0, position) + 1)
        _, position = decoder.raw_decode(text, position)


def _reference_date(document, path, problems):
    try:
        reference_date = _optional_date(document.get("reference_date"), "reference_date")
    except (ValueError, AttributeError):
        reference_date = None
    if reference_date is None:
        problems.append(f"{path.name}:1: reference_date must be a YYYY-MM-DD date")
    return reference_date


def _customer_case(raw):
    if not isinstance(raw, dict):
        raise ValueError("must be an object")
    for field in ("test_name", "category", "customer", "expected"):
        if field not in raw:
            raise ValueError(f"missing field {field!r}")
    if not isinstance(raw["test_name"], str) or not raw["test_name"].strip():
        raise ValueError("test_name must be a non-empty string")
    if raw["category"] not in CUSTOMER_CATEGORIES:
        raise ValueError(f"category must be one of {', '.join(CUSTOMER_CATEGORIES)}, got {raw['category']!r}")
    if not isinstance(raw["customer"], dict):
        raise ValueError("customer must be an object")
    expected = raw["expected"]
    if not isinstance(expected, dict) or not isinstance(expected.get("is_valid"), bool):
        raise ValueError("expected.is_valid must be true or false")
    errors = expected.get("errors")
    if not isinstance(errors, list) or not all(isinstance(error, str) for error in errors):
        raise ValueError("expected.errors must be a list of strings")
    if expected["is_valid"] == bool(errors):
        raise ValueError("expected.is_valid must be true exactly when expected.errors is empty")
    return CustomerCase(raw["test_name"], raw["category"], raw["customer"], expected["is_valid"], errors)


def _workflow_errors(workflow):
    if not isinstance(workflow, dict):
        return ["must be an object"]
    errors = []
    if not isinstance(workflow.get("name"), str) or not workflow["name"].strip():
        errors.append("name must be a non-empty string")
    credit = (workflow.get("gateway") or {}).get("available_credit")
    if not isinstance(credit, (int, float)) or isinstance(credit, bool) or credit < 0:
        errors.append("gateway.available_credit must be a number of at least 0")
    steps = workflow.get("steps")
    if not isinstance(steps, list) or not steps:
        return errors + ["steps must be a non-empty list"]
    for number, step in enumerate(steps):
        errors.extend(f"step {number}: {error}" for error in _step_errors(step))
    return errors


def _step_errors(step):
    if not isinstance(step, dict):
        return ["must be an object"]
    errors = []
    if step.get("action") not in WORKFLOW_ACTIONS:
        errors.append(f"action must be one of {', '.join(WORKFLOW_ACTIONS)}, got {step.get('action')!r}")
    if not isinstance(step.get("data", {}), dict):
        errors.append("data must be an object")
    has_expected = isinstance(step.get("expected"), dict)
    has_error = isinstance(step.get("expected_error"), str)
    if has_expected == has_error:
        errors.append("needs exactly one of 'expected' (an object) or 'expected_error' (a string)")
    return errors


def main():
    checks = (
        (load_order_cases, "order_calculations.csv"),
        (load_order_cases, "order_comparison.csv"),
        (load_order_cases, "generated_orders.csv"),
        (load_customer_data, "customer_validation.json"),
        (load_workflow_data, "order_workflows.json"),
    )
    failed = False
    for loader, file_name in checks:
        try:
            loader(TEST_DATA_DIR / file_name)
            print(f"OK      {file_name}")
        except DataFileError as error:
            failed = True
            print(f"INVALID {file_name}\n" + "\n".join(f"        {problem}" for problem in error.problems))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
