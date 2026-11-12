"""Preflight checks for the external CSV and JSON test-data files."""

import csv
import json
import math
from pathlib import Path
from typing import Any

ORDER_EXPECTED_FIELDS = (
    "expected_subtotal",
    "expected_discount",
    "expected_tax",
    "expected_shipping",
    "expected_total",
)
ORDER_NUMERIC_FIELDS = ("distance_km", *ORDER_EXPECTED_FIELDS)
ORDER_REQUIRED_FIELDS = ("test_name", "items", "customer_type", "discount_code")
ORDER_HEADERS = {
    "test_name",
    "items",
    "customer_type",
    "discount_code",
    "distance_km",
    "is_express",
} | set(ORDER_EXPECTED_FIELDS)


def _validate_row_fields(row: dict[str, Any], line_number: int) -> list[str]:
    errors = []
    if None in row:
        errors.append(f"line {line_number}: unexpected extra CSV fields")
    for field in ORDER_REQUIRED_FIELDS:
        if not row.get(field):
            errors.append(f"line {line_number}: {field} is required")
    if row.get("is_express") not in {"true", "false"}:
        errors.append(f"line {line_number}: is_express must be true or false")
    return errors


def _validate_row_items(row: dict[str, Any], line_number: int) -> list[str]:
    items_text = row.get("items")
    if not isinstance(items_text, str) or not items_text:
        return [f"line {line_number}: items must be a JSON array"]

    try:
        items = json.loads(items_text)
    except json.JSONDecodeError as error:
        return [f"line {line_number}: invalid items JSON: {error.msg}"]
    if not isinstance(items, list) or not items:
        return [f"line {line_number}: items must be a non-empty array"]
    if any(
        not isinstance(item, dict)
        or not {"name", "price", "quantity", "weight"}.issubset(item)
        for item in items
    ):
        return [
            f"line {line_number}: each item needs name, price, quantity, and weight"
        ]
    return []


def _validate_row_numbers(row: dict[str, Any], line_number: int) -> list[str]:
    errors = []
    for field in ORDER_NUMERIC_FIELDS:
        try:
            number = float(row.get(field, ""))
            if not math.isfinite(number):
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"line {line_number}: {field} must be a finite number")
    return errors


def validate_order_csv(path: Path) -> list[str]:
    """Return line-numbered errors for malformed order calculation records."""
    errors: list[str] = []
    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            return ["line 1: missing CSV header"]
        missing_headers = ORDER_HEADERS.difference(reader.fieldnames)
        if missing_headers:
            errors.append(
                f"line 1: missing columns: {', '.join(sorted(missing_headers))}"
            )
        for row in reader:
            line_number = reader.line_num
            errors.extend(_validate_row_fields(row, line_number))
            errors.extend(_validate_row_items(row, line_number))
            errors.extend(_validate_row_numbers(row, line_number))
    return errors


def validate_customer_json(path: Path) -> list[str]:
    """Return record-numbered errors for malformed customer validation data."""
    with path.open(encoding="utf-8") as file:
        try:
            records: Any = json.load(file)
        except json.JSONDecodeError as error:
            return [f"line {error.lineno}: invalid JSON: {error.msg}"]

    if not isinstance(records, list):
        return ["record 1: expected a JSON array"]
    errors: list[str] = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"record {index}: expected an object")
            continue
        if not isinstance(record.get("test_name"), str) or not record["test_name"]:
            errors.append(f"record {index}: test_name is required")
        if record.get("customer") is not None and not isinstance(
            record["customer"], dict
        ):
            errors.append(f"record {index}: customer must be an object or null")
        expected = record.get("expected")
        if not isinstance(expected, dict) or not isinstance(
            expected.get("is_valid"), bool
        ):
            errors.append(f"record {index}: expected.is_valid must be a boolean")
        elif not isinstance(expected.get("errors"), list) or any(
            not isinstance(message, str) for message in expected["errors"]
        ):
            errors.append(f"record {index}: expected.errors must be a string array")
    return errors
