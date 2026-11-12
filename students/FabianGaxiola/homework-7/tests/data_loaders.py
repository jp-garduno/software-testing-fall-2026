"""Shared, path-stable loaders for the homework's external test data."""

import csv
import json
from pathlib import Path
from typing import Any

from data_validation import ORDER_EXPECTED_FIELDS

DATA_DIR = Path(__file__).resolve().parents[1] / "test_data"


def load_order_cases() -> list[dict[str, Any]]:
    with (DATA_DIR / "order_calculations.csv").open(
        encoding="utf-8", newline=""
    ) as file:
        rows = list(csv.DictReader(file))
    for row in rows:
        row["items"] = json.loads(row["items"])
        row["distance_km"] = float(row["distance_km"])
        row["is_express"] = row["is_express"] == "true"
        for field in ORDER_EXPECTED_FIELDS:
            row[field] = float(row[field])
        row["discount_code"] = (
            None if row["discount_code"] == "NONE" else row["discount_code"]
        )
    return rows


def load_customer_cases() -> list[dict[str, Any]]:
    with (DATA_DIR / "customer_validation.json").open(encoding="utf-8") as file:
        return json.load(file)


def load_workflows() -> list[dict[str, Any]]:
    with (DATA_DIR / "order_workflows.json").open(encoding="utf-8") as file:
        return json.load(file)["workflows"]
