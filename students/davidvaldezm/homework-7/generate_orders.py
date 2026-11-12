"""Generate reproducible order regression data using Faker and an integer-cent oracle."""

import csv
import json
import random
from pathlib import Path

from faker import Faker

OUTPUT = Path(__file__).resolve().parent / "test_data" / "generated_orders.csv"
HEADER = (
    "test_name",
    "items",
    "customer_type",
    "discount_code",
    "distance_km",
    "is_express",
    "discount_applied",
    "expected_error",
    "expected_subtotal",
    "expected_discount",
    "expected_tax",
    "expected_shipping",
    "expected_total",
)
SEED = 731


def _half_up(numerator, denominator):
    return (2 * numerator + denominator) // (2 * denominator)


def _dollars(cents):
    return f"{cents // 100}.{cents % 100:02d}"


def _basket(rng, fake):
    items = []
    subtotal = 0
    weight_charge = 0
    for _ in range(rng.randint(1, 5)):
        price = rng.randint(100, 12000)
        quantity = rng.randint(1, 6)
        weight = rng.randint(1, 100)  # Tenths of a kilogram.
        items.append(
            {
                "name": f"{fake.color_name()} {rng.choice(('Mug', 'Notebook', 'Bag', 'Lamp'))}",
                "price": price / 100,
                "quantity": quantity,
                "weight": weight / 10,
            }
        )
        subtotal += price * quantity
        weight_charge += 5 * weight * quantity
    return items, subtotal, weight_charge


def _case(index, rng, fake):
    customer = rng.choice(("new", "regular"))
    code = ("NONE", "SAVE10", "SAVE20", "NEWUSER", "FREESHIP")[index % 5]
    distance = rng.randint(0, 2500)  # Tenths of a kilometer.
    express = rng.choice((True, False))
    items, subtotal, shipping = _basket(rng, fake)
    shipping += distance  # One cent per tenth of a kilometer.
    rate = 0
    applied = False
    if code == "SAVE10" and subtotal > 5000:
        rate, applied = 10, True
    elif code == "SAVE20" and subtotal > 10000:
        rate, applied = 20, True
    elif code == "NEWUSER" and customer == "new":
        rate, applied = 15, True
    elif code == "FREESHIP":
        shipping, applied = 0, True
    if express:
        shipping = _half_up(3 * shipping, 2)
    discount = _half_up(subtotal * rate, 100)
    tax = _half_up((subtotal - discount) * 8, 100)
    total = subtotal - discount + tax + shipping
    return (
        f"generated_order_{index + 1:03d}",
        json.dumps(items, separators=(",", ":")),
        customer,
        code,
        distance / 10,
        str(express).lower(),
        "" if code == "NONE" else str(applied).lower(),
        "",
        *map(_dollars, (subtotal, discount, tax, shipping, total)),
    )


def generate():
    """Write 100 cases without importing the production calculator."""
    rng = random.Random(SEED)
    fake = Faker("en_US")
    fake.seed_instance(SEED)
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(HEADER)
        writer.writerows(_case(index, rng, fake) for index in range(100))


if __name__ == "__main__":
    generate()
