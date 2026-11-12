"""Shared paths and imports for the whole suite.

pytest.ini already puts the root and src/ on pythonpath. This file repeats the
adjustment through sys.path so the suite also runs on a runner whose pytest
does not support that option, and centralises loading the data files.
"""

import csv
import json
import os
import sys

import pytest

HW_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(HW_ROOT, "src")
DATA_DIR = os.path.join(HW_ROOT, "test_data")

for path in (SRC_DIR, HW_ROOT):
    if path not in sys.path:
        sys.path.insert(0, path)

# Must come after sys.path is adjusted, hence the exception.
from order_calculator import Order  # noqa: E402  pylint: disable=wrong-import-position


def data_path(name):
    """Absolute path to a file in test_data/, independent of the cwd."""
    return os.path.join(DATA_DIR, name)


def load_csv(name):
    """Read a CSV from test_data/ as a list of dictionaries."""
    with open(data_path(name), newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(name):
    """Read a JSON file from test_data/."""
    with open(data_path(name), encoding="utf-8") as handle:
        return json.load(handle)


def order_cases():
    """Rows of order_calculations.csv with their types already converted."""
    cases = []
    for row in load_csv("order_calculations.csv"):
        cases.append(
            {
                "test_name": row["test_name"],
                "category": row["category"],
                "items": json.loads(row["items"]),
                "customer_type": row["customer_type"],
                "discount_code": row["discount_code"],
                "distance_km": float(row["distance_km"]),
                "is_express": row["is_express"] == "true",
                "expected": {
                    key: float(row[f"expected_{key}"])
                    for key in ("subtotal", "discount", "tax", "shipping", "total")
                }
                if not row["expected_error"]
                else None,
                "expected_error": row["expected_error"],
            }
        )
    return cases


def build_order(case):
    """Build the Order for a case and apply its discount and shipping."""
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"] != "NONE":
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance_km"], case["is_express"])
    return order


@pytest.fixture(scope="session")
def customer_cases():
    """Cases from customer_validation.json."""
    return load_json("customer_validation.json")["test_cases"]


@pytest.fixture(scope="session")
def workflows():
    """Workflows from order_workflows.json."""
    return load_json("order_workflows.json")["workflows"]
