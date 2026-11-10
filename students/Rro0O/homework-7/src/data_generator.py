"""Bonus A: generate valid random orders (Faker) as a CSV for regression tests.

Usage:  python src/data_generator.py [output.csv] [count] [seed]

The expected_* columns are a snapshot of the current calculator output, so the
file is a regression baseline: if the pricing rules change the baseline test
fails and shows exactly which orders moved.
"""

import csv
import json
import random
import sys
from pathlib import Path

from faker import Faker

from order_calculator import VALID_CODES, Order

HEADER = (
    "test_name,items,customer_type,discount_code,distance_km,is_express,"
    "expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total"
).split(",")
CODES = ["NONE", "NONE"] + sorted(VALID_CODES)  # NONE is twice as likely


def generate_orders(count: int = 100, seed: int = 2026):
    """Return ``count`` reproducible, valid order rows (list of dicts)."""
    fake = Faker()
    Faker.seed(seed)
    rng = random.Random(seed)
    rows = []
    for number in range(1, count + 1):
        items = [
            {
                "name": fake.word().capitalize(),
                "price": round(rng.uniform(0.5, 400), 2),
                "quantity": rng.randint(1, 10),
                "weight": round(rng.uniform(0, 15), 1),
            }
            for _ in range(rng.randint(1, 5))
        ]
        customer_type = rng.choice(["new", "regular"])
        code = rng.choice(CODES)
        distance = round(rng.uniform(0, 2000), 1)
        express = rng.random() < 0.3

        order = Order(items, customer_type)
        if code != "NONE":
            order.apply_discount(code)
        order.set_shipping(distance, express)
        result = order.calculate_total()
        rows.append(
            {
                "test_name": f"generated_{number:03d}_{fake.last_name().lower()}",
                "items": json.dumps(items, separators=(",", ":")).replace('"', "'"),
                "customer_type": customer_type,
                "discount_code": code,
                "distance_km": distance,
                "is_express": str(express).lower(),
                **{f"expected_{k}": f"{v:.2f}" for k, v in result.items()},
            }
        )
    return rows


def write_csv(path, rows) -> None:
    """Write rows with the same columns as order_calculations.csv."""
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    default = Path(__file__).resolve().parent.parent / "test_data" / "generated_orders.csv"
    out = Path(argv[0]) if argv else default
    count = int(argv[1]) if len(argv) > 1 else 100
    seed = int(argv[2]) if len(argv) > 2 else 2026
    write_csv(out, generate_orders(count, seed))
    print(f"wrote {count} orders to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
