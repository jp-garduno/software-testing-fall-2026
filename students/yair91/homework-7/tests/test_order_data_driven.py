"""Version guiada por datos: los mismos diez escenarios, una sola prueba.

Es la otra mitad de la comparacion de la Parte 3. Los escenarios se eligen por
nombre desde order_calculations.csv, asi que agregar uno once es agregar su
nombre a la lista, no escribir otra funcion.
"""

import pytest

from conftest import casos_de_pedido, construir_pedido

CENTAVO = 0.005

ESCENARIOS = [
    "simple_single_item",
    "simple_two_products",
    "discount_save10_at_minimum",
    "discount_save10_below_minimum",
    "discount_save20_at_minimum",
    "discount_invalid_code",
    "discount_newuser_for_new_customer",
    "shipping_weight_and_distance",
    "shipping_express_multiplies",
    "shipping_freeship_waives_cost",
]

CASOS = [caso for caso in casos_de_pedido() if caso["test_name"] in ESCENARIOS]


def test_los_diez_escenarios_existen_en_el_csv():
    """Si alguien renombra una fila del CSV, esto avisa en vez de saltarsela."""
    assert sorted(caso["test_name"] for caso in CASOS) == sorted(ESCENARIOS)


@pytest.mark.parametrize("caso", CASOS, ids=lambda caso: caso["test_name"])
def test_desglose_del_pedido(caso):
    """Los cinco montos de cada escenario, leidos del CSV."""
    desglose = construir_pedido(caso).calculate_total()

    for clave, esperado in caso["expected"].items():
        assert desglose[clave] == pytest.approx(esperado, abs=CENTAVO), f"{clave} en {caso['test_name']}"
