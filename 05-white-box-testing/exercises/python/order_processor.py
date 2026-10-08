"""Order validation, totals, shipping, and delivery-date calculations."""

from datetime import datetime, timedelta
from enum import Enum


class OrderStatus(Enum):
    """Order status enumeration."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class ShippingMethod(Enum):
    """Available shipping methods."""

    STANDARD = "standard"
    EXPRESS = "express"
    OVERNIGHT = "overnight"
    INTERNATIONAL = "international"


class Order:
    """Represents a customer order."""

    def __init__(self, order_id, customer_id, items, shipping_address):
        """Initialize an order in its pending state."""
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.shipping_address = shipping_address
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()
        self.shipping_method = None
        self.discount_code = None
        self.tracking_number = None

    def get_subtotal(self):
        """Calculate the subtotal from complete line items only."""
        total = 0
        for item in self.items:
            if "price" in item and "quantity" in item:
                total += item["price"] * item["quantity"]
        return total


class OrderProcessor:
    """Processes and validates orders."""

    def __init__(self, tax_rate=0.08, free_shipping_threshold=50.0):
        """Initialize tax, free-shipping, and discount-code configuration."""
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.discount_codes = {
            "SAVE10": 0.10,
            "SAVE20": 0.20,
            "SAVE30": 0.30,
            "FREESHIP": 0.0,
        }

    def validate_order(self, order):
        """Return whether an order has valid items and a shipping address."""
        if not order.items or len(order.items) == 0:
            return False, "Order must contain at least one item"

        for index, item in enumerate(order.items):
            if "name" not in item or not item["name"]:
                return False, f"Item {index} is missing name"
            if "price" not in item:
                return False, f"Item {index} is missing price"
            if item["price"] <= 0:
                return False, f"Item {index} has invalid price"
            if "quantity" not in item:
                return False, f"Item {index} is missing quantity"
            if item["quantity"] <= 0:
                return False, f"Item {index} has invalid quantity"
            if item["quantity"] > 100:
                return False, f"Item {index} quantity exceeds maximum (100)"

        if not order.shipping_address:
            return False, "Shipping address is required"

        for field in ["street", "city", "state", "zip_code", "country"]:
            if field not in order.shipping_address or not order.shipping_address[field]:
                return False, f"Shipping address missing {field}"

        zip_code = order.shipping_address["zip_code"]
        if order.shipping_address["country"] == "US":
            if not (len(zip_code) == 5 or len(zip_code) == 10):
                return False, "Invalid US ZIP code format"
            if len(zip_code) == 5:
                if not zip_code.isdigit():
                    return False, "ZIP code must be 5 digits"
            elif len(zip_code) == 10:
                valid_zip_plus_four = (
                    zip_code[:5].isdigit()
                    and zip_code[5] == "-"
                    and zip_code[6:].isdigit()
                )
                if not valid_zip_plus_four:
                    return False, "ZIP+4 must be in format 12345-6789"

        return True, None

    def calculate_shipping(self, order, shipping_method):
        """Calculate shipping from subtotal, method, item count, and destination."""
        subtotal = order.get_subtotal()
        if subtotal >= self.free_shipping_threshold:
            return 0.0

        rates = {
            ShippingMethod.STANDARD: 5.99,
            ShippingMethod.EXPRESS: 12.99,
            ShippingMethod.OVERNIGHT: 24.99,
            ShippingMethod.INTERNATIONAL: 35.99,
        }
        base_rate = rates.get(shipping_method, 5.99)

        item_count = sum(item["quantity"] for item in order.items)
        if item_count > 10:
            base_rate += 5.0
        elif item_count > 5:
            base_rate += 2.0

        if (
            shipping_method == ShippingMethod.INTERNATIONAL
            and order.shipping_address.get("country") != "US"
        ):
            base_rate += 15.0
        return base_rate

    def apply_discount(self, subtotal, discount_code):
        """Return discount amount and an optional error for a discount code."""
        if not discount_code:
            return 0.0, None

        code = discount_code.upper().strip()
        if code not in self.discount_codes:
            return 0.0, f"Invalid discount code: {discount_code}"

        discount_percent = self.discount_codes[code]
        if code == "FREESHIP":
            return 0.0, None

        discount_amount = subtotal * discount_percent
        if discount_amount > subtotal:
            discount_amount = subtotal
        return discount_amount, None

    def calculate_total(
        self, order, shipping_method=ShippingMethod.STANDARD, discount_code=None
    ):
        """Return a complete order-total breakdown."""
        subtotal = order.get_subtotal()
        discount_amount, discount_error = self.apply_discount(subtotal, discount_code)
        discounted_subtotal = subtotal - discount_amount
        tax = discounted_subtotal * self.tax_rate

        if discount_code and discount_code.upper().strip() == "FREESHIP":
            shipping = 0.0
        else:
            shipping = self.calculate_shipping(order, shipping_method)

        total = discounted_subtotal + tax + shipping
        return {
            "subtotal": subtotal,
            "discount": discount_amount,
            "discount_code": discount_code,
            "discount_error": discount_error,
            "discounted_subtotal": discounted_subtotal,
            "tax": tax,
            "tax_rate": self.tax_rate,
            "shipping": shipping,
            "shipping_method": shipping_method.value,
            "total": total,
        }

    def process_order(
        self, order, shipping_method=ShippingMethod.STANDARD, discount_code=None
    ):
        """Validate, total, and confirm an order."""
        is_valid, error = self.validate_order(order)
        if not is_valid:
            raise ValueError(f"Order validation failed: {error}")

        total_breakdown = self.calculate_total(order, shipping_method, discount_code)
        order.status = OrderStatus.CONFIRMED
        order.shipping_method = shipping_method
        order.discount_code = discount_code
        return {
            "order_id": order.order_id,
            "status": order.status.value,
            "total_breakdown": total_breakdown,
            "confirmed_at": datetime.now().isoformat(),
        }

    def estimate_delivery_date(self, order, shipping_method):
        """Estimate a delivery date without excluding weekends."""
        business_days = {
            ShippingMethod.STANDARD: 7,
            ShippingMethod.EXPRESS: 3,
            ShippingMethod.OVERNIGHT: 1,
            ShippingMethod.INTERNATIONAL: 14,
        }
        days = business_days.get(shipping_method, 7)
        if (
            shipping_method == ShippingMethod.INTERNATIONAL
            and order.shipping_address.get("country") != "US"
        ):
            days += 7
        return order.created_at + timedelta(days=days)
