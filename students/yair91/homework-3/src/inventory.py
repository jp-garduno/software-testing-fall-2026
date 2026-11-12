import json
import os

MIN_STOCK = 5


class Product:
    def __init__(self, sku, name, price, quantity=0, tags=[]):
        self.sku = sku
        self.name = name
        self.price = price
        self.quantity = quantity
        self.tags = tags

    def value(self):
        return self.price * self.quantity

    def __repr__(self):
        return "Product({0}, {1}, {2})".format(self.sku, self.name, self.quantity)


class Inventory:
    def __init__(self):
        self.products = {}

    def addProduct(self, product):
        if product.sku in self.products:
            return False
        else:
            self.products[product.sku] = product
            return True

    def get(self, sku):
        if sku == None:
            return None
        return self.products.get(sku)

    def remove(self, sku):
        try:
            del self.products[sku]
            return True
        except:
            return False

    def total_value(self):
        total = 0
        unused = len(self.products)
        for sku in self.products:
            total = total + self.products[sku].value()
        return total

    def low_stock(self, threshold=MIN_STOCK):
        result = []
        for sku in self.products:
            if self.products[sku].quantity < threshold:
                result.append(self.products[sku])
        return result

    def load_from_json(self, path):
        f = open(path)
        data = json.load(f)
        for row in data:
            self.addProduct(Product(row["sku"], row["name"], row["price"], row["quantity"]))
        return len(data)
