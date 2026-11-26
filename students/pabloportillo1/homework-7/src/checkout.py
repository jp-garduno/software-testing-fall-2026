from datetime import date
from typing import Protocol

from src.customer_validator import validate_customer
from src.order_calculator import Order


class PaymentGateway(Protocol):
    def charge(self, card_number: str, amount: float) -> str | None:
        """Charge the card and return a transaction id, or None when the issuer declines it."""


class CheckoutError(Exception):
    """A checkout step was called out of order."""


class Checkout:
    """One customer's checkout: validate the customer, create the order, pay, then confirm."""

    def __init__(self, gateway: PaymentGateway, today=None):
        self._gateway = gateway
        self._today = today or date.today()
        self._customer = None
        self._order = None
        self._transaction_id = None

    def validate_customer(self, customer):
        if self._order is not None:
            raise CheckoutError("Customer cannot change after the order is created")
        result = validate_customer(customer, self._today)
        self._customer = customer if result.is_valid else None
        return {"valid": result.is_valid, "errors": list(result.errors)}

    def create_order(self, items, customer_type="regular", discount_code=None, distance_km=0, is_express=False):
        """Create or replace the unpaid order; an invalid customer or order is rejected, not raised."""
        if self._transaction_id is not None:
            raise CheckoutError("Order has already been paid")
        if self._customer is None:
            return {"status": "rejected", "reason": "Customer has not been validated"}
        try:
            order = Order(items, customer_type, self._today)
            order.set_shipping(distance_km, is_express)
        except ValueError as error:
            return {"status": "rejected", "reason": str(error)}
        discount_applied = order.apply_discount(discount_code) if discount_code else False
        self._order = order
        return {"status": "created", "discount_applied": discount_applied}

    def calculate_total(self):
        return self._require_order().calculate_total()

    def process_payment(self):
        order = self._require_order()
        if self._transaction_id is not None:
            raise CheckoutError("Order has already been paid")
        amount = order.calculate_total()["total"]
        transaction_id = self._gateway.charge(self._customer["credit_card"]["number"], amount)
        if transaction_id is None:
            return {"status": "declined", "reason": "Payment declined by the card issuer"}
        self._transaction_id = transaction_id
        return {"status": "success", "amount": amount, "transaction_id": transaction_id}

    def generate_confirmation(self):
        if self._transaction_id is None:
            raise CheckoutError("Order has not been paid")
        return {
            "status": "confirmed",
            "transaction_id": self._transaction_id,
            "email": self._customer["email"],
            "item_count": sum(item["quantity"] for item in self._order.items),
            **self._order.calculate_total(),
        }

    def _require_order(self):
        if self._order is None:
            raise CheckoutError("No order has been created")
        return self._order
