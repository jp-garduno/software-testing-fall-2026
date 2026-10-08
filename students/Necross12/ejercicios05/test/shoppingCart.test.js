const { Item, ShoppingCart } = require("../src/shoppingCart");

describe("Item", () => {
  test("should create item with valid parameters", () => {
    const item = new Item("Apple", 1.5, 3);
    expect(item.name).toBe("Apple");
    expect(item.price).toBe(1.5);
    expect(item.quantity).toBe(3);
  });

  test("should use default quantity of 1", () => {
    // TODO: Implement this test
    const item = new Item("Apple", 1.5);
    expect(item.quantity).toBe(1);
  });

  test("should throw error for negative price", () => {
    // TODO: Implement this test
    expect(() => new Item("Apple", -1.5, 3)).toThrow("Price must be positive");
  });

  test("should throw error for zero price", () => {
    // TODO: Implement this test
    expect(() => new Item("Apple", 0, 3)).toThrow("Price must be positive");
  });

  test("should throw error for negative quantity", () => {
    // TODO: Implement this test
    expect(() => new Item("Apple", 1.5, -3)).toThrow("Quantity must be positive");
  });

  test("should throw error for zero quantity", () => {
    // TODO: Implement this test
    expect(() => new Item("Apple", 1.5, 0)).toThrow("Quantity must be positive");
  });

  test("should calculate total for single quantity", () => {
    // TODO: Implement this test
    const item = new Item("Apple", 1.5, 1);
    expect(item.getTotal()).toBe(1.5);
  });

  test("should calculate total for multiple quantity", () => {
    // TODO: Implement this test
    const item = new Item("Apple", 1.5, 3);
    expect(item.getTotal()).toBe(4.5);
  });
});

describe("ShoppingCart", () => {
  let cart;

  beforeEach(() => {
    // Create a fresh cart before each test
    cart = new ShoppingCart();
  });

  // Test initialization
  describe("initialization", () => {
    test("should start empty", () => {
      expect(cart.isEmpty()).toBe(true);
      expect(cart.getItemCount()).toBe(0);
      expect(cart.getTotal()).toBe(0);
    });
  });

  // Test addItem
  describe("addItem", () => {
    test("should add a single item to cart", () => {
      // TODO: Implement this test
        const item = new Item("Apple", 1.5, 2);
        cart.addItem(item);
        expect(cart.items.length).toBe(1);
        expect(cart.items[0].name).toBe("Apple");
        expect(cart.items[0].quantity).toBe(2);
    });

    test("should add multiple different items to cart", () => {
      // TODO: Implement this test
        const item1 = new Item("Apple", 1.5, 2);
        const item2 = new Item("Banana", 0.5, 3);
        cart.addItem(item1);
        cart.addItem(item2);
        expect(cart.items.length).toBe(2);
        expect(cart.items[0].name).toBe("Apple");
        expect(cart.items[1].name).toBe("Banana");
        expect(cart.items[0].quantity).toBe(2);
        expect(cart.items[1].quantity).toBe(3);
    });

    test("should increase quantity when adding duplicate item", () => {
      // TODO: Implement this test
      // Hint: Add same item twice and verify there's only one entry with combined quantity
        const item1 = new Item("Apple", 1.5, 2);
        const item2 = new Item("Apple", 1.5, 3);
        cart.addItem(item1);
        cart.addItem(item2);
        expect(cart.items.length).toBe(1);
        expect(cart.items[0].name).toBe("Apple");
        expect(cart.items[0].quantity).toBe(5); // 2 + 3
    });
  });

  // Test removeItem
  describe("removeItem", () => {
    test("should remove an existing item", () => {
      // TODO: Implement this test
        const item = new Item("Apple", 1.5, 2);
        cart.addItem(item);
        const removed = cart.removeItem("Apple");
        expect(removed).toBe(true);
        expect(cart.items.length).toBe(0);
        expect(cart.isEmpty()).toBe(true);
    });

    test("should return false when removing nonexistent item", () => {
      // TODO: Implement this test
        const removed = cart.removeItem("NonExistent");
        expect(removed).toBe(false);
    });

    test("should return false when removing from empty cart", () => {
      // TODO: Implement this test
        const removed = cart.removeItem("Apple");
        expect(removed).toBe(false);
    });
  });

  // Test getSubtotal
  describe("getSubtotal", () => {
    test("should calculate subtotal for single item", () => {
      // TODO: Implement this test
      const item = new Item("Apple", 1.5, 2);
      cart.addItem(item);
      const subtotal = cart.getSubtotal();
      expect(subtotal).toBe(3); // 1.5 * 2
    });

    test("should calculate subtotal for multiple items", () => {
      // TODO: Implement this test
        const item1 = new Item("Apple", 1.5, 2); // 3
        const item2 = new Item("Banana", 0.5, 4); // 2
        cart.addItem(item1);
        cart.addItem(item2);
        const subtotal = cart.getSubtotal();
        expect(subtotal).toBe(5); // 3 + 2
    });

    test("should return zero for empty cart", () => {
      // TODO: Implement this test
      const subtotal = cart.getSubtotal();
      expect(subtotal).toBe(0);
    });
  });

  // Test applyDiscount
  describe("applyDiscount", () => {
    test("should apply valid discount percentage", () => {
      // TODO: Implement this test
      const item = new Item("Apple", 1.5, 2);
      cart.addItem(item);
      cart.applyDiscount(20); // 20% de descuento
      const total = cart.getTotal();
      expect(total).toBe(2.4); // 3 * 0.8
    });

    test("should apply zero discount", () => {
      // TODO: Implement this test
        const item = new Item("Apple", 1.5, 2);
        cart.addItem(item);
        cart.applyDiscount(0);
        const total = cart.getTotal();
        expect(total).toBe(3);
    });

    test("should apply full discount", () => {
      // TODO: Implement this test
        const item = new Item("Apple", 1.5, 2);
        cart.addItem(item);
        cart.applyDiscount(100);
        const total = cart.getTotal();
        expect(total).toBe(0);
    });

    test("should throw error for negative discount", () => {
      // TODO: Implement this test
        expect(() => {
            cart.applyDiscount(-10);
        }).toThrow("Discount must be between 0 and 100");
    });

    test("should throw error for discount over 100", () => {
      // TODO: Implement this test
        expect(() => {
            cart.applyDiscount(120);
        }).toThrow("Discount must be between 0 and 100");
    });
  });

  // Test getTotal with discount
  describe("getTotal", () => {
    test("should calculate total with discount applied", () => {
      // TODO: Implement this test
      // Example: Add items totaling $100, apply 20% discount, verify total is $80
        const item1 = new Item("Item1", 50, 1); // 50
        const item2 = new Item("Item2", 50, 1); // 50
        cart.addItem(item1);
        cart.addItem(item2);
        cart.applyDiscount(20);
        const total = cart.getTotal();
        expect(total).toBe(80); // 100 * 0.8
    });

    test("should equal subtotal when no discount", () => {
      // TODO: Implement this test
        const item1 = new Item("Item1", 50, 1); // 50
        const item2 = new Item("Item2", 50, 1); // 50
        cart.addItem(item1);
        cart.addItem(item2);
        const total = cart.getTotal();
        const subtotal = cart.getSubtotal();
        expect(total).toBe(subtotal);
    });
  });

  // Test clear
  describe("clear", () => {
    test("should clear all items and reset discount", () => {
      // TODO: Implement this test
        const item1 = new Item("Item1", 50, 1);
        const item2 = new Item("Item2", 50, 1);
        cart.addItem(item1);
        cart.addItem(item2);
        cart.applyDiscount(20);
        cart.clear();
        expect(cart.items.length).toBe(0);
        expect(cart.discountPercent).toBe(0);
    });

    test("should not error when clearing empty cart", () => {
      // TODO: Implement this test
        cart.clear();
        expect(cart.items.length).toBe(0);
        expect(cart.discountPercent).toBe(0);
    });
  });

  // Test getItemCount
  describe("getItemCount", () => {
    test("should sum all quantities", () => {
      // TODO: Implement this test
      // Example: Add item with qty 2 and item with qty 3, verify count is 5
        const item1 = new Item("Item1", 50, 2);
        const item2 = new Item("Item2", 50, 3);
        cart.addItem(item1);
        cart.addItem(item2);
        const count = cart.getItemCount();
        expect(count).toBe(5); // 2 + 3
    });
  });

  // Test isEmpty
  describe("isEmpty", () => {
    test("should return true after adding and removing all items", () => {
      // TODO: Implement this test
        const item1 = new Item("Item1", 50, 1);
        const item2 = new Item("Item2", 50, 1);
        cart.addItem(item1);
        cart.addItem(item2);
        cart.removeItem(item1.name);
        cart.removeItem(item2.name);
        expect(cart.isEmpty()).toBe(true);
    });
  });
});
