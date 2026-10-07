const {
  Order,
  OrderProcessor,
  OrderStatus,
  ShippingMethod,
} = require("../orderProccessor");

describe("OrderProcessor & Order Comprehensive Tests", () => {
  let processor;
  let sampleOrder;

  beforeEach(() => {
    processor = new OrderProcessor();
    sampleOrder = new Order(
      "ORD-001",
      "CUST-001",
      [{ name: "Widget", price: 10.0, quantity: 2 }],
      {
        street: "123 Main St",
        city: "Springfield",
        state: "IL",
        zip_code: "62701",
        country: "US",
      },
    );
  });

  describe("Order class", () => {
    test("should ignore items missing price or quantity when calculating subtotal", () => {
      const order = new Order(
        "ORD-SUB",
        "CUST-1",
        [
          { name: "Valid", price: 10, quantity: 2 },
          { name: "No Price", quantity: 5 },
          { name: "No Quantity", price: 15 },
        ],
        sampleOrder.shippingAddress,
      );

      expect(order.getSubtotal()).toBe(20);
    });
  });

  describe("validateOrder", () => {
    test("should fail if order has no items or empty array", () => {
      let result = processor.validateOrder({ items: null });
      expect(result.isValid).toBe(false);
      expect(result.error).toContain("at least one item");

      result = processor.validateOrder({ items: [] });
      expect(result.isValid).toBe(false);
    });

    test.each([
      ["missing name", [{ price: 10, quantity: 1 }], "missing name"],
      ["empty name", [{ name: "", price: 10, quantity: 1 }], "missing name"],
      ["missing price", [{ name: "Item" }], "missing price"],
      [
        "price <= 0",
        [{ name: "Item", price: 0, quantity: 1 }],
        "invalid price",
      ],
      ["missing quantity", [{ name: "Item", price: 10 }], "missing quantity"],
      [
        "quantity <= 0",
        [{ name: "Item", price: 10, quantity: 0 }],
        "invalid quantity",
      ],
      [
        "quantity > 100",
        [{ name: "Item", price: 10, quantity: 101 }],
        "exceeds maximum",
      ],
    ])("should fail item validation: %s", (_, items, expectedError) => {
      const order = {
        items,
        shippingAddress: sampleOrder.shippingAddress,
      };
      const result = processor.validateOrder(order);
      expect(result.isValid).toBe(false);
      expect(result.error).toContain(expectedError);
    });

    test("should fail if shipping address is missing", () => {
      const order = {
        items: [{ name: "Widget", price: 10, quantity: 1 }],
      };
      const result = processor.validateOrder(order);
      expect(result.isValid).toBe(false);
      expect(result.error).toBe("Shipping address is required");
    });

    test.each(["street", "city", "state", "zip_code", "country"])(
      "should fail when address field %s is missing or empty",
      (field) => {
        const address = { ...sampleOrder.shippingAddress, [field]: "" };
        const order = {
          items: sampleOrder.items,
          shippingAddress: address,
        };
        const result = processor.validateOrder(order);
        expect(result.isValid).toBe(false);
        expect(result.error).toContain(`Shipping address missing ${field}`);
      },
    );

    test.each([
      ["1234", "Invalid US ZIP code format"],
      ["123456", "Invalid US ZIP code format"],
      ["12345-678", "Invalid US ZIP code format"], // 9 caracteres -> cae en la validación de longitud
      ["1234a", "ZIP code must be 5 digits"], // 5 caracteres -> pasa primer check, falla regex
      ["abcde-1234", "ZIP+4 must be in format 12345-6789"], // 10 caracteres -> pasa primer check, falla regex
    ])(
      "should validate US ZIP code formatting for %s",
      (zip, expectedError) => {
        const address = {
          ...sampleOrder.shippingAddress,
          zip_code: zip,
          country: "US",
        };
        const order = {
          items: sampleOrder.items,
          shippingAddress: address,
        };
        const result = processor.validateOrder(order);
        expect(result.isValid).toBe(false);
        expect(result.error).toBe(expectedError);
      },
    );

    test("should accept valid 5-digit and ZIP+4 US zip codes", () => {
      const order5 = new Order("1", "1", sampleOrder.items, {
        ...sampleOrder.shippingAddress,
        zip_code: "90210",
      });
      const order9 = new Order("2", "1", sampleOrder.items, {
        ...sampleOrder.shippingAddress,
        zip_code: "90210-1234",
      });

      expect(processor.validateOrder(order5).isValid).toBe(true);
      expect(processor.validateOrder(order9).isValid).toBe(true);
    });

    test("should bypass US ZIP validation for non-US addresses", () => {
      const intlAddress = {
        street: "1 Main",
        city: "MX",
        state: "JAL",
        zip_code: "ABC-12",
        country: "MX",
      };
      const order = new Order("3", "1", sampleOrder.items, intlAddress);
      expect(processor.validateOrder(order).isValid).toBe(true);
    });

    test("should execute branch for zip code length 10 validation", () => {
      const address = {
        ...sampleOrder.shippingAddress,
        zip_code: "1234567890",
        country: "US",
      };
      const result = processor.validateOrder({
        items: sampleOrder.items,
        shippingAddress: address,
      });
      expect(result.isValid).toBe(false);
      expect(result.error).toBe("ZIP+4 must be in format 12345-6789");
    });
  });

  describe("calculateShipping", () => {
    test("should return 0.0 if subtotal >= freeShippingThreshold", () => {
      const expensiveOrder = new Order(
        "1",
        "1",
        [{ name: "TV", price: 100, quantity: 1 }],
        sampleOrder.shippingAddress,
      );
      expect(
        processor.calculateShipping(expensiveOrder, ShippingMethod.STANDARD),
      ).toBe(0.0);
    });

    test.each([
      [ShippingMethod.STANDARD, 5.99],
      [ShippingMethod.EXPRESS, 12.99],
      [ShippingMethod.OVERNIGHT, 24.99],
      [ShippingMethod.INTERNATIONAL, 35.99],
      ["UNKNOWN_METHOD", 5.99],
    ])("should return correct base rate for %s", (method, expectedRate) => {
      const cheapOrder = new Order(
        "1",
        "1",
        [{ name: "Pen", price: 5, quantity: 1 }],
        sampleOrder.shippingAddress,
      );
      expect(processor.calculateShipping(cheapOrder, method)).toBe(
        expectedRate,
      );
    });

    test("should add weight surcharges based on item count", () => {
      const order6Items = new Order(
        "1",
        "1",
        [{ name: "Pen", price: 1, quantity: 6 }],
        sampleOrder.shippingAddress,
      );
      const order11Items = new Order(
        "2",
        "1",
        [{ name: "Pen", price: 1, quantity: 11 }],
        sampleOrder.shippingAddress,
      );

      expect(
        processor.calculateShipping(order6Items, ShippingMethod.STANDARD),
      ).toBeCloseTo(7.99);
      expect(
        processor.calculateShipping(order11Items, ShippingMethod.STANDARD),
      ).toBeCloseTo(10.99);
    });

    test("should add international surcharge for non-US destinations with INTERNATIONAL method", () => {
      const intlAddress = {
        ...sampleOrder.shippingAddress,
        country: "CA",
      };
      const intlOrder = new Order(
        "1",
        "1",
        [{ name: "Item", price: 10, quantity: 1 }],
        intlAddress,
      );

      expect(
        processor.calculateShipping(intlOrder, ShippingMethod.INTERNATIONAL),
      ).toBeCloseTo(50.99);
    });
  });

  describe("applyDiscount", () => {
    test("should return 0 discount if code is missing/null/undefined", () => {
      expect(processor.applyDiscount(100, null)).toEqual({
        discountAmount: 0.0,
        error: null,
      });
      expect(processor.applyDiscount(100, "")).toEqual({
        discountAmount: 0.0,
        error: null,
      });
    });

    test("should handle case insensitivity and whitespace", () => {
      const result = processor.applyDiscount(100, "  save10  ");
      expect(result.discountAmount).toBe(10.0);
      expect(result.error).toBeNull();
    });

    test("should return error for unrecognized discount code", () => {
      const result = processor.applyDiscount(100, "INVALID_CODE");
      expect(result.discountAmount).toBe(0.0);
      expect(result.error).toContain("Invalid discount code: INVALID_CODE");
    });

    test("should handle FREESHIP code specially", () => {
      const result = processor.applyDiscount(100, "FREESHIP");
      expect(result).toEqual({ discountAmount: 0.0, error: null });
    });

    test("should cap discount at subtotal if discount calculation exceeds subtotal", () => {
      processor.discountCodes["SUPER100"] = 1.5;
      const result = processor.applyDiscount(100, "SUPER100");
      expect(result.discountAmount).toBe(100);
    });
  });

  describe("calculateTotal", () => {
    test("should apply FREESHIP code correctly resulting in $0 shipping", () => {
      const cheapOrder = new Order(
        "1",
        "1",
        [{ name: "Item", price: 10, quantity: 1 }],
        sampleOrder.shippingAddress,
      );
      const result = processor.calculateTotal(
        cheapOrder,
        ShippingMethod.STANDARD,
        "FREESHIP",
      );

      expect(result.shipping).toBe(0.0);
      expect(result.discount).toBe(0.0);
      expect(result.total).toBeCloseTo(10 + 10 * 0.08);
    });

    test("should calculate complete breakdown with regular discount code", () => {
      const result = processor.calculateTotal(
        sampleOrder,
        ShippingMethod.EXPRESS,
        "SAVE10",
      );

      expect(result.subtotal).toBe(20.0);
      expect(result.discount).toBe(2.0);
      expect(result.discountedSubtotal).toBe(18.0);
      expect(result.tax).toBeCloseTo(1.44);
      expect(result.shipping).toBe(12.99);
      expect(result.total).toBeCloseTo(32.43);
    });

    test("should handle FREESHIP code with spaces and lowercase in calculateTotal", () => {
      const result = processor.calculateTotal(
        sampleOrder,
        ShippingMethod.STANDARD,
        " freeship ",
      );
      expect(result.shipping).toBe(0.0);
    });
  });

  describe("processOrder", () => {
    test("should throw Error if order validation fails", () => {
      const invalidOrder = new Order("1", "1", [], sampleOrder.shippingAddress);
      expect(() => processor.processOrder(invalidOrder)).toThrow(
        "Order validation failed:",
      );
    });

    test("should successfully process order and update its status and properties", () => {
      const result = processor.processOrder(
        sampleOrder,
        ShippingMethod.EXPRESS,
        "SAVE20",
      );

      expect(sampleOrder.status).toBe(OrderStatus.CONFIRMED);
      expect(sampleOrder.shippingMethod).toBe(ShippingMethod.EXPRESS);
      expect(sampleOrder.discountCode).toBe("SAVE20");
      expect(result.orderId).toBe("ORD-001");
      expect(result.status).toBe(OrderStatus.CONFIRMED);
      expect(result.confirmedAt).toBeDefined();
    });
  });

  describe("estimateDeliveryDate", () => {
    test.each([
      [ShippingMethod.STANDARD, 7],
      [ShippingMethod.EXPRESS, 3],
      [ShippingMethod.OVERNIGHT, 1],
      [ShippingMethod.INTERNATIONAL, 14],
      ["UNKNOWN", 7],
    ])(
      "should calculate delivery days correctly for %s",
      (method, expectedDays) => {
        const deliveryDate = processor.estimateDeliveryDate(
          sampleOrder,
          method,
        );
        const diffTime = Math.abs(deliveryDate - sampleOrder.createdAt);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        expect(diffDays).toBe(expectedDays);
      },
    );

    test("should add extra 7 days for international delivery outside US", () => {
      const intlAddress = {
        ...sampleOrder.shippingAddress,
        country: "MX",
      };
      const intlOrder = new Order("1", "1", sampleOrder.items, intlAddress);

      const deliveryDate = processor.estimateDeliveryDate(
        intlOrder,
        ShippingMethod.INTERNATIONAL,
      );
      const diffTime = Math.abs(deliveryDate - intlOrder.createdAt);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      expect(diffDays).toBe(21);
    });
  });
});
