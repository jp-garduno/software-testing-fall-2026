"""Generador de datos de regresion (Bonus, opcion A).

El enunciado sugiere Faker. Aqui no se usa: el runner de calificacion instala
solo el requirements.txt de la raiz del repositorio, donde Faker no esta, asi
que una prueba que lo importara fallaria al calificar. En su lugar se genera
con random sembrado, que ademas da algo que Faker no da gratis: el mismo
semillero produce siempre el mismo archivo, que es justo lo que necesita un
conjunto de regresion.

Que son estos datos: una foto del comportamiento actual, no una verificacion
de que el comportamiento sea correcto. Sirven para detectar que algo cambio,
no para demostrar que algo esta bien. Lo segundo lo hace
order_calculations.csv, cuyos valores se escribieron a mano desde las reglas.
"""

import csv
import json
import random
from typing import Dict, List

from order_calculator import Order

ARTICULOS = (
    ("Notebook", 3.50, 0.30), ("Keyboard", 45.00, 0.90), ("Monitor", 189.99, 4.20),
    ("Mouse", 24.50, 0.15), ("Desk Lamp", 32.00, 1.10), ("Headphones", 79.90, 0.25),
    ("Webcam", 58.25, 0.20), ("Backpack", 64.00, 0.80), ("Cable", 9.99, 0.05),
    ("Chair", 149.00, 12.50), ("Tablet", 329.00, 0.55), ("Speaker", 88.40, 1.80),
)
CODIGOS = ("NONE", "SAVE10", "SAVE20", "FREESHIP", "NEWUSER")
TIPOS_DE_CLIENTE = ("regular", "new")

ENCABEZADO = (
    "test_name", "items", "customer_type", "discount_code", "distance_km", "is_express",
    "expected_subtotal", "expected_discount", "expected_tax", "expected_shipping", "expected_total",
)


def generar_pedido(azar: random.Random, indice: int) -> Dict:
    """Arma un pedido valido al azar, sin calcular todavia sus montos."""
    cuantos = azar.randint(1, 4)
    items = []
    for nombre, precio, peso in azar.sample(ARTICULOS, cuantos):
        items.append(
            {
                "name": nombre,
                "price": round(precio * azar.uniform(0.8, 1.2), 2),
                "quantity": azar.randint(1, 5),
                "weight": round(peso * azar.uniform(0.9, 1.1), 3),
            }
        )

    return {
        "test_name": f"generated_order_{indice:03d}",
        "items": items,
        "customer_type": azar.choice(TIPOS_DE_CLIENTE),
        "discount_code": azar.choice(CODIGOS),
        "distance_km": round(azar.uniform(0, 400), 1),
        "is_express": azar.random() < 0.3,
    }


def calcular_montos(pedido: Dict) -> Dict[str, float]:
    """Corre el pedido por el calculador real y devuelve su desglose."""
    orden = Order(pedido["items"], pedido["customer_type"])
    if pedido["discount_code"] != "NONE":
        orden.apply_discount(pedido["discount_code"])
    orden.set_shipping(pedido["distance_km"], pedido["is_express"])
    return orden.calculate_total()


def generar_pedidos(cantidad: int = 100, semilla: int = 20261111) -> List[Dict]:
    """Devuelve `cantidad` pedidos con su desglose, reproducibles por semilla."""
    if not isinstance(cantidad, int) or cantidad < 1:
        raise ValueError("cantidad debe ser un entero positivo")

    azar = random.Random(semilla)
    pedidos = []
    for indice in range(1, cantidad + 1):
        pedido = generar_pedido(azar, indice)
        pedido["expected"] = calcular_montos(pedido)
        pedidos.append(pedido)
    return pedidos


def escribir_csv(pedidos: List[Dict], ruta: str) -> str:
    """Guarda los pedidos en el mismo formato que order_calculations.csv."""
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(ENCABEZADO)
        for pedido in pedidos:
            desglose = pedido["expected"]
            escritor.writerow(
                [
                    pedido["test_name"],
                    json.dumps(pedido["items"]),
                    pedido["customer_type"],
                    pedido["discount_code"],
                    pedido["distance_km"],
                    str(pedido["is_express"]).lower(),
                    f"{desglose['subtotal']:.2f}",
                    f"{desglose['discount']:.2f}",
                    f"{desglose['tax']:.2f}",
                    f"{desglose['shipping']:.2f}",
                    f"{desglose['total']:.2f}",
                ]
            )
    return ruta


def main(ruta: str = "test_data/generated_orders.csv", cantidad: int = 100) -> str:
    """Genera el archivo de regresion. Se invoca a mano, no desde las pruebas."""
    return escribir_csv(generar_pedidos(cantidad), ruta)


if __name__ == "__main__":  # pragma: no cover
    print(main())
