"""Pruebas del generador de datos de regresion (Bonus, opcion A).

Lo que se prueba del generador es que produzca pedidos validos, que sea
reproducible y que el archivo que escribe se pueda volver a leer. Los montos
no se verifican aqui: salen del propio calculador, asi que afirmarlos seria
comparar el codigo consigo mismo. Esa verificacion vive en
test_order_calculator.py, contra valores escritos a mano.
"""

import csv
import json

import pytest

from data_generator import ENCABEZADO, escribir_csv, generar_pedidos, main
from order_calculator import Order

PEDIDOS = generar_pedidos(100)


class TestGeneracion:
    """Cantidad, forma y validez de lo generado."""

    def test_genera_los_cien_pedidos_que_pide_el_enunciado(self):
        assert len(PEDIDOS) == 100

    def test_los_nombres_no_se_repiten(self):
        nombres = [pedido["test_name"] for pedido in PEDIDOS]
        assert len(set(nombres)) == len(nombres)

    def test_cada_pedido_es_aceptado_por_el_calculador(self):
        """Ningun pedido generado puede hacer fallar al constructor."""
        for pedido in PEDIDOS:
            Order(pedido["items"], pedido["customer_type"])

    def test_cada_pedido_tiene_al_menos_un_articulo(self):
        assert all(pedido["items"] for pedido in PEDIDOS)

    def test_los_articulos_traen_los_cuatro_campos(self):
        for pedido in PEDIDOS:
            for item in pedido["items"]:
                assert set(item) == {"name", "price", "quantity", "weight"}

    def test_no_genera_valores_negativos(self):
        for pedido in PEDIDOS:
            assert pedido["distance_km"] >= 0
            for item in pedido["items"]:
                assert item["price"] >= 0 and item["quantity"] >= 0 and item["weight"] >= 0

    def test_el_desglose_viene_completo(self):
        for pedido in PEDIDOS:
            assert set(pedido["expected"]) == {"subtotal", "discount", "tax", "shipping", "total"}

    def test_la_variedad_cubre_descuentos_y_express(self):
        """Un generador que siempre produce lo mismo no sirve de regresion."""
        codigos = {pedido["discount_code"] for pedido in PEDIDOS}
        assert len(codigos) >= 4
        assert {pedido["is_express"] for pedido in PEDIDOS} == {True, False}
        assert {pedido["customer_type"] for pedido in PEDIDOS} == {"regular", "new"}


class TestReproducibilidad:
    """La misma semilla tiene que dar el mismo archivo."""

    def test_la_misma_semilla_da_lo_mismo(self):
        assert generar_pedidos(10, semilla=7) == generar_pedidos(10, semilla=7)

    def test_semillas_distintas_dan_cosas_distintas(self):
        assert generar_pedidos(10, semilla=7) != generar_pedidos(10, semilla=8)

    @pytest.mark.parametrize("cantidad", [0, -1, 1.5, "cien", None])
    def test_cantidad_invalida(self, cantidad):
        with pytest.raises(ValueError, match="cantidad debe ser un entero positivo"):
            generar_pedidos(cantidad)


class TestArchivo:
    """El CSV escrito tiene que poder releerse."""

    def test_el_encabezado_y_las_filas_cuadran(self, tmp_path):
        ruta = escribir_csv(generar_pedidos(5), str(tmp_path / "gen.csv"))

        with open(ruta, newline="", encoding="utf-8") as archivo:
            filas = list(csv.DictReader(archivo))

        assert len(filas) == 5
        assert tuple(filas[0]) == ENCABEZADO

    def test_los_items_vuelven_a_leerse_como_json(self, tmp_path):
        ruta = escribir_csv(generar_pedidos(5), str(tmp_path / "gen.csv"))

        with open(ruta, newline="", encoding="utf-8") as archivo:
            for fila in csv.DictReader(archivo):
                assert isinstance(json.loads(fila["items"]), list)

    def test_los_montos_quedan_con_dos_decimales(self, tmp_path):
        ruta = escribir_csv(generar_pedidos(5), str(tmp_path / "gen.csv"))

        with open(ruta, newline="", encoding="utf-8") as archivo:
            for fila in csv.DictReader(archivo):
                for columna in ("expected_subtotal", "expected_total"):
                    assert fila[columna].split(".")[1] != "" and len(fila[columna].split(".")[1]) == 2


def test_main_escribe_el_archivo(tmp_path):
    """main() es el punto de entrada que se corre a mano para regenerar."""
    ruta = main(str(tmp_path / "regresion.csv"), cantidad=3)

    with open(ruta, newline="", encoding="utf-8") as archivo:
        assert len(list(csv.DictReader(archivo))) == 3
