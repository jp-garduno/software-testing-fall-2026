"""Pruebas de integracion de extremo a extremo, guiadas por order_workflows.json.

Cada flujo valida al cliente, intenta el descuento, fija el envio y calcula el
total, y compara el desenlace completo contra el archivo.
"""

import pytest

from conftest import cargar_json
from customer_validator import validate_customer
from order_calculator import Order

FLUJOS = cargar_json("order_workflows.json")["workflows"]
CENTAVO = 0.005


def ejecutar(flujo):
    """Corre el flujo completo y devuelve el desenlace observado."""
    cliente_valido, _ = validate_customer(flujo["customer"])
    pedido = Order(flujo["items"], flujo["customer_type"])

    descuento_aplicado = False
    distancia, express = 0.0, False
    for paso in flujo["steps"]:
        if paso["action"] == "apply_discount":
            descuento_aplicado = pedido.apply_discount(paso["code"])
        elif paso["action"] == "set_shipping":
            distancia, express = paso["distance_km"], paso["is_express"]
            pedido.set_shipping(distancia, express)

    return {
        "customer_valid": cliente_valido,
        "discount_applied": descuento_aplicado,
        "order": pedido.calculate_total(),
        "outcome": "confirmed" if cliente_valido else "rejected_customer",
    }


@pytest.mark.parametrize("flujo", FLUJOS, ids=lambda flujo: flujo["workflow_name"])
def test_flujo_completo(flujo):
    """Cliente, descuento, envio y total de cada flujo del archivo."""
    resultado = ejecutar(flujo)

    assert resultado["customer_valid"] == flujo["expected_customer_valid"], flujo["description"]
    assert resultado["discount_applied"] == flujo["expected_discount_applied"], flujo["description"]
    assert resultado["outcome"] == flujo["expected_outcome"], flujo["description"]

    for clave, esperado in flujo["expected_order"].items():
        assert resultado["order"][clave] == pytest.approx(esperado, abs=CENTAVO), f"{clave} en {flujo['workflow_name']}"


class TestCoberturaDeLosFlujos:
    """El archivo tiene que cubrir algo mas que el camino feliz."""

    def test_minimo_de_flujos(self):
        assert len(FLUJOS) >= 3

    def test_hay_un_flujo_que_se_confirma(self):
        assert any(f["expected_outcome"] == "confirmed" for f in FLUJOS)

    def test_hay_un_flujo_que_rechaza_al_cliente(self):
        assert any(f["expected_outcome"] == "rejected_customer" for f in FLUJOS)

    def test_hay_un_flujo_donde_el_descuento_se_rechaza(self):
        assert any(f["expected_discount_applied"] is False for f in FLUJOS)


def test_un_pedido_rechazado_no_cambia_de_monto():
    """Que el cliente no pase no altera los montos del pedido."""
    rechazados = [f for f in FLUJOS if f["expected_outcome"] == "rejected_customer"]
    assert rechazados, "hace falta un flujo con cliente rechazado"

    for flujo in rechazados:
        resultado = ejecutar(flujo)
        assert resultado["order"]["total"] == pytest.approx(flujo["expected_order"]["total"], abs=CENTAVO)
