"""Generate realistic test data with Faker (Bonus option A).

``generate_orders`` builds random but valid orders and prices them with the
current ``Order`` implementation. Saved to CSV, they become a golden master:
the regression test re-prices every row and fails if a later change to the
calculator moves any amount. ``generate_customers`` builds customers that must
all pass validation, which cross-checks the validator against Faker's own
idea of a valid email, address and card.

Run ``python -m src.data_generator`` to rewrite test_data/generated_orders.csv.
"""

import csv
import random
from datetime import date
from pathlib import Path
from typing import Dict, List

from faker import Faker

from src.customer_validator import US_STATES
from src.data_validation import DATA_DIR, ORDER_COLUMNS
from src.order_calculator import Order

DISCOUNT_CHOICES = ("NONE", "SAVE10", "SAVE20", "FREESHIP", "NEWUSER", "EXPIRED99")
CARD_TYPES = ("visa16", "mastercard", "amex", "discover")


def _random_item(fake: Faker, rng: random.Random) -> Dict:
    return {
        "name": fake.word().capitalize(),
        "price": round(rng.uniform(0.5, 500), 2),
        "quantity": rng.randint(1, 5),
        "weight": round(rng.uniform(0, 15), 2),
    }


def _format_items(items: List[Dict]) -> str:
    # Same single-quoted style as the hand-written CSV.
    parts = [f"{{'name':'{i['name']}','price':{i['price']},'quantity':{i['quantity']},'weight':{i['weight']}}}"
             for i in items]
    return "[" + ",".join(parts) + "]"


def generate_orders(count: int = 100, seed: int = 2026) -> List[Dict[str, str]]:
    """Return ``count`` CSV rows (order_calculations.csv schema) with expected values."""
    fake = Faker("en_US")
    fake.seed_instance(seed)
    rng = random.Random(seed)
    rows = []
    for number in range(1, count + 1):
        items = [_random_item(fake, rng) for _ in range(rng.randint(1, 4))]
        customer_type = rng.choice(("new", "regular"))
        code = rng.choice(DISCOUNT_CHOICES)
        distance = rng.randint(0, 2000)
        is_express = rng.random() < 0.3
        order = Order(items, customer_type)
        if code != "NONE":
            order.apply_discount(code)
        order.set_shipping(distance, is_express)
        totals = order.calculate_total()
        rows.append({
            "test_name": f"generated_order_{number:03d}",
            "category": "generated",
            "items": _format_items(items),
            "customer_type": customer_type,
            "discount_code": code,
            "distance_km": str(distance),
            "is_express": "true" if is_express else "false",
            **{f"expected_{key}": f"{value:.2f}" for key, value in totals.items()},
            "expected_error": "",
        })
    return rows


def write_orders_csv(rows: List[Dict[str, str]], path: Path) -> None:
    """Write generated rows with the same header as order_calculations.csv."""
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ORDER_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _phone(rng: random.Random) -> str:
    # Area code and exchange start with 2-9, as the validator requires.
    return f"({rng.randint(2, 9)}{rng.randint(0, 99):02d}) {rng.randint(2, 9)}{rng.randint(0, 99):02d}-" \
           f"{rng.randint(0, 9999):04d}"


def generate_customers(count: int = 100, seed: int = 2026, today: date = date(2026, 6, 15)) -> List[Dict]:
    """Return ``count`` customers that are all valid on ``today``."""
    fake = Faker("en_US")
    fake.seed_instance(seed)
    rng = random.Random(seed)
    customers = []
    for _ in range(count):
        card_type = rng.choice(CARD_TYPES)
        customers.append({
            "email": fake.email(),
            "phone": _phone(rng),
            "billing_address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "state": rng.choice(sorted(US_STATES)),
                "zip": fake.zipcode(),
            },
            "credit_card": {
                "number": fake.credit_card_number(card_type=card_type),
                "expiration": f"{rng.randint(1, 12):02d}/{today.year + rng.randint(1, 6)}",
                "cvv": f"{rng.randint(0, 9999):04d}" if card_type == "amex" else f"{rng.randint(0, 999):03d}",
            },
        })
    return customers


if __name__ == "__main__":  # pragma: no cover
    write_orders_csv(generate_orders(), DATA_DIR / "generated_orders.csv")
    print(f"Wrote 100 orders to {DATA_DIR / 'generated_orders.csv'}")
