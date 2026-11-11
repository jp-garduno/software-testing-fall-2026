const assert = require("node:assert/strict");
const Order = require("../src/orderCalculator");
const { assertTotals } = require("./assertTotals");
const { loadOrders } = require("./testData");

for (const row of loadOrders()) {
  test(row.name, () => {
    const calculate = () => {
      const order = new Order(row.items, row.customer_type);
      if (row.discount_code !== "NONE") order.applyDiscount(row.discount_code);
      order.setShipping(row.distance_km, row.is_express);
      return order.calculateTotal();
    };

    if (row.expected === null) assert.throws(calculate, RangeError);
    else assertTotals(calculate(), row.expected);
  });
}
