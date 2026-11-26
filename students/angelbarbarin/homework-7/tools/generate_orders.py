"""Generate valid orders with Faker for regression testing (bonus option A).

    python tools/generate_orders.py                 # 100 orders -> test_data/generated_orders.csv
    python tools/generate_orders.py --count 500 --seed 7 --output other.csv

The expected amounts are NOT computed with src/order_calculator.py. They come from the small
oracle below, which uses exact fractions of a dollar, so the generated file can catch a
regression in the calculator instead of copying its answers. The fixed seed makes the file
reproducible: running the generator twice gives the same CSV.
"""

from __future__ import annotations

import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path

from faker import Faker

COLUMNS = (
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
)
CODES = ("NONE", "SAVE10", "SAVE20", "FREESHIP", "NEWUSER", "INVALID")
RULES = {  # code -> (minimum subtotal, percentage, required customer type)
    "SAVE10": (50, Fraction(10, 100), None),
    "SAVE20": (100, Fraction(20, 100), None),
    "FREESHIP": (0, Fraction(0), None),
    "NEWUSER": (0, Fraction(15, 100), "new"),
}


def round_cents(amount: Fraction) -> Fraction:
    """Round half up to whole cents."""
    cents = amount * 100
    whole = cents.numerator // cents.denominator
    if cents - whole >= Fraction(1, 2):
        whole += 1
    return Fraction(whole, 100)


def expected_amounts(items, customer_type, code, distance, express):
    """Independent implementation of the pricing rules (see README)."""
    subtotal = round_cents(sum(Fraction(str(i["price"])) * i["quantity"] for i in items))
    applied = None
    if code in RULES:
        minimum, _, required = RULES[code]
        if subtotal >= minimum and required in (None, customer_type):
            applied = code
    discount = round_cents(subtotal * RULES[applied][1]) if applied else Fraction(0)
    tax = round_cents((subtotal - discount) * Fraction(8, 100))
    if applied == "FREESHIP" or sum(i["quantity"] for i in items) == 0:
        shipping = Fraction(0)
    else:
        weight = sum(Fraction(str(i["weight"])) * i["quantity"] for i in items)
        shipping = 4 + weight / 2 + Fraction(str(distance)) / 10
        shipping = round_cents(shipping * Fraction(3, 2) if express else shipping)
    return subtotal, discount, tax, shipping, subtotal - discount + tax + shipping


def generate(count: int, seed: int):
    """Yield CSV rows for ``count`` random but valid orders."""
    fake = Faker("en_US")
    Faker.seed(seed)
    for number in range(1, count + 1):
        items = [
            {
                "name": fake.unique.catch_phrase()[:40],
                "price": float(fake.pydecimal(left_digits=3, right_digits=2, positive=True, max_value=500)),
                "quantity": fake.random_int(min=0, max=6),
                "weight": float(fake.pydecimal(left_digits=2, right_digits=2, positive=True, max_value=30)),
            }
            for _ in range(fake.random_int(min=1, max=5))
        ]
        customer_type = fake.random_element(("new", "regular"))
        code = fake.random_element(CODES)
        distance = fake.random_int(min=0, max=1500)
        express = fake.pybool()
        amounts = expected_amounts(items, customer_type, code, distance, express)
        yield [
            f"generated_order_{number:03d}",
            "generated",
            json.dumps(items, separators=(",", ":")),
            customer_type,
            code,
            distance,
            str(express).lower(),
            *(f"{float(value):.2f}" for value in amounts),
            "",
        ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument(
        "--output", type=Path, default=Path(__file__).resolve().parent.parent / "test_data" / "generated_orders.csv"
    )
    args = parser.parse_args()
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(COLUMNS)
        writer.writerows(generate(args.count, args.seed))
    print(f"Wrote {args.count} orders to {args.output}")


if __name__ == "__main__":
    main()
