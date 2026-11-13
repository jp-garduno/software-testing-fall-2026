"""End-to-end order workflow: validate customer, create order, price it, pay and confirm."""

from datetime import date
from typing import Dict, Optional

from customer_validator import validate_customer
from order_calculator import Order

# Card numbers the simulated payment processor always declines.
DECLINED_CARDS = frozenset({"4000000000000002"})


class OrderWorkflow:
    """Runs workflow steps in order, rejecting any step whose prerequisites were not met."""

    def __init__(self, today: Optional[date] = None, first_confirmation_number: int = 1):
        self.today = today
        self._next_confirmation = first_confirmation_number
        self.customer: Optional[Dict] = None
        self.customer_valid = False
        self.order: Optional[Order] = None
        self.totals: Optional[Dict[str, float]] = None
        self.payment_status: Optional[str] = None

    def execute(self, action: str, data: Optional[Dict] = None) -> Dict:
        """Run one named step and return its result dictionary."""
        handler = getattr(self, f"_do_{action}", None)
        if handler is None:
            raise ValueError(f"Unknown workflow action: {action}")
        return handler(data or {})

    @staticmethod
    def _rejected(reason):
        return {"status": "rejected", "error": reason}

    def _do_validate_customer(self, data):
        self.customer = data["customer"]
        result = validate_customer(self.customer, today=self.today)
        self.customer_valid = result["is_valid"]
        return {"valid": result["is_valid"], "errors": result["errors"]}

    def _do_create_order(self, data):
        if not self.customer_valid:
            return self._rejected("Customer not validated")
        self.order = Order(data["items"], data.get("customer_type", "regular"))
        self.totals = None
        self.payment_status = None
        return {"status": "created"}

    def _do_apply_discount(self, data):
        if self.order is None:
            return self._rejected("No order")
        return {"applied": self.order.apply_discount(data["code"])}

    def _do_set_shipping(self, data):
        if self.order is None:
            return self._rejected("No order")
        self.order.set_shipping(data["distance_km"], data.get("express", False))
        return {"status": "shipping_set"}

    def _do_calculate_total(self, data):  # pylint: disable=unused-argument
        if self.order is None:
            return self._rejected("No order")
        self.totals = self.order.calculate_total()
        return dict(self.totals)

    def _do_process_payment(self, data):  # pylint: disable=unused-argument
        if self.totals is None:
            return self._rejected("No order total to charge")
        card_number = self.customer["credit_card"]["number"].replace(" ", "").replace("-", "")
        self.payment_status = "declined" if card_number in DECLINED_CARDS else "success"
        return {"status": self.payment_status, "amount": self.totals["total"]}

    def _do_generate_confirmation(self, data):  # pylint: disable=unused-argument
        if self.payment_status != "success":
            return self._rejected("Payment not completed")
        number = f"ORD-{self._next_confirmation:06d}"
        self._next_confirmation += 1
        return {"status": "confirmed", "confirmation_number": number, "total": self.totals["total"]}
