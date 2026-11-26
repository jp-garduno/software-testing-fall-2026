"""Order calculator: subtotal, discount, tax, shipping and total for an e-commerce order."""

from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Dict, List, Optional

from src.discounts import DISCOUNT_RULES, is_code_applicable

TAX_RATE = Decimal("0.08")
WEIGHT_RATE = Decimal("0.50")  # per kg
DISTANCE_RATE = Decimal("0.10")  # per km
EXPRESS_MULTIPLIER = Decimal("1.5")
CUSTOMER_TYPES = ("new", "regular")
_CENT = Decimal("0.01")


def _dec(value: Any) -> Decimal:
    return Decimal(str(value))


def _money(value: Decimal) -> Decimal:
    """Round to cents, half up (0.005 -> 0.01)."""
    return value.quantize(_CENT, rounding=ROUND_HALF_UP)


def _validate_items(items: List[Dict[str, Any]]) -> None:
    for index, item in enumerate(items):
        for field in ("price", "quantity"):
            if field not in item:
                raise ValueError(f"Item {index} is missing '{field}'")
        if not isinstance(item["quantity"], int) or isinstance(item["quantity"], bool):
            raise ValueError(f"Item {index}: quantity must be an integer")
        for field in ("price", "quantity", "weight"):
            if item.get(field, 0) < 0:
                raise ValueError(f"Item {index}: {field} cannot be negative")


class Order:
    """An order with items, an optional discount code and shipping parameters."""

    def __init__(self, items: List[Dict[str, Any]], customer_type: str = "regular"):
        """
        Initialize order.

        Args:
            items: List of {"name": str, "price": float, "quantity": int, "weight": float (kg, per unit)}.
            customer_type: "new" or "regular".

        Raises:
            ValueError: negative price/quantity/weight, non-integer quantity or unknown customer type.
        """
        if customer_type not in CUSTOMER_TYPES:
            raise ValueError(f"Unknown customer type: {customer_type!r}")
        _validate_items(items)
        self.items = items
        self.customer_type = customer_type
        self.discount_code: Optional[str] = None
        self.shipping_distance: float = 0
        self.is_express = False

    def apply_discount(self, code: str) -> bool:
        """Apply a discount code; return True if valid. An invalid code leaves the order unchanged."""
        if not is_code_applicable(code, self._subtotal(), self.customer_type):
            return False
        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False) -> None:
        """Set shipping parameters. Raises ValueError for a negative distance."""
        if distance_km < 0:
            raise ValueError("Shipping distance cannot be negative")
        self.shipping_distance = distance_km
        self.is_express = is_express

    def _subtotal(self) -> Decimal:
        return _money(
            sum((_dec(i["price"]) * i["quantity"] for i in self.items), Decimal("0"))
        )

    def _discount(self) -> Decimal:
        if self.discount_code is None:
            return Decimal("0.00")
        return _money(
            self._subtotal() * DISCOUNT_RULES[self.discount_code]["discount_pct"]
        )

    def _tax(self) -> Decimal:
        return _money((self._subtotal() - self._discount()) * TAX_RATE)

    def _shipping(self) -> Decimal:
        if self.discount_code == "FREESHIP":
            return Decimal("0.00")
        weight = sum(
            (_dec(i.get("weight", 0)) * i["quantity"] for i in self.items), Decimal("0")
        )
        base = weight * WEIGHT_RATE + _dec(self.shipping_distance) * DISTANCE_RATE
        return _money(base * EXPRESS_MULTIPLIER if self.is_express else base)

    def calculate_subtotal(self) -> float:
        """Sum of price x quantity of all items."""
        return float(self._subtotal())

    def calculate_discount(self) -> float:
        """Discount amount (0 when no code applied or for FREESHIP)."""
        return float(self._discount())

    def calculate_tax(self) -> float:
        """Tax: 8% of (subtotal - discount)."""
        return float(self._tax())

    def calculate_shipping(self) -> float:
        """Shipping: 0.50/kg (weight x quantity) + 0.10/km, x1.5 if express, 0 with FREESHIP."""
        return float(self._shipping())

    def calculate_total(self) -> Dict[str, float]:
        """Return {"subtotal", "discount", "tax", "shipping", "total"}, every value rounded to 2 decimals."""
        subtotal, discount, tax, shipping = (
            self._subtotal(),
            self._discount(),
            self._tax(),
            self._shipping(),
        )
        return {
            "subtotal": float(subtotal),
            "discount": float(discount),
            "tax": float(tax),
            "shipping": float(shipping),
            "total": float(subtotal - discount + tax + shipping),
        }
