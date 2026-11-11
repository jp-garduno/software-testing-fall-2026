"""Order calculator module for the e-commerce order processing system."""

from typing import Any, Dict, List, Optional


class Order:
    """Calculates order subtotals, discounts, taxes, shipping, and totals."""

    VALID_CODES: Dict[str, Dict[str, float]] = {
        "SAVE10": {"min_order": 50.0, "discount_pct": 0.10},
        "SAVE20": {"min_order": 100.0, "discount_pct": 0.20},
        "FREESHIP": {"min_order": 0.0, "discount_pct": 0.0},
        "NEWUSER": {"min_order": 0.0, "discount_pct": 0.15},
    }

    TAX_RATE: float = 0.08
    WEIGHT_RATE_PER_KG: float = 0.50
    DISTANCE_RATE_PER_KM: float = 0.10
    EXPRESS_MULTIPLIER: float = 1.5

    def __init__(
        self, items: List[Dict[str, Any]], customer_type: str = "regular"
    ) -> None:
        """
        Initialize order.

        Args:
            items: List of {"name": str, "price": float, "quantity": int, "weight": float}
            customer_type: "new" or "regular"
        """
        self.items = items or []
        self.customer_type = customer_type
        self.discount_code: Optional[str] = None
        self.shipping_distance: float = 0.0
        self.is_express: bool = False

    def apply_discount(self, code: Optional[str]) -> bool:
        """Apply discount code, return True if valid."""
        if not code or code not in self.VALID_CODES:
            return False

        if code == "NEWUSER" and self.customer_type != "new":
            return False

        subtotal = self.calculate_subtotal()
        if subtotal <= 0:
            return False

        if code in ("SAVE10", "SAVE20") and subtotal < self.VALID_CODES[code]["min_order"]:
            return False

        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False) -> None:
        """Set shipping parameters."""
        self.shipping_distance = max(0.0, float(distance_km))
        self.is_express = bool(is_express)

    def calculate_subtotal(self) -> float:
        """Calculate subtotal (sum of valid item prices * quantities)."""
        subtotal = 0.0
        for item in self.items:
            price = max(0.0, float(item.get("price", 0.0)))
            quantity = max(0, int(item.get("quantity", 0)))
            subtotal += price * quantity
        return round(subtotal, 2)

    def calculate_discount(self) -> float:
        """Calculate discount amount."""
        if not self.discount_code or self.discount_code not in self.VALID_CODES:
            return 0.0

        subtotal = self.calculate_subtotal()
        discount_pct = self.VALID_CODES[self.discount_code]["discount_pct"]
        return round(subtotal * discount_pct, 2)

    def calculate_tax(self) -> float:
        """Calculate tax (8% of subtotal after discount)."""
        taxable_amount = max(
            0.0, self.calculate_subtotal() - self.calculate_discount()
        )
        return round(taxable_amount * self.TAX_RATE, 2)

    def calculate_shipping(self) -> float:
        """Calculate shipping cost based on weight, distance, and express option."""
        if self.discount_code == "FREESHIP":
            return 0.0

        total_weight = 0.0
        has_shippable_items = False
        for item in self.items:
            quantity = max(0, int(item.get("quantity", 0)))
            weight = max(0.0, float(item.get("weight", 0.0)))
            if quantity > 0:
                has_shippable_items = True
                total_weight += weight * quantity

        if not has_shippable_items:
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
        Calculate order total with breakdown.

        Returns:
            {
                "subtotal": float,
                "discount": float,
                "tax": float,
                "shipping": float,
                "total": float
            }
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
