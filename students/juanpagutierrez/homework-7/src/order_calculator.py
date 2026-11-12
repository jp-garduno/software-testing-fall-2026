"""Order calculator: subtotal, discounts, tax, shipping and total.

Rules (Homework 7, Part 1):

* Subtotal  = sum of price x quantity for every item.
* Discounts = SAVE10 (10% from $50), SAVE20 (20% from $100), FREESHIP (free
  shipping), NEWUSER (15% for customer_type "new"). Unknown or expired codes
  give no discount.
* Tax       = 8% of (subtotal - discount).
* Shipping  = $0.50 per kg of total weight + $0.10 per km, x1.5 for express,
  and $0 when FREESHIP is applied.
* Total     = subtotal - discount + tax + shipping.

Every amount is rounded to cents with ROUND_HALF_UP, and the total is built
from the rounded parts so the breakdown always adds up exactly.
"""

from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from typing import Dict, List, Optional

CENT = Decimal("0.01")
TAX_RATE = Decimal("0.08")
RATE_PER_KG = Decimal("0.50")
RATE_PER_KM = Decimal("0.10")
EXPRESS_MULTIPLIER = Decimal("1.5")

# min_order is inclusive: an order of exactly $50.00 qualifies for SAVE10.
DISCOUNT_CODES = {
    "SAVE10": {"min_order": Decimal("50"), "discount_pct": Decimal("0.10")},
    "SAVE20": {"min_order": Decimal("100"), "discount_pct": Decimal("0.20")},
    "FREESHIP": {"min_order": Decimal("0"), "discount_pct": Decimal("0")},
    "NEWUSER": {"min_order": Decimal("0"), "discount_pct": Decimal("0.15"), "customer_type": "new"},
    # Expired campaign codes stay in the table so they can be reported as such.
    "SUMMER25": {"min_order": Decimal("0"), "discount_pct": Decimal("0.25"), "expires": date(2025, 8, 31)},
    "BLACKFRIDAY": {"min_order": Decimal("0"), "discount_pct": Decimal("0.30"), "expires": date(2025, 11, 30)},
}

CUSTOMER_TYPES = ("new", "regular")
REQUIRED_ITEM_FIELDS = ("name", "price", "quantity", "weight")


def to_cents(value: Decimal) -> Decimal:
    """Round a Decimal amount to two decimals, half up."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def _as_decimal(value) -> Decimal:
    # str() first so 0.1 becomes Decimal("0.1") and not its binary expansion.
    return Decimal(str(value))


def _validate_item(item: Dict) -> None:
    missing = [field for field in REQUIRED_ITEM_FIELDS if field not in item]
    if missing:
        raise ValueError(f"Item is missing fields: {', '.join(missing)}")
    for field in ("price", "quantity", "weight"):
        if isinstance(item[field], bool) or not isinstance(item[field], (int, float)):
            raise ValueError(f"Item {field} must be a number")
        if item[field] < 0:
            raise ValueError(f"Item {field} cannot be negative")
    if int(item["quantity"]) != item["quantity"]:
        raise ValueError("Item quantity must be a whole number")


class Order:
    """A shopping cart that can price itself."""

    def __init__(self, items: List[Dict], customer_type: str = "regular"):
        """
        Initialize order.

        Args:
            items: List of {"name": str, "price": float, "quantity": int, "weight": float}.
                Weight is per unit, in kg. Zero quantities are allowed and add nothing.
            customer_type: "new" or "regular".

        Raises:
            ValueError: if an item is malformed or has a negative value, or the
                customer type is unknown.
        """
        if customer_type not in CUSTOMER_TYPES:
            raise ValueError(f"Unknown customer type: {customer_type}")
        for item in items:
            _validate_item(item)
        self.items = items
        self.customer_type = customer_type
        self.discount_code: Optional[str] = None
        self.shipping_distance = 0
        self.is_express = False

    def apply_discount(self, code: str, on_date: Optional[date] = None) -> bool:
        """
        Apply a discount code and return True if it was accepted.

        Codes are case-insensitive. A rejected code leaves any previously
        accepted code in place; an accepted one replaces it (codes do not stack).

        Args:
            code: The code typed by the customer.
            on_date: Date used to check expiration, today by default.
        """
        if not code:
            return False
        code = code.strip().upper()
        rule = DISCOUNT_CODES.get(code)
        if rule is None:
            return False
        if "expires" in rule and (on_date or date.today()) > rule["expires"]:
            return False
        if "customer_type" in rule and rule["customer_type"] != self.customer_type:
            return False
        if self._raw_subtotal() < rule["min_order"]:
            return False
        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False):
        """Set shipping parameters. Distance must not be negative."""
        if distance_km < 0:
            raise ValueError("Shipping distance cannot be negative")
        self.shipping_distance = distance_km
        self.is_express = is_express

    def total_weight(self) -> Decimal:
        """Total shipped weight in kg (unit weight x quantity)."""
        return sum((_as_decimal(i["weight"]) * _as_decimal(i["quantity"]) for i in self.items), Decimal("0"))

    def _raw_subtotal(self) -> Decimal:
        return sum((_as_decimal(i["price"]) * _as_decimal(i["quantity"]) for i in self.items), Decimal("0"))

    def calculate_subtotal(self) -> float:
        """Calculate subtotal (sum of item price x quantity)."""
        return float(to_cents(self._raw_subtotal()))

    def calculate_discount(self) -> float:
        """Calculate the discount amount for the applied code (0 when none)."""
        return float(self._discount())

    def calculate_tax(self) -> float:
        """Calculate tax (8% of subtotal after discount)."""
        return float(self._tax())

    def calculate_shipping(self) -> float:
        """Calculate shipping cost."""
        return float(self._shipping())

    def calculate_total(self) -> Dict[str, float]:
        """
        Calculate order total with breakdown.

        Returns:
            {"subtotal": float, "discount": float, "tax": float, "shipping": float, "total": float}
        """
        subtotal = to_cents(self._raw_subtotal())
        discount = self._discount()
        tax = self._tax()
        shipping = self._shipping()
        return {
            "subtotal": float(subtotal),
            "discount": float(discount),
            "tax": float(tax),
            "shipping": float(shipping),
            "total": float(subtotal - discount + tax + shipping),
        }

    def _discount(self) -> Decimal:
        if self.discount_code is None:
            return Decimal("0.00")
        pct = DISCOUNT_CODES[self.discount_code]["discount_pct"]
        return to_cents(to_cents(self._raw_subtotal()) * pct)

    def _tax(self) -> Decimal:
        return to_cents((to_cents(self._raw_subtotal()) - self._discount()) * TAX_RATE)

    def _shipping(self) -> Decimal:
        if self.discount_code == "FREESHIP":
            return Decimal("0.00")
        base = self.total_weight() * RATE_PER_KG + _as_decimal(self.shipping_distance) * RATE_PER_KM
        if self.is_express:
            base *= EXPRESS_MULTIPLIER
        return to_cents(base)
