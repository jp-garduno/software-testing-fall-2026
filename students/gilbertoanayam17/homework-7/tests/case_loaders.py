"""Loaders that turn the files in test_data/ into ready-to-use pytest cases.

Every loader returns a list of pytest.param objects whose id is the case name,
so a test only has to say which file drives it:

    @pytest.mark.parametrize("case", load_order_csv("order_calculations.csv"))

Paths are resolved from this file, not from the working directory, so the
suite runs the same from any folder.
"""

import csv
import json
from datetime import date
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"

# Card expirations in the data files are judged as of this date, so a case
# that passes today still passes next year.
REFERENCE_DATE = date(2025, 6, 15)

AMOUNTS = ("subtotal", "discount", "tax", "shipping", "total")


def order_case(row):
    """Turn one flat row (CSV text or typed Excel cells) into an order case."""
    return {
        "test_name": row["test_name"],
        "items": json.loads(row["items"].replace("'", '"')),
        "customer_type": row["customer_type"],
        "discount_code": None if row["discount_code"] == "NONE" else row["discount_code"],
        "distance_km": float(row["distance_km"]),
        "is_express": str(row["is_express"]).lower() == "true",
        "expected": {amount: float(row[f"expected_{amount}"]) for amount in AMOUNTS},
    }


def load_order_csv(filename):
    """Read an order CSV: one row per case, columns as in TEST_DATA_SPEC.md."""
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as csv_file:
        cases = [order_case(row) for row in csv.DictReader(csv_file)]
    return [pytest.param(case, id=case["test_name"]) for case in cases]


def load_customer_cases(filename):
    """Read customer cases: a JSON list of {"test_name", "customer", "expected"}."""
    cases = json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))
    return [pytest.param(case, id=case["test_name"]) for case in cases]


def load_workflows(filename):
    """Read end-to-end workflows: {"workflows": [{"name", "steps": [...]}]}."""
    document = json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))
    return [pytest.param(workflow, id=workflow["name"]) for workflow in document["workflows"]]
