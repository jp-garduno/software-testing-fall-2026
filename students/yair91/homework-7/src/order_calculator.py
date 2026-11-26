"""Order calculator for the e-commerce order processing system.

Rounding happens at each step, to cents, so the breakdown a customer sees adds
up exactly to the total instead of drifting by a fraction of a cent.
"""

import math
from typing import Dict, List

TAX_RATE = 0.08
SHIPPING_PER_KG = 0.50
SHIPPING_PER_KM = 0.10
EXPRESS_MULTIPLIER = 1.5

# min_order is the subtotal the code needs to be accepted; discount_pct is the
# share taken off the subtotal.
DISCOUNT_CODES = {
    "SAVE10": {"min_order": 50.0, "discount_pct": 0.10},
    "SAVE20": {"min_order": 100.0, "discount_pct": 0.20},
    "FREESHIP": {"min_order": 0.0, "discount_pct": 0.0},
    "NEWUSER": {"min_order": 0.0, "discount_pct": 0.15},
}

CUSTOMER_TYPES = ("new", "regular")
REQUIRED_ITEM_FIELDS = ("name", "price", "quantity", "weight")


def _money(amount: float) -> float:
    """Round a monetary amount to cents."""
    return round(amount + 0.0, 2)


def _require_non_negative_number(value, field: str) -> float:
    """Return value as a float, or raise when it is not a usable amount."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a number")
    if math.isnan(value) or math.isinf(value):
        raise ValueError(f"{field} must be a finite number")
    if value < 0:
        raise ValueError(f"{field} must not be negative")
    return float(value)


class Order:
    """A customer order and the amounts that can be derived from it."""

    def __init__(self, items: List[Dict], customer_type: str = "regular"):
        """Validate the order up front so every later calculation is safe.

        Args:
            items: list of {"name", "price", "quantity", "weight"}
            customer_type: "new" or "regular"

        Raises:
            ValueError: on an unusable item list or customer type.
        """
        if customer_type not in CUSTOMER_TYPES:
            raise ValueError("customer_type must be new or regular")
        if not isinstance(items, list):
            raise ValueError("items must be a list")

        self.items = [self._validate_item(item) for item in items]
        self.customer_type = customer_type
        self.discount_code = None
        self.shipping_distance = 0.0
        self.is_express = False

    @staticmethod
    def _validate_item(item) -> Dict:
        """Return a normalized copy of one item, or raise if it is unusable."""
        if not isinstance(item, dict):
            raise ValueError("each item must be an object")

        missing = [field for field in REQUIRED_ITEM_FIELDS if field not in item]
        if missing:
            raise ValueError(f"item is missing {', '.join(missing)}")

        name = item["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError("item name must be a non-empty string")

        quantity = item["quantity"]
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("quantity must be a whole number")
        if quantity < 0:
            raise ValueError("quantity must not be negative")

        return {
            "name": name,
            "price": _require_non_negative_number(item["price"], "price"),
            "quantity": quantity,
            "weight": _require_non_negative_number(item["weight"], "weight"),
        }

    def apply_discount(self, code: str) -> bool:
        """Apply a discount code and report whether it was accepted.

        A code is rejected when it is unknown, when the subtotal is below its
        minimum, or when NEWUSER is used by a customer who is not new. The
        brief calls NEWUSER "15% off first order", so a regular customer does
        not qualify even though the code itself is valid.
        """
        if code not in DISCOUNT_CODES:
            return False
        if code == "NEWUSER" and self.customer_type != "new":
            return False
        if self.calculate_subtotal() < DISCOUNT_CODES[code]["min_order"]:
            return False

        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False):
        """Set the shipping distance and whether the order ships express."""
        if not isinstance(is_express, bool):
            raise ValueError("is_express must be a boolean")
        self.shipping_distance = _require_non_negative_number(distance_km, "distance_km")
        self.is_express = is_express

    def calculate_subtotal(self) -> float:
        """Sum of price times quantity across every item."""
        return _money(sum(item["price"] * item["quantity"] for item in self.items))

    def calculate_discount(self) -> float:
        """Amount taken off the subtotal, zero when no code is applied."""
        if self.discount_code is None:
            return 0.0
        return _money(self.calculate_subtotal() * DISCOUNT_CODES[self.discount_code]["discount_pct"])

    def calculate_tax(self) -> float:
        """Tax on the discounted subtotal. Shipping is not taxed."""
        return _money((self.calculate_subtotal() - self.calculate_discount()) * TAX_RATE)

    def total_weight(self) -> float:
        """Combined weight of every unit in the order."""
        return _money(sum(item["weight"] * item["quantity"] for item in self.items))

    def calculate_shipping(self) -> float:
        """Weight and distance cost, multiplied for express, waived by FREESHIP."""
        if self.discount_code == "FREESHIP":
            return 0.0

        base = self.total_weight() * SHIPPING_PER_KG + self.shipping_distance * SHIPPING_PER_KM
        if self.is_express:
            base *= EXPRESS_MULTIPLIER
        return _money(base)

    def calculate_total(self) -> Dict[str, float]:
        """Full breakdown: subtotal, discount, tax, shipping and total."""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        tax = self.calculate_tax()
        shipping = self.calculate_shipping()

        return {
            "subtotal": subtotal,
            "discount": discount,
            "tax": tax,
            "shipping": shipping,
            "total": _money(subtotal - discount + tax + shipping),
        }
