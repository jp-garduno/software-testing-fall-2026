from datetime import datetime


class Movement:
    def __init__(self, sku, kind, quantity, note=""):
        self.sku = sku
        self.kind = kind
        self.quantity = quantity
        self.note = note
        self.at = datetime.now()


class MovementLog:
    def __init__(self, inventory):
        self.inventory = inventory
        self.entries = []

    def receive(self, sku, quantity, note=""):
        p = self.inventory.get(sku)
        if p == None:
            return False
        if quantity <= 0:
            return False
        p.quantity = p.quantity + quantity
        self.entries.append(Movement(sku, "in", quantity, note))
        return True

    def issue(self, sku, quantity, note=""):
        p = self.inventory.get(sku)
        if p == None:
            return False
        if quantity <= 0:
            return False
        if p.quantity < quantity:
            return False
        else:
            p.quantity = p.quantity - quantity
            self.entries.append(Movement(sku, "out", quantity, note))
            return True

    def history(self, sku=None):
        if sku == None:
            return self.entries
        out = []
        for e in self.entries:
            if e.sku == sku:
                out.append(e)
        return out

    def summary(self):
        received = 0
        issued = 0
        for e in self.entries:
            if e.kind == "in":
                received = received + e.quantity
            else:
                issued = issued + e.quantity
        return {"received": received, "issued": issued, "net": received - issued, "entries": len(self.entries)}
