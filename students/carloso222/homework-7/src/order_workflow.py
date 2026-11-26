"""End-to-end order workflow: validate customer -> create order -> calculate total -> process payment."""

from datetime import date
from typing import Any, Dict, List, Optional

from src.customer_validator import validate_customer
from src.order_calculator import Order

ACTIONS = ("validate_customer", "create_order", "calculate_total", "process_payment")


class OrderWorkflow:
    """Holds the state of one order flow; each step returns a result dict."""

    def __init__(self, today: Optional[date] = None):
        self.today = today
        self.validation: Optional[Dict[str, Any]] = None
        self.order: Optional[Order] = None

    def validate_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the customer; the result is {"valid": bool, "errors": [...]}."""
        self.validation = validate_customer(data, self.today)
        return {
            "valid": self.validation["is_valid"],
            "errors": self.validation["errors"],
        }

    def create_order(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Build the order from items, customer_type, discount_code, distance_km and is_express."""
        try:
            order = Order(data["items"], data.get("customer_type", "regular"))
            order.set_shipping(
                data.get("distance_km", 0), data.get("is_express", False)
            )
        except (KeyError, ValueError) as error:
            return {"status": "rejected", "reason": str(error)}
        code = data.get("discount_code")
        self.order = order
        return {
            "status": "created",
            "discount_applied": bool(code) and order.apply_discount(code),
        }

    def calculate_total(self) -> Dict[str, Any]:
        """Return the order breakdown, or a failed status when no order exists."""
        if self.order is None:
            return {"status": "failed", "reason": "No order created"}
        return self.order.calculate_total()

    def process_payment(self) -> Dict[str, Any]:
        """Charge the order total. Declined when the customer data is invalid or was never validated."""
        if self.order is None:
            return {"status": "failed", "reason": "No order created"}
        if self.validation is None or not self.validation["is_valid"]:
            return {"status": "declined", "reason": "Invalid payment information"}
        total = self.order.calculate_total()["total"]
        return {
            "status": "success",
            "amount": total,
            "confirmation": f"Order confirmed, total ${total:.2f}",
        }

    def run_step(
        self, action: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Dispatch one step by action name. Raises ValueError for an unknown action."""
        if action not in ACTIONS:
            raise ValueError(f"Unknown workflow action: {action!r}")
        if action in ("validate_customer", "create_order"):
            return getattr(self, action)(data or {})
        return getattr(self, action)()


def run_workflow(
    workflow: Dict[str, Any], today: Optional[date] = None
) -> List[Dict[str, Any]]:
    """Run every step of a workflow definition and return the list of step results."""
    flow = OrderWorkflow(today)
    return [
        flow.run_step(step["action"], step.get("data")) for step in workflow["steps"]
    ]
