"""Calculate e-commerce orders from the Homework 7 business rules."""

from decimal import Decimal, ROUND_HALF_UP


def money(value):
    """Round a Decimal amount to cents using commercial rounding."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def nonnegative(value):
    """Convert a finite nonnegative numeric value without binary-float drift."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError("Expected a nonnegative number")
    number = Decimal(str(value))
    if not number.is_finite() or number < 0:
        raise ValueError("Expected a nonnegative number")
    return number


class Order:
    """An order with validated items and a single replaceable discount code."""

    DISCOUNTS = {
        "SAVE10": Decimal("0.10"),
        "SAVE20": Decimal("0.20"),
        "NEWUSER": Decimal("0.15"),
        "FREESHIP": Decimal("0"),
    }

    def __init__(self, items, customer_type="regular"):
        if customer_type not in ("new", "regular") or not isinstance(items, list):
            raise ValueError("Invalid order")
        self.items = []
        for item in items:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("name"), str)
                or not item["name"].strip()
            ):
                raise ValueError("Invalid item")
            quantity = item.get("quantity")
            if (
                isinstance(quantity, bool)
                or not isinstance(quantity, int)
                or quantity < 0
            ):
                raise ValueError("Invalid quantity")
            self.items.append(
                {
                    "name": item["name"],
                    "quantity": quantity,
                    "price": nonnegative(item.get("price")),
                    "weight": nonnegative(item.get("weight")),
                }
            )
        self.customer_type = customer_type
        self.discount_code = None
        self.shipping_distance = Decimal("0")
        self.is_express = False

    def apply_discount(self, code):
        """Apply a qualifying code; reject and clear invalid/ineligible codes."""
        self.discount_code = None
        if not isinstance(code, str) or code not in self.DISCOUNTS:
            return False
        subtotal = self.calculate_subtotal()
        if code == "SAVE10" and subtotal <= 50:
            return False
        if code == "SAVE20" and subtotal <= 100:
            return False
        if code == "NEWUSER" and self.customer_type != "new":
            return False
        self.discount_code = code
        return True

    def set_shipping(self, distance_km, is_express=False):
        """Configure nonnegative distance and an explicit boolean service type."""
        if not isinstance(is_express, bool):
            raise ValueError("Express must be boolean")
        self.shipping_distance = nonnegative(distance_km)
        self.is_express = is_express

    def calculate_subtotal(self):
        """Sum each unit price multiplied by its quantity."""
        return money(
            sum((item["price"] * item["quantity"] for item in self.items), Decimal("0"))
        )

    def calculate_discount(self):
        """Calculate the selected percentage discount, rounded to cents."""
        return money(
            self.calculate_subtotal()
            * self.DISCOUNTS.get(self.discount_code, Decimal("0"))
        )

    def calculate_tax(self):
        """Tax the discounted merchandise subtotal at eight percent."""
        return money(
            (self.calculate_subtotal() - self.calculate_discount()) * Decimal("0.08")
        )

    def calculate_shipping(self):
        """Charge weight plus distance, with express or free-shipping rules."""
        if self.discount_code == "FREESHIP":
            return Decimal("0.00")
        weight = sum(
            (item["weight"] * item["quantity"] for item in self.items), Decimal("0")
        )
        base = weight * Decimal("0.50") + self.shipping_distance * Decimal("0.10")
        return money(base * (Decimal("1.5") if self.is_express else Decimal("1")))

    def calculate_total(self):
        """Return all monetary components as floats for the public API."""
        result = {
            "subtotal": self.calculate_subtotal(),
            "discount": self.calculate_discount(),
            "tax": self.calculate_tax(),
            "shipping": self.calculate_shipping(),
        }
        result["total"] = (
            result["subtotal"] - result["discount"] + result["tax"] + result["shipping"]
        )
        return {key: float(value) for key, value in result.items()}
