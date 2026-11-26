"""End-to-end order workflow processor for integration testing."""

from typing import Any, Dict, List, Optional

from src.customer_validator import validate_customer
from src.order_calculator import Order


class OrderWorkflowEngine:
    """Executes multi-step e-commerce order processing workflows."""

    def __init__(self) -> None:
        self.customer_valid: bool = False
        self.customer_data: Optional[Dict[str, Any]] = None
        self.current_order: Optional[Order] = None
        self.last_totals: Optional[Dict[str, float]] = None
        self.order_status: str = "uninitialized"

    def _handle_validate_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        validation = validate_customer(data)
        self.customer_valid = validation["is_valid"]
        self.customer_data = data
        return {"valid": validation["is_valid"], "errors": validation["errors"]}

    def _handle_create_order(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.customer_valid:
            self.order_status = "rejected_invalid_customer"
            return {"status": self.order_status}

        items = data.get("items", [])
        customer_type = data.get("customer_type", "regular")
        self.current_order = Order(items, customer_type=customer_type)

        discount_code = data.get("discount_code")
        if discount_code:
            self.current_order.apply_discount(discount_code)

        self.current_order.set_shipping(
            float(data.get("distance_km", 0.0)),
            bool(data.get("is_express", False)),
        )
        self.order_status = "created"
        return {"status": "created"}

    def _handle_calculate_total(self) -> Dict[str, Any]:
        if not self.current_order:
            return {"error": "Order not created", "total": 0.0}
        self.last_totals = self.current_order.calculate_total()
        return self.last_totals

    def _handle_process_payment(self) -> Dict[str, Any]:
        if not self.customer_valid or not self.current_order:
            self.order_status = "failed"
            return {"status": "failed", "reason": "Order or customer invalid"}

        totals = self.last_totals or self.current_order.calculate_total()
        if totals["total"] <= 0:
            self.order_status = "failed"
            return {"status": "failed", "reason": "Non-positive order total"}

        self.order_status = "confirmed"
        return {
            "status": "success",
            "confirmation_id": f"CONF-{int(totals['total'] * 100)}",
            "charged_amount": totals["total"],
        }

    def execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow action step and return its result."""
        action = step.get("action")
        data = step.get("data", {})

        if action == "validate_customer":
            return self._handle_validate_customer(data)
        if action == "create_order":
            return self._handle_create_order(data)
        if action == "calculate_total":
            return self._handle_calculate_total()
        if action == "process_payment":
            return self._handle_process_payment()

        raise ValueError(f"Unsupported workflow action: {action}")

    def run_workflow(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run all steps in a workflow sequentially and return step outputs."""
        return [self.execute_step(step) for step in steps]
