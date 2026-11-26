"""Valida los archivos de datos de prueba ANTES de ejecutar los tests."""
import csv
import json
from pathlib import Path
from typing import List

REQUIRED_COLUMNS = ["test_name", "items", "customer_type", "discount_code", "distance_km",
                    "is_express", "expected_subtotal", "expected_discount", "expected_tax",
                    "expected_shipping", "expected_total"]
ITEM_FIELDS = ("name", "price", "quantity", "weight")


def _is_number(value: str) -> bool:
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def validate_orders_csv(path) -> List[str]:
    """Devuelve una lista de errores 'Line N: ...' (vacia si el archivo es valido)."""
    errors: List[str] = []
    seen = set()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            return [f"Line 1: missing columns {missing}"]

        for row in reader:
            line = reader.line_num
            name = (row["test_name"] or "").strip()
            if not name:
                errors.append(f"Line {line}: test_name is empty")
            elif name in seen:
                errors.append(f"Line {line}: duplicate test_name '{name}'")
            seen.add(name)

            try:
                items = json.loads(row["items"].replace("'", '"'))
                if not isinstance(items, list):
                    raise ValueError("items must be a list")
                for item in items:
                    absent = [k for k in ITEM_FIELDS if k not in item]
                    if absent:
                        errors.append(f"Line {line}: item missing fields {absent}")
            except ValueError as error:
                errors.append(f"Line {line}: invalid items ({error})")

            if row["customer_type"].strip() not in ("new", "regular"):
                errors.append(f"Line {line}: customer_type must be 'new' or 'regular'")
            if row["is_express"].strip().lower() not in ("true", "false"):
                errors.append(f"Line {line}: is_express must be 'true' or 'false'")
            for column in ["distance_km"] + [c for c in REQUIRED_COLUMNS if c.startswith("expected_")]:
                if not _is_number(row[column]):
                    errors.append(f"Line {line}: '{column}' is not a number ({row[column]!r})")
    return errors


def validate_customers_json(path) -> List[str]:
    """Valida estructura de customer_validation.json."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"Line {error.lineno}: invalid JSON ({error.msg})"]

    if not isinstance(data, list):
        return ["Root must be a list"]
    errors = []
    for index, case in enumerate(data):
        for key in ("test_name", "customer", "expected"):
            if key not in case:
                errors.append(f"Case #{index}: missing '{key}'")
        expected = case.get("expected", {})
        if not isinstance(expected.get("is_valid"), bool):
            errors.append(f"Case #{index}: expected.is_valid must be boolean")
        if not isinstance(expected.get("errors"), list):
            errors.append(f"Case #{index}: expected.errors must be a list")
    return errors