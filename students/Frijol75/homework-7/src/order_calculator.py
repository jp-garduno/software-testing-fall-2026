"""
Order Calculator Module - E-Commerce Order Processing System.

Handles order item calculations, subtotal, discount codes, taxes,
weight and distance based shipping, and final total amounts.
"""

from typing import List, Dict, Optional

TAX_RATE = 0.08
WEIGHT_RATE_PER_KG = 0.50
DISTANCE_RATE_PER_KM = 0.10
EXPRESS_MULTIPLIER = 1.50

DISCOUNT_RULES = {
    "SAVE10": {"min_order": 50.0, "discount_pct": 0.10},
    "SAVE20": {"min_order": 100.0, "discount_pct": 0.20},
    "FREESHIP": {"min_order": 0.0, "discount_pct": 0.00},
    "NEWUSER": {"min_order": 0.0, "discount_pct": 0.15},
}


class Order:
    """Represents an e-commerce order and performs price and total calculations."""

    def __init__(self, items: List[Dict], customer_type: str = "regular"):
        """
        Initialize order.

        Args:
            items: List of {"name": str, "price": float, "quantity": int, "weight": float}
            customer_type: "new" or "regular"
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
        self.shipping_distance: float = 0.0
        self.is_express: bool = False

    def apply_discount(self, code: Optional[str]) -> bool:
        """
        Apply a discount code to the order.

        Returns:
            True if code is valid and all conditions are met, otherwise False.
        """
        if not code or code not in DISCOUNT_RULES:
            return False

        if code == "NEWUSER" and self.customer_type != "new":
            return False

        rule = DISCOUNT_RULES[code]
        if self.calculate_subtotal() < rule["min_order"]:
            return False

        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False):
        """
        Set shipping parameters for distance and express delivery.
        """
        if distance_km < 0:
            raise ValueError("Distance cannot be negative")
        self.shipping_distance = float(distance_km)
        self.is_express = bool(is_express)

    def calculate_subtotal(self) -> float:
        """Calculate subtotal (sum of item prices * quantities)."""
        subtotal = sum(item["price"] * item["quantity"] for item in self.items)
        return round(float(subtotal), 2)

    def calculate_discount(self) -> float:
        """Calculate discount amount based on applied code."""
        if not self.discount_code:
            return 0.0
        pct = DISCOUNT_RULES[self.discount_code]["discount_pct"]
        return round(self.calculate_subtotal() * pct, 2)

    def calculate_tax(self) -> float:
        """Calculate tax (8% of subtotal after discount)."""
        taxable_amount = self.calculate_subtotal() - self.calculate_discount()
        return round(taxable_amount * TAX_RATE, 2)

    def calculate_shipping(self) -> float:
        """Calculate shipping cost based on weight, distance and express option."""
        if self.discount_code == "FREESHIP":
            return 0.0

        total_weight = sum(item["weight"] * item["quantity"] for item in self.items)
        base_shipping = (total_weight * WEIGHT_RATE_PER_KG) + (self.shipping_distance * DISTANCE_RATE_PER_KM)

        if self.is_express:
            base_shipping *= EXPRESS_MULTIPLIER

        return round(base_shipping, 2)

    def calculate_total(self) -> Dict[str, float]:
        """
        Calculate order total with complete breakdown.

        Returns:
            Dict containing subtotal, discount, tax, shipping, and total.
        """
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

