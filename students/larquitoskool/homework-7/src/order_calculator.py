from typing import List, Dict
from datetime import datetime

class Order:
    def __init__(self, items: List[Dict], customer_type: str = "regular"):
        """
        Initialize order

        Args:
            items: List of {"name": str, "price": float, "quantity": int, "weight": float}
            customer_type: "new" or "regular"
        """
        self.items = items
        self.customer_type = customer_type
        self.discount_code = None
        self.shipping_distance = 0
        self.is_express = False

    def apply_discount(self, code: str) -> bool:
        """Apply discount code, return True if valid"""
        valid_codes = {
            "SAVE10": {"min_order": 50, "discount_pct": 0.10},
            "SAVE20": {"min_order": 100, "discount_pct": 0.20},
            "FREESHIP": {"min_order": 0, "discount_pct": 0},
            "NEWUSER": {"min_order": 0, "discount_pct": 0.15}
        }

        if code not in valid_codes:
            return False
            
        # Validar que NEWUSER solo aplique a clientes nuevos
        if code == "NEWUSER" and self.customer_type != "new":
            return False

        subtotal = self.calculate_subtotal()
        if subtotal < valid_codes[code]["min_order"]:
            return False

        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False):
        """Set shipping parameters"""
        self.shipping_distance = distance_km
        self.is_express = is_express

    def calculate_subtotal(self) -> float:
        """Calculate subtotal (sum of item prices * quantity)"""
        return sum(item.get("price", 0.0) * item.get("quantity", 1) for item in self.items)

    def calculate_discount(self) -> float:
        """Calculate discount amount"""
        if not self.discount_code:
            return 0.0
            
        valid_codes = {
            "SAVE10": 0.10,
            "SAVE20": 0.20,
            "FREESHIP": 0.0,
            "NEWUSER": 0.15
        }
        
        subtotal = self.calculate_subtotal()
        discount_pct = valid_codes.get(self.discount_code, 0.0)
        return subtotal * discount_pct

    def calculate_tax(self) -> float:
        """Calculate tax (8% of subtotal after discount)"""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        taxable_amount = max(0.0, subtotal - discount)
        return taxable_amount * 0.08

    def calculate_shipping(self) -> float:
        """Calculate shipping cost"""
        if self.discount_code == "FREESHIP":
            return 0.0
            
        total_weight = sum(item.get("weight", 0.0) * item.get("quantity", 1) for item in self.items)
        
        base_shipping = (total_weight * 0.50) + (self.shipping_distance * 0.10)
        
        if self.is_express:
            return base_shipping * 1.5
            
        return base_shipping

    def calculate_total(self) -> Dict[str, float]:
        """
        Calculate order total with breakdown
        """
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        tax = self.calculate_tax()
        shipping = self.calculate_shipping()
        
        total = subtotal - discount + tax + shipping
        
        return {
            "subtotal": round(subtotal, 2),
            "discount": round(discount, 2),
            "tax": round(tax, 2),
            "shipping": round(shipping, 2),
            "total": round(total, 2)
        }