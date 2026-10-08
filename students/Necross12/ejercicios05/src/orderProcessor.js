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
