"""Stock movements: what came in, what went out, and when."""

from datetime import datetime


class Movement:
    """One stock movement against a SKU."""

    def __init__(self, sku, kind, quantity, note=""):
        """Record the movement and stamp it with the current time."""
        self.sku = sku
        self.kind = kind
        self.quantity = quantity
        self.note = note
        self.at = datetime.now()

    def as_dict(self):
        """Return the movement as a plain dictionary, ready to serialise."""
        return {
            "sku": self.sku,
            "kind": self.kind,
            "quantity": self.quantity,
            "note": self.note,
            "at": self.at.isoformat(),
        }


class MovementLog:
    """The running log of movements against an inventory."""

    def __init__(self, inventory):
        """Bind the log to the inventory whose stock it will adjust."""
        self.inventory = inventory
        self.entries = []

    def receive(self, sku, quantity, note=""):
        """Add stock for a SKU and report whether it was accepted."""
        product = self.inventory.get(sku)
        if product is None or quantity <= 0:
            return False

        product.quantity += quantity
        self.entries.append(Movement(sku, "in", quantity, note))
        return True

    def issue(self, sku, quantity, note=""):
        """Take stock out of a SKU, refusing to go below zero."""
        product = self.inventory.get(sku)
        if product is None or quantity <= 0 or product.quantity < quantity:
            return False

        product.quantity -= quantity
        self.entries.append(Movement(sku, "out", quantity, note))
        return True

    def history(self, sku=None):
        """Return every movement, or only the ones for one SKU."""
        if sku is None:
            return self.entries
        return [entry for entry in self.entries if entry.sku == sku]

    def summary(self):
        """Return totals in, out, the net change and the movement count."""
        received = sum(entry.quantity for entry in self.entries if entry.kind == "in")
        issued = sum(entry.quantity for entry in self.entries if entry.kind == "out")

        return {
            "received": received,
            "issued": issued,
            "net": received - issued,
            "entries": len(self.entries),
        }
