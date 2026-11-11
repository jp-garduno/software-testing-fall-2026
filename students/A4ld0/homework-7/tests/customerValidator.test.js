const { test } = require("node:test");
const assert = require("node:assert/strict");
const { validateCustomer } = require("../src/customerValidator");
const { loadCustomers } = require("./testData");

const today = new Date("2026-06-15T00:00:00Z");

for (const { test_name, customer, expected } of loadCustomers()) {
  test(test_name, () => assert.deepEqual(validateCustomer(customer, today), expected));
}
