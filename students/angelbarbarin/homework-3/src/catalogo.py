"""Catalogo de productos para el cotizador de camaras de reversa.

Define el inventario disponible, el costo de instalacion por categoria y las
operaciones de consulta sobre el catalogo.
"""

import json
from typing import Any, Dict, List, Optional

PRODUCTOS: List[Dict[str, Any]] = [
    {
        "sku": "CAM-001",
        "nombre": "Camara de reversa universal",
        "precio": 850.0,
        "categoria": "camara",
    },
    {
        "sku": "CAM-002",
        "nombre": "Camara de reversa con guias dinamicas",
        "precio": 1450.0,
        "categoria": "camara",
    },
    {
        "sku": "PAN-007",
        "nombre": "Pantalla 7 pulgadas touch",
        "precio": 2300.0,
        "categoria": "pantalla",
    },
    {
        "sku": "PAN-010",
        "nombre": "Pantalla 10 pulgadas Android Auto",
        "precio": 4900.0,
        "categoria": "pantalla",
    },
    {
        "sku": "SEN-004",
        "nombre": "Kit 4 sensores de reversa",
        "precio": 1200.0,
        "categoria": "sensor",
    },
]

COSTO_INSTALACION: Dict[str, float] = {
    "camara": 350.0,
    "pantalla": 600.0,
    "sensor": 450.0,
}


class Catalogo:
    """Consulta de productos y costos de instalacion."""

    def __init__(self, productos: Optional[List[Dict[str, Any]]] = None) -> None:
        """Crea un catalogo. Sin argumentos usa el inventario por defecto."""
        self.productos = list(PRODUCTOS) if productos is None else productos

    def obtener_producto(self, sku: str) -> Optional[Dict[str, Any]]:
        """Devuelve el producto con ese SKU, o None si no existe."""
        for producto in self.productos:
            if producto["sku"] == sku:
                return producto
        return None

    def listar_por_categoria(self, categoria: str) -> List[Dict[str, Any]]:
        """Devuelve todos los productos de una categoria."""
        return [p for p in self.productos if p["categoria"] == categoria]

    def precio_instalacion(self, sku: str) -> float:
        """Costo de instalacion del producto; 0.0 si el SKU no existe."""
        producto = self.obtener_producto(sku)
        if producto is None:
            return 0.0
        return COSTO_INSTALACION.get(producto["categoria"], 0.0)

    def exportar_json(self, ruta: str) -> None:
        """Escribe el catalogo completo como JSON en la ruta indicada."""
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(self.productos, archivo, ensure_ascii=False, indent=2)
