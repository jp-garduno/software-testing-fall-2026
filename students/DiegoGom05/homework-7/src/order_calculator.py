"""
Order Calculator - E-Commerce Order Processing

Calcula subtotal, descuento, impuesto, envio y total de una orden.

Reglas:
    - Subtotal: suma de precio x cantidad de cada item
    - Descuentos:
        SAVE10   -> 10% (orden minima $50)
        SAVE20   -> 20% (orden minima $100)
        FREESHIP -> envio gratis
        NEWUSER  -> 15% (solo clientes "new")
        Codigo invalido -> sin descuento
    - Impuesto: 8% de (subtotal - descuento)
    - Envio: $0.50 por kg + $0.10 por km; express = 1.5x; FREESHIP = $0
    - Total: subtotal - descuento + impuesto + envio
"""

from typing import List, Dict, Optional

TAX_RATE = 0.08
COST_PER_KG = 0.50
COST_PER_KM = 0.10
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
        Inicializa la orden.

        Args:
            items: lista de {"name": str, "price": float, "quantity": int, "weight": float}
            customer_type: "new" o "regular"

        Raises:
            ValueError: si algun item tiene precio, cantidad o peso negativo,
                        o si el tipo de cliente no es valido.
        """
        if customer_type not in ("new", "regular"):
            raise ValueError(f"Invalid customer type: {customer_type}")

        for item in items:
            for field in ("price", "quantity", "weight"):
                if item.get(field, 0) < 0:
                    raise ValueError(f"Negative {field} in item '{item.get('name')}'")

        self.items = items
        self.customer_type = customer_type
        self.discount_code: Optional[str] = None
        self.shipping_distance = 0
        self.is_express = False

    def apply_discount(self, code: str) -> bool:
        """Aplica un codigo de descuento. Regresa True si es valido."""
        if code not in VALID_CODES:
            return False

        # NEWUSER solo aplica a clientes nuevos
        if code == "NEWUSER" and self.customer_type != "new":
            return False

        if self.calculate_subtotal() < VALID_CODES[code]["min_order"]:
            return False

        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False):
        """Configura los parametros de envio."""
        if distance_km < 0:
            raise ValueError("Distance cannot be negative")
        self.shipping_distance = distance_km
        self.is_express = is_express

    def calculate_subtotal(self) -> float:
        """Suma de precio x cantidad de todos los items."""
        subtotal = sum(item["price"] * item["quantity"] for item in self.items)
        return round(subtotal, 2)

    def calculate_discount(self) -> float:
        """Monto del descuento segun el codigo aplicado."""
        if self.discount_code is None:
            return 0.0
        pct = VALID_CODES[self.discount_code]["discount_pct"]
        return round(self.calculate_subtotal() * pct, 2)

    def calculate_tax(self) -> float:
        """Impuesto: 8% del subtotal despues del descuento."""
        taxable = self.calculate_subtotal() - self.calculate_discount()
        return round(taxable * TAX_RATE, 2)

    def calculate_shipping(self) -> float:
        """Envio por peso y distancia; express 1.5x; FREESHIP = 0."""
        if self.discount_code == "FREESHIP":
            return 0.0

        total_weight = sum(item["weight"] * item["quantity"] for item in self.items)
        base = total_weight * COST_PER_KG + self.shipping_distance * COST_PER_KM

        if self.is_express:
            base *= EXPRESS_MULTIPLIER
        return round(base, 2)

    def calculate_total(self) -> Dict[str, float]:
        """Regresa el desglose completo de la orden."""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        tax = self.calculate_tax()
        shipping = self.calculate_shipping()
        total = round(subtotal - discount + tax + shipping, 2)

        return {
            "subtotal": subtotal,
            "discount": discount,
            "tax": tax,
            "shipping": shipping,
            "total": total,
        }
