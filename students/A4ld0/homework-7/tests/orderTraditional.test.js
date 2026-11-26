const Order = require("../src/orderCalculator");
const { assertTotals } = require("./assertTotals");

test("simple_one", () => {
  const order = new Order([{"name":"Item","price":40,"quantity":1,"weight":0}], "regular");
  order.setShipping(0, false);
  assertTotals(order.calculateTotal(), {"subtotal":40,"discount":0,"tax":3.2,"shipping":0,"total":43.2});
});

test("simple_quantity", () => {
  const order = new Order([{"name":"Item","price":12.5,"quantity":2,"weight":0}], "regular");
  order.setShipping(0, false);
  assertTotals(order.calculateTotal(), {"subtotal":25,"discount":0,"tax":2,"shipping":0,"total":27});
});

test("simple_empty", () => {
  const order = new Order([], "regular");
  order.setShipping(0, false);
  assertTotals(order.calculateTotal(), {"subtotal":0,"discount":0,"tax":0,"shipping":0,"total":0});
});

test("save10_above_threshold", () => {
  const order = new Order([{"name":"Item","price":50.01,"quantity":1,"weight":0}], "regular");
  order.applyDiscount("SAVE10");
  order.setShipping(0, false);
  assertTotals(order.calculateTotal(), {"subtotal":50.01,"discount":5.001,"tax":3.60072,"shipping":0,"total":48.60972});
});

test("save10_exact_threshold", () => {
  const order = new Order([{"name":"Item","price":50,"quantity":1,"weight":0}], "regular");
  order.applyDiscount("SAVE10");
  order.setShipping(0, false);
  assertTotals(order.calculateTotal(), {"subtotal":50,"discount":0,"tax":4,"shipping":0,"total":54});
});

test("save20_above_threshold", () => {
  const order = new Order([
    { name: "Item", price: 60, quantity: 1, weight: 0 },
    { name: "Item", price: 45, quantity: 1, weight: 0 }
  ], "regular");
  order.applyDiscount("SAVE20");
  order.setShipping(0, false);
  assertTotals(order.calculateTotal(), {"subtotal":105,"discount":21,"tax":6.72,"shipping":0,"total":90.72});
});

test("save20_exact_threshold", () => {
  const order = new Order([{"name":"Item","price":100,"quantity":1,"weight":0}], "regular");
  order.applyDiscount("SAVE20");
  order.setShipping(0, false);
  assertTotals(order.calculateTotal(), {"subtotal":100,"discount":0,"tax":8,"shipping":0,"total":108});
});

test("unknown_discount", () => {
  const order = new Order([{"name":"Item","price":120,"quantity":1,"weight":0}], "regular");
  order.applyDiscount("EXPIRED");
  order.setShipping(0, false);
  assertTotals(order.calculateTotal(), {"subtotal":120,"discount":0,"tax":9.6,"shipping":0,"total":129.6});
});

test("tax_without_discount", () => {
  const order = new Order([{"name":"Item","price":19.99,"quantity":1,"weight":0}], "regular");
  order.setShipping(0, false);
  assertTotals(order.calculateTotal(), {"subtotal":19.99,"discount":0,"tax":1.5992,"shipping":0,"total":21.5892});
});

test("tax_after_first_order_discount", () => {
  const order = new Order([{"name":"Item","price":80,"quantity":1,"weight":0}], "new");
  order.applyDiscount("NEWUSER");
  order.setShipping(0, false);
  assertTotals(order.calculateTotal(), {"subtotal":80,"discount":12,"tax":5.44,"shipping":0,"total":73.44});
});
