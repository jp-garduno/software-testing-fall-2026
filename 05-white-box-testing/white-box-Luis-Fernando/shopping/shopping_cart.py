class Item:
    """Represents an item in the shopping cart."""

    def __init__(self, name, price, quantity=1):
        """
        Initialize an item.

        Args:
            name: Item name
            price: Item price (must be positive)
            quantity: Number of items (must be positive)

        Raises:
            ValueError: If price or quantity is invalid
        """
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
        """String representation of the item."""
        return f"Item('{self.name}', ${self.price}, qty={self.quantity})"


class ShoppingCart:
    """A shopping cart that can hold multiple items."""

    def __init__(self):
        """Initialize an empty shopping cart."""
        self.items = []
        self.discount_percent = 0

    def add_item(self, item):
        """
        Add an item to the cart. If item already exists, increase quantity.

        Args:
            item: Item object to add
        """
        # Check if item already exists
        for existing_item in self.items:
            if existing_item.name == item.name:
                existing_item.quantity += item.quantity
                return

        # Add new item
        self.items.append(item)

    def remove_item(self, item_name):
        """
        Remove an item from the cart by name.

        Args:
            item_name: Name of the item to remove

        Returns:
            True if item was removed, False if not found
        """
        for i, item in enumerate(self.items):
            if item.name == item_name:
                self.items.pop(i)
                return True
        return False

    def get_subtotal(self):
        """Calculate subtotal before discount."""
        return sum(item.get_total() for item in self.items)

    def apply_discount(self, percent):
        """
        Apply a discount percentage to the cart.

        Args:
            percent: Discount percentage (0-100)

        Raises:
            ValueError: If percent is not between 0 and 100
        """
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        self.discount_percent = percent

    def get_total(self):
        """Calculate total after discount."""
        subtotal = self.get_subtotal()
        discount_amount = subtotal * (self.discount_percent / 100)
        return subtotal - discount_amount

    def clear(self):
        """Remove all items from the cart."""
        self.items = []
        self.discount_percent = 0

    def get_item_count(self):
        """Get total number of items (sum of all quantities)."""
        return sum(item.quantity for item in self.items)

    def is_empty(self):
        """Check if cart is empty."""
        return len(self.items) == 0