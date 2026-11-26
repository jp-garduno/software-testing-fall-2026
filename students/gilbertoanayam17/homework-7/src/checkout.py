"""Checkout: the end-to-end flow that joins customer validation and order totals."""

from datetime import date
from typing import Any, Dict, List, Optional

import customer_validator
from order_calculator import Order


class Checkout:
    """One checkout session: validate the customer, create the order, total it, pay.

    The public methods are the "action" names used in test_data/order_workflows.json,
    so a workflow step is a method call with the step's data as arguments.
    """

    def __init__(self, today: Optional[date] = None):
        """`today` is the date card expirations are checked against (default: real date)."""
        self.today = today
        self.customer_valid = False
        self.order = Order([])
        self.totals: Optional[Dict[str, float]] = None

    def validate_customer(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the customer and remember the outcome for the payment step."""
        result = customer_validator.validate_customer(customer, self.today)
        self.customer_valid = result["is_valid"]
        return {"valid": result["is_valid"], "errors": result["errors"]}

    def create_order(
        self,
        items: List[Dict],
        customer_type: str = "regular",
        discount_code: Optional[str] = None,
        shipping: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Start a new order and report whether the discount code was accepted.

        Args:
            items: List of {"name", "price", "quantity", "weight"}
            customer_type: "new" or "regular"
            discount_code: optional code; an unknown or ineligible code is ignored
            shipping: optional {"distance_km": float, "is_express": bool}
        """
        self.order = Order(items, customer_type)
        self.totals = None
        discount_applied = self.order.apply_discount(discount_code)
        if shipping:
            self.order.set_shipping(**shipping)
        return {"status": "created", "discount_applied": discount_applied}

    def calculate_total(self) -> Dict[str, float]:
        """Calculate the breakdown of the current order and keep it for payment."""
        self.totals = self.order.calculate_total()
        return self.totals

    def process_payment(self) -> Dict[str, Any]:
        """Charge the calculated total and confirm the order.

        The payment is declined unless the customer passed validation and a
        total greater than zero has been calculated.
        """
        amount = self.totals["total"] if self.totals else 0.0
        if not self.customer_valid or amount <= 0:
            return {"status": "declined", "amount_charged": 0.0}

        confirmation = f"Order confirmed: {len(self.order.items)} item(s), ${amount:,.2f} charged"
        return {"status": "success", "amount_charged": amount, "confirmation": confirmation}
