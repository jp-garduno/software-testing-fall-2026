"""
Data Generator Module (Bonus Option A).

Generates synthetic e-commerce orders for regression and performance testing,
computing their expected subtotal, discount, tax, shipping, and total.
"""

import csv
import json
import random
from typing import List, Dict
from src.order_calculator import Order

SAMPLE_ITEMS = [
    {"name": "Wireless Mouse", "price": 25.00, "weight": 0.20},
    {"name": "Mechanical Keyboard", "price": 85.00, "weight": 1.10},
    {"name": "USB-C Hub", "price": 35.00, "weight": 0.15},
    {"name": "Gaming Headset", "price": 60.00, "weight": 0.45},
    {"name": "Desk Mat", "price": 20.00, "weight": 0.30},
    {"name": "Laptop Stand", "price": 45.00, "weight": 0.80},
    {"name": "Webcam 1080p", "price": 55.00, "weight": 0.25},
    {"name": "Monitor Arm", "price": 70.00, "weight": 2.50},
    {"name": "LED Desk Lamp", "price": 30.00, "weight": 0.90},
    {"name": "Bluetooth Speaker", "price": 40.00, "weight": 0.60},
]

DISCOUNT_CODES = ["NONE", "SAVE10", "SAVE20", "FREESHIP", "NEWUSER"]


def generate_single_order(index: int, seed: int = None) -> Dict:
    """Generate a single valid order with calculated expected outcomes."""
    if seed is not None:
        random.seed(seed + index)

    num_items = random.randint(1, 3)
    chosen_samples = random.sample(SAMPLE_ITEMS, num_items)
    items = []
    for s in chosen_samples:
        items.append({
            "name": s["name"],
            "price": s["price"],
            "quantity": random.randint(1, 3),
            "weight": s["weight"],
        })

    customer_type = random.choice(["regular", "new"])
    discount_code = random.choice(DISCOUNT_CODES)
    distance_km = float(random.randint(0, 150))
    is_express = random.choice([True, False])

    order = Order(items=items, customer_type=customer_type)
    if discount_code != "NONE":
        order.apply_discount(discount_code)
    order.set_shipping(distance_km=distance_km, is_express=is_express)

    breakdown = order.calculate_total()

    return {
        "test_name": f"generated_order_{index:03d}",
        "items": json.dumps(items),
        "customer_type": customer_type,
        "discount_code": order.discount_code if order.discount_code else "NONE",
        "distance_km": distance_km,
        "is_express": str(is_express).lower(),
        "expected_subtotal": f"{breakdown['subtotal']:.2f}",
        "expected_discount": f"{breakdown['discount']:.2f}",
        "expected_tax": f"{breakdown['tax']:.2f}",
        "expected_shipping": f"{breakdown['shipping']:.2f}",
        "expected_total": f"{breakdown['total']:.2f}",
    }


def generate_orders_to_csv(filepath: str, count: int = 100, seed: int = 42) -> List[Dict]:
    """
    Generate multiple synthetic orders and write them to a CSV file.
    """
    records = []
    for i in range(1, count + 1):
        record = generate_single_order(i, seed=seed)
        records.append(record)

    fieldnames = [
        "test_name", "items", "customer_type", "discount_code",
        "distance_km", "is_express", "expected_subtotal", "expected_discount",
        "expected_tax", "expected_shipping", "expected_total"
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    return records


if __name__ == "__main__":
    generate_orders_to_csv("test_data/generated_orders.csv", 100)
    print("Generated 100 orders successfully.")

