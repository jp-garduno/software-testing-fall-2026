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
