"""Order calculation for the e-commerce order processing system.

Money is handled with ``Decimal`` and rounded half-up to whole cents at each step, so the
breakdown returned by ``calculate_total`` always adds up exactly.
"""

from decimal import ROUND_HALF_UP, Decimal
from typing import Dict, List

TAX_RATE = Decimal("0.08")
WEIGHT_RATE_PER_KG = Decimal("0.50")
DISTANCE_RATE_PER_KM = Decimal("0.10")
EXPRESS_MULTIPLIER = Decimal("1.5")
CENT = Decimal("0.01")

VALID_CUSTOMER_TYPES = ("new", "regular")

# min_order is inclusive: an order of exactly min_order qualifies.
DISCOUNT_CODES = {
    "SAVE10": {"min_order": Decimal("50"), "discount_pct": Decimal("0.10"), "customer_type": None},
    "SAVE20": {"min_order": Decimal("100"), "discount_pct": Decimal("0.20"), "customer_type": None},
    "FREESHIP": {"min_order": Decimal("0"), "discount_pct": Decimal("0"), "customer_type": None},
    "NEWUSER": {"min_order": Decimal("0"), "discount_pct": Decimal("0.15"), "customer_type": "new"},
}
FREE_SHIPPING_CODE = "FREESHIP"


def _to_decimal(value, field):
    """Convert a number to Decimal, rejecting booleans and non-numeric values."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError(f"Invalid item: {field} must be a number")
    return Decimal(str(value))


def _cents(amount):
    """Round a Decimal amount half-up to whole cents."""
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


class Order:
    """A customer order: items, an optional discount code and shipping settings."""

    def __init__(self, items: List[Dict], customer_type: str = "regular"):
        """Create an order.

        Args:
            items: list of {"name": str, "price": float, "quantity": int, "weight": float}
            customer_type: "new" or "regular"
        """
        if customer_type not in VALID_CUSTOMER_TYPES:
            raise ValueError(f"Invalid customer type: {customer_type!r}")
        if not items:
            raise ValueError("Order must contain at least one item")
        self.items = [self._validate_item(item) for item in items]
        self.customer_type = customer_type
        self.discount_code = None
        self.shipping_distance = Decimal("0")
        self.is_express = False

    @staticmethod
    def _validate_item(item):
        """Return a normalised copy of an item, or raise ValueError."""
        price = _to_decimal(item.get("price"), "price")
        quantity = item.get("quantity")
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Invalid item: quantity must be a whole number")
        weight = _to_decimal(item.get("weight", 0), "weight")
        if price < 0:
            raise ValueError("Invalid item: price must not be negative")
        if quantity < 0:
            raise ValueError("Invalid item: quantity must not be negative")
        if weight < 0:
            raise ValueError("Invalid item: weight must not be negative")
        return {"name": item.get("name", ""), "price": price, "quantity": quantity, "weight": weight}

    def apply_discount(self, code: str) -> bool:
        """Apply a discount code. Returns True if it was valid for this order.

        An invalid code leaves any previously applied code untouched; a valid one replaces it.
        """
        rule = DISCOUNT_CODES.get(code)
        if rule is None:
            return False
        if self._subtotal() < rule["min_order"]:
            return False
        if rule["customer_type"] is not None and rule["customer_type"] != self.customer_type:
            return False
        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False):
        """Set the shipping distance (km) and whether express shipping is used."""
        distance = _to_decimal(distance_km, "distance")
        if distance < 0:
            raise ValueError("Shipping distance must not be negative")
        self.shipping_distance = distance
        self.is_express = bool(is_express)

    def _subtotal(self):
        return _cents(sum((item["price"] * item["quantity"] for item in self.items), Decimal("0")))

    def _discount(self):
        if self.discount_code is None:
            return Decimal("0.00")
        return _cents(self._subtotal() * DISCOUNT_CODES[self.discount_code]["discount_pct"])

    def _tax(self):
        return _cents((self._subtotal() - self._discount()) * TAX_RATE)

    def _shipping(self):
        if self.discount_code == FREE_SHIPPING_CODE:
            return Decimal("0.00")
        total_weight = sum((item["weight"] * item["quantity"] for item in self.items), Decimal("0"))
        base = total_weight * WEIGHT_RATE_PER_KG + self.shipping_distance * DISTANCE_RATE_PER_KM
        if self.is_express:
            base *= EXPRESS_MULTIPLIER
        return _cents(base)

    def calculate_subtotal(self) -> float:
        """Sum of price x quantity over all items."""
        return float(self._subtotal())

    def calculate_discount(self) -> float:
        """Discount amount for the applied code (0 if none)."""
        return float(self._discount())

    def calculate_tax(self) -> float:
        """8% of (subtotal - discount)."""
        return float(self._tax())

    def calculate_shipping(self) -> float:
        """Weight- and distance-based shipping, x1.5 for express, free with FREESHIP."""
        return float(self._shipping())

    def calculate_total(self) -> Dict[str, float]:
        """Return the full breakdown: subtotal, discount, tax, shipping and total."""
        subtotal, discount = self._subtotal(), self._discount()
        tax, shipping = self._tax(), self._shipping()
        return {
            "subtotal": float(subtotal),
            "discount": float(discount),
            "tax": float(tax),
            "shipping": float(shipping),
            "total": float(subtotal - discount + tax + shipping),
        }
