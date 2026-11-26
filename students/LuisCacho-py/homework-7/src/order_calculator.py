"""Order calculator module for e-commerce order processing."""

from typing import Dict, List, Optional


class Order:
    """Represents an e-commerce customer order with discount, tax, and shipping calculation."""

    VALID_CODES = {
        "SAVE10": {"min_order": 50.0, "discount_pct": 0.10},
        "SAVE20": {"min_order": 100.0, "discount_pct": 0.20},
        "FREESHIP": {"min_order": 0.0, "discount_pct": 0.0},
        "NEWUSER": {"min_order": 0.0, "discount_pct": 0.15},
    }
    TAX_RATE = 0.08
    WEIGHT_RATE_PER_KG = 0.50
    DISTANCE_RATE_PER_KM = 0.10
    EXPRESS_MULTIPLIER = 1.5

    def __init__(self, items: List[Dict], customer_type: str = "regular"):
        """
        Initialize an order.

        Args:
            items: List of {"name": str, "price": float, "quantity": int, "weight": float}
            customer_type: "new" or "regular"
        """
        self.items = items if items is not None else []
        self.customer_type = customer_type
        self.discount_code: Optional[str] = None
        self.shipping_distance: float = 0.0
        self.is_express: bool = False

    def apply_discount(self, code: str) -> bool:
        """Apply discount code and return True if valid and applicable."""
        if not code or code not in self.VALID_CODES:
            return False

        if code == "NEWUSER" and self.customer_type != "new":
            return False

        subtotal = self.calculate_subtotal()
        if subtotal < self.VALID_CODES[code]["min_order"]:
            return False

        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False) -> None:
        """Set shipping distance in km and express delivery flag."""
        self.shipping_distance = max(0.0, float(distance_km))
        self.is_express = bool(is_express)

    def calculate_subtotal(self) -> float:
        """Calculate order subtotal (sum of valid item prices * quantities)."""
        subtotal = 0.0
        for item in self.items:
            price = max(0.0, float(item.get("price", 0.0)))
            quantity = max(0, int(item.get("quantity", 0)))
            subtotal += price * quantity
        return round(subtotal, 2)

    def calculate_discount(self) -> float:
        """Calculate discount amount based on applied discount code."""
        if not self.discount_code or self.discount_code not in self.VALID_CODES:
            return 0.0

        subtotal = self.calculate_subtotal()
        code_info = self.VALID_CODES[self.discount_code]

        if subtotal < code_info["min_order"]:
            return 0.0

        if self.discount_code == "NEWUSER" and self.customer_type != "new":
            return 0.0

        return round(subtotal * code_info["discount_pct"], 2)

    def calculate_tax(self) -> float:
        """Calculate 8% tax on (subtotal - discount)."""
        taxable_amount = max(0.0, self.calculate_subtotal() - self.calculate_discount())
        return round(taxable_amount * self.TAX_RATE, 2)

    def calculate_shipping(self) -> float:
        """Calculate shipping cost based on total weight, distance, express flag, and FREESHIP."""
        if self.discount_code == "FREESHIP":
            return 0.0

        total_weight = 0.0
        for item in self.items:
            weight = max(0.0, float(item.get("weight", 0.0)))
            quantity = max(0, int(item.get("quantity", 0)))
            total_weight += weight * quantity

        if total_weight == 0.0 and self.shipping_distance == 0.0:
            return 0.0

        base_shipping = (
            total_weight * self.WEIGHT_RATE_PER_KG
            + self.shipping_distance * self.DISTANCE_RATE_PER_KM
        )
        if self.is_express:
            base_shipping *= self.EXPRESS_MULTIPLIER

        return round(base_shipping, 2)

    def calculate_total(self) -> Dict[str, float]:
        """
        Calculate order total with full breakdown.

        Returns:
            Dictionary with subtotal, discount, tax, shipping, and total.
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
