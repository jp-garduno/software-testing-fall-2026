"""End-to-end order workflow engine used by the integration tests.

A workflow is a list of steps ``{"action", "data", "expected"}``. Each step is
executed against an :class:`OrderWorkflow` and returns a result dict that the
tests compare with ``expected``.
"""

from datetime import date
from typing import Dict, Optional

from customer_validator import validate_customer
from order_calculator import Order

PAYMENT_LIMIT = 10000.00


class WorkflowError(Exception):
    """Raised for an unknown action."""


class OrderWorkflow:
    """Stateful processor: validate customer -> order -> total -> payment."""

    def __init__(self, today: Optional[date] = None):
        self.today = today
        self.customer: Optional[Dict] = None
        self.customer_valid = False
        self.order: Optional[Order] = None
        self.totals: Optional[Dict[str, float]] = None
        self.paid = False
        self._confirmation_seq = 0

    def execute(self, action: str, data: Optional[Dict] = None) -> Dict:
        """Run one action and return its result."""
        handler = getattr(self, f"_do_{action}", None)
        if handler is None:
            raise WorkflowError(f"unknown action: {action}")
        return handler(data or {})

    # ---- actions ------------------------------------------------------
    def _do_validate_customer(self, data):
        self.customer = data
        result = validate_customer(data, self.today)
        self.customer_valid = result["is_valid"]
        return {"valid": result["is_valid"], "errors": result["errors"]}

    def _do_create_order(self, data):
        if not self.customer_valid:
            return {"status": "rejected", "reason": "invalid customer"}
        if not data.get("items"):
            return {"status": "rejected", "reason": "empty order"}
        self.order = Order(data["items"], data.get("customer_type", "regular"))
        self.totals = None
        self.paid = False
        return {"status": "created", "item_count": len(data["items"])}

    def _do_apply_discount(self, data):
        if self.order is None:
            return {"applied": False, "reason": "no order"}
        return {"applied": self.order.apply_discount(data.get("code", ""))}

    def _do_set_shipping(self, data):
        if self.order is None:
            return {"status": "rejected", "reason": "no order"}
        self.order.set_shipping(data.get("distance_km", 0), data.get("is_express", False))
        return {"status": "set"}

    def _do_calculate_total(self, _data):
        if self.order is None:
            return {"status": "rejected", "reason": "no order"}
        self.totals = self.order.calculate_total()
        return dict(self.totals)

    def _do_process_payment(self, _data):
        if self.totals is None:
            return {"status": "failed", "reason": "total not calculated"}
        if self.totals["total"] > PAYMENT_LIMIT:
            return {"status": "declined", "reason": "limit exceeded"}
        self.paid = True
        return {"status": "success", "charged": self.totals["total"]}

    def _do_confirm_order(self, _data):
        if not self.paid:
            return {"status": "rejected", "reason": "payment required"}
        self._confirmation_seq += 1
        return {
            "status": "confirmed",
            "confirmation_id": f"ORD-{self._confirmation_seq:06d}",
            "total": self.totals["total"],
        }
