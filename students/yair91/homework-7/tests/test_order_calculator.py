"""Pruebas del calculador de pedidos, guiadas por order_calculations.csv.

Una fila del CSV es un caso completo: entradas, los cinco montos esperados y,
cuando aplica, el error que debe lanzarse. Agregar un caso es agregar una
linea al CSV, sin tocar este archivo.
"""

import pytest

from conftest import casos_de_pedido, construir_pedido
from order_calculator import Order

CASOS = casos_de_pedido()
CENTAVO = 0.005


@pytest.mark.parametrize("caso", CASOS, ids=lambda caso: caso["test_name"])
def test_calculo_completo_del_pedido(caso):
    """Verifica los cinco montos, o el error, de cada fila del CSV."""
    if caso["expected_error"]:
        with pytest.raises(ValueError) as error:
            construir_pedido(caso)
        assert str(error.value) == caso["expected_error"]
        return

    desglose = construir_pedido(caso).calculate_total()

    for clave, esperado in caso["expected"].items():
        assert desglose[clave] == pytest.approx(esperado, abs=CENTAVO), f"{clave} en {caso['test_name']}"


@pytest.mark.parametrize("caso", [c for c in CASOS if not c["expected_error"]], ids=lambda c: c["test_name"])
def test_el_total_es_la_suma_de_sus_partes(caso):
    """subtotal - descuento + impuesto + envio tiene que dar el total."""
    d = construir_pedido(caso).calculate_total()
    suma = d["subtotal"] - d["discount"] + d["tax"] + d["shipping"]

    assert d["total"] == pytest.approx(suma, abs=CENTAVO)


class TestCoberturaDelCsv:
    """El CSV tiene que seguir cumpliendo lo que pide el enunciado."""

    def test_minimo_de_casos(self):
        assert len(CASOS) >= 25

    @pytest.mark.parametrize(
        "categoria,minimo",
        [("simple", 3), ("discount", 5), ("tax", 4), ("shipping", 6), ("complex", 7)],
    )
    def test_minimo_por_categoria(self, categoria, minimo):
        assert len([c for c in CASOS if c["category"] == categoria]) >= minimo

    def test_hay_casos_de_error(self):
        assert any(c["expected_error"] for c in CASOS)


class TestReglasDeDescuento:
    """Comportamiento de apply_discount que el CSV no expresa como monto."""

    def test_codigo_desconocido_se_rechaza(self):
        pedido = Order([{"name": "X", "price": 100.0, "quantity": 1, "weight": 0.0}])
        assert pedido.apply_discount("NOPE") is False
        assert pedido.discount_code is None

    def test_newuser_solo_para_clientes_nuevos(self):
        nuevo = Order([{"name": "X", "price": 10.0, "quantity": 1, "weight": 0.0}], "new")
        regular = Order([{"name": "X", "price": 10.0, "quantity": 1, "weight": 0.0}], "regular")

        assert nuevo.apply_discount("NEWUSER") is True
        assert regular.apply_discount("NEWUSER") is False

    def test_un_codigo_rechazado_no_pisa_al_anterior(self):
        pedido = Order([{"name": "X", "price": 100.0, "quantity": 1, "weight": 0.0}])
        pedido.apply_discount("SAVE20")

        assert pedido.apply_discount("NOPE") is False
        assert pedido.discount_code == "SAVE20"

    def test_freeship_no_descuenta_del_precio(self):
        pedido = Order([{"name": "X", "price": 100.0, "quantity": 1, "weight": 5.0}])
        pedido.apply_discount("FREESHIP")
        pedido.set_shipping(100)

        assert pedido.calculate_discount() == 0.0
        assert pedido.calculate_shipping() == 0.0


class TestEntradasInvalidas:
    """Lo que el constructor y set_shipping tienen que rechazar."""

    @pytest.mark.parametrize(
        "items,mensaje",
        [
            ("no soy lista", "items must be a list"),
            ([["no", "soy", "dict"]], "each item must be an object"),
            ([{"price": 1.0, "quantity": 1, "weight": 1.0}], "item is missing name"),
            ([{"name": "", "price": 1.0, "quantity": 1, "weight": 1.0}], "item name must be a non-empty string"),
            ([{"name": "X", "price": "1.0", "quantity": 1, "weight": 1.0}], "price must be a number"),
            ([{"name": "X", "price": float("nan"), "quantity": 1, "weight": 1.0}], "price must be a finite number"),
            ([{"name": "X", "price": float("inf"), "quantity": 1, "weight": 1.0}], "price must be a finite number"),
            ([{"name": "X", "price": 1.0, "quantity": 1.5, "weight": 1.0}], "quantity must be a whole number"),
            ([{"name": "X", "price": 1.0, "quantity": True, "weight": 1.0}], "quantity must be a whole number"),
            ([{"name": "X", "price": 1.0, "quantity": 1, "weight": -1.0}], "weight must not be negative"),
        ],
    )
    def test_items_invalidos(self, items, mensaje):
        with pytest.raises(ValueError, match=mensaje):
            Order(items)

    def test_tipo_de_cliente_invalido(self):
        with pytest.raises(ValueError, match="customer_type must be new or regular"):
            Order([], "vip")

    def test_express_debe_ser_booleano(self):
        with pytest.raises(ValueError, match="is_express must be a boolean"):
            Order([]).set_shipping(10, "si")

    def test_distancia_no_numerica(self):
        with pytest.raises(ValueError, match="distance_km must be a number"):
            Order([]).set_shipping("diez")
