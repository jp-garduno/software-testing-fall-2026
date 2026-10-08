const {
  Order,
  OrderProcessor,
  OrderStatus,
  ShippingMethod,
} = require("../src/orderProcessor");

const validAddress = () => ({
  street: "123 Main St",
  city: "Springfield",
  state: "IL",
  zip_code: "62701",
  country: "US",
});

const makeOrder = (items, address = validAddress()) =>
  new Order("ORD-001", "CUST-001", items, address);

const widget = (price = 10, quantity = 2) => ({ name: "Widget", price, quantity });

describe("OrderProcessor", () => {
  let processor;
  let sampleOrder;

  beforeEach(() => {
    processor = new OrderProcessor();
    sampleOrder = makeOrder([widget()]);
  });

  describe("Order", () => {
    test("initializes with default state", () => {
      expect(sampleOrder.status).toBe(OrderStatus.PENDING);
      expect(sampleOrder.shippingMethod).toBeNull();
      expect(sampleOrder.discountCode).toBeNull();
      expect(sampleOrder.trackingNumber).toBeNull();
      expect(sampleOrder.createdAt).toBeInstanceOf(Date);
    });

    test("getSubtotal sums price * quantity", () => {
      const order = makeOrder([widget(10, 2), widget(5.5, 2)]);
      expect(order.getSubtotal()).toBeCloseTo(31);
    });

    test("getSubtotal is 0 for no items", () => {
      expect(makeOrder([]).getSubtotal()).toBe(0);
    });

    test.each([
      ["price", { name: "A", quantity: 3 }],
      ["quantity", { name: "A", price: 3 }],
    ])("getSubtotal ignores items missing %s", (_f, badItem) => {
      const order = makeOrder([badItem, widget(10, 1)]);
      expect(order.getSubtotal()).toBe(10);
    });
  });

  describe("constructor", () => {
    test("uses default tax rate and threshold", () => {
      expect(processor.taxRate).toBe(0.08);
      expect(processor.freeShippingThreshold).toBe(50.0);
    });

    test("accepts custom tax rate and threshold", () => {
      const p = new OrderProcessor(0.1, 100);
      expect(p.taxRate).toBe(0.1);
      expect(p.freeShippingThreshold).toBe(100);
    });
  });

  describe("validateOrder", () => {
    test("accepts a valid order", () => {
      expect(processor.validateOrder(sampleOrder)).toEqual({
        isValid: true,
        error: null,
      });
    });

    test.each([
      ["items is undefined", undefined],
      ["items is empty", []],
    ])("rejects order when %s", (_d, items) => {
      const result = processor.validateOrder(makeOrder(items));
      expect(result.isValid).toBe(false);
      expect(result.error).toBe("Order must contain at least one item");
    });

    test.each([
      ["name is missing", { price: 10, quantity: 1 }, "Item 0 is missing name"],
      ["name is empty", { name: "", price: 10, quantity: 1 }, "Item 0 is missing name"],
      ["price is missing", { name: "A", quantity: 1 }, "Item 0 is missing price"],
      ["price is zero", { name: "A", price: 0, quantity: 1 }, "Item 0 has invalid price"],
      ["price is negative", { name: "A", price: -5, quantity: 1 }, "Item 0 has invalid price"],
      ["quantity is missing", { name: "A", price: 10 }, "Item 0 is missing quantity"],
      ["quantity is zero", { name: "A", price: 10, quantity: 0 }, "Item 0 has invalid quantity"],
      ["quantity is negative", { name: "A", price: 10, quantity: -1 }, "Item 0 has invalid quantity"],
      ["quantity exceeds 100", { name: "A", price: 10, quantity: 101 }, "Item 0 quantity exceeds maximum (100)"],
    ])("rejects item when %s", (_d, item, expectedError) => {
      const result = processor.validateOrder(makeOrder([item]));
      expect(result).toEqual({ isValid: false, error: expectedError });
    });

    test("accepts quantity of exactly 100 (boundary)", () => {
      const result = processor.validateOrder(makeOrder([widget(1, 100)]));
      expect(result.isValid).toBe(true);
    });

    test("reports the index of the offending item", () => {
      const result = processor.validateOrder(
        makeOrder([widget(), { price: 10, quantity: 1 }]),
      );
      expect(result.error).toBe("Item 1 is missing name");
    });

    test("rejects order without shipping address", () => {
      const result = processor.validateOrder(makeOrder([widget()], null));
      expect(result).toEqual({
        isValid: false,
        error: "Shipping address is required",
      });
    });

    test.each(["street", "city", "state", "zip_code", "country"])(
      "rejects address missing %s",
      (field) => {
        const address = validAddress();
        delete address[field];
        const result = processor.validateOrder(makeOrder([widget()], address));
        expect(result).toEqual({
          isValid: false,
          error: `Shipping address missing ${field}`,
        });
      },
    );

    test("rejects address with empty string field", () => {
      const address = { ...validAddress(), city: "" };
      const result = processor.validateOrder(makeOrder([widget()], address));
      expect(result.error).toBe("Shipping address missing city");
    });

    describe("US ZIP codes", () => {
      test.each([
        ["1234", "Invalid US ZIP code format"],
        ["123456", "Invalid US ZIP code format"],
        ["123456789", "Invalid US ZIP code format"],
        ["12a45", "ZIP code must be 5 digits"],
        ["12345-678a", "ZIP+4 must be in format 12345-6789"],
        ["123456-789", "ZIP+4 must be in format 12345-6789"],
        ["1234567890", "ZIP+4 must be in format 12345-6789"],
      ])("rejects %s", (zip, expectedError) => {
        const address = { ...validAddress(), zip_code: zip };
        const result = processor.validateOrder(makeOrder([widget()], address));
        expect(result).toEqual({ isValid: false, error: expectedError });
      });

      test.each(["62701", "62701-1234"])("accepts %s", (zip) => {
        const address = { ...validAddress(), zip_code: zip };
        expect(
          processor.validateOrder(makeOrder([widget()], address)).isValid,
        ).toBe(true);
      });
    });

    test("does not apply US ZIP rules to other countries", () => {
      const address = { ...validAddress(), country: "CA", zip_code: "K1A 0B1" };
      expect(
        processor.validateOrder(makeOrder([widget()], address)).isValid,
      ).toBe(true);
    });
  });

  describe("calculateShipping", () => {
    const orderWithCount = (count, country = "US", price = 1) =>
      makeOrder([widget(price, count)], { ...validAddress(), country });

    test.each([
      [ShippingMethod.STANDARD, 5.99],
      [ShippingMethod.EXPRESS, 12.99],
      [ShippingMethod.OVERNIGHT, 24.99],
      [ShippingMethod.INTERNATIONAL, 35.99], // US address: no surcharge
      ["unknown-method", 5.99],
      [undefined, 5.99],
    ])("base rate for %s is %d", (method, expected) => {
      expect(processor.calculateShipping(orderWithCount(1), method)).toBeCloseTo(
        expected,
      );
    });

    test("free shipping when subtotal is above threshold", () => {
      const order = makeOrder([widget(60, 1)]);
      expect(processor.calculateShipping(order, ShippingMethod.OVERNIGHT)).toBe(0);
    });

    test("free shipping when subtotal equals threshold exactly", () => {
      const order = makeOrder([widget(50, 1)]);
      expect(processor.calculateShipping(order, ShippingMethod.STANDARD)).toBe(0);
    });

    test("charges shipping just below threshold", () => {
      const order = makeOrder([widget(49.99, 1)]);
      expect(processor.calculateShipping(order, ShippingMethod.STANDARD)).toBeCloseTo(5.99);
    });

    test("respects a custom free shipping threshold", () => {
      const p = new OrderProcessor(0.08, 10);
      expect(p.calculateShipping(makeOrder([widget(10, 1)]), ShippingMethod.STANDARD)).toBe(0);
    });

    test.each([
      [5, 5.99], // boundary: not > 5
      [6, 7.99], // > 5
      [10, 7.99], // boundary: not > 10
      [11, 10.99], // > 10
    ])("item count %d adds surcharge -> %d", (count, expected) => {
      expect(
        processor.calculateShipping(orderWithCount(count), ShippingMethod.STANDARD),
      ).toBeCloseTo(expected);
    });

    test("international method to non-US adds $15 surcharge", () => {
      expect(
        processor.calculateShipping(orderWithCount(1, "MX"), ShippingMethod.INTERNATIONAL),
      ).toBeCloseTo(50.99);
    });

    test("international surcharge combines with item count surcharge", () => {
      expect(
        processor.calculateShipping(orderWithCount(11, "MX"), ShippingMethod.INTERNATIONAL),
      ).toBeCloseTo(55.99);
    });

    test("non-international method to non-US has no surcharge", () => {
      expect(
        processor.calculateShipping(orderWithCount(1, "MX"), ShippingMethod.STANDARD),
      ).toBeCloseTo(5.99);
    });
  });

  describe("applyDiscount", () => {
    test.each([null, undefined, ""])("no discount for %p", (code) => {
      expect(processor.applyDiscount(100, code)).toEqual({
        discountAmount: 0.0,
        error: null,
      });
    });

    test.each([
      ["SAVE10", 100, 10],
      ["SAVE20", 100, 20],
      ["SAVE30", 100, 30],
      ["save10", 100, 10],
      ["  SAVE10  ", 100, 10],
      ["SaVe20", 200, 40],
    ])("applies %p to %d -> %d", (code, subtotal, expected) => {
      const result = processor.applyDiscount(subtotal, code);
      expect(result.discountAmount).toBeCloseTo(expected);
      expect(result.error).toBeNull();
    });

    test.each(["FREESHIP", "freeship", " FreeShip "])(
      "%p gives no monetary discount",
      (code) => {
        expect(processor.applyDiscount(100, code)).toEqual({
          discountAmount: 0.0,
          error: null,
        });
      },
    );

    test.each(["INVALID", "SAVE50", "SAVE 10"])("rejects %p", (code) => {
      const result = processor.applyDiscount(100, code);
      expect(result.discountAmount).toBe(0.0);
      expect(result.error).toBe(`Invalid discount code: ${code}`);
    });

    test("discount on zero subtotal is zero", () => {
      expect(processor.applyDiscount(0, "SAVE30").discountAmount).toBe(0);
    });

    test("discount never exceeds subtotal for any configured code", () => {
      Object.keys(processor.discountCodes).forEach((code) => {
        const { discountAmount } = processor.applyDiscount(80, code);
        expect(discountAmount).toBeLessThanOrEqual(80);
        expect(discountAmount).toBeGreaterThanOrEqual(0);
      });
    });

    test("caps discount at subtotal if a code exceeds 100%", () => {
      processor.discountCodes.HUGE = 1.5;
      expect(processor.applyDiscount(100, "HUGE").discountAmount).toBe(100);
    });
  });

  describe("calculateTotal", () => {
    test("uses STANDARD shipping and no discount by default", () => {
      const r = processor.calculateTotal(sampleOrder); // subtotal 20
      expect(r.subtotal).toBe(20);
      expect(r.discount).toBe(0);
      expect(r.discountCode).toBeNull();
      expect(r.discountError).toBeNull();
      expect(r.discountedSubtotal).toBe(20);
      expect(r.tax).toBeCloseTo(1.6);
      expect(r.taxRate).toBe(0.08);
      expect(r.shippingMethod).toBe(ShippingMethod.STANDARD);
      expect(r.shipping).toBeCloseTo(5.99);
      expect(r.total).toBeCloseTo(20 + 1.6 + 5.99);
    });

    test("applies percentage discount before tax", () => {
      const r = processor.calculateTotal(sampleOrder, ShippingMethod.STANDARD, "SAVE10");
      expect(r.discount).toBeCloseTo(2);
      expect(r.discountedSubtotal).toBeCloseTo(18);
      expect(r.tax).toBeCloseTo(18 * 0.08);
      expect(r.total).toBeCloseTo(18 + 18 * 0.08 + 5.99);
    });

    test.each(["FREESHIP", "freeship", " FreeShip "])(
      "%p makes shipping free without changing subtotal",
      (code) => {
        const r = processor.calculateTotal(sampleOrder, ShippingMethod.OVERNIGHT, code);
        expect(r.shipping).toBe(0);
        expect(r.discount).toBe(0);
        expect(r.total).toBeCloseTo(20 * 1.08);
      },
    );

    test("invalid code reports error but still calculates total", () => {
      const r = processor.calculateTotal(sampleOrder, ShippingMethod.STANDARD, "BOGUS");
      expect(r.discountError).toBe("Invalid discount code: BOGUS");
      expect(r.discount).toBe(0);
      expect(r.total).toBeCloseTo(20 * 1.08 + 5.99);
    });

    test("free shipping threshold applies in totals", () => {
      const order = makeOrder([widget(100, 1)]);
      const r = processor.calculateTotal(order, ShippingMethod.EXPRESS);
      expect(r.shipping).toBe(0);
      expect(r.total).toBeCloseTo(108);
    });

    test("discount can drop the subtotal below the free shipping line without affecting shipping", () => {
      // shipping is decided on the pre-discount subtotal
      const order = makeOrder([widget(55, 1)]);
      const r = processor.calculateTotal(order, ShippingMethod.STANDARD, "SAVE30");
      expect(r.shipping).toBe(0);
      expect(r.discountedSubtotal).toBeCloseTo(38.5);
    });

    test("uses custom tax rate", () => {
      const p = new OrderProcessor(0.2);
      const r = p.calculateTotal(sampleOrder, ShippingMethod.STANDARD);
      expect(r.tax).toBeCloseTo(4);
      expect(r.taxRate).toBe(0.2);
    });

    test("empty order totals only shipping", () => {
      const r = processor.calculateTotal(makeOrder([]));
      expect(r.subtotal).toBe(0);
      expect(r.tax).toBe(0);
      expect(r.total).toBeCloseTo(5.99);
    });
  });

  describe("processOrder", () => {
    afterEach(() => jest.useRealTimers());

    test("confirms a valid order and updates it", () => {
      jest.useFakeTimers().setSystemTime(new Date("2026-03-01T10:00:00Z"));
      const result = processor.processOrder(sampleOrder, ShippingMethod.EXPRESS, "SAVE10");

      expect(result.orderId).toBe("ORD-001");
      expect(result.status).toBe(OrderStatus.CONFIRMED);
      expect(result.confirmedAt).toBe("2026-03-01T10:00:00.000Z");
      expect(result.totalBreakdown.shippingMethod).toBe(ShippingMethod.EXPRESS);
      expect(result.totalBreakdown.discount).toBeCloseTo(2);

      expect(sampleOrder.status).toBe(OrderStatus.CONFIRMED);
      expect(sampleOrder.shippingMethod).toBe(ShippingMethod.EXPRESS);
      expect(sampleOrder.discountCode).toBe("SAVE10");
    });

    test("uses defaults for shipping method and discount code", () => {
      const result = processor.processOrder(sampleOrder);
      expect(sampleOrder.shippingMethod).toBe(ShippingMethod.STANDARD);
      expect(sampleOrder.discountCode).toBeNull();
      expect(result.totalBreakdown.discountCode).toBeNull();
    });

    test("throws on invalid order and leaves it untouched", () => {
      const bad = makeOrder([]);
      expect(() => processor.processOrder(bad)).toThrow(
        "Order validation failed: Order must contain at least one item",
      );
      expect(bad.status).toBe(OrderStatus.PENDING);
      expect(bad.shippingMethod).toBeNull();
    });
  });

  describe("estimateDeliveryDate", () => {
    const created = new Date("2026-03-01T12:00:00Z");
    const daysUntil = (date) => Math.round((date - created) / 86400000);

    const orderIn = (country) => {
      const o = makeOrder([widget()], { ...validAddress(), country });
      o.createdAt = created;
      return o;
    };

    test.each([
      [ShippingMethod.STANDARD, "US", 7],
      [ShippingMethod.EXPRESS, "US", 3],
      [ShippingMethod.OVERNIGHT, "US", 1],
      [ShippingMethod.INTERNATIONAL, "US", 14],
      [ShippingMethod.INTERNATIONAL, "MX", 21],
      [ShippingMethod.EXPRESS, "MX", 3],
      ["unknown-method", "US", 7],
      [undefined, "US", 7],
    ])("%s to %s takes %d days", (method, country, expectedDays) => {
      const result = processor.estimateDeliveryDate(orderIn(country), method);
      expect(result).toBeInstanceOf(Date);
      expect(daysUntil(result)).toBe(expectedDays);
    });

    test("does not mutate the order's createdAt", () => {
      const order = orderIn("US");
      processor.estimateDeliveryDate(order, ShippingMethod.STANDARD);
      expect(order.createdAt.getTime()).toBe(created.getTime());
    });

    test("rolls over month boundaries", () => {
      const order = orderIn("US");
      order.createdAt = new Date("2026-01-30T12:00:00Z");
      const result = processor.estimateDeliveryDate(order, ShippingMethod.EXPRESS);
      expect(result.getUTCMonth()).toBe(1); // February
    });
  });
});
