"""Bonus Option A: generate valid random orders as a regression CSV.

Usage:  python tools/generate_orders.py [count] [output.csv]

Product names come from Faker; numbers from a seeded RNG so the file is
reproducible. Expected values are computed here with an independent Decimal
implementation of the business rules (not by importing ``order_calculator``),
so the generated file is a real cross-check and not a tautology.
"""
import csv
import json
import random
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from faker import Faker

SEED = 42
HEADER = ["test_name", "items", "customer_type", "discount_code", "distance_km",
          "is_express", "expected_subtotal", "expected_discount", "expected_tax",
          "expected_shipping", "expected_total", "expected_error"]
PCT = {"SAVE10": ("50", "0.10"), "SAVE20": ("100", "0.20"),
       "FREESHIP": ("0", "0"), "NEWUSER": ("0", "0.15")}


def cents(value):
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def expected_for(items, customer_type, code, distance, express):
    """Return (code_actually_applied, subtotal, discount, tax, shipping, total)."""
    subtotal = cents(sum((Decimal(str(i["price"])) * i["quantity"] for i in items), Decimal(0)))
    applied = None
    if code:
        minimum, _ = PCT[code]
        if subtotal >= Decimal(minimum) and not (code == "NEWUSER" and customer_type != "new"):
            applied = code
    discount = cents(subtotal * Decimal(PCT[applied][1])) if applied else Decimal("0.00")
    tax = cents((subtotal - discount) * Decimal("0.08"))
    if applied == "FREESHIP":
        shipping = Decimal("0.00")
    else:
        weight = sum((Decimal(str(i["weight"])) * i["quantity"] for i in items), Decimal(0))
        base = weight * Decimal("0.5") + Decimal(str(distance)) * Decimal("0.1")
        shipping = cents(base * (Decimal("1.5") if express else 1))
    return applied, subtotal, discount, tax, shipping, subtotal - discount + tax + shipping


def generate(count=100):
    rng, fake = random.Random(SEED), Faker()
    Faker.seed(SEED)
    rows = []
    for number in range(1, count + 1):
        items = [{"name": fake.word().capitalize(),
                  "price": round(rng.uniform(1, 250), 2),
                  "quantity": rng.randint(1, 6),
                  "weight": round(rng.uniform(0.1, 12), 1)}
                 for _ in range(rng.randint(1, 5))]
        customer_type = rng.choice(["new", "regular"])
        code = rng.choice([None, "SAVE10", "SAVE20", "FREESHIP", "NEWUSER"])
        distance = rng.choice([0, 5, 12.5, 40, 150, 800])
        express = rng.random() < 0.3
        # The CSV records the code that was requested; the expected values
        # reflect whether it is actually accepted for this order.
        _, sub, disc, tax, ship, total = expected_for(items, customer_type, code, distance, express)
        rows.append([f"generated_order_{number:03d}", json.dumps(items, separators=(",", ":")),
                     customer_type, code or "NONE", distance, str(express).lower(),
                     f"{sub:.2f}", f"{disc:.2f}", f"{tax:.2f}", f"{ship:.2f}", f"{total:.2f}", ""])
    return rows


def main(argv):
    count = int(argv[1]) if len(argv) > 1 else 100
    default = Path(__file__).resolve().parent.parent / "test_data" / "generated_orders.csv"
    out = Path(argv[2]) if len(argv) > 2 else default
    with open(out, "w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(HEADER)
        writer.writerows(generate(count))
    print(f"Wrote {count} orders to {out}")


if __name__ == "__main__":
    main(sys.argv)
