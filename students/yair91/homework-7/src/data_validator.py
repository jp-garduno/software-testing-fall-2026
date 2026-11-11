"""Validacion de los archivos de datos de prueba (Bonus, opcion C).

Antes de correr la suite conviene saber si los datos estan bien formados. Un
CSV con una columna de menos o un numero escrito como texto no hace fallar una
prueba por la razon correcta: la hace fallar por una razon confusa, o peor, la
hace pasar con datos silenciosamente mal convertidos.

Cada problema se reporta con el archivo, la linea y la columna.
"""

import csv
import json
import os
from typing import Dict, List

COLUMNAS_DE_PEDIDOS = (
    "test_name", "category", "items", "customer_type", "discount_code",
    "distance_km", "is_express", "expected_subtotal", "expected_discount",
    "expected_tax", "expected_shipping", "expected_total", "expected_error",
)
COLUMNAS_NUMERICAS = (
    "distance_km", "expected_subtotal", "expected_discount",
    "expected_tax", "expected_shipping", "expected_total",
)
CAMPOS_DE_ITEM = ("name", "price", "quantity", "weight")
CLAVES_DE_CASO = ("test_name", "category", "customer", "expected_valid", "expected_errors", "reason")
CATEGORIAS_DE_PEDIDO = ("simple", "discount", "tax", "shipping", "complex")


class DataValidationError(Exception):
    """Se lanza cuando un archivo de datos no se puede usar."""


def _problema(archivo: str, linea, columna, mensaje: str) -> str:
    """Arma un mensaje que siempre dice donde esta el problema."""
    ubicacion = f"{os.path.basename(archivo)}"
    if linea is not None:
        ubicacion += f":{linea}"
    if columna is not None:
        ubicacion += f" [{columna}]"
    return f"{ubicacion}: {mensaje}"


def validar_csv_de_pedidos(ruta: str) -> List[str]:
    """Revisa order_calculations.csv y devuelve la lista de problemas."""
    problemas = []

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        faltantes = [c for c in COLUMNAS_DE_PEDIDOS if c not in (lector.fieldnames or [])]
        if faltantes:
            return [_problema(ruta, 1, None, f"faltan columnas: {', '.join(faltantes)}")]

        nombres = set()
        for numero, fila in enumerate(lector, start=2):
            problemas.extend(_revisar_fila_de_pedido(ruta, numero, fila, nombres))

    if not problemas and not nombres:
        problemas.append(_problema(ruta, None, None, "el archivo no tiene filas de datos"))
    return problemas


def _revisar_fila_de_pedido(ruta: str, numero: int, fila: Dict, nombres: set) -> List[str]:
    """Revisa una fila: nombre unico, categoria, booleano, items y numeros."""
    problemas = []

    nombre = (fila.get("test_name") or "").strip()
    if not nombre:
        problemas.append(_problema(ruta, numero, "test_name", "esta vacio"))
    elif nombre in nombres:
        problemas.append(_problema(ruta, numero, "test_name", f"'{nombre}' esta repetido"))
    else:
        nombres.add(nombre)

    if fila.get("category") not in CATEGORIAS_DE_PEDIDO:
        problemas.append(
            _problema(ruta, numero, "category", f"'{fila.get('category')}' no es una categoria conocida")
        )

    if fila.get("is_express") not in ("true", "false"):
        problemas.append(_problema(ruta, numero, "is_express", "debe ser true o false en minusculas"))

    problemas.extend(_revisar_items(ruta, numero, fila.get("items", "")))

    espera_error = bool((fila.get("expected_error") or "").strip())
    for columna in COLUMNAS_NUMERICAS:
        valor = (fila.get(columna) or "").strip()
        if valor == "":
            if not espera_error and columna != "distance_km":
                problemas.append(_problema(ruta, numero, columna, "esta vacio y no se espera un error"))
            continue
        try:
            float(valor)
        except ValueError:
            problemas.append(_problema(ruta, numero, columna, f"'{valor}' no es un numero"))

    return problemas


def _revisar_items(ruta: str, numero: int, crudo: str) -> List[str]:
    """La celda items tiene que ser JSON con los cuatro campos por articulo."""
    try:
        items = json.loads(crudo)
    except json.JSONDecodeError as error:
        return [_problema(ruta, numero, "items", f"no es JSON valido: {error.msg}")]

    if not isinstance(items, list):
        return [_problema(ruta, numero, "items", "debe ser una lista")]

    problemas = []
    for posicion, item in enumerate(items):
        if not isinstance(item, dict):
            problemas.append(_problema(ruta, numero, "items", f"el articulo {posicion} no es un objeto"))
            continue
        faltan = [campo for campo in CAMPOS_DE_ITEM if campo not in item]
        if faltan:
            problemas.append(
                _problema(ruta, numero, "items", f"al articulo {posicion} le faltan {', '.join(faltan)}")
            )
    return problemas


def validar_json_de_clientes(ruta: str) -> List[str]:
    """Revisa customer_validation.json y devuelve la lista de problemas."""
    with open(ruta, encoding="utf-8") as archivo:
        datos = json.load(archivo)

    if not isinstance(datos, dict) or "test_cases" not in datos:
        return [_problema(ruta, None, None, "falta la clave test_cases")]

    casos = datos["test_cases"]
    if not isinstance(casos, list) or not casos:
        return [_problema(ruta, None, "test_cases", "debe ser una lista con al menos un caso")]

    problemas, nombres = [], set()
    for indice, caso in enumerate(casos):
        etiqueta = f"test_cases[{indice}]"
        if not isinstance(caso, dict):
            problemas.append(_problema(ruta, None, etiqueta, "no es un objeto"))
            continue

        faltan = [clave for clave in CLAVES_DE_CASO if clave not in caso]
        if faltan:
            problemas.append(_problema(ruta, None, etiqueta, f"le faltan {', '.join(faltan)}"))
            continue

        nombre = caso["test_name"]
        if nombre in nombres:
            problemas.append(_problema(ruta, None, etiqueta, f"'{nombre}' esta repetido"))
        nombres.add(nombre)

        if not isinstance(caso["expected_valid"], bool):
            problemas.append(_problema(ruta, None, etiqueta, "expected_valid debe ser booleano"))
        if not isinstance(caso["expected_errors"], list):
            problemas.append(_problema(ruta, None, etiqueta, "expected_errors debe ser una lista"))
        elif caso["expected_valid"] and caso["expected_errors"]:
            problemas.append(
                _problema(ruta, None, etiqueta, "un caso valido no puede traer errores esperados")
            )
        elif not caso["expected_valid"] and not caso["expected_errors"]:
            problemas.append(
                _problema(ruta, None, etiqueta, "un caso invalido tiene que decir que error espera")
            )

    return problemas


def validar_todo(directorio: str) -> Dict[str, List[str]]:
    """Revisa los dos archivos principales y devuelve los problemas por archivo."""
    return {
        "order_calculations.csv": validar_csv_de_pedidos(os.path.join(directorio, "order_calculations.csv")),
        "customer_validation.json": validar_json_de_clientes(
            os.path.join(directorio, "customer_validation.json")
        ),
    }


def exigir_datos_validos(directorio: str) -> None:
    """Lanza DataValidationError si algun archivo tiene problemas."""
    hallazgos = validar_todo(directorio)
    todos = [problema for lista in hallazgos.values() for problema in lista]
    if todos:
        raise DataValidationError("\n".join(todos))
