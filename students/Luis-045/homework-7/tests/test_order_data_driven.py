"""Load order cases from CSV and run the ten comparison scenarios."""

import csv
import json
from pathlib import Path
from typing import NamedTuple

import pytest

from src.order_calculator import Order

DATA_DIR = Path(__file__).resolve().parents[1] / "test_data"
AMOUNTS = ("subtotal", "discount", "tax", "shipping", "total")


class OrderCase(NamedTuple):
    """Inputs and expectations from one row of the order CSV."""

    name: str
    items: list[dict]
    customer_type: str
    discount_code: str | None
    distance_km: float
    is_express: bool
    expected: dict[str, float] | None
    discount_applied: bool | None
    error: str | None
    comparison: bool


def load_order_cases() -> list[OrderCase]:
    """Read order CSV rows; item arrays are JSON inside a CSV field."""
    cases = []
    with (DATA_DIR / "order_calculations.csv").open(
        encoding="utf-8", newline=""
    ) as file:
        for row in csv.DictReader(file):
            error = row["expected_error"] or None
            cases.append(
                OrderCase(
                    name=row["test_name"],
                    items=json.loads(row["items"]),
                    customer_type=row["customer_type"],
                    discount_code=(
                        None if row["discount_code"] == "NONE" else row["discount_code"]
                    ),
                    distance_km=float(row["distance_km"]),
                    is_express=row["is_express"] == "true",
                    expected=(
                        None
                        if error
                        else {key: float(row[f"expected_{key}"]) for key in AMOUNTS}
                    ),
                    discount_applied=(
                        row["expected_discount_applied"] == "true"
                        if row["expected_discount_applied"]
                        else None
                    ),
                    error=error,
                    comparison=row["comparison"] == "true",
                )
            )
    return cases


def configure_order(case: OrderCase) -> Order:
    """Create the order and assert the acceptance result for any supplied coupon."""
    order = Order(case.items, case.customer_type)
    if case.discount_code is not None:
        assert order.apply_discount(case.discount_code) is case.discount_applied
    order.set_shipping(case.distance_km, case.is_express)
    return order


ORDER_CASES = load_order_cases()
COMPARISON_CASES = [case for case in ORDER_CASES if case.comparison]


@pytest.mark.parametrize("case", COMPARISON_CASES, ids=lambda case: case.name)
def test_order_from_data(case):
    """Check the coupon result and all five amounts for each selected order."""
    assert configure_order(case).calculate_total() == case.expected
