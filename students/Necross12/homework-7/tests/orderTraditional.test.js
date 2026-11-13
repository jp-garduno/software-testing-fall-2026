const Order = require("../src/orderCalculator");

describe("Order (tradicional, datos hardcodeados)", () => {
    test("pedido simple de 1 articulo", () => {
        const order = new Order([{ name: "Item1", price: 50, quantity: 1, weight: 1 }], "regular");
        order.setShipping(10, false);
        const result = order.calculateTotal();

        expect(result.subtotal).toBeCloseTo(50.0, 2);
        expect(result.discount).toBeCloseTo(0.0, 2);
        expect(result.tax).toBeCloseTo(4.0, 2);
        expect(result.shipping).toBeCloseTo(1.5, 2);
        expect(result.total).toBeCloseTo(55.5, 2);
    });

    test("SAVE10 aplica justo en el limite de $50", () => {
        const order = new Order([{ name: "A", price: 50, quantity: 1, weight: 0 }], "regular");
        order.applyDiscount("SAVE10");
        order.setShipping(0, false);
        const result = order.calculateTotal();

        expect(result.subtotal).toBeCloseTo(50.0, 2);
        expect(result.discount).toBeCloseTo(5.0, 2);
        expect(result.tax).toBeCloseTo(3.6, 2);
        expect(result.shipping).toBeCloseTo(0.0, 2);
        expect(result.total).toBeCloseTo(48.6, 2);
    });

    test("SAVE20 aplica justo en el limite de $100", () => {
        const order = new Order([{ name: "A", price: 100, quantity: 1, weight: 0 }], "regular");
        order.applyDiscount("SAVE20");
        order.setShipping(0, false);
        const result = order.calculateTotal();

        expect(result.subtotal).toBeCloseTo(100.0, 2);
        expect(result.discount).toBeCloseTo(20.0, 2);
        expect(result.tax).toBeCloseTo(6.4, 2);
        expect(result.shipping).toBeCloseTo(0.0, 2);
        expect(result.total).toBeCloseTo(86.4, 2);
    });

    test("NEWUSER aplica 15% a un cliente nuevo", () => {
        const order = new Order([{ name: "A", price: 40, quantity: 1, weight: 0 }], "new");
        order.applyDiscount("NEWUSER");
        order.setShipping(0, false);
        const result = order.calculateTotal();

        expect(result.subtotal).toBeCloseTo(40.0, 2);
        expect(result.discount).toBeCloseTo(6.0, 2);
        expect(result.tax).toBeCloseTo(2.72, 2);
        expect(result.shipping).toBeCloseTo(0.0, 2);
        expect(result.total).toBeCloseTo(36.72, 2);
    });

    test("NEWUSER no aplica a un cliente regular", () => {
        const order = new Order([{ name: "A", price: 40, quantity: 1, weight: 0 }], "regular");
        order.applyDiscount("NEWUSER");
        order.setShipping(0, false);
        const result = order.calculateTotal();

        expect(result.subtotal).toBeCloseTo(40.0, 2);
        expect(result.discount).toBeCloseTo(0.0, 2);
        expect(result.tax).toBeCloseTo(3.2, 2);
        expect(result.shipping).toBeCloseTo(0.0, 2);
        expect(result.total).toBeCloseTo(43.2, 2);
    });

    test("codigo invalido no da descuento", () => {
        const order = new Order([{ name: "A", price: 40, quantity: 2, weight: 0 }], "regular");
        order.applyDiscount("SAVE99");
        order.setShipping(0, false);
        const result = order.calculateTotal();

        expect(result.subtotal).toBeCloseTo(80.0, 2);
        expect(result.discount).toBeCloseTo(0.0, 2);
        expect(result.tax).toBeCloseTo(6.4, 2);
        expect(result.shipping).toBeCloseTo(0.0, 2);
        expect(result.total).toBeCloseTo(86.4, 2);
    });

    test("el impuesto se calcula despues del descuento", () => {
        const order = new Order([{ name: "A", price: 200, quantity: 1, weight: 0 }], "regular");
        order.applyDiscount("SAVE20");
        order.setShipping(0, false);
        const result = order.calculateTotal();

        expect(result.subtotal).toBeCloseTo(200.0, 2);
        expect(result.discount).toBeCloseTo(40.0, 2);
        expect(result.tax).toBeCloseTo(12.8, 2);
        expect(result.shipping).toBeCloseTo(0.0, 2);
        expect(result.total).toBeCloseTo(172.8, 2);
    });

    test("envio por peso de varios productos (peso x cantidad)", () => {
        const order = new Order(
            [
                { name: "A", price: 10, quantity: 2, weight: 1.5 },
                { name: "B", price: 15, quantity: 1, weight: 4 },
            ],
            "regular",
        );
        order.setShipping(0, false);
        const result = order.calculateTotal();

        expect(result.subtotal).toBeCloseTo(35.0, 2);
        expect(result.discount).toBeCloseTo(0.0, 2);
        expect(result.tax).toBeCloseTo(2.8, 2);
        expect(result.shipping).toBeCloseTo(3.5, 2);
        expect(result.total).toBeCloseTo(41.3, 2);
    });

    test("FREESHIP deja el envio en 0", () => {
        const order = new Order([{ name: "A", price: 30, quantity: 1, weight: 5 }], "regular");
        order.applyDiscount("FREESHIP");
        order.setShipping(100, false);
        const result = order.calculateTotal();

        expect(result.subtotal).toBeCloseTo(30.0, 2);
        expect(result.discount).toBeCloseTo(0.0, 2);
        expect(result.tax).toBeCloseTo(2.4, 2);
        expect(result.shipping).toBeCloseTo(0.0, 2);
        expect(result.total).toBeCloseTo(32.4, 2);
    });

    test("envio expres de varios productos (x1.5)", () => {
        const order = new Order(
            [
                { name: "A", price: 10, quantity: 2, weight: 2 },
                { name: "B", price: 25, quantity: 1, weight: 1 },
            ],
            "regular",
        );
        order.setShipping(20, true);
        const result = order.calculateTotal();

        expect(result.subtotal).toBeCloseTo(45.0, 2);
        expect(result.discount).toBeCloseTo(0.0, 2);
        expect(result.tax).toBeCloseTo(3.6, 2);
        expect(result.shipping).toBeCloseTo(6.75, 2);
        expect(result.total).toBeCloseTo(55.35, 2);
    });
});
