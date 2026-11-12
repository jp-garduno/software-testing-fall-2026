"""Order calculator for the e-commerce order processing system.

Business rules
--------------
* subtotal  = sum(price * quantity)
* discount  = percentage of the subtotal, if a valid code is applied
* tax       = 8% of (subtotal - discount)
* shipping  = (0.50 $/kg * total weight + 0.10 $/km * distance),
              x1.5 when express, $0 when FREESHIP is applied
* total     = subtotal - discount + tax + shipping

Design decisions (where the assignment text is ambiguous)
---------------------------------------------------------
* Money is computed with ``Decimal`` and rounded to cents (ROUND_HALF_UP)
  per component, so ``total`` is exactly the sum of the displayed parts.
* A code's minimum is inclusive: a $50.00 order qualifies for SAVE10
  (this follows the ``subtotal < min_order`` check in the starter code).
* NEWUSER is only valid for ``customer_type == "new"`` (first order).
* Codes are case-sensitive; unknown/lower-case codes are simply rejected.
* Total weight = sum(weight * quantity).
* Negative or non-numeric prices/quantities/weights/distances raise
  ``ValueError``.
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List

TAX_RATE = Decimal("0.08")
WEIGHT_RATE_PER_KG = Decimal("0.50")
DISTANCE_RATE_PER_KM = Decimal("0.10")
EXPRESS_MULTIPLIER = Decimal("1.5")
CENT = Decimal("0.01")

CUSTOMER_TYPES = ("new", "regular")

DISCOUNT_CODES = {
    "SAVE10": {"min_order": 50, "discount_pct": 0.10},
    "SAVE20": {"min_order": 100, "discount_pct": 0.20},
    "FREESHIP": {"min_order": 0, "discount_pct": 0},
    "NEWUSER": {"min_order": 0, "discount_pct": 0.15},
}


def _dec(value) -> Decimal:
    """Convert a number to Decimal through ``str`` (avoids float noise)."""
    return Decimal(str(value))


def _money(value: Decimal) -> Decimal:
    """Round to cents, half up."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def _is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate_items(items: List[Dict]) -> None:
    """Raise ValueError if the item list is malformed."""
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"item {index} must be a dict")
        price = item.get("price")
        quantity = item.get("quantity")
        weight = item.get("weight", 0)
        if not _is_number(price) or price < 0:
            raise ValueError(f"item {index}: price must be a number >= 0")
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 0:
            raise ValueError(f"item {index}: quantity must be an integer >= 0")
        if not _is_number(weight) or weight < 0:
            raise ValueError(f"item {index}: weight must be a number >= 0")


class Order:
    def __init__(self, items: List[Dict], customer_type: str = "regular"):
        """
        Initialize order

        Args:
            items: List of {"name": str, "price": float, "quantity": int, "weight": float}
            customer_type: "new" or "regular"
        """
        _validate_items(items)
        if customer_type not in CUSTOMER_TYPES:
            raise ValueError(f"customer_type must be one of {CUSTOMER_TYPES}")
        self.items = items
        self.customer_type = customer_type
        self.discount_code = None
        self.shipping_distance = 0
        self.is_express = False

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------
    def apply_discount(self, code: str) -> bool:
        """Apply discount code, return True if valid"""
        if code not in DISCOUNT_CODES:
            return False

        rule = DISCOUNT_CODES[code]
        if self._subtotal() < _dec(rule["min_order"]):
            return False
        if code == "NEWUSER" and self.customer_type != "new":
            return False

        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False):
        """Set shipping parameters"""
        if not _is_number(distance_km) or distance_km < 0:
            raise ValueError("distance_km must be a number >= 0")
        self.shipping_distance = distance_km
        self.is_express = bool(is_express)

    # ------------------------------------------------------------------
    # Internal exact (Decimal) computations
    # ------------------------------------------------------------------
    def _subtotal(self) -> Decimal:
        total = sum((_dec(i["price"]) * i["quantity"] for i in self.items), Decimal(0))
        return _money(total)

    def _discount(self) -> Decimal:
        if self.discount_code is None:
            return Decimal("0.00")
        pct = _dec(DISCOUNT_CODES[self.discount_code]["discount_pct"])
        return _money(self._subtotal() * pct)

    def _tax(self) -> Decimal:
        return _money((self._subtotal() - self._discount()) * TAX_RATE)

    def _shipping(self) -> Decimal:
        if self.discount_code == "FREESHIP":
            return Decimal("0.00")
        weight = sum((_dec(i.get("weight", 0)) * i["quantity"] for i in self.items), Decimal(0))
        base = weight * WEIGHT_RATE_PER_KG + _dec(self.shipping_distance) * DISTANCE_RATE_PER_KM
        if self.is_express:
            base *= EXPRESS_MULTIPLIER
        return _money(base)

    # ------------------------------------------------------------------
    # Public API (floats, rounded to cents)
    # ------------------------------------------------------------------
    def calculate_subtotal(self) -> float:
        """Calculate subtotal (sum of item prices x quantities)"""
        return float(self._subtotal())

    def calculate_discount(self) -> float:
        """Calculate discount amount"""
        return float(self._discount())

    def calculate_tax(self) -> float:
        """Calculate tax (8% of subtotal after discount)"""
        return float(self._tax())

    def calculate_shipping(self) -> float:
        """Calculate shipping cost"""
        return float(self._shipping())

    def calculate_total(self) -> Dict[str, float]:
        """
        Calculate order total with breakdown

        Returns:
            {
                "subtotal": float,
                "discount": float,
                "tax": float,
                "shipping": float,
                "total": float
            }
        """
        subtotal, discount = self._subtotal(), self._discount()
        tax, shipping = self._tax(), self._shipping()
        total = subtotal - discount + tax + shipping
        return {
            "subtotal": float(subtotal),
            "discount": float(discount),
            "tax": float(tax),
            "shipping": float(shipping),
            "total": float(total),
        }
