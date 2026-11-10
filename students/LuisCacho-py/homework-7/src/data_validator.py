"""Bonus module: Test data validation (Option C) and synthetic test data generation (Option A)."""

import csv
import json
import random
from pathlib import Path
from typing import Any, Dict, List

from order_calculator import Order

REQUIRED_ORDER_CSV_FIELDS = [
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

REQUIRED_CUSTOMER_JSON_FIELDS = ["test_name", "customer", "expected"]


def validate_order_csv_file(filepath: str) -> Dict[str, Any]:
    """
    Validate an order calculations CSV file before running tests.

    Checks required columns, verifies JSON item structure and numeric/boolean types,
    and reports any invalid rows with their 1-based line numbers.
    """
    path = Path(filepath)
    if not path.exists():
        return {"is_valid": False, "errors": [f"Line 0: File not found: {filepath}"]}

    errors: List[str] = []
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames:
            return {"is_valid": False, "errors": ["Line 1: Empty CSV or missing header"]}

        missing = [col for col in REQUIRED_ORDER_CSV_FIELDS if col not in reader.fieldnames]
        if missing:
            return {
                "is_valid": False,
                "errors": [f"Line 1: Missing required columns: {', '.join(missing)}"],
            }

        for row_idx, row in enumerate(reader, start=2):
            if not row.get("test_name") or not row["test_name"].strip():
                errors.append(f"Line {row_idx}: Missing test_name")

            try:
                items = json.loads((row.get("items") or "").replace("'", '"'))
                if not isinstance(items, list):
                    errors.append(f"Line {row_idx}: items must be a JSON list")
            except json.JSONDecodeError:
                errors.append(f"Line {row_idx}: Invalid JSON in items field")

            if row.get("customer_type") not in ("regular", "new"):
                errors.append(f"Line {row_idx}: Invalid customer_type '{row.get('customer_type')}'")

            if (row.get("is_express") or "").lower() not in ("true", "false"):
                errors.append(f"Line {row_idx}: is_express must be 'true' or 'false'")

            for num_field in (
                "distance_km",
                "expected_subtotal",
                "expected_discount",
                "expected_tax",
                "expected_shipping",
                "expected_total",
            ):
                try:
                    float(row.get(num_field, ""))
                except (TypeError, ValueError):
                    errors.append(f"Line {row_idx}: Invalid float in '{num_field}'")

    return {"is_valid": len(errors) == 0, "errors": errors}


def validate_customer_json_file(filepath: str) -> Dict[str, Any]:
    """
    Validate customer validation JSON test data file and report invalid entries with index/line.
    """
    path = Path(filepath)
    if not path.exists():
        return {"is_valid": False, "errors": [f"File not found: {filepath}"]}

    try:
        raw_text = path.read_text(encoding="utf-8")
        records = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        return {"is_valid": False, "errors": [f"Line {exc.lineno}: Invalid JSON ({exc.msg})"]}

    if not isinstance(records, list):
        return {"is_valid": False, "errors": ["Line 1: Root JSON element must be a list"]}

    errors: List[str] = []
    for index, entry in enumerate(records, start=1):
        if not isinstance(entry, dict):
            errors.append(f"Entry {index}: Record must be an object")
            continue

        for req in REQUIRED_CUSTOMER_JSON_FIELDS:
            if req not in entry:
                errors.append(f"Entry {index}: Missing required field '{req}'")

        expected = entry.get("expected")
        if isinstance(expected, dict):
            if not isinstance(expected.get("is_valid"), bool):
                errors.append(f"Entry {index}: expected.is_valid must be a boolean")
            if not isinstance(expected.get("errors"), list):
                errors.append(f"Entry {index}: expected.errors must be a list")

    return {"is_valid": len(errors) == 0, "errors": errors}


def generate_valid_orders(count: int = 100, seed: int = 42) -> List[Dict[str, Any]]:
    """
    Programmatically generate valid order test cases for regression testing (Bonus Option A).
    """
    rng = random.Random(seed)
    catalog = [
        ("Laptop", 899.99, 2.2),
        ("Wireless Mouse", 29.50, 0.2),
        ("Mechanical Keyboard", 110.00, 0.9),
        ("USB-C Hub", 45.00, 0.3),
        ("Monitor 27in", 320.00, 4.5),
        ("Desk Lamp", 35.00, 0.8),
        ("Webcam HD", 65.00, 0.4),
        ("Noise Canceling Headphones", 199.00, 0.6),
    ]
    discount_choices = ["NONE", "SAVE10", "SAVE20", "FREESHIP", "NEWUSER"]
    generated: List[Dict[str, Any]] = []

    for idx in range(1, count + 1):
        num_items = rng.randint(1, 3)
        chosen = rng.sample(catalog, num_items)
        items = []
        for name, price, weight in chosen:
            items.append(
                {
                    "name": name,
                    "price": price,
                    "quantity": rng.randint(1, 3),
                    "weight": weight,
                }
            )

        customer_type = rng.choice(["regular", "new"])
        discount_code = rng.choice(discount_choices)
        distance_km = round(rng.uniform(5.0, 200.0), 1)
        is_express = rng.choice([True, False])

        order = Order(items, customer_type=customer_type)
        if discount_code != "NONE":
            order.apply_discount(discount_code)
        order.set_shipping(distance_km, is_express)
        totals = order.calculate_total()

        generated.append(
            {
                "test_name": f"generated_order_{idx:03d}",
                "items": json.dumps(items),
                "customer_type": customer_type,
                "discount_code": discount_code,
                "distance_km": distance_km,
                "is_express": "true" if is_express else "false",
                "expected_subtotal": f"{totals['subtotal']:.2f}",
                "expected_discount": f"{totals['discount']:.2f}",
                "expected_tax": f"{totals['tax']:.2f}",
                "expected_shipping": f"{totals['shipping']:.2f}",
                "expected_total": f"{totals['total']:.2f}",
            }
        )

    return generated


def save_generated_orders_csv(filepath: str, count: int = 100, seed: int = 42) -> int:
    """Generate and save valid orders to a CSV file, returning the number of rows written."""
    rows = generate_valid_orders(count=count, seed=seed)
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=REQUIRED_ORDER_CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)
