"""Generate valid random orders with Faker and save them as a regression CSV (bonus option A).

Usage (from the homework-7 folder):  python -m src.order_generator
"""

import csv
import json
import random
from pathlib import Path
from typing import Dict, List

from faker import Faker  # pylint: disable=import-error
from src.discounts import DISCOUNT_RULES
from src.order_calculator import Order
from src.orders_csv_check import REQUIRED_COLUMNS

DEFAULT_OUTPUT = (
    Path(__file__).resolve().parent.parent / "test_data" / "generated_orders.csv"
)
COLUMNS = REQUIRED_COLUMNS + ("category",)


def _random_items(rng: random.Random, fake: Faker) -> List[Dict[str, object]]:
    return [
        {
            "name": fake.word().capitalize(),
            "price": round(rng.uniform(1, 200), 2),
            "quantity": rng.randint(1, 5),
            "weight": round(rng.uniform(0, 10), 1),
        }
        for _ in range(rng.randint(1, 4))
    ]


def generate_order_rows(count: int = 100, seed: int = 2026) -> List[Dict[str, str]]:
    """Build `count` valid order rows; expected values are a regression snapshot taken from Order."""
    fake = Faker()
    fake.seed_instance(seed)
    rng = random.Random(seed)
    rows = []
    for number in range(1, count + 1):
        customer_type = rng.choice(("new", "regular"))
        code = rng.choice(
            ["NONE"]
            + [
                c
                for c, rule in DISCOUNT_RULES.items()
                if rule["customer_type"] in (None, customer_type)
            ]
        )
        distance, express = round(rng.uniform(0, 500), 1), rng.random() < 0.3
        items = _random_items(rng, fake)
        order = Order(items, customer_type)
        if code != "NONE":
            order.apply_discount(code)
        order.set_shipping(distance, express)
        result = order.calculate_total()
        rows.append(
            {
                "test_name": f"generated_{number:03d}",
                "items": json.dumps(items),
                "customer_type": customer_type,
                "discount_code": code,
                "distance_km": str(distance),
                "is_express": "true" if express else "false",
                **{f"expected_{key}": f"{value:.2f}" for key, value in result.items()},
                "category": "generated",
            }
        )
    return rows


def write_orders_csv(rows: List[Dict[str, str]], path: Path = DEFAULT_OUTPUT) -> Path:
    """Write the rows to a CSV with the same columns as order_calculations.csv."""
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return path


if __name__ == "__main__":
    print(f"Wrote {write_orders_csv(generate_order_rows())}")
