"""
Pruebas de integracion data-driven.

Cada workflow de test_data/order_workflows.json es una secuencia de pasos
que usa customer_validator y order_calculator juntos, de punta a punta:

    validate_customer -> create_order -> apply_discount -> set_shipping
    -> calculate_total -> process_payment

Los pasos comparten un "contexto" (el cliente validado y la orden creada),
igual que en un flujo real de compra.
"""

import json
import os
import sys
from datetime import date

import pytest

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from customer_validator import validate_customer  # noqa: E402
from order_calculator import Order  # noqa: E402

DATA_FILE = os.path.join(BASE_DIR, "test_data", "order_workflows.json")

# Fecha fija para que la expiracion de tarjetas no cambie con el tiempo
REFERENCE_DATE = date(2026, 11, 10)


# ---------------------------------------------------------------------------
# Acciones: cada una recibe el contexto y los datos del paso, y regresa un dict
# ---------------------------------------------------------------------------

def action_validate_customer(ctx, data):
    result = validate_customer(data["customer"], today=REFERENCE_DATE)
    ctx["customer_valid"] = result["is_valid"]
    return {"valid": result["is_valid"], "errors": result["errors"]}


def action_create_order(ctx, data):
    try:
        ctx["order"] = Order(data["items"], data.get("customer_type", "regular"))
        return {"status": "created"}
    except ValueError as exc:
        ctx["order"] = None
        return {"status": "error", "message": str(exc)}


def action_apply_discount(ctx, data):
    return {"applied": ctx["order"].apply_discount(data["code"])}


def action_set_shipping(ctx, data):
    ctx["order"].set_shipping(data["distance_km"], data.get("is_express", False))
    return {"status": "set"}


def action_calculate_total(ctx, data):
    ctx["totals"] = ctx["order"].calculate_total()
    return ctx["totals"]


def action_process_payment(ctx, data):
    """Pago simulado: requiere cliente valido, orden creada y total > 0."""
    if ctx.get("order") is None:
        return {"status": "failed", "reason": "No order"}
    if not ctx.get("customer_valid"):
        return {"status": "failed", "reason": "Invalid customer"}

    total = ctx["order"].calculate_total()["total"]
    if total <= 0:
        return {"status": "failed", "reason": "Invalid order total"}
    return {"status": "success", "amount": total}


ACTIONS = {
    "validate_customer": action_validate_customer,
    "create_order": action_create_order,
    "apply_discount": action_apply_discount,
    "set_shipping": action_set_shipping,
    "calculate_total": action_calculate_total,
    "process_payment": action_process_payment,
}


# ---------------------------------------------------------------------------
# Carga de datos y test
# ---------------------------------------------------------------------------

def load_workflows():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        workflows = json.load(f)["workflows"]
    return [pytest.param(wf, id=wf["name"]) for wf in workflows]


def assert_matches(actual, expected, label):
    """Compara solo las llaves que el JSON define como esperadas."""
    for key, exp_value in expected.items():
        assert key in actual, f"{label}: falta '{key}' en el resultado"
        if isinstance(exp_value, float):
            assert actual[key] == pytest.approx(exp_value, abs=0.01), f"{label}: {key}"
        else:
            assert actual[key] == exp_value, f"{label}: {key}"


@pytest.mark.parametrize("workflow", load_workflows())
def test_workflow(workflow):
    """Ejecuta todos los pasos del workflow en orden y verifica cada resultado."""
    ctx = {}
    for i, step in enumerate(workflow["steps"], start=1):
        label = f"{workflow['name']} paso {i} ({step['action']})"
        assert step["action"] in ACTIONS, f"{label}: accion desconocida"

        result = ACTIONS[step["action"]](ctx, step.get("data", {}))
        assert_matches(result, step.get("expected", {}), label)


def test_workflow_file_has_minimum_workflows():
    """El enunciado pide al menos 3 workflows completos."""
    assert len(load_workflows()) >= 3
