"""Helpers that load the external test data files (CSV / JSON).

Paths are resolved relative to this file so tests work from any directory.
"""

import csv
import json
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"
DEFAULT_REFERENCE_DATE = date(2026, 1, 1)


def parse_items(raw: str):
    """Parse the CSV ``items`` column (JSON with single quotes)."""
    return json.loads(raw.replace("'", '"'))


def parse_reference_date(value):
    """ISO string -> date; None -> the fixed default (keeps tests deterministic)."""
    return date.fromisoformat(value) if value else DEFAULT_REFERENCE_DATE


def load_order_cases(path=None):
    """Return the rows of order_calculations.csv as dicts ready for tests."""
    path = Path(path) if path else DATA_DIR / "order_calculations.csv"
    cases = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            code = row["discount_code"]
            cases.append(
                {
                    "test_name": row["test_name"],
                    "items": parse_items(row["items"]),
                    "customer_type": row["customer_type"],
                    "discount_code": None if code == "NONE" else code,
                    "distance": float(row["distance_km"]),
                    "is_express": row["is_express"] == "true",
                    "expected": {
                        "subtotal": float(row["expected_subtotal"]),
                        "discount": float(row["expected_discount"]),
                        "tax": float(row["expected_tax"]),
                        "shipping": float(row["expected_shipping"]),
                        "total": float(row["expected_total"]),
                    },
                }
            )
    return cases


def load_customer_cases(path=None):
    """Return the list of cases in customer_validation.json."""
    path = Path(path) if path else DATA_DIR / "customer_validation.json"
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def load_workflows(path=None):
    """Return (reference_date, workflows) from order_workflows.json."""
    path = Path(path) if path else DATA_DIR / "order_workflows.json"
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    return parse_reference_date(data.get("reference_date")), data["workflows"]


def case_ids(cases, key="test_name"):
    """pytest ids from the ``test_name`` field."""
    return [case[key] for case in cases]
