"""
Tests data-driven para customer_validator.

Todos los casos viven en test_data/customer_validation.json.
Cada caso tiene: test_name, customer y expected {is_valid, errors}.
"""

import json
import os
import sys
from datetime import date

import pytest

# Permite importar los modulos de src/ sin archivos de configuracion extra
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from customer_validator import luhn_check, validate_customer  # noqa: E402

DATA_FILE = os.path.join(BASE_DIR, "test_data", "customer_validation.json")

# Fecha fija para que los resultados de expiracion no cambien con el tiempo
REFERENCE_DATE = date(2026, 11, 10)


def load_customer_test_data():
    """Carga los casos desde JSON y los convierte en parametros de pytest."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)
    return [
        pytest.param(case["customer"], case["expected"], id=case["test_name"])
        for case in cases
    ]


@pytest.mark.parametrize("customer,expected", load_customer_test_data())
def test_customer_validation(customer, expected):
    """Compara is_valid y la lista exacta de errores con lo esperado."""
    result = validate_customer(customer, today=REFERENCE_DATE)

    assert result["is_valid"] == expected["is_valid"]
    assert result["errors"] == expected["errors"]


def test_card_expiring_this_month_is_valid():
    """Una tarjeta que vence este mes todavia es valida."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        customer = json.load(f)[0]["customer"]
    customer["credit_card"]["expiration"] = "11/2026"
    assert validate_customer(customer, today=REFERENCE_DATE)["is_valid"] is True


@pytest.mark.parametrize("number,expected", [
    ("4532015112830366", True),
    ("4111111111111111", True),
    ("4532015112830367", False),
    ("12ab", False),
])
def test_luhn_check(number, expected):
    """Pruebas directas del algoritmo de Luhn."""
    assert luhn_check(number) is expected
