"""Calculadora de pedidos para el sistema de e-commerce.

Reglas:
  - Subtotal = suma(precio * cantidad)
  - Descuento segun codigo (SAVE10, SAVE20, FREESHIP, NEWUSER)
  - Impuesto = 8% de (subtotal - descuento)
  - Envio = peso * 0.50/kg + distancia * 0.10/km (x1.5 si es express)
  - FREESHIP => envio gratis
  - Total = subtotal - descuento + impuesto + envio
"""
from typing import Dict, List

TAX_RATE = 0.08
WEIGHT_RATE_PER_KG = 0.50
DISTANCE_RATE_PER_KM = 0.10
EXPRESS_MULTIPLIER = 1.5

VALID_CODES = {
    "SAVE10": {"min_order": 50, "discount_pct": 0.10},
    "SAVE20": {"min_order": 100, "discount_pct": 0.20},
    "FREESHIP": {"min_order": 0, "discount_pct": 0},
    "NEWUSER": {"min_order": 0, "discount_pct": 0.15},
}


class Order:
    def __init__(self, items: List[Dict], customer_type: str = "regular"):
        """
        Args:
            items: lista de {"name": str, "price": float, "quantity": int, "weight": float}
            customer_type: "new" o "regular"

        Raises:
            ValueError: si customer_type es invalido o algun item tiene valores negativos.
        """
        if customer_type not in ("new", "regular"):
            raise ValueError(f"Invalid customer_type: {customer_type}")
        for item in items:
            self._validate_item(item)

        self.items = items
        self.customer_type = customer_type
        self.discount_code = None
        self.shipping_distance = 0
        self.is_express = False

    @staticmethod
    def _validate_item(item: Dict) -> None:
        if item["price"] < 0 or item["quantity"] < 0 or item.get("weight", 0) < 0:
            raise ValueError(f"Negative values are not allowed: {item}")

    def apply_discount(self, code: str) -> bool:
        """Aplica un codigo de descuento. Devuelve True si fue valido."""
        rule = VALID_CODES.get(code)
        if rule is None:
            return False
        # NEWUSER solo para clientes nuevos
        if code == "NEWUSER" and self.customer_type != "new":
            return False
        if self.calculate_subtotal() < rule["min_order"]:
            return False

        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False):
        """Configura los parametros de envio."""
        if distance_km < 0:
            raise ValueError("distance_km cannot be negative")
        self.shipping_distance = distance_km
        self.is_express = is_express

    def _total_weight(self) -> float:
        return sum(i.get("weight", 0) * i["quantity"] for i in self.items)

    def calculate_subtotal(self) -> float:
        """Suma de precio * cantidad de todos los items."""
        return round(sum(i["price"] * i["quantity"] for i in self.items), 2)

    def calculate_discount(self) -> float:
        """Monto del descuento (0 si no hay codigo aplicado)."""
        if self.discount_code is None:
            return 0.0
        pct = VALID_CODES[self.discount_code]["discount_pct"]
        return round(self.calculate_subtotal() * pct, 2)

    def calculate_tax(self) -> float:
        """8% de (subtotal - descuento)."""
        taxable = self.calculate_subtotal() - self.calculate_discount()
        return round(taxable * TAX_RATE, 2)

    def calculate_shipping(self) -> float:
        """Costo de envio (por peso + distancia, x1.5 si es express)."""
        if self.discount_code == "FREESHIP":
            return 0.0
        base = (self._total_weight() * WEIGHT_RATE_PER_KG
                + self.shipping_distance * DISTANCE_RATE_PER_KM)
        if self.is_express:
            base *= EXPRESS_MULTIPLIER
        return round(base, 2)

    def calculate_total(self) -> Dict[str, float]:
        """Devuelve el desglose completo del pedido."""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        tax = self.calculate_tax()
        shipping = self.calculate_shipping()
        return {
            "subtotal": subtotal,
            "discount": discount,
            "tax": tax,
            "shipping": shipping,
            "total": round(subtotal - discount + tax + shipping, 2),
        }