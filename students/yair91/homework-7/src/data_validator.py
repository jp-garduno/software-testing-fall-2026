"""Validation of the test data files (bonus, option C).

Before running the suite it is worth knowing whether the data is well formed.
A CSV with a missing column or a number written as text does not make a test
fail for the right reason: it makes it fail confusingly, or worse, makes it
pass with silently wrong values.

Every problem is reported with the file, the line and the column.
"""

import csv
import json
import os
from typing import Dict, List

ORDER_COLUMNS = (
    "test_name", "category", "items", "customer_type", "discount_code",
    "distance_km", "is_express", "expected_subtotal", "expected_discount",
    "expected_tax", "expected_shipping", "expected_total", "expected_error",
)
NUMERIC_COLUMNS = (
    "distance_km", "expected_subtotal", "expected_discount",
    "expected_tax", "expected_shipping", "expected_total",
)
ITEM_FIELDS = ("name", "price", "quantity", "weight")
CASE_KEYS = ("test_name", "category", "customer", "expected_valid", "expected_errors", "reason")
ORDER_CATEGORIES = ("simple", "discount", "tax", "shipping", "complex")


class DataValidationError(Exception):
    """Raised when a test data file cannot be used."""


def _problem(path: str, line, column, message: str) -> str:
    """Build a message that always says where the problem is."""
    location = os.path.basename(path)
    if line is not None:
        location += f":{line}"
    if column is not None:
        location += f" [{column}]"
    return f"{location}: {message}"


def validate_order_csv(path: str) -> List[str]:
    """Check order_calculations.csv and return the list of problems."""
    problems = []

    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in ORDER_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            return [_problem(path, 1, None, f"missing columns: {', '.join(missing)}")]

        names = set()
        for number, row in enumerate(reader, start=2):
            problems.extend(_check_order_row(path, number, row, names))

    if not problems and not names:
        problems.append(_problem(path, None, None, "the file has no data rows"))
    return problems


def _check_order_row(path: str, number: int, row: Dict, names: set) -> List[str]:
    """Check one row: unique name, category, boolean, items and numbers."""
    problems = []

    name = (row.get("test_name") or "").strip()
    if not name:
        problems.append(_problem(path, number, "test_name", "is empty"))
    elif name in names:
        problems.append(_problem(path, number, "test_name", f"'{name}' is duplicated"))
    else:
        names.add(name)

    if row.get("category") not in ORDER_CATEGORIES:
        problems.append(
            _problem(path, number, "category", f"'{row.get('category')}' is not a known category")
        )

    if row.get("is_express") not in ("true", "false"):
        problems.append(_problem(path, number, "is_express", "must be true or false in lowercase"))

    problems.extend(_check_items(path, number, row.get("items", "")))

    expects_error = bool((row.get("expected_error") or "").strip())
    for column in NUMERIC_COLUMNS:
        value = (row.get(column) or "").strip()
        if value == "":
            if not expects_error and column != "distance_km":
                problems.append(_problem(path, number, column, "is empty and no error is expected"))
            continue
        try:
            float(value)
        except ValueError:
            problems.append(_problem(path, number, column, f"'{value}' is not a number"))

    return problems


def _check_items(path: str, number: int, raw: str) -> List[str]:
    """The items cell must be JSON with the four fields on every article."""
    try:
        items = json.loads(raw)
    except json.JSONDecodeError as error:
        return [_problem(path, number, "items", f"is not valid JSON: {error.msg}")]

    if not isinstance(items, list):
        return [_problem(path, number, "items", "must be a list")]

    problems = []
    for position, item in enumerate(items):
        if not isinstance(item, dict):
            problems.append(_problem(path, number, "items", f"article {position} is not an object"))
            continue
        missing = [field for field in ITEM_FIELDS if field not in item]
        if missing:
            problems.append(
                _problem(path, number, "items", f"article {position} is missing {', '.join(missing)}")
            )
    return problems


def validate_customer_json(path: str) -> List[str]:
    """Check customer_validation.json and return the list of problems."""
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict) or "test_cases" not in data:
        return [_problem(path, None, None, "the test_cases key is missing")]

    cases = data["test_cases"]
    if not isinstance(cases, list) or not cases:
        return [_problem(path, None, "test_cases", "must be a list with at least one case")]

    problems, names = [], set()
    for index, case in enumerate(cases):
        label = f"test_cases[{index}]"
        if not isinstance(case, dict):
            problems.append(_problem(path, None, label, "is not an object"))
            continue

        missing = [key for key in CASE_KEYS if key not in case]
        if missing:
            problems.append(_problem(path, None, label, f"is missing {', '.join(missing)}"))
            continue

        name = case["test_name"]
        if name in names:
            problems.append(_problem(path, None, label, f"'{name}' is duplicated"))
        names.add(name)

        if not isinstance(case["expected_valid"], bool):
            problems.append(_problem(path, None, label, "expected_valid must be a boolean"))
        if not isinstance(case["expected_errors"], list):
            problems.append(_problem(path, None, label, "expected_errors must be a list"))
        elif case["expected_valid"] and case["expected_errors"]:
            problems.append(_problem(path, None, label, "a valid case cannot list expected errors"))
        elif not case["expected_valid"] and not case["expected_errors"]:
            problems.append(_problem(path, None, label, "an invalid case must say which error it expects"))

    return problems


def validate_all(directory: str) -> Dict[str, List[str]]:
    """Check both main files and return the problems per file."""
    return {
        "order_calculations.csv": validate_order_csv(os.path.join(directory, "order_calculations.csv")),
        "customer_validation.json": validate_customer_json(
            os.path.join(directory, "customer_validation.json")
        ),
    }


def require_valid_data(directory: str) -> None:
    """Raise DataValidationError when any file has problems."""
    findings = validate_all(directory)
    everything = [problem for problems in findings.values() for problem in problems]
    if everything:
        raise DataValidationError("\n".join(everything))
