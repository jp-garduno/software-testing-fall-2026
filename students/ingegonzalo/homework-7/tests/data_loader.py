"""Utilidades compartidas para cargar datos de prueba desde archivos externos."""
import csv
import json
from pathlib import Path

import pytest

from src.order_calculator import Order

# Ruta relativa al archivo, funciona sin importar desde donde se ejecute pytest
DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"


def parse_order_row(row: dict) -> dict:
    """Convierte una fila del CSV en un caso de prueba tipado."""
    code = row["discount_code"].strip()
    return {
        "name": row["test_name"],
        "items": json.loads(row["items"].replace("'", '"')),
        "customer_type": row["customer_type"].strip(),
        "discount_code": None if code == "NONE" else code,
        "distance": float(row["distance_km"]),
        "is_express": row["is_express"].strip().lower() == "true",
        "expected": {
            key: float(row[f"expected_{key}"])
            for key in ("subtotal", "discount", "tax", "shipping", "total")
        },
    }


def load_order_cases(names=None, filename="order_calculations.csv"):
    """Carga casos del CSV. Si `names` se indica, filtra por test_name."""
    cases = []
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if names is not None and row["test_name"] not in names:
                continue
            case = parse_order_row(row)
            cases.append(pytest.param(case, id=case["name"]))
    return cases


def run_order_case(case: dict) -> dict:
    """Ejecuta un caso contra Order y devuelve el desglose."""
    order = Order(case["items"], case["customer_type"])
    if case["discount_code"]:
        order.apply_discount(case["discount_code"])
    order.set_shipping(case["distance"], case["is_express"])
    return order.calculate_total()


def load_customer_cases():
    with open(DATA_DIR / "customer_validation.json", encoding="utf-8") as f:
        return [pytest.param(c, id=c["test_name"]) for c in json.load(f)]


def load_workflows():
    with open(DATA_DIR / "order_workflows.json", encoding="utf-8") as f:
        return [pytest.param(w, id=w["name"]) for w in json.load(f)["workflows"]]