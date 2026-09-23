"""Calculo de cotizaciones de venta e instalacion."""

from typing import Any, Dict, List, Optional

from src.catalogo import Catalogo
from src.validaciones import validar_cantidad, validar_descuento, validar_sku

IVA = 0.16


class Cotizador:
    """Arma carritos y calcula el total de una cotizacion."""

    def __init__(self, catalogo: Optional[Catalogo] = None) -> None:
        """Crea un cotizador sobre el catalogo dado o sobre el catalogo por defecto."""
        self.catalogo = Catalogo() if catalogo is None else catalogo

    def agregar_item(
        self,
        sku: str,
        cantidad: object,
        carrito: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """Agrega un producto al carrito y devuelve el carrito resultante.

        Sin carrito explicito se crea uno nuevo en cada llamada: usar una lista
        como valor por defecto haria que todas las cotizaciones compartieran el
        mismo carrito.
        """
        if carrito is None:
            carrito = []
        if not validar_sku(sku):
            raise ValueError(f"SKU invalido: {sku}")
        if not validar_cantidad(cantidad):
            raise ValueError(f"Cantidad invalida: {cantidad}")
        producto = self.catalogo.obtener_producto(sku)
        if producto is None:
            raise ValueError(f"Producto no encontrado: {sku}")
        carrito.append(
            {
                "sku": sku,
                "cantidad": int(cantidad),  # type: ignore[arg-type]
                "precio": producto["precio"],
            }
        )
        return carrito

    def calcular_subtotal(self, carrito: List[Dict[str, Any]]) -> float:
        """Suma el precio de los productos, sin instalacion ni impuestos."""
        return sum(item["precio"] * item["cantidad"] for item in carrito)

    def calcular_instalacion(self, carrito: List[Dict[str, Any]]) -> float:
        """Suma el costo de instalacion de todos los productos del carrito."""
        return sum(
            self.catalogo.precio_instalacion(item["sku"]) * item["cantidad"]
            for item in carrito
        )

    def cotizar(
        self,
        carrito: List[Dict[str, Any]],
        descuento: float = 0,
        incluir_instalacion: bool = True,
    ) -> Dict[str, float]:
        """Devuelve el desglose de la cotizacion: subtotal, instalacion, IVA y total."""
        if not validar_descuento(descuento):
            raise ValueError(f"Descuento invalido: {descuento}")
        subtotal = self.calcular_subtotal(carrito)
        instalacion = self.calcular_instalacion(carrito) if incluir_instalacion else 0.0
        base = subtotal + instalacion
        ahorro = base * (descuento / 100.0)
        base_con_descuento = base - ahorro
        impuesto = base_con_descuento * IVA
        return {
            "subtotal": subtotal,
            "instalacion": instalacion,
            "descuento": ahorro,
            "iva": impuesto,
            "total": base_con_descuento + impuesto,
        }
