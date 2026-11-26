from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from numbers import Real

CENT = Decimal("0.01")
TAX_RATE = Decimal("0.08")
RATE_PER_KG = Decimal("0.50")
RATE_PER_KM = Decimal("0.10")
EXPRESS_MULTIPLIER = Decimal("1.5")
CUSTOMER_TYPES = ("new", "regular")
ITEM_FIELDS = ("name", "price", "quantity", "weight")


@dataclass(frozen=True)
class DiscountCode:
    """A discount code; min_order is inclusive and expires_on is the last day the code is accepted."""

    min_order: Decimal
    discount_pct: Decimal
    free_shipping: bool = False
    new_customers_only: bool = False
    expires_on: date | None = None


DISCOUNT_CODES = {
    "SAVE10": DiscountCode(min_order=Decimal("50"), discount_pct=Decimal("0.10")),
    "SAVE20": DiscountCode(min_order=Decimal("100"), discount_pct=Decimal("0.20")),
    "FREESHIP": DiscountCode(min_order=Decimal("0"), discount_pct=Decimal("0"), free_shipping=True),
    "NEWUSER": DiscountCode(min_order=Decimal("0"), discount_pct=Decimal("0.15"), new_customers_only=True),
    "SUMMER25": DiscountCode(min_order=Decimal("0"), discount_pct=Decimal("0.25"), expires_on=date(2026, 8, 31)),
}


def _is_number(value):
    return isinstance(value, Real) and not isinstance(value, bool)


def _to_decimal(value):
    return Decimal(str(value))


def _to_cents(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def _validated_item(item):
    for field in ITEM_FIELDS:
        if field not in item:
            raise ValueError(f"Item is missing the {field} field")
    name = item["name"]
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Item name is required")
    if not isinstance(item["quantity"], int) or isinstance(item["quantity"], bool):
        raise ValueError(f"Item {name!r}: quantity must be a whole number")
    for field in ("price", "quantity", "weight"):
        if not _is_number(item[field]):
            raise ValueError(f"Item {name!r}: {field} must be a number")
        if item[field] < 0:
            raise ValueError(f"Item {name!r}: {field} cannot be negative")
    return dict(item)


class Order:
    """An order whose money amounts are computed in Decimal and rounded half up to the cent."""

    def __init__(self, items, customer_type="regular", order_date=None):
        if customer_type not in CUSTOMER_TYPES:
            raise ValueError(f"Unknown customer type: {customer_type}")
        if not items:
            raise ValueError("An order needs at least one item")
        self.items = [_validated_item(item) for item in items]
        self.customer_type = customer_type
        self.order_date = order_date or date.today()
        self.discount_code = None
        self.shipping_distance = Decimal("0")
        self.is_express = False

    def apply_discount(self, code):
        """Apply a code, case-insensitively; return False and keep the current code if it does not qualify."""
        normalized = code.strip().upper() if isinstance(code, str) else ""
        discount = DISCOUNT_CODES.get(normalized)
        if discount is None or not self._qualifies_for(discount):
            return False
        self.discount_code = normalized
        return True

    def set_shipping(self, distance_km, is_express=False):
        if not _is_number(distance_km):
            raise ValueError("Distance must be a number")
        if distance_km < 0:
            raise ValueError("Distance cannot be negative")
        self.shipping_distance = _to_decimal(distance_km)
        self.is_express = bool(is_express)

    def calculate_subtotal(self):
        return float(self._subtotal())

    def calculate_discount(self):
        return float(self._discount())

    def calculate_tax(self):
        return float(self._tax())

    def calculate_shipping(self):
        return float(self._shipping())

    def calculate_total(self):
        """Return subtotal, discount, tax, shipping and total; the total is the sum of the rounded parts."""
        subtotal, discount, tax, shipping = self._subtotal(), self._discount(), self._tax(), self._shipping()
        return {
            "subtotal": float(subtotal),
            "discount": float(discount),
            "tax": float(tax),
            "shipping": float(shipping),
            "total": float(subtotal - discount + tax + shipping),
        }

    def _qualifies_for(self, discount):
        if discount.expires_on is not None and self.order_date > discount.expires_on:
            return False
        if discount.new_customers_only and self.customer_type != "new":
            return False
        return self._subtotal() >= discount.min_order

    def _active_discount(self):
        return DISCOUNT_CODES[self.discount_code] if self.discount_code else None

    def _subtotal(self):
        return _to_cents(sum((_to_decimal(item["price"]) * item["quantity"] for item in self.items), Decimal("0")))

    def _discount(self):
        discount = self._active_discount()
        if discount is None:
            return Decimal("0.00")
        return _to_cents(self._subtotal() * discount.discount_pct)

    def _tax(self):
        return _to_cents((self._subtotal() - self._discount()) * TAX_RATE)

    def _shipping(self):
        discount = self._active_discount()
        if discount is not None and discount.free_shipping:
            return Decimal("0.00")
        weight = sum((_to_decimal(item["weight"]) * item["quantity"] for item in self.items), Decimal("0"))
        cost = weight * RATE_PER_KG + self.shipping_distance * RATE_PER_KM
        if self.is_express:
            cost *= EXPRESS_MULTIPLIER
        return _to_cents(cost)
