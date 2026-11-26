const assert = require("node:assert/strict");

function assertTotals(actual, expected) {
  assert.deepEqual(Object.keys(actual).sort(), Object.keys(expected).sort());
  for (const [field, value] of Object.entries(expected)) {
    if (typeof value === "number") {
      assert.ok(Math.abs(actual[field] - value) < 0.000001,
        `${field}: expected ${value}, got ${actual[field]}`);
    } else {
      assert.equal(actual[field], value, field);
    }
  }
}

module.exports = { assertTotals };
