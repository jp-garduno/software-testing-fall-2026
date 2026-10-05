"""Shopping cart implementation for white-box testing exercise 2."""


class Item:
    """Represents an item in the shopping cart."""

    def __init__(self, name, price, quantity=1):
        """Initialize an item with a positive price and quantity."""
        if price <= 0:
            raise ValueError("Price must be positive")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.name = name
        self.price = price
        self.quantity = quantity

    def get_total(self):
        """Calculate total cost for this item."""
        return self.price * self.quantity

    def __eq__(self, other):
        """Check equality based on name."""
        if not isinstance(other, Item):
            return False
        return self.name == other.name

    def __repr__(self):
        """Return a readable representation of an item."""
        return f"Item('{self.name}', ${self.price}, qty={self.quantity})"


class ShoppingCart:
    """A shopping cart that can hold multiple items."""

    def __init__(self):
        """Initialize an empty shopping cart."""
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
        """Calculate subtotal before discount."""
        return sum(item.get_total() for item in self.items)

    def apply_discount(self, percent):
        """Apply a discount percentage between zero and one hundred."""
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        self.discount_percent = percent

    def get_total(self):
        """Calculate total after discount."""
        subtotal = self.get_subtotal()
        discount_amount = subtotal * (self.discount_percent / 100)
        return subtotal - discount_amount

    def clear(self):
        """Remove all items and reset the discount."""
        self.items = []
        self.discount_percent = 0

    def get_item_count(self):
        """Get the total number of item units."""
        return sum(item.quantity for item in self.items)

    def is_empty(self):
        """Check whether the cart has no entries."""
        return len(self.items) == 0
