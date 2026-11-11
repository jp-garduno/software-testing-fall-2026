const { test } = require("node:test");
const assert = require("node:assert/strict");
const OrderWorkflow = require("../src/orderWorkflow");
const { loadWorkflows } = require("./testData");
const { assertTotals } = require("./assertTotals");

const handlers = {
  validate_customer: "validateCustomer",
  create_order: "createOrder",
  calculate_total: "calculateTotal",
  process_payment: "processPayment",
  confirm_order: "confirmOrder"
};

for (const { name, steps } of loadWorkflows()) {
  test(name, async t => {
    const workflow = new OrderWorkflow(new Date("2026-06-15T00:00:00Z"));
    for (const { action, data, expected } of steps) {
      const passed = await t.test(action, () => {
        assertTotals(workflow[handlers[action]](data), expected);
      });
      if (!passed) break;
    }
  });
}

test("paid orders cannot be created again or paid twice", () => {
  const workflow = new OrderWorkflow(new Date("2026-06-15T00:00:00Z"));
  const [validation, creation] = loadWorkflows()[0].steps;
  workflow.validateCustomer(validation.data);
  workflow.createOrder(creation.data);
  assert.deepEqual(workflow.createOrder(creation.data), { status: "rejected" });
  assert.deepEqual(workflow.processPayment(), { status: "rejected" });
  workflow.calculateTotal();
  assert.deepEqual(workflow.processPayment(), { status: "success" });
  assert.deepEqual(workflow.processPayment(), { status: "rejected" });
});
