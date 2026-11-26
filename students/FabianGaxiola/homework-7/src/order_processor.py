"""Small in-memory order workflow used by the integration test data."""

from datetime import date
from typing import Any, Mapping

from customer_validator import validate_customer
from order_calculator import Order


class OrderProcessor:
    """Coordinate customer validation, order calculation, and simulated payment."""

    def __init__(self, today: date | None = None) -> None:
        self.today = today
        self.customer_valid = False
        self.customer_errors: list[str] = []
        self.order: Order | None = None
        self.status = "new"

    def validate_customer(self, customer: Any) -> dict[str, Any]:
        result = validate_customer(customer, self.today)
        self.customer_valid = result["is_valid"]
        self.customer_errors = result["errors"]
        self.status = "validated" if self.customer_valid else "rejected"
        return {"valid": self.customer_valid, "errors": self.customer_errors}

    def create_order(self, data: Mapping[str, Any]) -> dict[str, Any]:
        if not self.customer_valid:
            self.status = "rejected"
            return {"status": self.status, "errors": list(self.customer_errors)}
        if not isinstance(data, Mapping):
            raise ValueError("order data must be an object")

        order = Order(data.get("items"), data.get("customer_type", "regular"))
        discount_code = data.get("discount_code")
        if discount_code is not None:
            order.apply_discount(discount_code)
        order.set_shipping(data.get("distance_km", 0), data.get("is_express", False))
        self.order = order
        self.status = "created"
        return {"status": self.status}

    def calculate_total(self) -> dict[str, Any]:
        if self.order is None:
            return {"status": "blocked"}
        return {"status": "calculated", **self.order.calculate_total()}

    def process_payment(self, approved: bool = True) -> dict[str, str]:
        if not self.customer_valid or self.order is None:
            return {"status": "blocked"}
        self.status = "paid" if approved else "declined"
        return {"status": self.status}
