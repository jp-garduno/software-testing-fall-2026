"""Pruebas del validador de datos de prueba (Bonus, opcion C).

Los archivos rotos se escriben en tmp_path en vez de commitearlos, para que el
directorio test_data/ solo contenga datos que la suite usa de verdad.
"""

import json

import pytest

from conftest import DATA_DIR
from data_validator import (
    DataValidationError,
    exigir_datos_validos,
    validar_csv_de_pedidos,
    validar_json_de_clientes,
    validar_todo,
)

ENCABEZADO = (
    "test_name,category,items,customer_type,discount_code,distance_km,is_express,"
    "expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total,expected_error"
)
FILA_BUENA = (
    'ok,simple,"[{""name"": ""X"", ""price"": 1.0, ""quantity"": 1, ""weight"": 0.0}]",'
    "regular,NONE,0,false,1.00,0.00,0.08,0.00,1.08,"
)


def escribir_csv(tmp_path, *filas):
    """Arma un CSV temporal con el encabezado bueno y las filas dadas."""
    ruta = tmp_path / "order_calculations.csv"
    ruta.write_text("\n".join((ENCABEZADO,) + filas) + "\n", encoding="utf-8")
    return str(ruta)


def escribir_json(tmp_path, contenido):
    """Arma un JSON temporal de clientes."""
    ruta = tmp_path / "customer_validation.json"
    ruta.write_text(json.dumps(contenido), encoding="utf-8")
    return str(ruta)


class TestLosDatosRealesEstanBien:
    """La razon de ser del modulo: avisar antes de correr la suite."""

    def test_el_csv_de_pedidos_no_tiene_problemas(self):
        assert not validar_csv_de_pedidos(f"{DATA_DIR}/order_calculations.csv")

    def test_el_json_de_clientes_no_tiene_problemas(self):
        assert not validar_json_de_clientes(f"{DATA_DIR}/customer_validation.json")

    def test_validar_todo_revisa_los_dos(self):
        hallazgos = validar_todo(DATA_DIR)
        assert set(hallazgos) == {"order_calculations.csv", "customer_validation.json"}
        assert all(not problemas for problemas in hallazgos.values())

    def test_exigir_datos_validos_no_lanza(self):
        exigir_datos_validos(DATA_DIR)


class TestProblemasEnElCsv:
    """Cada problema se reporta con archivo, linea y columna."""

    def test_falta_una_columna(self, tmp_path):
        ruta = tmp_path / "order_calculations.csv"
        ruta.write_text("test_name,category\nok,simple\n", encoding="utf-8")
        problemas = validar_csv_de_pedidos(str(ruta))

        assert len(problemas) == 1
        assert "faltan columnas" in problemas[0]
        assert "order_calculations.csv:1" in problemas[0]

    def test_archivo_sin_filas(self, tmp_path):
        problemas = validar_csv_de_pedidos(escribir_csv(tmp_path))
        assert any("no tiene filas de datos" in p for p in problemas)

    def test_nombre_vacio(self, tmp_path):
        fila = FILA_BUENA.replace("ok,simple", ",simple", 1)
        problemas = validar_csv_de_pedidos(escribir_csv(tmp_path, fila))
        assert any("[test_name]" in p and "vacio" in p for p in problemas)

    def test_nombre_repetido_nombra_la_segunda_linea(self, tmp_path):
        problemas = validar_csv_de_pedidos(escribir_csv(tmp_path, FILA_BUENA, FILA_BUENA))
        assert any(":3" in p and "repetido" in p for p in problemas)

    def test_categoria_desconocida(self, tmp_path):
        fila = FILA_BUENA.replace("ok,simple", "ok,inventada", 1)
        problemas = validar_csv_de_pedidos(escribir_csv(tmp_path, fila))
        assert any("[category]" in p for p in problemas)

    def test_booleano_mal_escrito(self, tmp_path):
        fila = FILA_BUENA.replace(",NONE,0,false,", ",NONE,0,False,", 1)
        problemas = validar_csv_de_pedidos(escribir_csv(tmp_path, fila))
        assert any("[is_express]" in p for p in problemas)

    def test_numero_que_no_es_numero(self, tmp_path):
        fila = FILA_BUENA.replace(",1.00,0.00,", ",mucho,0.00,", 1)
        problemas = validar_csv_de_pedidos(escribir_csv(tmp_path, fila))
        assert any("[expected_subtotal]" in p and "no es un numero" in p for p in problemas)

    def test_monto_vacio_sin_error_esperado(self, tmp_path):
        fila = FILA_BUENA.replace(",1.00,0.00,0.08,0.00,1.08,", ",,0.00,0.08,0.00,1.08,", 1)
        problemas = validar_csv_de_pedidos(escribir_csv(tmp_path, fila))
        assert any("[expected_subtotal]" in p and "no se espera un error" in p for p in problemas)

    def test_monto_vacio_con_error_esperado_es_valido(self, tmp_path):
        fila = FILA_BUENA.replace(",1.00,0.00,0.08,0.00,1.08,", ",,,,,,price must not be negative", 1)
        assert not validar_csv_de_pedidos(escribir_csv(tmp_path, fila))

    @pytest.mark.parametrize(
        "celda,fragmento",
        [
            ("no es json", "no es JSON valido"),
            ('"{""a"": 1}"', "debe ser una lista"),
            ("[1]", "no es un objeto"),
            ('"[{""name"": ""X""}]"', "le faltan"),
        ],
    )
    def test_items_mal_formados(self, tmp_path, celda, fragmento):
        fila = FILA_BUENA.replace(
            '"[{""name"": ""X"", ""price"": 1.0, ""quantity"": 1, ""weight"": 0.0}]"', celda, 1
        )
        problemas = validar_csv_de_pedidos(escribir_csv(tmp_path, fila))
        assert any("[items]" in p and fragmento in p for p in problemas)


class TestProblemasEnElJson:
    """Lo mismo para el archivo de clientes."""

    CASO = {
        "test_name": "x", "category": "valid_customers", "customer": {},
        "expected_valid": False, "expected_errors": ["algo"], "reason": "r",
    }

    def test_falta_test_cases(self, tmp_path):
        problemas = validar_json_de_clientes(escribir_json(tmp_path, {"otra": 1}))
        assert any("falta la clave test_cases" in p for p in problemas)

    def test_lista_vacia(self, tmp_path):
        problemas = validar_json_de_clientes(escribir_json(tmp_path, {"test_cases": []}))
        assert any("al menos un caso" in p for p in problemas)

    def test_caso_que_no_es_objeto(self, tmp_path):
        problemas = validar_json_de_clientes(escribir_json(tmp_path, {"test_cases": ["x"]}))
        assert any("no es un objeto" in p for p in problemas)

    def test_caso_al_que_le_faltan_claves(self, tmp_path):
        problemas = validar_json_de_clientes(escribir_json(tmp_path, {"test_cases": [{"test_name": "x"}]}))
        assert any("le faltan" in p for p in problemas)

    def test_nombre_repetido(self, tmp_path):
        problemas = validar_json_de_clientes(escribir_json(tmp_path, {"test_cases": [self.CASO, self.CASO]}))
        assert any("repetido" in p for p in problemas)

    def test_valido_con_errores_esperados(self, tmp_path):
        caso = {**self.CASO, "expected_valid": True, "expected_errors": ["algo"]}
        problemas = validar_json_de_clientes(escribir_json(tmp_path, {"test_cases": [caso]}))
        assert any("no puede traer errores" in p for p in problemas)

    def test_invalido_sin_errores_esperados(self, tmp_path):
        caso = {**self.CASO, "expected_valid": False, "expected_errors": []}
        problemas = validar_json_de_clientes(escribir_json(tmp_path, {"test_cases": [caso]}))
        assert any("tiene que decir que error espera" in p for p in problemas)

    def test_tipos_equivocados(self, tmp_path):
        caso = {**self.CASO, "expected_valid": "no", "expected_errors": "tampoco"}
        problemas = validar_json_de_clientes(escribir_json(tmp_path, {"test_cases": [caso]}))
        assert any("debe ser booleano" in p for p in problemas)
        assert any("debe ser una lista" in p for p in problemas)


def test_exigir_datos_validos_lanza_con_todo_junto(tmp_path):
    """El error reune los problemas de los dos archivos."""
    escribir_csv(tmp_path, FILA_BUENA.replace("ok,simple", "ok,inventada", 1))
    escribir_json(tmp_path, {"test_cases": []})

    with pytest.raises(DataValidationError) as error:
        exigir_datos_validos(str(tmp_path))

    assert "[category]" in str(error.value)
    assert "al menos un caso" in str(error.value)
