"""Product catalogue and stock levels for a small warehouse."""

import json

MIN_STOCK = 5


class Product:
    """A single catalogue entry with its price and the stock on hand."""

    def __init__(self, sku, name, price, quantity=0):
        """Store the product with an empty tag list of its own.

        Tags are set afterwards through add_tag rather than taken here. The
        first version accepted `tags=[]`, which creates the list once and
        shares it between every product built without tags; moving it out
        removes the shared-state bug and keeps the constructor to five
        arguments.
        """
        self.sku = sku
        self.name = name
        self.price = price
        self.quantity = quantity
        self.tags = []

    def value(self):
        """Return the money tied up in this product."""
        return self.price * self.quantity

    def add_tag(self, tag):
        """Add a tag once, ignoring repeats."""
        if tag not in self.tags:
            self.tags.append(tag)
        return self.tags

    def __repr__(self):
        """Readable form used when a product shows up in a traceback."""
        return f"Product({self.sku}, {self.name}, {self.quantity})"


class Inventory:
    """The catalogue: products indexed by SKU."""

    def __init__(self):
        """Start with an empty catalogue."""
        self.products = {}

    def add_product(self, product):
        """Add a product, or report False when the SKU is already taken."""
        if product.sku in self.products:
            return False

        self.products[product.sku] = product
        return True

    def get(self, sku):
        """Return the product for a SKU, or None when it is not catalogued."""
        if sku is None:
            return None
        return self.products.get(sku)

    def remove(self, sku):
        """Remove a product and report whether it was there to begin with."""
        try:
            del self.products[sku]
            return True
        except KeyError:
            return False

    def total_value(self):
        """Return the value of the whole catalogue."""
        return sum(product.value() for product in self.products.values())

    def low_stock(self, threshold=MIN_STOCK):
        """Return the products at or below the reorder point."""
        return [product for product in self.products.values() if product.quantity < threshold]

    def load_from_json(self, path):
        """Load products from a JSON file and return how many were read."""
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)

        for row in data:
            self.add_product(Product(row["sku"], row["name"], row["price"], row["quantity"]))
        return len(data)
