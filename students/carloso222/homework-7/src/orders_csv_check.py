"""Validate order CSV files (required columns, types, items JSON) and report line numbers."""

import csv
import json
from pathlib import Path
from typing import Dict, List

from src.data_checks import DataIssue, is_integer, is_number, parse_float

REQUIRED_COLUMNS = (
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
)
FLOAT_COLUMNS = (
    "distance_km",
    "expected_subtotal",
    "expected_discount",
    "expected_tax",
    "expected_shipping",
    "expected_total",
)


def _item_problems(items_text: str) -> List[str]:
    try:
        items = json.loads(items_text)
    except json.JSONDecodeError as error:
        return [f"items is not valid JSON ({error.msg})"]
    if not isinstance(items, list):
        return ["items must be a JSON list"]
    problems = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            problems.append(f"items[{index}] must be an object")
            continue
        if not isinstance(item.get("name"), str):
            problems.append(f"items[{index}].name must be a string")
        if not is_number(item.get("price")):
            problems.append(f"items[{index}].price must be a number")
        if not is_integer(item.get("quantity")):
            problems.append(f"items[{index}].quantity must be an integer")
        if not is_number(item.get("weight")):
            problems.append(f"items[{index}].weight must be a number")
    return problems


def _row_problems(row: Dict[str, str]) -> List[str]:
    problems = [
        f"{column} is empty"
        for column in REQUIRED_COLUMNS
        if not (row.get(column) or "").strip()
    ]
    if problems:
        return problems
    if row["customer_type"] not in ("new", "regular"):
        problems.append("customer_type must be 'new' or 'regular'")
    if row["is_express"] not in ("true", "false"):
        problems.append("is_express must be 'true' or 'false'")
    problems += [
        f"{column} must be a number"
        for column in FLOAT_COLUMNS
        if not parse_float(row[column])
    ]
    return problems + _item_problems(row["items"])


def validate_orders_csv(path: Path) -> List[DataIssue]:
    """Return every problem found in an order CSV (empty list = file is valid)."""
    name = path.name
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [
            column
            for column in REQUIRED_COLUMNS
            if column not in (reader.fieldnames or [])
        ]
        if missing:
            return [
                DataIssue(name, 1, f"missing required columns: {', '.join(missing)}")
            ]
        issues: List[DataIssue] = []
        seen: set = set()
        for row in reader:
            issues += [
                DataIssue(name, reader.line_num, problem)
                for problem in _row_problems(row)
            ]
            if row["test_name"] in seen:
                issues.append(
                    DataIssue(
                        name,
                        reader.line_num,
                        f"duplicate test_name '{row['test_name']}'",
                    )
                )
            seen.add(row["test_name"])
        return issues
