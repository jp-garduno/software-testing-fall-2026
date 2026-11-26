const { Item, ShoppingCart } = require("./shoppingCart");

describe("Item", () => {
  test("should create item with valid parameters", () => {
    const item = new Item("Apple", 1.5, 3);
    expect(item.name).toBe("Apple");
    expect(item.price).toBe(1.5);
    expect(item.quantity).toBe(3);
  });

  test("should use default quantity of 1", () => {
    const item = new Item("Banana", 2.0);
    expect(item.quantity).toBe(1);
  });

  test("should throw error for negative price", () => {
    expect(() => {
      new Item("Apple", -1.5);
    }).toThrow("Price must be positive");
  });

  test("should throw error for zero price", () => {
    expect(() => {
      new Item("Apple", 0);
    }).toThrow("Price must be positive");
  });

  test("should throw error for negative quantity", () => {
    expect(() => {
      new Item("Apple", 1.5, -2);
    }).toThrow("Quantity must be positive");
  });

  test("should throw error for zero quantity", () => {
    expect(() => {
      new Item("Apple", 1.5, 0);
    }).toThrow("Quantity must be positive");
  });

  test("should calculate total for single quantity", () => {
    const item = new Item("Apple", 1.5);
    expect(item.getTotal()).toBe(1.5);
  });

  test("should calculate total for multiple quantity", () => {
    const item = new Item("Apple", 1.5, 4);
    expect(item.getTotal()).toBe(6.0);
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
      cart.addItem(new Item("Apple", 1.5));
      expect(cart.items.length).toBe(1);
      expect(cart.getItemCount()).toBe(1);
    });

    test("should add multiple different items to cart", () => {
      cart.addItem(new Item("Apple", 1.5));
      cart.addItem(new Item("Banana", 2.0));
      expect(cart.items.length).toBe(2);
      expect(cart.getItemCount()).toBe(2);
    });

    test("should increase quantity when adding duplicate item", () => {
      cart.addItem(new Item("Apple", 1.5, 2));
      cart.addItem(new Item("Apple", 1.5, 3));
      
      expect(cart.items.length).toBe(1); // Only one entry in the array
      expect(cart.items[0].quantity).toBe(5); // Combined quantity
      expect(cart.getItemCount()).toBe(5);
    });
  });

  // Test removeItem
  describe("removeItem", () => {
    test("should remove an existing item", () => {
      cart.addItem(new Item("Apple", 1.5));
      cart.addItem(new Item("Banana", 2.0));
      
      const result = cart.removeItem("Apple");
      expect(result).toBe(true);
      expect(cart.items.length).toBe(1);
      expect(cart.items[0].name).toBe("Banana");
    });

    test("should return false when removing nonexistent item", () => {
      cart.addItem(new Item("Apple", 1.5));
      
      const result = cart.removeItem("Orange");
      expect(result).toBe(false);
      expect(cart.items.length).toBe(1);
    });

    test("should return false when removing from empty cart", () => {
      const result = cart.removeItem("Apple");
      expect(result).toBe(false);
    });
  });

  // Test getSubtotal
  describe("getSubtotal", () => {
    test("should calculate subtotal for single item", () => {
      cart.addItem(new Item("Apple", 1.5, 2));
      expect(cart.getSubtotal()).toBe(3.0);
    });

    test("should calculate subtotal for multiple items", () => {
      cart.addItem(new Item("Apple", 1.5, 2)); // 3.0
      cart.addItem(new Item("Banana", 2.0, 3)); // 6.0
      expect(cart.getSubtotal()).toBe(9.0);
    });

    test("should return zero for empty cart", () => {
      expect(cart.getSubtotal()).toBe(0);
    });
  });

  // Test applyDiscount
  describe("applyDiscount", () => {
    test("should apply valid discount percentage", () => {
      cart.applyDiscount(15);
      expect(cart.discountPercent).toBe(15);
    });

    test("should apply zero discount", () => {
      cart.applyDiscount(0);
      expect(cart.discountPercent).toBe(0);
    });

    test("should apply full discount", () => {
      cart.applyDiscount(100);
      expect(cart.discountPercent).toBe(100);
    });

    test("should throw error for negative discount", () => {
      expect(() => {
        cart.applyDiscount(-10);
      }).toThrow("Discount must be between 0 and 100");
    });

    test("should throw error for discount over 100", () => {
      expect(() => {
        cart.applyDiscount(110);
      }).toThrow("Discount must be between 0 and 100");
    });
  });

  // Test getTotal with discount
  describe("getTotal", () => {
    test("should calculate total with discount applied", () => {
      cart.addItem(new Item("Shoes", 50.0, 2)); // Subtotal: 100
      cart.applyDiscount(20); // 20% off
      
      expect(cart.getTotal()).toBe(80.0);
    });

    test("should equal subtotal when no discount", () => {
      cart.addItem(new Item("Shoes", 50.0, 2));
      expect(cart.getTotal()).toBe(100.0);
      expect(cart.getTotal()).toBe(cart.getSubtotal());
    });
  });

  // Test clear
  describe("clear", () => {
    test("should clear all items and reset discount", () => {
      cart.addItem(new Item("Apple", 1.5));
      cart.applyDiscount(10);
      
      cart.clear();
      
      expect(cart.isEmpty()).toBe(true);
      expect(cart.discountPercent).toBe(0);
      expect(cart.items.length).toBe(0);
    });

    test("should not error when clearing empty cart", () => {
      expect(() => {
        cart.clear();
      }).not.toThrow();
      expect(cart.isEmpty()).toBe(true);
    });
  });

  // Test getItemCount
  describe("getItemCount", () => {
    test("should sum all quantities", () => {
      cart.addItem(new Item("Apple", 1.5, 2));
      cart.addItem(new Item("Banana", 2.0, 3));
      
      expect(cart.getItemCount()).toBe(5);
    });
  });

  // Test isEmpty
  describe("isEmpty", () => {
    test("should return true after adding and removing all items", () => {
      cart.addItem(new Item("Apple", 1.5));
      expect(cart.isEmpty()).toBe(false);
      
      cart.removeItem("Apple");
      expect(cart.isEmpty()).toBe(true);
    });
  });
});