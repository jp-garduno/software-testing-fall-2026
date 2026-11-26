"""Write a seeded snapshot of 100 valid orders to test_data/generated_orders.csv for regression testing.

Run ``python -m tools.generate_orders`` from the homework root. The expected amounts are produced by the
current Order implementation, so the snapshot detects unintended behaviour changes but cannot prove the
rules are right: that is the job of the hand-calculated order_calculations.csv.
"""

import csv
import json
import random
from datetime import date

from faker import Faker

from src.order_calculator import Order
from tools.data_files import ORDER_COLUMNS, TEST_DATA_DIR

SEED = 2026
ORDER_COUNT = 100
ORDER_DATE = date(2026, 11, 1)
CODES = ("NONE", "SAVE10", "SAVE20", "FREESHIP", "NEWUSER", "SUMMER25", "WELCOME5")
PRODUCTS = ("backpack", "blender", "desk lamp", "headphones", "jacket", "keyboard", "mug", "rug", "sneakers", "tent")
OUTPUT = TEST_DATA_DIR / "generated_orders.csv"


def generate_rows(count=ORDER_COUNT, seed=SEED):
    fake = Faker()
    fake.seed_instance(seed)
    rng = random.Random(seed)
    return [_row(number, fake, rng) for number in range(1, count + 1)]


def _row(number, fake, rng):
    items = [
        {
            "name": f"{fake.color_name()} {rng.choice(PRODUCTS)}",
            "price": round(rng.uniform(0.5, 300), 2),
            "quantity": rng.randint(1, 5),
            "weight": round(rng.uniform(0, 20), 2),
        }
        for _ in range(rng.randint(1, 4))
    ]
    customer_type = rng.choice(("new", "regular"))
    discount_code = rng.choice(CODES)
    distance_km = round(rng.uniform(0, 800), 1)
    is_express = rng.random() < 0.3

    order = Order(items, customer_type, ORDER_DATE)
    if discount_code != "NONE":
        order.apply_discount(discount_code)
    order.set_shipping(distance_km, is_express)
    totals = order.calculate_total()

    return {
        "test_name": f"generated_order_{number:03d}",
        "category": "generated",
        "items": json.dumps(items).replace('"', "'"),
        "customer_type": customer_type,
        "discount_code": discount_code,
        "distance_km": distance_km,
        "is_express": "true" if is_express else "false",
        "order_date": ORDER_DATE.isoformat(),
        **{f"expected_{name}": f"{amount:.2f}" for name, amount in totals.items()},
        "expected_error": "",
    }


def main():
    rows = generate_rows()
    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=ORDER_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} orders to {OUTPUT.relative_to(TEST_DATA_DIR.parent)}")


if __name__ == "__main__":
    main()
