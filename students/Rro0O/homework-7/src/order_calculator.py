"""Order calculator for the e-commerce order processing system.

All money arithmetic uses :class:`decimal.Decimal` and is rounded half-up to
cents, so results never suffer from binary floating point drift.
"""

from decimal import ROUND_HALF_UP, Decimal
from typing import Dict, List, Optional

TAX_RATE = Decimal("0.08")
WEIGHT_RATE_PER_KG = Decimal("0.50")
DISTANCE_RATE_PER_KM = Decimal("0.10")
EXPRESS_MULTIPLIER = Decimal("1.5")
CENT = Decimal("0.01")

# code -> minimum subtotal (inclusive) and percentage discount
VALID_CODES = {
    "SAVE10": {"min_order": 50, "discount_pct": Decimal("0.10")},
    "SAVE20": {"min_order": 100, "discount_pct": Decimal("0.20")},
    "FREESHIP": {"min_order": 0, "discount_pct": Decimal("0")},
    "NEWUSER": {"min_order": 0, "discount_pct": Decimal("0.15")},
}


def _money(value: Decimal) -> Decimal:
    """Round a Decimal to cents (half up)."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def _dec(value) -> Decimal:
    """Convert a number to Decimal through ``str`` to avoid float noise."""
    return Decimal(str(value))


class Order:
    """A customer order with items, an optional discount and shipping data."""

    def __init__(self, items: List[Dict], customer_type: str = "regular"):
        """Initialize an order.

        Args:
            items: list of {"name", "price", "quantity", "weight"} dicts.
            customer_type: "new" or "regular".
        """
        self.items = items
        self.customer_type = customer_type
        self.discount_code: Optional[str] = None
        self.shipping_distance = 0
        self.is_express = False

    # ------------------------------------------------------------------
    # configuration
    # ------------------------------------------------------------------
    def apply_discount(self, code: str) -> bool:
        """Apply a discount code. Return True when the code is accepted.

        A code is rejected (and any previous code is kept) when it is unknown,
        when the subtotal is below its minimum, or when NEWUSER is used by a
        customer that is not new.
        """
        rule = VALID_CODES.get(code)
        if rule is None:
            return False
        if self.calculate_subtotal() < rule["min_order"]:
            return False
        if code == "NEWUSER" and self.customer_type != "new":
            return False
        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False):
        """Set shipping parameters."""
        if distance_km < 0:
            raise ValueError("distance must not be negative")
        self.shipping_distance = distance_km
        self.is_express = is_express

    # ------------------------------------------------------------------
    # calculations
    # ------------------------------------------------------------------
    def _subtotal(self) -> Decimal:
        total = Decimal("0")
        for item in self.items:
            price = _dec(item["price"])
            quantity = _dec(item["quantity"])
            if price < 0:
                raise ValueError(f"negative price for {item.get('name')}")
            if quantity < 0:
                raise ValueError(f"negative quantity for {item.get('name')}")
            total += price * quantity
        return total

    def _discount(self) -> Decimal:
        if self.discount_code is None:
            return Decimal("0")
        pct = VALID_CODES[self.discount_code]["discount_pct"]
        return self._subtotal() * pct

    def _shipping(self) -> Decimal:
        if self.discount_code == "FREESHIP":
            return Decimal("0")
        weight = Decimal("0")
        for item in self.items:
            item_weight = _dec(item.get("weight", 0))
            if item_weight < 0:
                raise ValueError(f"negative weight for {item.get('name')}")
            weight += item_weight * _dec(item["quantity"])
        base = weight * WEIGHT_RATE_PER_KG
        base += _dec(self.shipping_distance) * DISTANCE_RATE_PER_KM
        if self.is_express:
            base *= EXPRESS_MULTIPLIER
        return base

    def calculate_subtotal(self) -> float:
        """Sum of price x quantity for every item."""
        return float(_money(self._subtotal()))

    def calculate_discount(self) -> float:
        """Discount amount for the applied code (0 when none)."""
        return float(_money(self._discount()))

    def calculate_tax(self) -> float:
        """Tax: 8% of (subtotal - discount)."""
        taxable = self._subtotal() - self._discount()
        return float(_money(taxable * TAX_RATE))

    def calculate_shipping(self) -> float:
        """Shipping: weight + distance, x1.5 if express, free with FREESHIP."""
        return float(_money(self._shipping()))

    def calculate_total(self) -> Dict[str, float]:
        """Return the full breakdown. Total = subtotal - discount + tax + shipping."""
        subtotal = _money(self._subtotal())
        discount = _money(self._discount())
        tax = _money((self._subtotal() - self._discount()) * TAX_RATE)
        shipping = _money(self._shipping())
        total = subtotal - discount + tax + shipping
        return {
            "subtotal": float(subtotal),
            "discount": float(discount),
            "tax": float(tax),
            "shipping": float(shipping),
            "total": float(total),
        }
