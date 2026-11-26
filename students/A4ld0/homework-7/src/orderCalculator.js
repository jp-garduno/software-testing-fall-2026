const discounts = { SAVE10: 0.10, SAVE20: 0.20, NEWUSER: 0.15, FREESHIP: 0 };

class Order {
  constructor(items, customerType = "regular") {
    for (const { price, quantity, weight } of items) {
      if (!Number.isFinite(price) || price < 0 ||
          !Number.isSafeInteger(quantity) || quantity < 0 ||
          !Number.isFinite(weight) || weight < 0) {
        throw new RangeError("Invalid item price, quantity, or weight");
      }
    }
    this.items = items;
    this.customerType = customerType;
    this.discountCode = null;
    this.shippingDistance = 0;
    this.isExpress = false;
  }

  applyDiscount(code) {
    const subtotal = this.calculateSubtotal();
    const eligible = Object.hasOwn(discounts, code) &&
      (code !== "SAVE10" || subtotal > 50) &&
      (code !== "SAVE20" || subtotal > 100) &&
      (code !== "NEWUSER" || this.customerType === "new");
    if (eligible) this.discountCode = code;
    return eligible;
  }

  setShipping(distanceKm, isExpress = false) {
    if (!Number.isFinite(distanceKm) || distanceKm < 0) {
      throw new RangeError("Invalid shipping distance");
    }
    this.shippingDistance = distanceKm;
    this.isExpress = isExpress;
  }

  calculateSubtotal() {
    return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }

  calculateDiscount() {
    return this.calculateSubtotal() * (discounts[this.discountCode] ?? 0);
  }

  calculateTax() {
    return (this.calculateSubtotal() - this.calculateDiscount()) * 0.08;
  }

  calculateShipping() {
    if (this.discountCode === "FREESHIP") return 0;
    const weight = this.items.reduce((sum, item) => sum + item.weight * item.quantity, 0);
    const base = 0.5 * weight + 0.1 * this.shippingDistance;
    return base * (this.isExpress ? 1.5 : 1);
  }

  calculateTotal() {
    const subtotal = this.calculateSubtotal();
    const discount = this.calculateDiscount();
    const tax = this.calculateTax();
    const shipping = this.calculateShipping();
    return { subtotal, discount, tax, shipping, total: subtotal - discount + tax + shipping };
  }
}

module.exports = Order;
