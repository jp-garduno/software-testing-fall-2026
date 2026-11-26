const Order = require("./orderCalculator");
const { validateCustomer } = require("./customerValidator");

class OrderWorkflow {
  constructor(today = new Date()) {
    this.today = today;
    this.customerValid = false;
    this.order = null;
    this.totals = null;
    this.paid = false;
  }

  validateCustomer(customer) {
    this.customerValid = validateCustomer(customer, this.today).is_valid;
    return { valid: this.customerValid };
  }

  createOrder({ items, customer_type, discount_code, distance_km, is_express }) {
    if (!this.customerValid || this.order) return { status: "rejected" };
    const order = new Order(items, customer_type);
    order.setShipping(distance_km, is_express);
    if (discount_code) order.applyDiscount(discount_code);
    this.order = order;
    return { status: "created" };
  }

  calculateTotal() {
    if (!this.order) return { status: "rejected" };
    this.totals = this.order.calculateTotal();
    return { total: this.totals.total };
  }

  processPayment() {
    if (!this.customerValid || !this.totals || this.paid) return { status: "rejected" };
    this.paid = true;
    return { status: "success" };
  }

  confirmOrder() {
    if (!this.paid) return { status: "rejected" };
    return { status: "confirmed", total: this.totals.total };
  }
}

module.exports = OrderWorkflow;
