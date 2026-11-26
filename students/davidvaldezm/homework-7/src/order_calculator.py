"""Calculate an order in dollars using decimal arithmetic."""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

CENT = Decimal("0.01")
DISCOUNTS = {
    "SAVE10": (50, Decimal("0.10")),
    "SAVE20": (100, Decimal("0.20")),
    "NEWUSER": (0, Decimal("0.15")),
    "FREESHIP": (0, Decimal("0")),
}


def _nonnegative(value, field):
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise ValueError(f"{field} must be a finite, nonnegative number") from error
    if not amount.is_finite() or amount < 0:
        raise ValueError(f"{field} must be a finite, nonnegative number")
    return amount


def _money(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


class Order:
    """An order with one optional discount code and configurable shipping."""

    def __init__(self, items, customer_type="regular"):
        self.items = items
        self.customer_type = customer_type
        self.discount_code = None
        self.shipping_distance = Decimal(0)
        self.is_express = False
        self._lines = []
        for item in items:
            quantity = item["quantity"]
            if (
                not isinstance(quantity, int)
                or isinstance(quantity, bool)
                or quantity < 0
            ):
                raise ValueError("quantity must be a nonnegative integer")
            price = _nonnegative(item["price"], "price")
            weight = _nonnegative(item["weight"], "weight")
            self._lines.append((price * quantity, weight * quantity))

    def apply_discount(self, code):
        """Apply an eligible code and preserve any prior code on failure."""
        if code not in DISCOUNTS:
            return False
        if code == "NEWUSER" and self.customer_type != "new":
            return False
        minimum, _ = DISCOUNTS[code]
        if minimum and self._subtotal() <= minimum:
            return False
        self.discount_code = code
        return True

    def set_shipping(self, distance_km, is_express=False):
        """Set distance and delivery speed."""
        self.shipping_distance = _nonnegative(distance_km, "distance")
        self.is_express = is_express

    def _subtotal(self):
        return sum((price for price, _ in self._lines), Decimal(0))

    def _discount(self):
        rate = DISCOUNTS.get(self.discount_code, (0, Decimal(0)))[1]
        return _money(self._subtotal() * rate)

    def _tax(self):
        return _money((self._subtotal() - self._discount()) * Decimal("0.08"))

    def _shipping(self):
        if self.discount_code == "FREESHIP":
            return Decimal(0)
        weight = sum(weight for _, weight in self._lines)
        base = weight * Decimal("0.50") + self.shipping_distance * Decimal("0.10")
        return _money(base * Decimal("1.5") if self.is_express else base)

    def calculate_subtotal(self):
        """Return the merchandise subtotal."""
        return float(_money(self._subtotal()))

    def calculate_discount(self):
        """Return the merchandise discount."""
        return float(self._discount())

    def calculate_tax(self):
        """Return tax on the discounted merchandise."""
        return float(self._tax())

    def calculate_shipping(self):
        """Return the shipping charge."""
        return float(self._shipping())

    def calculate_total(self):
        """Return the amount due and its breakdown in dollars."""
        subtotal = _money(self._subtotal())
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
