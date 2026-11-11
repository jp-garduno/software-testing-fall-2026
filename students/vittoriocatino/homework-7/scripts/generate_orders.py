"""Bonus A: generate 100 reproducible, synthetic Faker regression orders."""

import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from faker import Faker

FIELDS = [
    "test_name",
    "category",
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
    "expected_error",
]


def generate(destination, count=100, seed=2026):
    """Use independent no-discount arithmetic; never import production code."""
    fake = Faker("en_US")
    fake.seed_instance(seed)
    with Path(destination).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        for index in range(count):
            price = fake.random_int(1, 10000)
            quantity = fake.random_int(1, 10)
            weight = fake.random_int(0, 20)
            distance = fake.random_int(0, 1000)
            express = fake.boolean()
            subtotal = Decimal(price * quantity)
            tax = (subtotal * Decimal("0.08")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            shipping = Decimal(weight * quantity) / 2 + Decimal(distance) / 10
            if express:
                shipping *= Decimal("1.5")
            shipping = shipping.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            writer.writerow(
                dict(
                    zip(
                        FIELDS,
                        [
                            f"generated_{index:03}",
                            "generated",
                            json.dumps(
                                [
                                    {
                                        "name": fake.catch_phrase(),
                                        "price": price,
                                        "quantity": quantity,
                                        "weight": weight,
                                    }
                                ]
                            ),
                            "regular",
                            "NONE",
                            distance,
                            str(express).lower(),
                            subtotal,
                            0,
                            tax,
                            shipping,
                            subtotal + tax + shipping,
                            "",
                        ],
                    )
                )
            )


if __name__ == "__main__":
    generate(Path(__file__).resolve().parents[1] / "test_data/generated_orders.csv")
