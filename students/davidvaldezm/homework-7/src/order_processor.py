"""Validate a customer, price an order, collect payment and confirm it."""

from src.customer_validator import validate_customer
from src.order_calculator import Order


class OrderProcessor:
    """Handle one order using an injected payment function."""

    def __init__(self, order_id, charge, *, today=None):
        self._order_id = order_id
        self._charge = charge
        self._today = today
        self._email = None
        self._order = None
        self._payment_status = None

    def validate_customer(self, customer):
        """Validate contact and payment information before creating an order."""
        if self._order is not None:
            return {"valid": False, "errors": ["Order already created"]}
        result = validate_customer(customer, today=self._today)
        self._email = customer["email"] if result["is_valid"] else None
        return {"valid": result["is_valid"], "errors": result["errors"]}

    def create_order(
        self,
        items,
        customer_type="regular",
        discount_code=None,
        distance_km=0,
        is_express=False,
    ):
        """Create an order for a validated customer."""
        if self._order is not None:
            return {"status": "already_created"}
        if self._email is None:
            return {"status": "invalid_customer"}
        try:
            order = Order(items, customer_type)
            order.set_shipping(distance_km, is_express)
        except ValueError as error:
            return {"status": "invalid_order", "error": str(error)}
        if discount_code:
            order.apply_discount(discount_code)
        self._order = order
        return {"status": "created"}

    def calculate_total(self):
        """Return the current order totals."""
        if self._order is None:
            return {"status": "no_order"}
        return self._order.calculate_total()

    def process_payment(self):
        """Charge the order once and allow a declined payment to be retried."""
        if self._order is None:
            return {"status": "no_order"}
        total = self._order.calculate_total()["total"]
        if self._payment_status != "success":
            self._payment_status = "success" if self._charge(total) else "declined"
        return {"status": self._payment_status, "amount": total}

    def generate_confirmation(self):
        """Return confirmation details after a successful payment."""
        if self._payment_status != "success":
            return {"status": "unpaid"}
        return {
            "status": "confirmed",
            "order_id": self._order_id,
            "email": self._email,
            "total": self._order.calculate_total()["total"],
        }
