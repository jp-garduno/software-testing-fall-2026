const path = require("path");
const fs = require("fs");
const { parse } = require("csv-parse/sync");
const Order = require("../src/orderCalculator");

const ESCENARIOS = [
    "pedido simplre n2 1 articulo",
    "10% de descuento apenas (limite enfeeriro)",
    "20% de descuento",
    "primer pedido (15%)",
    "NEWUSER en cliente regular (no aplica)",
    "codigo invalido (sin descuento)",
    "calcular impuesto con descuentos",
    "pedido por peso de varios productos",
    "pedido gratis",
    "pedido expres de varios productos",
];

const csvPath = path.join(__dirname, "..", "test_data", "orderCalculations.csv");
const records = parse(fs.readFileSync(csvPath, "utf8"), { columns: true, skip_empty_lines: true });

const testCases = ESCENARIOS.map((nombre) => {
    const row = records.find((r) => r.test_name === nombre);
    if (!row) throw new Error(`Escenario no encontrado en el CSV: ${nombre}`);
    return {
        testName: row.test_name,
        items: JSON.parse(row.items.replace(/'/g, '"')),
        customerType: row.customer_type,
        discountCode: row.discount_code === "NONE" ? null : row.discount_code,
        distance: parseFloat(row.distance_km),
        isExpress: row.is_express === "true",
        expected: {
            subtotal: parseFloat(row.expected_subtotal),
            discount: parseFloat(row.expected_discount),
            tax: parseFloat(row.expected_tax),
            shipping: parseFloat(row.expected_shipping),
            total: parseFloat(row.expected_total),
        },
    };
});

describe("Order (data-driven, datos desde CSV)", () => {
    test.each(testCases)(
        "$testName",
        ({ items, customerType, discountCode, distance, isExpress, expected }) => {
            const order = new Order(items, customerType);
            if (discountCode) order.applyDiscount(discountCode);
            order.setShipping(distance, isExpress);
            const result = order.calculateTotal();

            expect(result.subtotal).toBeCloseTo(expected.subtotal, 2);
            expect(result.discount).toBeCloseTo(expected.discount, 2);
            expect(result.tax).toBeCloseTo(expected.tax, 2);
            expect(result.shipping).toBeCloseTo(expected.shipping, 2);
            expect(result.total).toBeCloseTo(expected.total, 2);
        },
    );
});
