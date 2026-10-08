// Test suite for Exercise 2: Shopping Cart Class Testing (Module 05 - White Box Testing).
const { Item, ShoppingCart } = require("./shoppingCart");

describe("Item", () => {
  test("should create item with valid parameters", () => {
    const item = new Item("Apple", 1.5, 3);
    expect(item.name).toBe("Apple");
    expect(item.price).toBe(1.5);
    expect(item.quantity).toBe(3);
  });

  test("should use default quantity of 1", () => {
    const item = new Item("Apple", 1.5);
    expect(item.quantity).toBe(1);
  });

  test("should throw error for negative price", () => {
    expect(() => new Item("Apple", -1.5)).toThrow("Price must be positive");
  });

  test("should throw error for zero price", () => {
    expect(() => new Item("Apple", 0)).toThrow("Price must be positive");
  });

  test("should accept smallest positive price", () => {
    const item = new Item("Gum", 0.01);
    expect(item.price).toBe(0.01);
  });

  test("should throw error for negative quantity", () => {
    expect(() => new Item("Apple", 1.5, -1)).toThrow(
      "Quantity must be positive",
    );
  });

  test("should throw error for zero quantity", () => {
    expect(() => new Item("Apple", 1.5, 0)).toThrow(
      "Quantity must be positive",
    );
  });

  test("should validate price before quantity when both are invalid", () => {
    expect(() => new Item("Apple", 0, 0)).toThrow("Price must be positive");
  });

  test("should calculate total for single quantity", () => {
    const item = new Item("Apple", 1.5);
    expect(item.getTotal()).toBeCloseTo(1.5);
  });

  test("should calculate total for multiple quantity", () => {
    const item = new Item("Apple", 1.5, 4);
    expect(item.getTotal()).toBeCloseTo(6.0);
  });
});

describe("ShoppingCart", () => {
  let cart;

  beforeEach(() => {
    // Create a fresh cart before each test
    cart = new ShoppingCart();
  });

  describe("initialization", () => {
    test("should start empty", () => {
      expect(cart.isEmpty()).toBe(true);
      expect(cart.getItemCount()).toBe(0);
      expect(cart.getTotal()).toBe(0);
    });

    test("should start without discount", () => {
      expect(cart.discountPercent).toBe(0);
    });

    test("should not share items between carts", () => {
      // The only test that needs a second cart: it checks for shared mutable state
      const otherCart = new ShoppingCart();
      cart.addItem(new Item("Apple", 1.5));
      expect(otherCart.isEmpty()).toBe(true);
    });
  });

  describe("addItem", () => {
    test("should add a single item to cart", () => {
      const item = new Item("Apple", 1.5, 2);
      cart.addItem(item);

      expect(cart.isEmpty()).toBe(false);
      expect(cart.getItemCount()).toBe(2);
      expect(cart.getSubtotal()).toBeCloseTo(3.0);
    });

    test("should add multiple different items to cart", () => {
      cart.addItem(new Item("Apple", 1.5));
      cart.addItem(new Item("Banana", 0.5));

      expect(cart.items.length).toBe(2);
      expect(cart.items.map((item) => item.name)).toEqual(["Apple", "Banana"]);
    });

    test("should increase quantity when adding duplicate item", () => {
      cart.addItem(new Item("Apple", 1.5, 2));
      cart.addItem(new Item("Apple", 1.5, 3));

      // Should have only 1 unique item with combined quantity
      expect(cart.items.length).toBe(1);
      expect(cart.items[0].quantity).toBe(5);
      expect(cart.getItemCount()).toBe(5);
    });

    test("should skip non-matching items before finding the duplicate", () => {
      cart.addItem(new Item("Apple", 1.5));
      cart.addItem(new Item("Banana", 0.5));
      cart.addItem(new Item("Banana", 0.5, 2));

      expect(cart.items.length).toBe(2);
      expect(cart.items[0].quantity).toBe(1);
      expect(cart.items[1].quantity).toBe(3);
    });

    test("should keep original price when adding duplicate", () => {
      cart.addItem(new Item("Apple", 1.0, 1));
      cart.addItem(new Item("Apple", 5.0, 1));

      expect(cart.getSubtotal()).toBeCloseTo(2.0);
    });
  });

  describe("removeItem", () => {
    test("should remove an existing item", () => {
      cart.addItem(new Item("Apple", 1.5));

      expect(cart.removeItem("Apple")).toBe(true);
      expect(cart.isEmpty()).toBe(true);
    });

    test("should remove item after non-matching items", () => {
      cart.addItem(new Item("Apple", 1.5));
      cart.addItem(new Item("Banana", 0.5));
      cart.addItem(new Item("Cherry", 3.0));

      expect(cart.removeItem("Banana")).toBe(true);
      expect(cart.items.map((item) => item.name)).toEqual(["Apple", "Cherry"]);
    });

    test("should return false when removing nonexistent item", () => {
      cart.addItem(new Item("Apple", 1.5));

      expect(cart.removeItem("Banana")).toBe(false);
      expect(cart.items.length).toBe(1);
    });

    test("should return false when removing from empty cart", () => {
      expect(cart.removeItem("Apple")).toBe(false);
    });

    test("should return false when removing same item twice", () => {
      cart.addItem(new Item("Apple", 1.5));
      cart.removeItem("Apple");

      expect(cart.removeItem("Apple")).toBe(false);
    });
  });

  describe("getSubtotal", () => {
    test("should calculate subtotal for single item", () => {
      cart.addItem(new Item("Apple", 2.5, 2));
      expect(cart.getSubtotal()).toBeCloseTo(5.0);
    });

    test("should calculate subtotal for multiple items", () => {
      cart.addItem(new Item("Apple", 10.0, 5));
      cart.addItem(new Item("Banana", 5.0, 4));
      expect(cart.getSubtotal()).toBeCloseTo(70.0);
    });

    test("should return zero for empty cart", () => {
      expect(cart.getSubtotal()).toBe(0);
    });

    test("should ignore discount", () => {
      cart.addItem(new Item("Apple", 10.0, 10));
      cart.applyDiscount(50);
      expect(cart.getSubtotal()).toBeCloseTo(100.0);
    });
  });

  describe("applyDiscount", () => {
    test("should apply valid discount percentage", () => {
      cart.applyDiscount(25);
      expect(cart.discountPercent).toBe(25);
    });

    test("should apply zero discount", () => {
      cart.applyDiscount(0);
      expect(cart.discountPercent).toBe(0);
    });

    test("should apply full discount", () => {
      cart.addItem(new Item("Apple", 10.0));
      cart.applyDiscount(100);

      expect(cart.discountPercent).toBe(100);
      expect(cart.getTotal()).toBeCloseTo(0.0);
    });

    test("should throw error for negative discount", () => {
      // First condition of the OR
      expect(() => cart.applyDiscount(-1)).toThrow(
        "Discount must be between 0 and 100",
      );
    });

    test("should throw error for discount over 100", () => {
      // Second condition of the OR
      expect(() => cart.applyDiscount(101)).toThrow(
        "Discount must be between 0 and 100",
      );
    });

    test("should keep previous discount when new one is invalid", () => {
      cart.applyDiscount(10);
      expect(() => cart.applyDiscount(150)).toThrow();
      expect(cart.discountPercent).toBe(10);
    });

    test("should replace previous discount", () => {
      cart.applyDiscount(10);
      cart.applyDiscount(30);
      expect(cart.discountPercent).toBe(30);
    });
  });

  describe("getTotal", () => {
    test("should calculate total with discount applied", () => {
      cart.addItem(new Item("Apple", 10.0, 5));
      cart.addItem(new Item("Banana", 5.0, 4));
      // Subtotal: 50 + 20 = 70

      cart.applyDiscount(20);

      // 70 - (70 * 0.20) = 70 - 14 = 56
      expect(cart.getTotal()).toBeCloseTo(56.0);
    });

    test("should equal subtotal when no discount", () => {
      cart.addItem(new Item("Apple", 10.0, 3));
      expect(cart.getTotal()).toBeCloseTo(cart.getSubtotal());
    });

    test("should calculate total with fractional discount", () => {
      cart.addItem(new Item("Apple", 100.0));
      cart.applyDiscount(12.5);
      expect(cart.getTotal()).toBeCloseTo(87.5);
    });

    test("should return zero for empty cart with discount", () => {
      cart.applyDiscount(50);
      expect(cart.getTotal()).toBe(0);
    });
  });

  describe("clear", () => {
    test("should clear all items and reset discount", () => {
      cart.addItem(new Item("Apple", 1.5, 2));
      cart.addItem(new Item("Banana", 0.5));
      cart.applyDiscount(15);

      cart.clear();

      expect(cart.isEmpty()).toBe(true);
      expect(cart.discountPercent).toBe(0);
      expect(cart.getTotal()).toBe(0);
    });

    test("should not error when clearing empty cart", () => {
      cart.clear();
      expect(cart.isEmpty()).toBe(true);
    });

    test("should be reusable after clear", () => {
      cart.addItem(new Item("Apple", 1.5));
      cart.clear();
      cart.addItem(new Item("Banana", 0.5, 2));

      expect(cart.getItemCount()).toBe(2);
      expect(cart.getTotal()).toBeCloseTo(1.0);
    });
  });

  describe("getItemCount", () => {
    test("should sum all quantities", () => {
      cart.addItem(new Item("Apple", 1.5, 2));
      cart.addItem(new Item("Banana", 0.5, 3));
      expect(cart.getItemCount()).toBe(5);
    });

    test("should drop by full quantity of removed item", () => {
      cart.addItem(new Item("Apple", 1.5, 2));
      cart.addItem(new Item("Banana", 0.5, 3));
      cart.removeItem("Banana");
      expect(cart.getItemCount()).toBe(2);
    });
  });

  describe("isEmpty", () => {
    test("should return true after adding and removing all items", () => {
      cart.addItem(new Item("Apple", 1.5));
      cart.addItem(new Item("Banana", 0.5));
      expect(cart.isEmpty()).toBe(false);

      cart.removeItem("Apple");
      cart.removeItem("Banana");
      expect(cart.isEmpty()).toBe(true);
    });
  });
});
