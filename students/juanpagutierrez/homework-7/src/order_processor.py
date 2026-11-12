"""End-to-end order workflow: validate customer, create order, price, pay, confirm.

Each step returns a plain dict with a "status" (or "valid"/"applied") so a
workflow can be described as data and checked step by step. Steps taken out
of order are refused with an "error" status rather than raising, the way a web
checkout would answer a request it cannot serve.
"""

from datetime import date
from typing import Dict, List, Optional

from src.customer_validator import normalize_card_number, validate_customer
from src.order_calculator import Order

# Card numbers that pass validation but that the simulated payment gateway
# declines, in the spirit of the test cards real gateways publish.
DECLINED_CARDS = frozenset({"4000000000000002", "5105105105105100"})


class OrderProcessor:
    """Drives one customer through a single checkout."""

    def __init__(self, today: Optional[date] = None):
        self.today = today
        self.customer: Optional[Dict] = None
        self.order: Optional[Order] = None
        self.order_id: Optional[str] = None
        self.totals: Optional[Dict[str, float]] = None
        self.transaction_id: Optional[str] = None

    def validate_customer(self, customer: Dict) -> Dict:
        """Validate the customer and remember them if valid."""
        result = validate_customer(customer, self.today)
        self.customer = customer if result["is_valid"] else None
        return {"valid": result["is_valid"], "errors": result["errors"]}

    # The keyword arguments are the fields of a create_order step in order_workflows.json.
    def create_order(self, items: List[Dict], customer_type: str = "regular",  # pylint: disable=too-many-arguments
                     discount_code: Optional[str] = None, distance_km: float = 0, is_express: bool = False) -> Dict:
        """Create the order for the validated customer."""
        if self.customer is None:
            return {"status": "rejected", "error": "Customer has not been validated"}
        try:
            order = Order(items, customer_type)
            order.set_shipping(distance_km, is_express)
        except ValueError as error:
            return {"status": "rejected", "error": str(error)}
        applied = order.apply_discount(discount_code, self.today) if discount_code else False
        self.order = order
        self.order_id = "ORD-0001"
        self.totals = None
        return {"status": "created", "order_id": self.order_id, "discount_applied": applied}

    def apply_discount(self, code: str) -> Dict:
        """Apply (or replace) the discount code on the current order."""
        if self.order is None:
            return {"applied": False, "error": "No order to discount"}
        applied = self.order.apply_discount(code, self.today)
        self.totals = None
        return {"applied": applied, "discount_code": self.order.discount_code}

    def calculate_total(self) -> Dict:
        """Price the current order."""
        if self.order is None:
            return {"status": "error", "error": "No order to calculate"}
        self.totals = self.order.calculate_total()
        return {"status": "calculated", **self.totals}

    def process_payment(self, amount: Optional[float] = None) -> Dict:
        """Charge the customer's card for the calculated total."""
        if self.transaction_id is not None:
            return {"status": "failed", "error": "Order already paid"}
        if self.totals is None:
            return {"status": "failed", "error": "No order total to pay"}
        if amount is not None and round(amount, 2) != self.totals["total"]:
            return {"status": "failed", "error": "Amount does not match order total"}
        if normalize_card_number(self.customer["credit_card"]["number"]) in DECLINED_CARDS:
            return {"status": "declined", "error": "Card declined by issuer"}
        self.transaction_id = f"TXN-{self.order_id}"
        return {"status": "success", "transaction_id": self.transaction_id, "amount": self.totals["total"]}

    def generate_confirmation(self) -> Dict:
        """Produce the confirmation for a paid order."""
        if self.transaction_id is None:
            return {"status": "error", "error": "Order has not been paid"}
        return {
            "status": "confirmed",
            "confirmation_number": f"CONF-{self.order_id}",
            "email": self.customer["email"],
            "total": self.totals["total"],
            "items": len(self.order.items),
        }
