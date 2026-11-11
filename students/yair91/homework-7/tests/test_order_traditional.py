"""Version tradicional: diez pruebas sin parametrizar, con los datos a mano.

Es la mitad de la comparacion de la Parte 3. Cubre exactamente los mismos
diez escenarios que test_order_data_driven.py, con las mismas afirmaciones,
para que el conteo de lineas compare lo mismo contra lo mismo.
"""

import pytest

from order_calculator import Order

CENTAVO = 0.005


def test_pedido_simple_de_un_articulo():
    """Un articulo, sin descuento ni envio."""
    pedido = Order([{"name": "Notebook", "price": 25.0, "quantity": 1, "weight": 0.0}], "regular")
    pedido.set_shipping(0, False)
    desglose = pedido.calculate_total()
    assert desglose["subtotal"] == pytest.approx(25.00, abs=CENTAVO)
    assert desglose["discount"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["tax"] == pytest.approx(2.00, abs=CENTAVO)
    assert desglose["shipping"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["total"] == pytest.approx(27.00, abs=CENTAVO)


def test_pedido_simple_de_dos_productos():
    """Dos productos distintos, sin descuento ni envio."""
    pedido = Order(
        [
            {"name": "Pen", "price": 5.0, "quantity": 3, "weight": 0.0},
            {"name": "Folder", "price": 10.0, "quantity": 2, "weight": 0.0},
        ],
        "regular",
    )
    pedido.set_shipping(0, False)
    desglose = pedido.calculate_total()
    assert desglose["subtotal"] == pytest.approx(35.00, abs=CENTAVO)
    assert desglose["discount"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["tax"] == pytest.approx(2.80, abs=CENTAVO)
    assert desglose["shipping"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["total"] == pytest.approx(37.80, abs=CENTAVO)


def test_save10_justo_en_el_minimo():
    """SAVE10 pide mas de 50; en 50 exactos se acepta."""
    pedido = Order([{"name": "Backpack", "price": 50.0, "quantity": 1, "weight": 0.0}], "regular")
    pedido.apply_discount("SAVE10")
    pedido.set_shipping(0, False)
    desglose = pedido.calculate_total()
    assert desglose["subtotal"] == pytest.approx(50.00, abs=CENTAVO)
    assert desglose["discount"] == pytest.approx(5.00, abs=CENTAVO)
    assert desglose["tax"] == pytest.approx(3.60, abs=CENTAVO)
    assert desglose["shipping"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["total"] == pytest.approx(48.60, abs=CENTAVO)


def test_save10_debajo_del_minimo():
    """Un centavo abajo del minimo y el codigo no aplica."""
    pedido = Order([{"name": "Backpack", "price": 49.99, "quantity": 1, "weight": 0.0}], "regular")
    pedido.apply_discount("SAVE10")
    pedido.set_shipping(0, False)
    desglose = pedido.calculate_total()
    assert desglose["subtotal"] == pytest.approx(49.99, abs=CENTAVO)
    assert desglose["discount"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["tax"] == pytest.approx(4.00, abs=CENTAVO)
    assert desglose["shipping"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["total"] == pytest.approx(53.99, abs=CENTAVO)


def test_save20_justo_en_el_minimo():
    """SAVE20 pide mas de 100; en 100 exactos se acepta."""
    pedido = Order([{"name": "Monitor", "price": 100.0, "quantity": 1, "weight": 0.0}], "regular")
    pedido.apply_discount("SAVE20")
    pedido.set_shipping(0, False)
    desglose = pedido.calculate_total()
    assert desglose["subtotal"] == pytest.approx(100.00, abs=CENTAVO)
    assert desglose["discount"] == pytest.approx(20.00, abs=CENTAVO)
    assert desglose["tax"] == pytest.approx(6.40, abs=CENTAVO)
    assert desglose["shipping"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["total"] == pytest.approx(86.40, abs=CENTAVO)


def test_codigo_invalido_no_descuenta():
    """Un codigo que no existe deja el pedido a precio completo."""
    pedido = Order([{"name": "Monitor", "price": 100.0, "quantity": 1, "weight": 0.0}], "regular")
    pedido.apply_discount("SAVE50")
    pedido.set_shipping(0, False)
    desglose = pedido.calculate_total()
    assert desglose["subtotal"] == pytest.approx(100.00, abs=CENTAVO)
    assert desglose["discount"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["tax"] == pytest.approx(8.00, abs=CENTAVO)
    assert desglose["shipping"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["total"] == pytest.approx(108.00, abs=CENTAVO)


def test_newuser_para_cliente_nuevo():
    """NEWUSER descuenta 15% cuando el cliente es nuevo."""
    pedido = Order([{"name": "Lamp", "price": 40.0, "quantity": 1, "weight": 0.0}], "new")
    pedido.apply_discount("NEWUSER")
    pedido.set_shipping(0, False)
    desglose = pedido.calculate_total()
    assert desglose["subtotal"] == pytest.approx(40.00, abs=CENTAVO)
    assert desglose["discount"] == pytest.approx(6.00, abs=CENTAVO)
    assert desglose["tax"] == pytest.approx(2.72, abs=CENTAVO)
    assert desglose["shipping"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["total"] == pytest.approx(36.72, abs=CENTAVO)


def test_envio_por_peso_y_distancia():
    """El envio suma peso por 0.50 y distancia por 0.10."""
    pedido = Order([{"name": "Box", "price": 10.0, "quantity": 1, "weight": 3.0}], "regular")
    pedido.set_shipping(40, False)
    desglose = pedido.calculate_total()
    assert desglose["subtotal"] == pytest.approx(10.00, abs=CENTAVO)
    assert desglose["discount"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["tax"] == pytest.approx(0.80, abs=CENTAVO)
    assert desglose["shipping"] == pytest.approx(5.50, abs=CENTAVO)
    assert desglose["total"] == pytest.approx(16.30, abs=CENTAVO)


def test_express_multiplica_el_envio():
    """El mismo pedido en express cuesta 1.5 veces el envio base."""
    pedido = Order([{"name": "Box", "price": 10.0, "quantity": 1, "weight": 3.0}], "regular")
    pedido.set_shipping(40, True)
    desglose = pedido.calculate_total()
    assert desglose["subtotal"] == pytest.approx(10.00, abs=CENTAVO)
    assert desglose["discount"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["tax"] == pytest.approx(0.80, abs=CENTAVO)
    assert desglose["shipping"] == pytest.approx(8.25, abs=CENTAVO)
    assert desglose["total"] == pytest.approx(19.05, abs=CENTAVO)


def test_freeship_anula_el_envio():
    """FREESHIP deja el envio en cero sin tocar el precio."""
    pedido = Order([{"name": "Heavy", "price": 10.0, "quantity": 1, "weight": 20.0}], "regular")
    pedido.apply_discount("FREESHIP")
    pedido.set_shipping(100, False)
    desglose = pedido.calculate_total()
    assert desglose["subtotal"] == pytest.approx(10.00, abs=CENTAVO)
    assert desglose["discount"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["tax"] == pytest.approx(0.80, abs=CENTAVO)
    assert desglose["shipping"] == pytest.approx(0.00, abs=CENTAVO)
    assert desglose["total"] == pytest.approx(10.80, abs=CENTAVO)
