# Exercise 4: Coverage Challenge

**Duration**: 90 minutes  
**Difficulty**: Advanced  
**Topics**: High coverage, complex code paths, edge cases, comprehensive testing

## Objectives

By completing this exercise, you will:

- Analyze existing code to identify untested paths
- Write tests to achieve >95% coverage
- Handle complex branching logic and nested conditions
- Test loops, error handling, and edge cases
- Understand the limitations of coverage metrics
- Balance coverage goals with test quality

## Background

You've been given a partially tested codebase with low coverage (~40%). Your mission is to analyze the code, identify untested paths, and write comprehensive tests to achieve >95% statement and branch coverage. This exercise simulates real-world scenarios where you inherit legacy code that needs testing.

## Part 1: Analyze the Code (15 minutes)

You are provided with `orderProcessor.js` - a complex order processing system with validation, calculations, and business rules.

### `orderProcessor.js`

```javascript
const OrderStatus = {
  PENDING: "pending",
  CONFIRMED: "confirmed",
  SHIPPED: "shipped",
  DELIVERED: "delivered",
  CANCELLED: "cancelled",
};

const ShippingMethod = {
  STANDARD: "standard",
  EXPRESS: "express",
  OVERNIGHT: "overnight",
  INTERNATIONAL: "international",
};

class Order {
  /**
   * Represents a customer order.
   */
  constructor(orderId, customerId, items, shippingAddress) {
    this.orderId = orderId;
    this.customerId = customerId;
    this.items = items;
    this.shippingAddress = shippingAddress;
    this.status = OrderStatus.PENDING;
    this.createdAt = new Date();
    this.shippingMethod = null;
    this.discountCode = null;
    this.trackingNumber = null;
  }

  getSubtotal() {
    let total = 0;
    for (const item of this.items) {
      if (item.price !== undefined && item.quantity !== undefined) {
        total += item.price * item.quantity;
      }
    }
    return total;
  }
}

class OrderProcessor {
  /**
   * Processes and validates orders.
   */
  constructor(taxRate = 0.08, freeShippingThreshold = 50.0) {
    this.taxRate = taxRate;
    this.freeShippingThreshold = freeShippingThreshold;
    this.discountCodes = {
      SAVE10: 0.1,
      SAVE20: 0.2,
      SAVE30: 0.3,
      FREESHIP: 0.0,
    };
  }

  /**
   * Validate an order before processing.
   * @returns {Object} { isValid: boolean, error: string|null }
   */
  validateOrder(order) {
    // Check if order has items
    if (!order.items || order.items.length === 0) {
      return { isValid: false, error: "Order must contain at least one item" };
    }

    // Validate each item
    for (let i = 0; i < order.items.length; i++) {
      const item = order.items[i];

      if (!item.name || item.name === "") {
        return { isValid: false, error: `Item ${i} is missing name` };
      }

      if (item.price === undefined) {
        return { isValid: false, error: `Item ${i} is missing price` };
      }

      if (item.price <= 0) {
        return { isValid: false, error: `Item ${i} has invalid price` };
      }

      if (item.quantity === undefined) {
        return { isValid: false, error: `Item ${i} is missing quantity` };
      }

      if (item.quantity <= 0) {
        return { isValid: false, error: `Item ${i} has invalid quantity` };
      }

      // Check for excessive quantity (potential fraud)
      if (item.quantity > 100) {
        return {
          isValid: false,
          error: `Item ${i} quantity exceeds maximum (100)`,
        };
      }
    }

    // Validate shipping address
    if (!order.shippingAddress) {
      return { isValid: false, error: "Shipping address is required" };
    }

    const requiredFields = ["street", "city", "state", "zip_code", "country"];
    for (const field of requiredFields) {
      if (
        !order.shippingAddress[field] ||
        order.shippingAddress[field] === ""
      ) {
        return { isValid: false, error: `Shipping address missing ${field}` };
      }
    }

    // Validate ZIP code format (US only for simplicity)
    const zipCode = order.shippingAddress.zip_code;
    if (order.shippingAddress.country === "US") {
      if (zipCode.length !== 5 && zipCode.length !== 10) {
        return { isValid: false, error: "Invalid US ZIP code format" };
      }

      // Check if it's all digits (for 5-digit) or has hyphen (for ZIP+4)
      if (zipCode.length === 5) {
        if (!/^\d{5}$/.test(zipCode)) {
          return { isValid: false, error: "ZIP code must be 5 digits" };
        }
      } else if (zipCode.length === 10) {
        if (!/^\d{5}-\d{4}$/.test(zipCode)) {
          return {
            isValid: false,
            error: "ZIP+4 must be in format 12345-6789",
          };
        }
      }
    }

    return { isValid: true, error: null };
  }

  /**
   * Calculate shipping cost based on method and order details.
   */
  calculateShipping(order, shippingMethod) {
    const subtotal = order.getSubtotal();

    // Free shipping for orders over threshold
    if (subtotal >= this.freeShippingThreshold) {
      return 0.0;
    }

    // Base shipping rates
    let baseRate;
    if (shippingMethod === ShippingMethod.STANDARD) {
      baseRate = 5.99;
    } else if (shippingMethod === ShippingMethod.EXPRESS) {
      baseRate = 12.99;
    } else if (shippingMethod === ShippingMethod.OVERNIGHT) {
      baseRate = 24.99;
    } else if (shippingMethod === ShippingMethod.INTERNATIONAL) {
      baseRate = 35.99;
    } else {
      baseRate = 5.99;
    }

    // Additional charges based on weight (estimated by item count)
    const itemCount = order.items.reduce((sum, item) => sum + item.quantity, 0);
    if (itemCount > 10) {
      baseRate += 5.0;
    } else if (itemCount > 5) {
      baseRate += 2.0;
    }

    // International shipping surcharge for non-US
    if (
      shippingMethod === ShippingMethod.INTERNATIONAL &&
      order.shippingAddress.country !== "US"
    ) {
      baseRate += 15.0;
    }

    return baseRate;
  }

  /**
   * Apply discount code to subtotal.
   * @returns {Object} { discountAmount: number, error: string|null }
   */
  applyDiscount(subtotal, discountCode) {
    if (!discountCode) {
      return { discountAmount: 0.0, error: null };
    }

    // Normalize code
    const code = discountCode.toUpperCase().trim();

    if (!(code in this.discountCodes)) {
      return {
        discountAmount: 0.0,
        error: `Invalid discount code: ${discountCode}`,
      };
    }

    const discountPercent = this.discountCodes[code];

    // Special handling for FREESHIP code
    if (code === "FREESHIP") {
      return { discountAmount: 0.0, error: null }; // Handled separately in shipping
    }

    // Calculate discount
    let discountAmount = subtotal * discountPercent;

    // Cap discount at subtotal (can't be negative)
    if (discountAmount > subtotal) {
      discountAmount = subtotal;
    }

    return { discountAmount, error: null };
  }

  /**
   * Calculate order total including tax, shipping, and discounts.
   */
  calculateTotal(
    order,
    shippingMethod = ShippingMethod.STANDARD,
    discountCode = null,
  ) {
    const subtotal = order.getSubtotal();

    // Apply discount
    const discountResult = this.applyDiscount(subtotal, discountCode);
    const discountAmount = discountResult.discountAmount;
    const discountedSubtotal = subtotal - discountAmount;

    // Calculate tax on discounted subtotal
    const tax = discountedSubtotal * this.taxRate;

    // Calculate shipping (free shipping for FREESHIP code)
    let shipping;
    if (discountCode && discountCode.toUpperCase().trim() === "FREESHIP") {
      shipping = 0.0;
    } else {
      shipping = this.calculateShipping(order, shippingMethod);
    }

    // Calculate total
    const total = discountedSubtotal + tax + shipping;

    return {
      subtotal,
      discount: discountAmount,
      discountCode,
      discountError: discountResult.error,
      discountedSubtotal,
      tax,
      taxRate: this.taxRate,
      shipping,
      shippingMethod,
      total,
    };
  }

  /**
   * Process an order: validate, calculate total, and update status.
   */
  processOrder(
    order,
    shippingMethod = ShippingMethod.STANDARD,
    discountCode = null,
  ) {
    // Validate order
    const validation = this.validateOrder(order);
    if (!validation.isValid) {
      throw new Error(`Order validation failed: ${validation.error}`);
    }

    // Calculate total
    const totalBreakdown = this.calculateTotal(
      order,
      shippingMethod,
      discountCode,
    );

    // Update order
    order.status = OrderStatus.CONFIRMED;
    order.shippingMethod = shippingMethod;
    order.discountCode = discountCode;

    return {
      orderId: order.orderId,
      status: order.status,
      totalBreakdown,
      confirmedAt: new Date().toISOString(),
    };
  }

  /**
   * Estimate delivery date based on shipping method.
   */
  estimateDeliveryDate(order, shippingMethod) {
    const businessDays = {
      [ShippingMethod.STANDARD]: 7,
      [ShippingMethod.EXPRESS]: 3,
      [ShippingMethod.OVERNIGHT]: 1,
      [ShippingMethod.INTERNATIONAL]: 14,
    };

    let days = businessDays[shippingMethod] || 7;

    // Add extra days for international
    if (
      shippingMethod === ShippingMethod.INTERNATIONAL &&
      order.shippingAddress.country !== "US"
    ) {
      days += 7;
    }

    // Calculate delivery date (simplified, doesn't account for weekends)
    const deliveryDate = new Date(order.createdAt);
    deliveryDate.setDate(deliveryDate.getDate() + days);

    return deliveryDate;
  }
}

module.exports = { Order, OrderProcessor, OrderStatus, ShippingMethod };
```

## Part 2: Run Initial Coverage Report (5 minutes)

You're provided with minimal existing tests in `orderProcessor.test.js`:

```javascript
const {
  Order,
  OrderProcessor,
  OrderStatus,
  ShippingMethod,
} = require("./orderProcessor");

describe("OrderProcessor", () => {
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

  test("should validate a valid order", () => {
    const result = processor.validateOrder(sampleOrder);
    expect(result.isValid).toBe(true);
    expect(result.error).toBeNull();
  });

  test("should calculate total without discount", () => {
    const result = processor.calculateTotal(sampleOrder);
    expect(result.subtotal).toBe(20.0);
    expect(result.discount).toBe(0.0);
    expect(result.tax).toBeGreaterThan(0);
  });
});
```

### Run Coverage

```bash
npm run test:coverage
```

You should see coverage around 40%. Your goal is to get it above 95%.

## Part 3: Achieve >95% Coverage (60 minutes)

Analyze the coverage report and write tests to cover untested code. Consider:

### Areas to Test

1. **Validation Edge Cases**

   - Empty order (no items)
   - Missing item fields (name, price, quantity)
   - Invalid prices (zero, negative)
   - Invalid quantities (zero, negative, >100)
   - Missing address fields
   - Invalid ZIP codes (wrong length, non-digit, invalid ZIP+4 format)
   - International addresses

2. **Shipping Calculations**

   - All shipping methods (STANDARD, EXPRESS, OVERNIGHT, INTERNATIONAL)
   - Free shipping threshold
   - Item count surcharges (>5 items, >10 items)
   - International surcharges
   - Different combinations

3. **Discount Logic**

   - All discount codes (SAVE10, SAVE20, SAVE30, FREESHIP)
   - Invalid discount codes
   - Null/empty discount codes
   - Case sensitivity and whitespace
   - FREESHIP special handling

4. **Total Calculations**

   - Various combinations of items, shipping, discounts
   - Edge case: discount larger than subtotal
   - Tax calculations

5. **Process Order**

   - Invalid orders (validation failures)
   - Valid orders with various configurations
   - Status updates

6. **Delivery Estimation**
   - All shipping methods
   - US vs international addresses
   - Date calculations

### Your Tasks

1. **Analyze coverage gaps** - Identify which lines and branches aren't covered
2. **Write comprehensive tests** - Cover all paths through the code
3. **Test edge cases** - Don't just test happy paths
4. **Verify behavior** - Make sure the code does what it should
5. **Achieve >95% coverage** - Both statement and branch coverage

### Example Tests to Get You Started

```javascript
describe("validateOrder", () => {
  test("should fail for order with no items", () => {
    const order = new Order(
      "ORD-002",
      "CUST-001",
      [],
      sampleOrder.shippingAddress,
    );
    const result = processor.validateOrder(order);
    expect(result.isValid).toBe(false);
    expect(result.error).toContain("at least one item");
  });

  test("should fail for item without name", () => {
    const order = new Order(
      "ORD-002",
      "CUST-001",
      [{ price: 10.0, quantity: 1 }],
      sampleOrder.shippingAddress,
    );
    const result = processor.validateOrder(order);
    expect(result.isValid).toBe(false);
    expect(result.error).toContain("missing name");
  });
});

describe("calculateShipping", () => {
  test("should have free shipping for orders over threshold", () => {
    const order = new Order(
      "ORD-003",
      "CUST-001",
      [{ name: "Expensive Widget", price: 60.0, quantity: 1 }],
      sampleOrder.shippingAddress,
    );

    const shipping = processor.calculateShipping(
      order,
      ShippingMethod.STANDARD,
    );
    expect(shipping).toBe(0.0);
  });
});

describe("applyDiscount", () => {
  test("should apply SAVE20 discount code", () => {
    const result = processor.applyDiscount(100.0, "SAVE20");
    expect(result.discountAmount).toBe(20.0);
    expect(result.error).toBeNull();
  });

  test("should return error for invalid code", () => {
    const result = processor.applyDiscount(100.0, "INVALID");
    expect(result.discountAmount).toBe(0.0);
    expect(result.error).toContain("Invalid discount code");
  });
});
```

## Part 4: Verify and Analyze (10 minutes)

### Check Your Coverage

```bash
npm run test:coverage
```

View the HTML report in `coverage/lcov-report/index.html` and verify:

- Statement coverage >95%
- Branch coverage >95%
- No critical paths left untested

### Reflect on Coverage

Consider these questions:

1. Did you achieve high coverage without sacrificing test quality?
2. Are there any branches that are hard or impossible to test?
3. Would you feel confident deploying this code?
4. What's the difference between high coverage and good testing?

## Evaluation Criteria

Your solution will be evaluated on:

- **Coverage Achievement**: >95% statement and branch coverage
- **Test Quality**: Tests are meaningful, not just coverage padding
- **Edge Case Coverage**: All edge cases identified and tested
- **Code Organization**: Tests are well-organized and readable
- **Test Independence**: Tests don't depend on each other
- **Assertion Quality**: Tests verify correct behavior, not just execution

## Common Mistakes to Avoid

1. **Writing tests just for coverage** - Tests should verify behavior
2. **Not testing error paths** - Validation and error handling need testing
3. **Ignoring branch coverage** - Statement coverage alone is insufficient
4. **Not testing edge cases** - Boundaries and special values are critical
5. **Copy-paste tests** - Use test.each or helper functions for similar tests
6. **Over-complicated tests** - Keep tests simple and focused

## Tips for Success

- Use coverage report to guide your testing, not dictate it
- Test one method at a time to see coverage increase
- Use `test.each` for testing multiple similar cases
- Group related tests in describe blocks
- Use descriptive test names
- Write tests for behavior, not implementation
- Don't obsess over 100% - focus on meaningful coverage

## Advanced: Using test.each

```javascript
describe("discount codes", () => {
  test.each([
    ["SAVE10", 100, 10.0],
    ["SAVE20", 100, 20.0],
    ["SAVE30", 100, 30.0],
    ["save10", 100, 10.0], // Test case insensitivity
    ["  SAVE10  ", 100, 10.0], // Test whitespace handling
  ])(
    "should apply %s discount to %d resulting in %d",
    (code, subtotal, expected) => {
      const result = processor.applyDiscount(subtotal, code);
      expect(result.discountAmount).toBe(expected);
      expect(result.error).toBeNull();
    },
  );
});
```

## Submission

Submit the following files:

- `orderProcessor.test.js` - Your comprehensive test suite
- Screenshot showing >95% statement and branch coverage
- Brief reflection (200 words): What did you learn about coverage metrics? Are there diminishing returns?

## Reflection Questions

1. How many tests did you write to achieve >95% coverage?
2. Were there any paths that were difficult to test? Why?
3. Is high coverage the same as good testing?
4. What percentage of coverage do you think is reasonable for production code?
5. Can you have high coverage but poor tests? How?

## Next Steps

After completing this exercise:

- Complete [Homework 5](../homework/homework-5.md)
- Review all Module 5 theory materials
- Prepare for [Module 6: Test Driven Development](../../06-test-driven-development/README.md)
- Consider: When is 95% coverage too much? When is it not enough?
