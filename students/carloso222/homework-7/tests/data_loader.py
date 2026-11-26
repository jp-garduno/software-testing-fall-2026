"""Test-data access for the data-driven tests. Paths are relative to this file, never to the cwd."""

import csv
import json
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest
from src.order_calculator import Order

TEST_DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"
REFERENCE_DATE = date(
    2026, 1, 15
)  # fixed "today" so expiration checks never depend on the real clock


def _parse_order_row(row: Dict[str, str]) -> Dict[str, Any]:
    return {
        "test_name": row["test_name"],
        "items": json.loads(row["items"]),
        "customer_type": row["customer_type"],
        "discount_code": (
            None if row["discount_code"] == "NONE" else row["discount_code"]
        ),
        "distance": float(row["distance_km"]),
        "is_express": row["is_express"] == "true",
        "expected": {
            key: float(row[f"expected_{key}"])
            for key in ("subtotal", "discount", "tax", "shipping", "total")
        },
    }


def load_order_cases(
    filename: str = "order_calculations.csv", names: Optional[List[str]] = None
) -> List[Any]:
    """Load order cases from a CSV as pytest params (id = test_name); optionally only the named rows, in that order."""
    with (TEST_DATA_DIR / filename).open(newline="", encoding="utf-8") as handle:
        cases = {
            row["test_name"]: _parse_order_row(row) for row in csv.DictReader(handle)
        }
    selected = names if names is not None else list(cases)
    return [pytest.param(cases[name], id=name) for name in selected]


def calculate_case(case: Dict[str, Any]) -> Dict[str, float]:
    """Run one loaded case through Order and return the calculated breakdown."""
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance"], case["is_express"])
    return order.calculate_total()


def load_customer_cases() -> List[Any]:
    """Load customer_validation.json as pytest params (id = test_name)."""
    cases = json.loads(
        (TEST_DATA_DIR / "customer_validation.json").read_text(encoding="utf-8")
    )
    return [pytest.param(case, id=case["test_name"]) for case in cases]


def load_workflows() -> Dict[str, Any]:
    """Load order_workflows.json (reference_date + workflows)."""
    return json.loads(
        (TEST_DATA_DIR / "order_workflows.json").read_text(encoding="utf-8")
    )
