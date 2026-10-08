"""Shopping-cart classes used to practice class and branch testing."""


class Item:
    """Represent an item that can be placed in a shopping cart."""

    def __init__(self, name, price, quantity=1):
        """Create a valid item with a positive price and quantity."""
        if price <= 0:
            raise ValueError("Price must be positive")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.name = name
        self.price = price
        self.quantity = quantity

    def get_total(self):
        """Return the price for all units of this item."""
        return self.price * self.quantity

    def __eq__(self, other):
        """Compare items by name."""
        if not isinstance(other, Item):
            return False
        return self.name == other.name

    def __repr__(self):
        """Return an unambiguous display representation."""
        return f"Item('{self.name}', ${self.price}, qty={self.quantity})"


class ShoppingCart:
    """Maintain items and an optional percentage discount."""

    def __init__(self):
        """Create an empty cart with no discount."""
        self.items = []
        self.discount_percent = 0

    def add_item(self, item):
        """Add an item or increase the quantity of an existing item."""
        for existing_item in self.items:
            if existing_item.name == item.name:
                existing_item.quantity += item.quantity
                return
        self.items.append(item)

    def remove_item(self, item_name):
        """Remove an item by name and report whether it was found."""
        for index, item in enumerate(self.items):
            if item.name == item_name:
                self.items.pop(index)
                return True
        return False

    def get_subtotal(self):
        """Return the sum before applying a discount."""
        return sum(item.get_total() for item in self.items)

    def apply_discount(self, percent):
        """Set a discount percentage in the inclusive range from 0 to 100."""
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        self.discount_percent = percent

    def get_total(self):
        """Return the subtotal after the active discount."""
        subtotal = self.get_subtotal()
        discount_amount = subtotal * (self.discount_percent / 100)
        return subtotal - discount_amount

    def clear(self):
        """Remove every item and reset the discount."""
        self.items = []
        self.discount_percent = 0

    def get_item_count(self):
        """Return the total units across all cart items."""
        return sum(item.quantity for item in self.items)

    def is_empty(self):
        """Return whether the cart contains no item entries."""
        return len(self.items) == 0

