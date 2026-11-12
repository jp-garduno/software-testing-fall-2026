"""End-to-end order workflow (homework 7, part 4).

OrderProcessor chains the steps of a checkout. Every step takes a plain dict and returns a
plain dict, so a whole workflow can be described step by step in JSON and replayed by a test:

    validate_customer -> create_order -> apply_discount -> set_shipping
    -> calculate_total -> process_payment -> generate_confirmation

Payments go through a gateway object with a ``charge(card_number, amount)`` method. The
SimulatedPaymentGateway below is a deterministic stand-in: no network, same answer every run.
"""

from __future__ import annotations

from datetime import date
from typing import Dict, Iterable, Optional

from customer_validator import normalize_card_number, validate_customer
from order_calculator import InvalidOrderError, Order


class SimulatedPaymentGateway:
    """Approves every charge except declined card numbers or amounts above the limit."""

    def __init__(self, declined_cards: Iterable[str] = (), limit: float = 5000.0) -> None:
        self.declined_cards = {normalize_card_number(card) for card in declined_cards}
        self.limit = limit
        self.charges = []

    def charge(self, card_number: str, amount: float) -> Dict:
        number = normalize_card_number(card_number)
        if number in self.declined_cards:
            return {"approved": False, "reason": "Card declined"}
        if amount > self.limit:
            return {"approved": False, "reason": "Amount exceeds limit"}
        self.charges.append((number, amount))
        return {"approved": True, "transaction_id": f"TXN-{len(self.charges):05d}"}


class OrderProcessor:  # pylint: disable=too-many-instance-attributes
    """Runs one checkout: one customer, one order, one payment."""

    _sequence = 0

    def __init__(self, payment_gateway=None, today: Optional[date] = None) -> None:
        self.gateway = payment_gateway or SimulatedPaymentGateway()
        self.today = today
        self.customer: Optional[Dict] = None
        self.order: Optional[Order] = None
        self.order_id: Optional[str] = None
        self.breakdown: Optional[Dict] = None
        self.transaction_id: Optional[str] = None
        self.status = "new"

    def run_step(self, action: str, data: Optional[Dict] = None) -> Dict:
        """Dispatch a workflow step by name (used by the JSON-driven integration tests)."""
        handler = getattr(self, action, None)
        if action.startswith("_") or action == "run_step" or not callable(handler):
            return {"status": "error", "error": f"Unknown action: {action}"}
        return handler(data or {})

    def validate_customer(self, data: Dict) -> Dict:
        result = validate_customer(data, self.today)
        self.customer = data if result.is_valid else None
        return {"valid": result.is_valid, "errors": result.errors}

    def create_order(self, data: Dict) -> Dict:
        if self.customer is None:
            return {"status": "rejected", "error": "Customer must be validated first"}
        try:
            self.order = Order(data.get("items", []), data.get("customer_type", "regular"))
        except InvalidOrderError as exc:
            return {"status": "rejected", "error": str(exc)}
        if not self.order.items:
            self.order = None
            return {"status": "rejected", "error": "Order must contain at least one item"}
        OrderProcessor._sequence += 1
        self.order_id = f"ORD-{OrderProcessor._sequence:04d}"
        self.status = "created"
        return {"status": "created", "order_id": self.order_id, "items_count": len(self.order.items)}

    def apply_discount(self, data: Dict) -> Dict:
        if self.order is None:
            return {"status": "error", "error": "No order to discount"}
        applied = self.order.apply_discount(data.get("code"))
        return {"applied": applied, "discount_code": self.order.discount_code}

    def set_shipping(self, data: Dict) -> Dict:
        if self.order is None:
            return {"status": "error", "error": "No order to ship"}
        try:
            self.order.set_shipping(data.get("distance_km", 0), data.get("is_express", False))
        except InvalidOrderError as exc:
            return {"status": "error", "error": str(exc)}
        return {"status": "ok"}

    def calculate_total(self, _data: Dict) -> Dict:
        if self.order is None:
            return {"status": "error", "error": "No order to calculate"}
        self.breakdown = self.order.calculate_total()
        return {"status": "calculated", **self.breakdown}

    def process_payment(self, _data: Dict) -> Dict:
        if self.breakdown is None:
            return {"status": "error", "error": "Total must be calculated first"}
        if self.status == "paid":
            return {"status": "error", "error": "Order already paid"}
        response = self.gateway.charge(self.customer["credit_card"]["number"], self.breakdown["total"])
        if not response["approved"]:
            self.status = "payment_declined"
            return {"status": "declined", "error": response["reason"]}
        self.transaction_id = response["transaction_id"]
        self.status = "paid"
        return {"status": "success", "transaction_id": self.transaction_id, "amount": self.breakdown["total"]}

    def generate_confirmation(self, _data: Dict) -> Dict:
        if self.status != "paid":
            return {"status": "error", "error": "Order is not paid"}
        last_digits = normalize_card_number(self.customer["credit_card"]["number"])[-4:]
        total = self.breakdown["total"]
        return {
            "status": "confirmed",
            "order_id": self.order_id,
            "email": self.customer["email"],
            "total": total,
            "message": f"Order {self.order_id} confirmed: ${total:.2f} charged to card ending {last_digits}",
        }
