"""In-memory order workflow with an injected simulated payment function."""

from customer_validator import validate_customer
from order_calculator import Order


class OrderProcessor:
    """Coordinate validation, pricing, simulated payment and confirmation."""

    def __init__(self, payment, today, order_id):
        self.payment = payment
        self.today = today
        self.order_id = order_id
        self.customer_valid = False
        self.order = None
        self.paid = False

    def validate(self, customer):
        """Validate customer information before accepting an order."""
        result = validate_customer(customer, self.today)
        self.customer_valid = result["is_valid"]
        return result

    def create(self, data):
        """Create a priced order only for a validated customer."""
        if not self.customer_valid:
            return {"status": "blocked"}
        self.order = Order(data["items"], data.get("customer_type", "regular"))
        if data.get("discount_code"):
            self.order.apply_discount(data["discount_code"])
        self.order.set_shipping(
            data.get("distance_km", 0), data.get("is_express", False)
        )
        self.paid = False
        return {"status": "created"}

    def total(self):
        """Expose the complete price breakdown for the current order."""
        if self.order is None:
            raise ValueError("Order not created")
        return self.order.calculate_total()

    def pay(self):
        """Simulate one charge; never charge an already paid order twice."""
        if self.paid:
            return {"status": "already_paid"}
        amount = self.total()["total"]
        self.paid = bool(self.payment(amount))
        return {"status": "success" if self.paid else "declined"}

    def confirmation(self):
        """Generate a confirmation only after a successful payment."""
        if not self.paid:
            return {"status": "unpaid"}
        return {
            "status": "confirmed",
            "order_id": self.order_id,
            "total": self.total()["total"],
        }
