"""Order pricing rules for the data-driven testing assignment."""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any, Mapping, Sequence

CENT = Decimal("0.01")
TAX_RATE = Decimal("0.08")
WEIGHT_RATE = Decimal("0.50")
DISTANCE_RATE = Decimal("0.10")


def _decimal(value: Any, label: str) -> Decimal:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be a finite number")
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{label} must be a finite number") from None
    if not number.is_finite():
        raise ValueError(f"{label} must be a finite number")
    return number


def _money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def _float(value: Decimal) -> float:
    return float(_money(value))


class Order:
    """Calculate subtotal, discounts, tax, shipping, and total for an order."""

    def __init__(
        self, items: Sequence[Mapping[str, Any]], customer_type: str = "regular"
    ) -> None:
        if not isinstance(customer_type, str) or customer_type not in {
            "new",
            "regular",
        }:
            raise ValueError("customer_type must be 'new' or 'regular'")
        if (
            isinstance(items, (str, bytes))
            or not isinstance(items, Sequence)
            or not items
        ):
            raise ValueError("items must be a non-empty sequence")

        self.items: list[dict[str, Any]] = []
        for index, item in enumerate(items):
            if not isinstance(item, Mapping):
                raise ValueError(f"item {index} must be an object")
            name = item.get("name")
            if not isinstance(name, str) or not name.strip():
                raise ValueError(f"item {index} name is required")
            price = _decimal(item.get("price"), f"item {index} price")
            weight = _decimal(item.get("weight"), f"item {index} weight")
            quantity = item.get("quantity")
            if isinstance(quantity, bool) or not isinstance(quantity, int):
                raise ValueError(f"item {index} quantity must be an integer")
            if price < 0 or weight < 0 or quantity < 0:
                raise ValueError(f"item {index} values cannot be negative")
            self.items.append(
                {
                    "name": name.strip(),
                    "price": price,
                    "quantity": quantity,
                    "weight": weight,
                }
            )

        self.customer_type = customer_type
        self.discount_code: str | None = None
        self.shipping_distance = Decimal("0")
        self.is_express = False

    def apply_discount(self, code: str) -> bool:
        """Store a valid discount code; return False and clear prior codes otherwise."""
        self.discount_code = None
        if not isinstance(code, str):
            return False

        subtotal = self.calculate_subtotal()
        if code == "SAVE10" and subtotal > Decimal("50.00"):
            self.discount_code = code
        elif code == "SAVE20" and subtotal > Decimal("100.00"):
            self.discount_code = code
        elif code == "FREESHIP":
            self.discount_code = code
        elif code == "NEWUSER" and self.customer_type == "new":
            self.discount_code = code
        return self.discount_code is not None

    def set_shipping(self, distance_km: float, is_express: bool = False) -> None:
        """Set non-negative shipping distance and shipping speed."""
        distance = _decimal(distance_km, "distance_km")
        if distance < 0:
            raise ValueError("distance_km cannot be negative")
        if not isinstance(is_express, bool):
            raise ValueError("is_express must be a boolean")
        self.shipping_distance = distance
        self.is_express = is_express

    def calculate_subtotal(self) -> Decimal:
        """Return the unrounded sum of all item prices multiplied by quantities."""
        return sum(
            (item["price"] * item["quantity"] for item in self.items), Decimal("0")
        )

    def calculate_discount(self) -> Decimal:
        """Return the rounded discount amount for the currently applied code."""
        percentages = {
            "SAVE10": Decimal("0.10"),
            "SAVE20": Decimal("0.20"),
            "NEWUSER": Decimal("0.15"),
        }
        percentage = percentages.get(self.discount_code)
        if percentage is None:
            return Decimal("0.00")
        return _money(self.calculate_subtotal() * percentage)

    def calculate_tax(self) -> Decimal:
        """Return 8% tax on the subtotal after discount, rounded to cents."""
        taxable_amount = self.calculate_subtotal() - self.calculate_discount()
        return _money(taxable_amount * TAX_RATE)

    def calculate_shipping(self) -> Decimal:
        """Return weight and distance shipping charges, including express uplift."""
        if self.discount_code == "FREESHIP":
            return Decimal("0.00")
        total_weight = sum(
            (item["weight"] * item["quantity"] for item in self.items),
            Decimal("0"),
        )
        shipping = total_weight * WEIGHT_RATE + self.shipping_distance * DISTANCE_RATE
        if self.is_express:
            shipping *= Decimal("1.5")
        return _money(shipping)

    def calculate_total(self) -> dict[str, float]:
        """Return a two-decimal breakdown of the order price."""
        subtotal = _money(self.calculate_subtotal())
        discount = self.calculate_discount()
        tax = self.calculate_tax()
        shipping = self.calculate_shipping()
        total = subtotal - discount + tax + shipping
        return {
            "subtotal": _float(subtotal),
            "discount": _float(discount),
            "tax": _float(tax),
            "shipping": _float(shipping),
            "total": _float(total),
        }
