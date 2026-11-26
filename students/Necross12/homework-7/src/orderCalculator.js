const round = (n) => Math.round((n + Number.EPSILON) * 100) / 100;

const CODES = {
  SAVE10: { min: 50, pct: 0.1 },
  SAVE20: { min: 100, pct: 0.2 },
  FREESHIP: { min: 0, pct: 0 },
  NEWUSER: { min: 0, pct: 0.15 },
};

function validateItems(items) {
  if (!Array.isArray(items))
    throw new Error("Los productos deben ser un arreglo");

  for (const item of items) {
    if (!item || typeof item !== "object")
      throw new Error("Cada producto debe ser un objeto");
    if (
      typeof item.price !== "number" ||
      !Number.isFinite(item.price) ||
      typeof item.quantity !== "number" ||
      !Number.isFinite(item.quantity)
    )
      throw new Error("El precio y la cantidad deben ser números");
    if (item.price < 0 || item.quantity < 0)
      throw new Error("El precio y la cantidad no deben ser negativos");
    if (item.price === 0) throw new Error("El precio debe ser mayor que cero");
    if (
      item.weight !== undefined &&
      (typeof item.weight !== "number" || !Number.isFinite(item.weight))
    )
      throw new Error("El peso debe ser un número");
    if (item.weight < 0) throw new Error("El peso no debe ser negativo");
  }
}

// quisas debería que hacer una clase producto y la lista llamarla carrito, jejejeje
/*
class Product {
    constructor(name, price, weight = 0) {
        this.name = name;
        this.price = price;
        this.weight = weight;
    }
}
    */

class Order {
  constructor(items, customerType = "regular") {
    this.items = items;
    this.customerType = customerType;
    this.discountCode = null;
    this.shippingDistance = 0;
    this.isExpress = false;
  }

  applyDiscount(code) {
    const rule = CODES[code];
    if (!rule) return false;
    if (rule.min >= 0 && this.calculateSubtotal() < rule.min) return false;
    if (code === "NEWUSER" && this.customerType !== "new") return false;
    this.discountCode = code;
    return true;
  }

  setShipping(distanceKm, isExpress = false) {
    if (typeof distanceKm !== "number" || !Number.isFinite(distanceKm))
      throw new Error("La distancia debe ser un número");
    if (distanceKm < 0) throw new Error("La distancia no debe ser negativa");
    this.shippingDistance = distanceKm;
    this.isExpress = isExpress;
  }

  calculateSubtotal() {
    validateItems(this.items);
    return round(this.items.reduce((sum, i) => sum + i.price * i.quantity, 0));
  }

  calculateDiscount() {
    if (!this.discountCode) return 0;
    return round(this.calculateSubtotal() * CODES[this.discountCode].pct);
  }

  calculateTax() {
    return round((this.calculateSubtotal() - this.calculateDiscount()) * 0.08);
  }

  calculateShipping() {
    validateItems(this.items);
    if (this.discountCode === "FREESHIP") return 0;
    const weight = this.items.reduce(
      (s, i) => s + (i.weight || 0) * i.quantity,
      0,
    );
    let cost = weight * 0.5 + this.shippingDistance * 0.1;
    if (this.isExpress) cost *= 1.5;
    return round(cost);
  }

  calculateTotal() {
    const subtotal = this.calculateSubtotal();
    const discount = this.calculateDiscount();
    const tax = this.calculateTax();
    const shipping = this.calculateShipping();
    return {
      subtotal,
      discount,
      tax,
      shipping,
      total: round(subtotal - discount + tax + shipping),
    };
  }
}

module.exports = Order;
