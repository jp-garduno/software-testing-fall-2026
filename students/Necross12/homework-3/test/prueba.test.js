const assert = require("node:assert");
const { test } = require("node:test");
const { Utils } = require("../src/utils");

test("Revisar rangos", () => {
  assert.strictEqual(Utils.cambiarNum(-5), 0);
  assert.strictEqual(Utils.cambiarNum(50), 50);
  assert.strictEqual(Utils.cambiarNum(150), 100);
});

test("revisar color", () => {
  assert.strictEqual(Utils.cambiarColor(10), "rojo");
  assert.strictEqual(Utils.cambiarColor(50), "amarillo");
  assert.strictEqual(Utils.cambiarColor(90), "verde");
});
