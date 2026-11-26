"""Discount code rules for the order calculator."""

from decimal import Decimal
from typing import Dict, Optional

# min_order is an EXCLUSIVE lower bound: the subtotal must be strictly greater (a min of 0 means "no minimum").
# customer_type restricts the code to one kind of customer (None = any customer).
DISCOUNT_RULES: Dict[str, Dict[str, object]] = {
    "SAVE10": {
        "min_order": Decimal("50"),
        "discount_pct": Decimal("0.10"),
        "customer_type": None,
    },
    "SAVE20": {
        "min_order": Decimal("100"),
        "discount_pct": Decimal("0.20"),
        "customer_type": None,
    },
    "FREESHIP": {
        "min_order": Decimal("0"),
        "discount_pct": Decimal("0"),
        "customer_type": None,
    },
    "NEWUSER": {
        "min_order": Decimal("0"),
        "discount_pct": Decimal("0.15"),
        "customer_type": "new",
    },
}


def is_code_applicable(code: object, subtotal: Decimal, customer_type: str) -> bool:
    """Return True when the code exists, the subtotal is high enough and the customer type matches."""
    rule = DISCOUNT_RULES.get(code) if isinstance(code, str) else None
    if rule is None:
        return False
    min_order: Optional[Decimal] = rule["min_order"]  # type: ignore[assignment]
    if min_order and subtotal <= min_order:
        return False
    return rule["customer_type"] in (None, customer_type)
