"""Order calculator for the e-commerce order processing system.

Calculation rules (homework 7, part 1):

* Subtotal  = sum(price x quantity) of every item.
* Discounts = SAVE10 (10%, subtotal >= $50), SAVE20 (20%, subtotal >= $100),
              FREESHIP (free shipping, no money off), NEWUSER (15%, only for "new" customers).
              Unknown codes or codes whose minimum is not met give no discount.
* Tax       = 8% of (subtotal - discount).
* Shipping  = $4.00 base + $0.50 per kg + $0.10 per km; express multiplies it by 1.5;
              FREESHIP makes it 0. An order with no units to ship pays no shipping.
* Total     = subtotal - discount + tax + shipping.

Money is handled with Decimal and every component is rounded to cents (half up), so
the expected values in the CSV files can be written by hand without float noise.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Dict, List, Optional

CENT = Decimal("0.01")
TAX_RATE = Decimal("0.08")
BASE_SHIPPING_FEE = Decimal("4.00")  # derived from the assignment's own example row (5.50 for 1 kg / 10 km)
RATE_PER_KG = Decimal("0.50")
RATE_PER_KM = Decimal("0.10")
EXPRESS_MULTIPLIER = Decimal("1.5")
CUSTOMER_TYPES = ("new", "regular")

# code -> (minimum subtotal, discount percentage, customer type required or None)
DISCOUNT_CODES = {
    "SAVE10": (Decimal("50"), Decimal("0.10"), None),
    "SAVE20": (Decimal("100"), Decimal("0.20"), None),
    "FREESHIP": (Decimal("0"), Decimal("0"), None),
    "NEWUSER": (Decimal("0"), Decimal("0.15"), "new"),
}


class InvalidOrderError(ValueError):
    """Raised when an order, an item or the shipping data is not valid."""


def to_money(value: Decimal) -> Decimal:
    """Round a Decimal to cents, half up (12.345 -> 12.35)."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def _number(value, field: str, item_name: str) -> Decimal:
    """Convert an item field to Decimal, rejecting booleans, text and negatives."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise InvalidOrderError(f"Item '{item_name}': {field} must be a number")
    number = Decimal(str(value))
    if number < 0:
        raise InvalidOrderError(f"Item '{item_name}': {field} cannot be negative")
    return number


class Order:
    """A shopping cart that knows how to price itself."""

    def __init__(self, items: List[Dict], customer_type: str = "regular") -> None:
        """
        Args:
            items: list of {"name": str, "price": number, "quantity": int, "weight": number (kg)}
            customer_type: "new" or "regular"
        """
        if customer_type not in CUSTOMER_TYPES:
            raise InvalidOrderError(f"Invalid customer type: {customer_type!r}")
        if not isinstance(items, list):
            raise InvalidOrderError("Items must be a list")
        self.items = [self._parse_item(item) for item in items]
        self.customer_type = customer_type
        self.discount_code: Optional[str] = None
        self.shipping_distance = Decimal("0")
        self.is_express = False

    @staticmethod
    def _parse_item(item: Dict) -> Dict:
        """Validate one item and normalise its numbers to Decimal."""
        if not isinstance(item, dict):
            raise InvalidOrderError("Each item must be an object")
        name = str(item.get("name", "")).strip()
        if not name:
            raise InvalidOrderError("Item name is required")
        quantity = item.get("quantity", 1)
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise InvalidOrderError(f"Item '{name}': quantity must be a whole number")
        return {
            "name": name,
            "price": _number(item.get("price"), "price", name),
            "quantity": _number(quantity, "quantity", name),
            "weight": _number(item.get("weight", 0), "weight", name),
        }

    # ------------------------------------------------------------------ #
    # Configuration
    # ------------------------------------------------------------------ #
    def apply_discount(self, code: Optional[str]) -> bool:
        """Apply a discount code. Returns False (and keeps the previous code) when it is not valid."""
        if not code:
            return False
        normalized = code.strip().upper()
        if normalized not in DISCOUNT_CODES:
            return False
        minimum, _, required_customer = DISCOUNT_CODES[normalized]
        if required_customer and self.customer_type != required_customer:
            return False
        if self._subtotal() < minimum:
            return False
        self.discount_code = normalized
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False) -> None:
        """Set the delivery distance (km) and the shipping speed."""
        if isinstance(distance_km, bool) or not isinstance(distance_km, (int, float, Decimal)):
            raise InvalidOrderError("Distance must be a number")
        distance = Decimal(str(distance_km))
        if distance < 0:
            raise InvalidOrderError("Distance cannot be negative")
        self.shipping_distance = distance
        self.is_express = bool(is_express)

    # ------------------------------------------------------------------ #
    # Calculations (Decimal internally, float in the public API)
    # ------------------------------------------------------------------ #
    def _subtotal(self) -> Decimal:
        return to_money(sum((item["price"] * item["quantity"] for item in self.items), Decimal("0")))

    def _discount(self) -> Decimal:
        if self.discount_code is None:
            return Decimal("0.00")
        _, percentage, _ = DISCOUNT_CODES[self.discount_code]
        return to_money(self._subtotal() * percentage)

    def _tax(self) -> Decimal:
        return to_money((self._subtotal() - self._discount()) * TAX_RATE)

    def total_weight(self) -> Decimal:
        """Total weight in kg (weight x quantity of every item)."""
        return sum((item["weight"] * item["quantity"] for item in self.items), Decimal("0"))

    def _shipping(self) -> Decimal:
        units = sum((item["quantity"] for item in self.items), Decimal("0"))
        if units == 0 or self.discount_code == "FREESHIP":
            return Decimal("0.00")
        base = BASE_SHIPPING_FEE + self.total_weight() * RATE_PER_KG + self.shipping_distance * RATE_PER_KM
        if self.is_express:
            base *= EXPRESS_MULTIPLIER
        return to_money(base)

    def calculate_subtotal(self) -> float:
        """Sum of price x quantity."""
        return float(self._subtotal())

    def calculate_discount(self) -> float:
        """Money taken off by the applied discount code."""
        return float(self._discount())

    def calculate_tax(self) -> float:
        """8% of the subtotal after discount."""
        return float(self._tax())

    def calculate_shipping(self) -> float:
        """Shipping cost after express and FREESHIP rules."""
        return float(self._shipping())

    def calculate_total(self) -> Dict[str, float]:
        """Full breakdown: subtotal, discount, tax, shipping and total."""
        subtotal, discount, tax, shipping = self._subtotal(), self._discount(), self._tax(), self._shipping()
        return {
            "subtotal": float(subtotal),
            "discount": float(discount),
            "tax": float(tax),
            "shipping": float(shipping),
            "total": float(subtotal - discount + tax + shipping),
        }
