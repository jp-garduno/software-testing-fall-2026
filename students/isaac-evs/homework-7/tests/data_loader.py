"""Helpers that load external test data (CSV, JSON, XLSX) for the data-driven tests."""

import csv
import json
from datetime import date
from pathlib import Path

import pytest

from order_calculator import Order

DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"
ORDER_CSV = DATA_DIR / "order_calculations.csv"
CUSTOMER_JSON = DATA_DIR / "customer_validation.json"
WORKFLOW_JSON = DATA_DIR / "order_workflows.json"
COMPONENTS = ("subtotal", "discount", "tax", "shipping", "total")
REFERENCE_DATE = date(2026, 6, 15)  # "today" for card expiry checks unless a case sets as_of


def _text(value):
    """Return a cell value as stripped text; empty cells become an empty string."""
    return "" if value is None else str(value).strip()


def _optional_float(value):
    text = _text(value)
    return float(text) if text else None


def parse_order_row(row):
    """Turn one CSV/XLSX row (a dict of cell values) into a structured test case."""
    code = _text(row["discount_code"])
    return {
        "test_name": _text(row["test_name"]),
        "category": _text(row["category"]),
        "items": json.loads(_text(row["items"])),
        "customer_type": _text(row["customer_type"]),
        "discount_code": None if code in ("", "NONE") else code,
        "distance": float(_text(row["distance_km"])),
        "is_express": _text(row["is_express"]).lower() == "true",
        "expected": {name: _optional_float(row[f"expected_{name}"]) for name in COMPONENTS},
        "expected_error": _text(row.get("expected_error")),
    }


def read_order_rows(path=ORDER_CSV):
    """Read the raw rows of an order CSV file."""
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def to_params(rows, error_cases):
    """Convert rows to pytest params, keeping only error cases or only valid cases."""
    cases = [parse_order_row(row) for row in rows]
    return [pytest.param(case, id=case["test_name"]) for case in cases if bool(case["expected_error"]) == error_cases]


def load_order_cases(path=ORDER_CSV, error_cases=False):
    """Load order test cases from a CSV file as pytest params."""
    return to_params(read_order_rows(path), error_cases)


def run_order_case(case):
    """Build the order described by a test case and return its calculated breakdown."""
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance"], case["is_express"])
    return order.calculate_total()


def load_customer_cases(path=CUSTOMER_JSON, category=None):
    """Load customer validation cases from JSON as pytest params, optionally for one category."""
    with open(path, encoding="utf-8") as handle:
        cases = json.load(handle)
    return [pytest.param(case, id=case["test_name"]) for case in cases if category in (None, case["category"])]


def case_date(case):
    """The date a customer case is validated on: its as_of field or the shared reference date."""
    return date.fromisoformat(case["as_of"]) if "as_of" in case else REFERENCE_DATE
