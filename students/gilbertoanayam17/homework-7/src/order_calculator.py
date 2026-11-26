"""Order totals for the e-commerce system: subtotal, discount, tax and shipping.

Every amount is rounded to cents (half up) as soon as it is calculated, and the
next amount is derived from the rounded one. The total is therefore always
exactly subtotal - discount + tax + shipping, as it would read on a receipt.
"""

from decimal import ROUND_HALF_UP, Decimal
from typing import Dict, Iterator, List, Tuple

TAX_RATE = Decimal("0.08")
RATE_PER_KG = Decimal("0.50")
RATE_PER_KM = Decimal("0.10")
EXPRESS_MULTIPLIER = Decimal("1.5")
FREE_SHIPPING_CODE = "FREESHIP"
NEW_CUSTOMER_CODE = "NEWUSER"

# min_order is inclusive: SAVE10 already applies to an order of exactly $50.
DISCOUNT_CODES = {
    "SAVE10": {"min_order": 50, "discount_pct": Decimal("0.10")},
    "SAVE20": {"min_order": 100, "discount_pct": Decimal("0.20")},
    FREE_SHIPPING_CODE: {"min_order": 0, "discount_pct": Decimal("0")},
    NEW_CUSTOMER_CODE: {"min_order": 0, "discount_pct": Decimal("0.15")},
}


def _decimal(number) -> Decimal:
    """Read a number the way it is written: 19.99 becomes 19.99, not 19.989999..."""
    return Decimal(str(number))


def _money(amount: Decimal) -> float:
    """Round an amount to cents, half up, so 2.625 becomes 2.63."""
    return float(amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


class Order:
    """Items bought by one customer, plus the discount and shipping they chose."""

    def __init__(self, items: List[Dict], customer_type: str = "regular"):
        """
        Initialize order

        Args:
            items: List of {"name": str, "price": float, "quantity": int, "weight": float}
            customer_type: "new" or "regular"
        """
        self.items = items
        self.customer_type = customer_type
        self.discount_code = None
        self.shipping_distance = 0
        self.is_express = False

    def apply_discount(self, code: str) -> bool:
        """Apply discount code, return True if valid

        A code is rejected when it does not exist, when the subtotal is below
        its minimum order, or when NEWUSER is used by a customer who is not new.
        A rejected code leaves the previously applied one in place.
        """
        if code not in DISCOUNT_CODES:
            return False

        if code == NEW_CUSTOMER_CODE and self.customer_type != "new":
            return False

        subtotal = self.calculate_subtotal()
        if subtotal < DISCOUNT_CODES[code]["min_order"]:
            return False

        self.discount_code = code
        return True

    def set_shipping(self, distance_km: float, is_express: bool = False):
        """Set shipping parameters"""
        self.shipping_distance = distance_km
        self.is_express = is_express

    def _billable_lines(self) -> Iterator[Tuple[Decimal, Decimal, Decimal]]:
        """Yield (price, quantity, weight) per item, skipping corrupted lines.

        A line with any negative value is not a real purchase, so it is left
        out completely: it adds nothing to the subtotal or to the weight.
        """
        for item in self.items:
            line = tuple(_decimal(item[field]) for field in ("price", "quantity", "weight"))
            if min(line) >= 0:
                yield line

    def calculate_subtotal(self) -> float:
        """Calculate subtotal (sum of item prices x quantities)"""
        lines = self._billable_lines()
        return _money(sum((price * quantity for price, quantity, _ in lines), Decimal(0)))

    def calculate_discount(self) -> float:
        """Calculate discount amount"""
        if self.discount_code is None:
            return 0.0

        rate = DISCOUNT_CODES[self.discount_code]["discount_pct"]
        return _money(_decimal(self.calculate_subtotal()) * rate)

    def calculate_tax(self) -> float:
        """Calculate tax (8% of subtotal after discount)"""
        taxable = _decimal(self.calculate_subtotal()) - _decimal(self.calculate_discount())
        return _money(taxable * TAX_RATE)

    def calculate_shipping(self) -> float:
        """Calculate shipping cost

        $0.50 per kg plus $0.10 per km, 1.5x for express, free with FREESHIP.
        A negative distance is charged as zero kilometres.
        """
        if self.discount_code == FREE_SHIPPING_CODE:
            return 0.0

        lines = self._billable_lines()
        weight = sum((unit_weight * quantity for _, quantity, unit_weight in lines), Decimal(0))
        distance = max(_decimal(self.shipping_distance), Decimal(0))

        cost = weight * RATE_PER_KG + distance * RATE_PER_KM
        if self.is_express:
            cost *= EXPRESS_MULTIPLIER
        return _money(cost)

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
        breakdown = {
            "subtotal": self.calculate_subtotal(),
            "discount": self.calculate_discount(),
            "tax": self.calculate_tax(),
            "shipping": self.calculate_shipping(),
        }
        charges = sum(_decimal(breakdown[part]) for part in ("subtotal", "tax", "shipping"))
        breakdown["total"] = _money(charges - _decimal(breakdown["discount"]))
        return breakdown
