"""
Tests data-driven para order_calculator.

Todos los datos viven en test_data/order_calculations.csv.
Las filas con "ERROR" en las columnas expected_* son entradas invalidas
(valores negativos, tipo de cliente invalido) que deben lanzar ValueError.
"""

import csv
import json
import os
import sys

import pytest

# Permite importar los modulos de src/ sin archivos de configuracion extra
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from order_calculator import Order  # noqa: E402

DATA_FILE = os.path.join(BASE_DIR, "test_data", "order_calculations.csv")


def parse_items(raw: str):
    """Convierte el texto de la columna 'items' (comillas simples) en lista de dicts."""
    return json.loads(raw.replace("'", '"'))


def load_rows():
    """Lee todas las filas del CSV."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_order_test_data():
    """Casos validos: filas con valores numericos esperados."""
    test_data = []
    for row in load_rows():
        if row["expected_total"] == "ERROR":
            continue
        test_data.append(
            pytest.param(
                row["test_name"],
                parse_items(row["items"]),
                row["customer_type"],
                row["discount_code"] if row["discount_code"] != "NONE" else None,
                float(row["distance_km"]),
                row["is_express"] == "true",
                float(row["expected_subtotal"]),
                float(row["expected_discount"]),
                float(row["expected_tax"]),
                float(row["expected_shipping"]),
                float(row["expected_total"]),
                id=row["test_name"],  # nombre legible en la salida de pytest
            )
        )
    return test_data


def load_invalid_test_data():
    """Casos invalidos: filas marcadas con ERROR."""
    return [
        pytest.param(
            parse_items(row["items"]),
            row["customer_type"],
            float(row["distance_km"]),
            id=row["test_name"],
        )
        for row in load_rows()
        if row["expected_total"] == "ERROR"
    ]


@pytest.mark.parametrize(
    "test_name,items,customer_type,discount_code,distance,is_express,"
    "exp_subtotal,exp_discount,exp_tax,exp_shipping,exp_total",
    load_order_test_data(),
)
def test_order_calculation(test_name, items, customer_type, discount_code,
                           distance, is_express, exp_subtotal, exp_discount,
                           exp_tax, exp_shipping, exp_total):
    """Verifica cada componente del total con los datos del CSV."""
    order = Order(items, customer_type)

    if discount_code:
        order.apply_discount(discount_code)

    order.set_shipping(distance, is_express)
    result = order.calculate_total()

    # abs=0.01 -> tolerancia de un centavo (rel no sirve cuando el esperado es 0)
    assert result["subtotal"] == pytest.approx(exp_subtotal, abs=0.01), f"{test_name}: Subtotal mismatch"
    assert result["discount"] == pytest.approx(exp_discount, abs=0.01), f"{test_name}: Discount mismatch"
    assert result["tax"] == pytest.approx(exp_tax, abs=0.01), f"{test_name}: Tax mismatch"
    assert result["shipping"] == pytest.approx(exp_shipping, abs=0.01), f"{test_name}: Shipping mismatch"
    assert result["total"] == pytest.approx(exp_total, abs=0.01), f"{test_name}: Total mismatch"


@pytest.mark.parametrize("items,customer_type,distance", load_invalid_test_data())
def test_invalid_inputs_raise(items, customer_type, distance):
    """Entradas negativas o invalidas deben lanzar ValueError."""
    with pytest.raises(ValueError):
        order = Order(items, customer_type)
        order.set_shipping(distance)


def test_apply_discount_return_values():
    """apply_discount regresa True/False segun la validez del codigo."""
    order = Order([{"name": "A", "price": 60, "quantity": 1, "weight": 0}])
    assert order.apply_discount("SAVE10") is True
    assert order.apply_discount("SAVE20") is False   # 60 < 100
    assert order.apply_discount("FAKE") is False
    assert order.discount_code == "SAVE10"           # el codigo invalido no reemplaza al valido
