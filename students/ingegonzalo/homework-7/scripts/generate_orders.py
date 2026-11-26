"""Genera 100 ordenes validas con Faker para pruebas de regresion.

Los valores esperados se calculan con la implementacion actual, asi que este
CSV detecta CAMBIOS de comportamiento (regresion), no errores de la logica original.
"""
import csv
import json
import random
import sys
from pathlib import Path

from faker import Faker

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from src.order_calculator import Order  # noqa: E402

fake = Faker()
Faker.seed(42)
random.seed(42)

COLUMNS = ["test_name", "items", "customer_type", "discount_code", "distance_km", "is_express",
           "expected_subtotal", "expected_discount", "expected_tax", "expected_shipping", "expected_total"]
CODES = ["NONE", "SAVE10", "SAVE20", "FREESHIP", "NEWUSER"]


def build_row(index: int) -> dict:
    items = [
        {"name": fake.word().capitalize(), "price": round(random.uniform(1, 200), 2),
         "quantity": random.randint(1, 5), "weight": round(random.uniform(0.1, 10), 1)}
        for _ in range(random.randint(1, 4))
    ]
    customer_type = random.choice(["new", "regular"])
    code = random.choice(CODES)
    distance = random.randint(0, 500)
    express = random.choice([True, False])

    order = Order(items, customer_type)
    if code != "NONE":
        order.apply_discount(code)
    order.set_shipping(distance, express)
    result = order.calculate_total()

    return {
        "test_name": f"generated_order_{index:03d}",
        "items": json.dumps(items, separators=(",", ":")).replace('"', "'"),
        "customer_type": customer_type,
        "discount_code": code,
        "distance_km": distance,
        "is_express": str(express).lower(),
        "expected_subtotal": f"{result['subtotal']:.2f}",
        "expected_discount": f"{result['discount']:.2f}",
        "expected_tax": f"{result['tax']:.2f}",
        "expected_shipping": f"{result['shipping']:.2f}",
        "expected_total": f"{result['total']:.2f}",
    }


if __name__ == "__main__":
    out = ROOT / "test_data" / "generated_orders.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(build_row(i) for i in range(1, 101))
    print(f"100 ordenes escritas en {out}")