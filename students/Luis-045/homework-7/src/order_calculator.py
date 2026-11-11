"""Calculate monetary amounts with decimal arithmetic and cent rounding."""

from copy import deepcopy
from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")
ZERO = Decimal("0")
DISCOUNTS = {
    "SAVE10": (Decimal("50"), Decimal("0.10")),
    "SAVE20": (Decimal("100"), Decimal("0.20")),
    "FREESHIP": (ZERO, ZERO),
    "NEWUSER": (ZERO, Decimal("0.15")),
}


def nonnegative_number(value: object, field: str) -> Decimal:
    """Reject booleans, nonnumeric values, infinities and negative amounts."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError(f"{field} must be a finite non-negative number")
    number = Decimal(str(value))
    if not number.is_finite() or number < 0:
        raise ValueError(f"{field} must be a finite non-negative number")
    return number


def money(value: Decimal) -> Decimal:
    """Round half cents upward, consistently across all monetary components."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


class Order:
    """One order with a single discount code and configurable shipping."""

    def __init__(self, items: list[dict], customer_type: str = "regular"):
        if customer_type not in ("new", "regular"):
            raise ValueError("customer_type must be new or regular")
        if not isinstance(items, list):
            raise ValueError("items must be a list")
        self.items = deepcopy(items)
        for item in self.items:
            self._validate_item(item)
        self.customer_type = customer_type
        self.discount_code = None
        self.shipping_distance = ZERO
        self.is_express = False

    @staticmethod
    def _validate_item(item: dict) -> None:
        if not isinstance(item, dict):
            raise ValueError("each item must be an object")
        if not isinstance(item.get("name"), str) or not item["name"].strip():
            raise ValueError("item name must be a non-empty string")
        nonnegative_number(item.get("price"), "price")
        nonnegative_number(item.get("weight"), "weight")
        quantity = item.get("quantity")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
            raise ValueError("quantity must be a non-negative integer")

    def apply_discount(self, code: str) -> bool:
        """Apply an eligible code; rejected codes leave the current code intact."""
        if not isinstance(code, str) or code not in DISCOUNTS:
            return False
        minimum, _ = DISCOUNTS[code]
        if self._subtotal() < minimum:
            return False
        if code == "NEWUSER" and self.customer_type != "new":
            return False
        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False) -> None:
        """Configure a non-negative distance and a strictly boolean service flag."""
        distance = nonnegative_number(distance_km, "distance_km")
        if not isinstance(is_express, bool):
            raise ValueError("is_express must be a boolean")
        self.shipping_distance = distance
        self.is_express = is_express

    def _subtotal(self) -> Decimal:
        return money(
            sum(
                (Decimal(str(item["price"])) * item["quantity"] for item in self.items),
                ZERO,
            )
        )

    def calculate_subtotal(self) -> float:
        """Return the sum of item prices times quantities, rounded to cents."""
        return float(self._subtotal())

    def _discount(self, subtotal: Decimal) -> Decimal:
        percentage = DISCOUNTS[self.discount_code][1] if self.discount_code else ZERO
        return money(subtotal * percentage)

    def calculate_discount(self) -> float:
        """Return the discount amount, rounded to cents."""
        return float(self._discount(self._subtotal()))

    @staticmethod
    def _tax(discounted_subtotal: Decimal) -> Decimal:
        return money(discounted_subtotal * Decimal("0.08"))

    def calculate_tax(self) -> float:
        """Return 8% tax on the subtotal after discount."""
        subtotal = self._subtotal()
        return float(self._tax(subtotal - self._discount(subtotal)))

    def _shipping(self) -> Decimal:
        if self.discount_code == "FREESHIP":
            return ZERO
        weight = sum(
            (Decimal(str(item["weight"])) * item["quantity"] for item in self.items),
            ZERO,
        )
        base = weight * Decimal("0.50") + self.shipping_distance * Decimal("0.10")
        return money(base * (Decimal("1.5") if self.is_express else 1))

    def calculate_shipping(self) -> float:
        """Charge per-unit weight and distance; express multiplies both charges."""
        return float(self._shipping())

    def calculate_total(self) -> dict[str, float]:
        """Return the rounded subtotal, discount, tax, shipping and final total."""
        subtotal = self._subtotal()
        discount = self._discount(subtotal)
        net = subtotal - discount
        tax = self._tax(net)
        shipping = self._shipping()
        return {
            "subtotal": float(subtotal),
            "discount": float(discount),
            "tax": float(tax),
            "shipping": float(shipping),
            "total": float(net + tax + shipping),
        }
