const path = require("path");
const fs = require("fs");
const { parse } = require("csv-parse/sync");
const Order = require("../src/orderCalculator");

let csvPath = path.join(__dirname, "..", "test_data", "orderCalculations.csv");
let records = parse(fs.readFileSync(csvPath, "utf8"), {
  columns: true,
  skip_empty_lines: true,
});

let testCases = records.map((row) => ({
  testName: row.test_name,
  items: JSON.parse(row.items.replace(/'/g, '"')),
  customerType: row.customer_type,
  discountCode: row.discount_code === "NONE" ? null : row.discount_code,
  distance: parseFloat(row.distance_km),
  isExpress: row.is_express === "true",
  expectError: row.expected_subtotal === "ERROR",
  expected: {
    subtotal: parseFloat(row.expected_subtotal),
    discount: parseFloat(row.expected_discount),
    tax: parseFloat(row.expected_tax),
    shipping: parseFloat(row.expected_shipping),
    total: parseFloat(row.expected_total),
  },
}));

describe("Order de datos data-driven desde CSV", () => {
  test.each(testCases)(
    "Order calculation: $testName",
    ({
      items,
      customerType,
      discountCode,
      distance,
      isExpress,
      expected,
      expectError,
    }) => {
      const calculate = () => {
        const order = new Order(items, customerType);
        if (discountCode) order.applyDiscount(discountCode);
        order.setShipping(distance, isExpress);
        return order.calculateTotal();
      };
      if (expectError) {
        expect(calculate).toThrow();
        return;
      }
      const result = calculate();

      expect(result.subtotal).toBeCloseTo(expected.subtotal, 2);
      expect(result.discount).toBeCloseTo(expected.discount, 2);
      expect(result.tax).toBeCloseTo(expected.tax, 2);
      expect(result.shipping).toBeCloseTo(expected.shipping, 2);
      expect(result.total).toBeCloseTo(expected.total, 2);
    },
  );
});

// si existe el archibo probar, si no, no
if (
  fs.existsSync(path.join(__dirname, "..", "test_data", "100PruebasAlAzar.csv"))
) {
  csvPath = path.join(__dirname, "..", "test_data", "100PruebasAlAzar.csv");
  records = parse(fs.readFileSync(csvPath, "utf8"), {
    columns: true,
    skip_empty_lines: true,
  });

  testCases = records.map((row) => ({
    testName: row.test_name,
    items: JSON.parse(row.items.replace(/'/g, '"')),
    customerType: row.customer_type,
    discountCode: row.discount_code === "NONE" ? null : row.discount_code,
    distance: parseFloat(row.distance_km),
    isExpress: row.is_express === "true",
    expectError: row.expected_subtotal === "ERROR",
    expected: {
      subtotal: parseFloat(row.expected_subtotal),
      discount: parseFloat(row.expected_discount),
      tax: parseFloat(row.expected_tax),
      shipping: parseFloat(row.expected_shipping),
      total: parseFloat(row.expected_total),
    },
  }));

  describe("Order de datos aleatorios desde CSV", () => {
    test.each(testCases)(
      "Order calculation: $testName",
      ({
        items,
        customerType,
        discountCode,
        distance,
        isExpress,
        expected,
        expectError,
      }) => {
        const calculate = () => {
          const order = new Order(items, customerType);
          if (discountCode) order.applyDiscount(discountCode);
          order.setShipping(distance, isExpress);
          return order.calculateTotal();
        };
        if (expectError) {
          expect(calculate).toThrow();
          return;
        }
        const result = calculate();

        expect(result.subtotal).toBeCloseTo(expected.subtotal, 2);
        expect(result.discount).toBeCloseTo(expected.discount, 2);
        expect(result.tax).toBeCloseTo(expected.tax, 2);
        expect(result.shipping).toBeCloseTo(expected.shipping, 2);
        expect(result.total).toBeCloseTo(expected.total, 2);
      },
    );
  });
}

describe("Order con distancia que no es un numero", () => {
  test.each([["abc"], [NaN], [undefined]])(
    "setShipping(%p) lanza error",
    (distancia) => {
      const order = new Order(
        [{ name: "A", price: 10, quantity: 1, weight: 0 }],
        "regular",
      );
      expect(() => order.setShipping(distancia, false)).toThrow(
        "La distancia debe ser un número",
      );
    },
  );
});

describe("Order con parametros por defecto", () => {
  test("sin customerType es regular (NEWUSER no aplica) y sin isExpress el envio es estandar", () => {
    const order = new Order([{ name: "A", price: 10, quantity: 1, weight: 2 }]);
    expect(order.applyDiscount("NEWUSER")).toBe(false);
    order.setShipping(10);
    expect(order.calculateShipping()).toBeCloseTo(2.0, 2);
  });
});
