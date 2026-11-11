"""Coordinate customer validation, order pricing, payment and confirmation."""

from datetime import date

from .customer_validator import validate_customer
from .order_calculator import Order


class Checkout:
    """One local checkout with a simulated payment outcome."""

    def __init__(self, order_id: str, *, today: date | None = None):
        self._order_id = order_id
        self._today = today
        self._state = "started"
        self._order: Order | None = None
        self._total: float | None = None

    def _require(self, action: str, *allowed: str) -> None:
        if self._state not in allowed:
            raise ValueError(f"{action} is not allowed in state {self._state}")

    def validate_customer(self, customer: object) -> dict:
        """Allow checkout to advance only when the customer details are valid."""
        self._require("validate_customer", "started", "customer_rejected")
        result = validate_customer(customer, today=self._today)
        self._state = (
            "customer_validated" if result["is_valid"] else "customer_rejected"
        )
        return {"valid": result["is_valid"], "errors": result["errors"]}

    def create_order(
        self,
        items: list[dict],
        *,
        customer_type: str = "regular",
        discount_code: str | None = None,
        shipping: dict | None = None,
    ) -> dict:
        """Configure an order for a validated customer."""
        self._require("create_order", "customer_validated")
        order = Order(items, customer_type)
        discount_applied = discount_code is not None and order.apply_discount(
            discount_code
        )
        if shipping is not None:
            order.set_shipping(**shipping)
        self._order = order
        self._state = "created"
        return {"status": "created", "discount_applied": discount_applied}

    def calculate_total(self) -> dict[str, float]:
        """Price the order and save the amount due."""
        self._require("calculate_total", "created")
        assert self._order is not None
        breakdown = self._order.calculate_total()
        self._total = breakdown["total"]
        self._state = "priced"
        return breakdown

    def process_payment(self, approved: bool = True) -> dict:
        """Simulate a payment approval or decline, allowing a declined attempt to retry."""
        self._require("process_payment", "priced", "payment_declined")
        if not approved:
            self._state = "payment_declined"
            return {"status": "declined"}
        self._state = "paid"
        return {"status": "success", "amount": self._total}

    def confirm_order(self) -> dict:
        """Generate the confirmation after a successful payment."""
        self._require("confirm_order", "paid")
        self._state = "confirmed"
        return {"status": "confirmed", "order_id": self._order_id, "total": self._total}
