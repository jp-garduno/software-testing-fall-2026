"""Bonus Option A & C: Test data validator and Faker-based order data generator."""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List

from faker import Faker

from src.order_calculator import Order

REQUIRED_CSV_COLUMNS = [
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
]

NUMERIC_CSV_FIELDS = (
    "distance_km",
    "expected_subtotal",
    "expected_discount",
    "expected_tax",
    "expected_shipping",
    "expected_total",
)


def _validate_csv_row(row_idx: int, row: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Validate a single row from an order calculation CSV file."""
    row_errors: List[Dict[str, Any]] = []
    if not row.get("test_name") or not row["test_name"].strip():
        row_errors.append({"line": row_idx, "message": "Empty test_name"})

    try:
        items = json.loads((row.get("items") or "").replace("'", '"'))
        if not isinstance(items, list):
            row_errors.append({"line": row_idx, "message": "items must be a list"})
    except json.JSONDecodeError:
        row_errors.append({"line": row_idx, "message": "Invalid JSON in items"})

    if row.get("is_express") not in ("true", "false"):
        row_errors.append(
            {"line": row_idx, "message": "is_express must be 'true' or 'false'"}
        )

    for field in NUMERIC_CSV_FIELDS:
        try:
            float(row.get(field, ""))
        except (TypeError, ValueError):
            row_errors.append(
                {"line": row_idx, "message": f"Invalid float in {field}"}
            )

    return row_errors


def validate_order_csv_file(csv_path: str | Path) -> Dict[str, Any]:
    """
    Validate an order calculations CSV file before running tests (Bonus Option C).

    Checks required columns, JSON item structure, numeric fields, and boolean flags,
    reporting any invalid rows with their exact line numbers.
    """
    errors: List[Dict[str, Any]] = []
    path = Path(csv_path)

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        missing_cols = [col for col in REQUIRED_CSV_COLUMNS if col not in fieldnames]
        if missing_cols:
            return {
                "is_valid": False,
                "errors": [
                    {
                        "line": 1,
                        "message": f"Missing required columns: {', '.join(missing_cols)}",
                    }
                ],
            }

        for row_idx, row in enumerate(reader, start=2):
            errors.extend(_validate_csv_row(row_idx, row))

    return {"is_valid": len(errors) == 0, "errors": errors}


def _build_synthetic_order_row(fake: Faker, idx: int) -> Dict[str, str]:
    """Build a single synthetic order CSV dictionary entry."""
    discount_pool = ("NONE", "SAVE10", "SAVE20", "FREESHIP", "NEWUSER")
    customer_types = ("regular", "new")

    items = [
        {
            "name": f"{fake.word().capitalize()}_{item_idx + 1}",
            "price": round(15.0 + ((idx * 7 + item_idx * 13) % 85), 2),
            "quantity": (item_idx % 2) + 1,
            "weight": round(0.5 + ((idx + item_idx) % 5) * 0.5, 2),
        }
        for item_idx in range((idx % 3) + 1)
    ]

    customer_type = customer_types[idx % len(customer_types)]
    discount_code = discount_pool[idx % len(discount_pool)]
    distance_km = float((idx * 5) % 100)
    is_express = (idx % 2) == 0

    order = Order(items, customer_type=customer_type)
    if discount_code != "NONE":
        order.apply_discount(discount_code)
    order.set_shipping(distance_km, is_express=is_express)
    totals = order.calculate_total()

    return {
        "test_name": f"generated_order_{idx:03d}",
        "items": json.dumps(items),
        "customer_type": customer_type,
        "discount_code": discount_code,
        "distance_km": f"{distance_km:.2f}",
        "is_express": "true" if is_express else "false",
        "expected_subtotal": f"{totals['subtotal']:.2f}",
        "expected_discount": f"{totals['discount']:.2f}",
        "expected_tax": f"{totals['tax']:.2f}",
        "expected_shipping": f"{totals['shipping']:.2f}",
        "expected_total": f"{totals['total']:.2f}",
    }


def generate_synthetic_orders_csv(
    output_path: str | Path, count: int = 100, seed: int = 42
) -> int:
    """
    Generate valid synthetic order test cases using Faker and save to CSV (Bonus Option A).
    """
    fake = Faker()
    Faker.seed(seed)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_CSV_COLUMNS)
        writer.writeheader()
        for idx in range(1, count + 1):
            writer.writerow(_build_synthetic_order_row(fake, idx))

    return count
