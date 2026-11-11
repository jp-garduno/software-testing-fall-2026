"""Rutas e importacion compartidas por toda la suite.

pytest.ini ya pone la raiz y src/ en pythonpath. Este archivo repite el
ajuste con sys.path para que la suite tambien corra en un runner cuyo pytest
no soporte esa opcion, y centraliza la carga de los archivos de datos.
"""

import csv
import json
import os
import sys

import pytest

HW_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(HW_ROOT, "src")
DATA_DIR = os.path.join(HW_ROOT, "test_data")

for ruta in (SRC_DIR, HW_ROOT):
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

# Tiene que ir despues de ajustar sys.path, por eso la excepcion.
from order_calculator import Order  # noqa: E402  pylint: disable=wrong-import-position


def ruta_de_datos(nombre):
    """Ruta absoluta a un archivo de test_data/, sin depender del cwd."""
    return os.path.join(DATA_DIR, nombre)


def cargar_csv(nombre):
    """Lee un CSV de test_data/ como lista de diccionarios."""
    with open(ruta_de_datos(nombre), newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def cargar_json(nombre):
    """Lee un JSON de test_data/."""
    with open(ruta_de_datos(nombre), encoding="utf-8") as archivo:
        return json.load(archivo)


def casos_de_pedido():
    """Filas de order_calculations.csv con los tipos ya convertidos."""
    casos = []
    for fila in cargar_csv("order_calculations.csv"):
        casos.append(
            {
                "test_name": fila["test_name"],
                "category": fila["category"],
                "items": json.loads(fila["items"]),
                "customer_type": fila["customer_type"],
                "discount_code": fila["discount_code"],
                "distance_km": float(fila["distance_km"]),
                "is_express": fila["is_express"] == "true",
                "expected": {
                    clave: float(fila[f"expected_{clave}"])
                    for clave in ("subtotal", "discount", "tax", "shipping", "total")
                }
                if not fila["expected_error"]
                else None,
                "expected_error": fila["expected_error"],
            }
        )
    return casos


def construir_pedido(caso):
    """Arma el Order de un caso y le aplica descuento y envio."""
    pedido = Order(caso["items"], caso["customer_type"])
    if caso["discount_code"] != "NONE":
        pedido.apply_discount(caso["discount_code"])
    pedido.set_shipping(caso["distance_km"], caso["is_express"])
    return pedido


@pytest.fixture(scope="session")
def casos_cliente():
    """Casos de customer_validation.json."""
    return cargar_json("customer_validation.json")["test_cases"]


@pytest.fixture(scope="session")
def flujos():
    """Flujos de order_workflows.json."""
    return cargar_json("order_workflows.json")["workflows"]
