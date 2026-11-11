const Order = require("../src/orderCalculator");
const { assertTotals } = require("./assertTotals");
const { loadOrders } = require("./testData");

for (const row of loadOrders().slice(0, 10)) {
  test(row.name, () => {
    const order = new Order(row.items, row.customer_type);
    if (row.discount_code !== "NONE") order.applyDiscount(row.discount_code);
    order.setShipping(row.distance_km, row.is_express);
    assertTotals(order.calculateTotal(), row.expected);
  });
}
