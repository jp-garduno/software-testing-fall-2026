"""End-to-end order workflow used by the integration tests.

An ``OrderWorkflow`` keeps the state of one order (customer, order, totals,
payment) and executes workflow steps by action name, e.g.::

    wf = OrderWorkflow(today=date(2025, 1, 15))
    wf.execute("validate_customer", customer_dict)
"""
import hashlib
from datetime import date
from typing import Dict, Optional

from customer_validator import validate_customer
from order_calculator import Order

ACTIONS = (
    "validate_customer",
    "create_order",
    "apply_discount",
    "set_shipping",
    "calculate_total",
    "process_payment",
    "generate_confirmation",
)

MAX_PAYMENT = 10000.00  # payments above this amount are declined

NO_ORDER = {"status": "rejected", "reason": "no active order"}


class OrderWorkflow:
    def __init__(self, today: Optional[date] = None):
        self.today = today or date.today()
        self.customer: Optional[Dict] = None
        self.customer_valid = False
        self.order: Optional[Order] = None
        self.totals: Optional[Dict[str, float]] = None
        self.paid = False

    def execute(self, action: str, data: Optional[Dict] = None) -> Dict:
        """Run one workflow step and return its result dict."""
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action}")
        return getattr(self, f"_do_{action}")(data or {})

    # -- steps ----------------------------------------------------------
    def _do_validate_customer(self, data: Dict) -> Dict:
        result = validate_customer(data, self.today)
        self.customer = data
        self.customer_valid = result["is_valid"]
        return {"valid": result["is_valid"], "errors": result["errors"]}

    def _do_create_order(self, data: Dict) -> Dict:
        self.order, self.totals, self.paid = None, None, False
        if not self.customer_valid:
            return {"status": "rejected", "reason": "customer not validated"}
        items = data.get("items", [])
        if not items:
            return {"status": "rejected", "reason": "order has no items"}
        try:
            self.order = Order(items, data.get("customer_type", "regular"))
        except ValueError as exc:
            return {"status": "rejected", "reason": str(exc)}
        return {"status": "created", "item_count": len(items)}

    def _do_apply_discount(self, data: Dict) -> Dict:
        if self.order is None:
            return NO_ORDER
        return {"applied": self.order.apply_discount(data.get("code", ""))}

    def _do_set_shipping(self, data: Dict) -> Dict:
        if self.order is None:
            return NO_ORDER
        try:
            self.order.set_shipping(data.get("distance_km", 0), data.get("is_express", False))
        except ValueError as exc:
            return {"status": "rejected", "reason": str(exc)}
        return {"status": "set"}

    def _do_calculate_total(self, data: Dict) -> Dict:
        if self.order is None:
            return NO_ORDER
        self.totals = self.order.calculate_total()
        return dict(self.totals)

    def _do_process_payment(self, data: Dict) -> Dict:
        if self.order is None:
            return NO_ORDER
        if self.totals is None:
            self.totals = self.order.calculate_total()
        amount = self.totals["total"]
        if amount <= 0:
            return {"status": "declined", "reason": "invalid amount"}
        if amount > MAX_PAYMENT:
            return {"status": "declined", "reason": "amount exceeds limit"}
        self.paid = True
        return {"status": "success", "amount": amount}

    def _do_generate_confirmation(self, data: Dict) -> Dict:
        if self.order is None:
            return NO_ORDER
        if not self.paid:
            return {"status": "rejected", "reason": "payment not completed"}
        seed = f"{self.customer['email']}:{self.totals['total']:.2f}"
        number = "ORD-" + hashlib.sha1(seed.encode()).hexdigest()[:8].upper()
        return {
            "status": "confirmed",
            "confirmation_number": number,
            "email": self.customer["email"],
            "total": self.totals["total"],
        }
