# Exercise 2: Shopping Cart Class Testing

**Duration**: 60 minutes  
**Difficulty**: Intermediate  
**Topics**: Class testing, branch coverage, object interactions, state management

## Objectives

By completing this exercise, you will:

- Test classes with multiple methods and state
- Achieve branch coverage in addition to statement coverage
- Test object interactions and relationships
- Handle edge cases in object-oriented code
- Understand the difference between statement and branch coverage

## Background

Real-world applications involve classes that maintain state and interact with other objects. This exercise introduces testing classes with complex behavior, including edge cases like empty collections, invalid inputs, and business logic rules.

## Part 1: Implementation (20 minutes)

Create a file named `shoppingCart.js`:

```javascript
class Item {
  /**
   * Represents an item in the shopping cart.
   * @param {string} name - Item name
   * @param {number} price - Item price (must be positive)
   * @param {number} quantity - Number of items (must be positive)
   */
  constructor(name, price, quantity = 1) {
    if (price <= 0) {
      throw new Error("Price must be positive");
    }
    if (quantity <= 0) {
      throw new Error("Quantity must be positive");
    }

    this.name = name;
    this.price = price;
    this.quantity = quantity;
  }

  /**
   * Calculate total cost for this item.
   */
  getTotal() {
    return this.price * this.quantity;
  }
}

class ShoppingCart {
  /**
   * A shopping cart that can hold multiple items.
   */
  constructor() {
    this.items = [];
    this.discountPercent = 0;
  }

  /**
   * Add an item to the cart. If item already exists, increase quantity.
   * @param {Item} item - Item object to add
   */
  addItem(item) {
    // Check if item already exists
    const existing = this.items.find((i) => i.name === item.name);
    if (existing) {
      existing.quantity += item.quantity;
      return;
    }

    // Add new item
    this.items.push(item);
  }

  /**
   * Remove an item from the cart by name.
   * @param {string} itemName - Name of the item to remove
   * @returns {boolean} True if item was removed, false if not found
   */
  removeItem(itemName) {
    const index = this.items.findIndex((item) => item.name === itemName);
    if (index !== -1) {
      this.items.splice(index, 1);
      return true;
    }
    return false;
  }

  /**
   * Calculate subtotal before discount.
   */
  getSubtotal() {
    return this.items.reduce((sum, item) => sum + item.getTotal(), 0);
  }

  /**
   * Apply a discount percentage to the cart.
   * @param {number} percent - Discount percentage (0-100)
   */
  applyDiscount(percent) {
    if (percent < 0 || percent > 100) {
      throw new Error("Discount must be between 0 and 100");
    }
    this.discountPercent = percent;
  }

  /**
   * Calculate total after discount.
   */
  getTotal() {
    const subtotal = this.getSubtotal();
    const discountAmount = subtotal * (this.discountPercent / 100);
    return subtotal - discountAmount;
  }

  /**
   * Remove all items from the cart.
   */
  clear() {
    this.items = [];
    this.discountPercent = 0;
  }

  /**
   * Get total number of items (sum of all quantities).
   */
  getItemCount() {
    return this.items.reduce((sum, item) => sum + item.quantity, 0);
  }

  /**
   * Check if cart is empty.
   */
  isEmpty() {
    return this.items.length === 0;
  }
}

module.exports = { Item, ShoppingCart };
```

## Part 2: Write Tests for Item Class (15 minutes)

Create `shoppingCart.test.js` and start with Item tests:

```javascript
const { Item, ShoppingCart } = require("./shoppingCart");

describe("Item", () => {
  test("should create item with valid parameters", () => {
    const item = new Item("Apple", 1.5, 3);
    expect(item.name).toBe("Apple");
    expect(item.price).toBe(1.5);
    expect(item.quantity).toBe(3);
  });

  test("should use default quantity of 1", () => {
    // TODO: Implement this test
  });

  test("should throw error for negative price", () => {
    // TODO: Implement this test
  });

  test("should throw error for zero price", () => {
    // TODO: Implement this test
  });

  test("should throw error for negative quantity", () => {
    // TODO: Implement this test
  });

  test("should throw error for zero quantity", () => {
    // TODO: Implement this test
  });

  test("should calculate total for single quantity", () => {
    // TODO: Implement this test
  });

  test("should calculate total for multiple quantity", () => {
    // TODO: Implement this test
  });
});
```

## Part 3: Write Tests for ShoppingCart Class (20 minutes)

Continue in `shoppingCart.test.js`:

```javascript
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
    });

    test("should add multiple different items to cart", () => {
      // TODO: Implement this test
    });

    test("should increase quantity when adding duplicate item", () => {
      // TODO: Implement this test
      // Hint: Add same item twice and verify there's only one entry with combined quantity
    });
  });

  // Test removeItem
  describe("removeItem", () => {
    test("should remove an existing item", () => {
      // TODO: Implement this test
    });

    test("should return false when removing nonexistent item", () => {
      // TODO: Implement this test
    });

    test("should return false when removing from empty cart", () => {
      // TODO: Implement this test
    });
  });

  // Test getSubtotal
  describe("getSubtotal", () => {
    test("should calculate subtotal for single item", () => {
      // TODO: Implement this test
    });

    test("should calculate subtotal for multiple items", () => {
      // TODO: Implement this test
    });

    test("should return zero for empty cart", () => {
      // TODO: Implement this test
    });
  });

  // Test applyDiscount
  describe("applyDiscount", () => {
    test("should apply valid discount percentage", () => {
      // TODO: Implement this test
    });

    test("should apply zero discount", () => {
      // TODO: Implement this test
    });

    test("should apply full discount", () => {
      // TODO: Implement this test
    });

    test("should throw error for negative discount", () => {
      // TODO: Implement this test
    });

    test("should throw error for discount over 100", () => {
      // TODO: Implement this test
    });
  });

  // Test getTotal with discount
  describe("getTotal", () => {
    test("should calculate total with discount applied", () => {
      // TODO: Implement this test
      // Example: Add items totaling $100, apply 20% discount, verify total is $80
    });

    test("should equal subtotal when no discount", () => {
      // TODO: Implement this test
    });
  });

  // Test clear
  describe("clear", () => {
    test("should clear all items and reset discount", () => {
      // TODO: Implement this test
    });

    test("should not error when clearing empty cart", () => {
      // TODO: Implement this test
    });
  });

  // Test getItemCount
  describe("getItemCount", () => {
    test("should sum all quantities", () => {
      // TODO: Implement this test
      // Example: Add item with qty 2 and item with qty 3, verify count is 5
    });
  });

  // Test isEmpty
  describe("isEmpty", () => {
    test("should return true after adding and removing all items", () => {
      // TODO: Implement this test
    });
  });
});
```

## Part 4: Achieve Branch Coverage (5 minutes)

Run coverage and analyze branches:

```bash
# Run with branch coverage
npm run test:coverage

# Or with Jest directly
jest --coverage
```

### Understanding Branch Coverage

Branch coverage checks that every decision point (if/else) executes both True and False paths:

```javascript
// This function has 2 branches
function divide(a, b) {
  if (b === 0) {
    // Branch 1: True path
    throw new Error();
  }
  return a / b; // Branch 2: False path (normal case)
}
```

To achieve 100% branch coverage, you need tests for:

- The case where `b === 0` (True branch)
- The case where `b !== 0` (False branch)

## Evaluation Criteria

Your solution will be evaluated on:

- **Statement Coverage**: 100% of statements executed
- **Branch Coverage**: 100% of branches executed (both True/False paths)
- **Edge Cases**: Empty cart, zero values, invalid inputs
- **State Testing**: Verify cart state changes correctly
- **Object Interactions**: Test that items and cart work together
- **Test Independence**: Each test can run independently

## Common Mistakes to Avoid

1. **Not testing both branches** - Every if/else needs two tests
2. **Not testing empty cart** - Many bugs occur with empty collections
3. **Not verifying state changes** - Check that methods actually modify state
4. **Not testing duplicate items** - The addItem logic for duplicates needs testing
5. **Not testing boundary values** - Test 0, 100, negative for discounts
6. **Mutating test data** - Each test should create its own data

## Tips for Success

- Test one method at a time and verify coverage increases
- Use descriptive test names that explain the scenario
- Set up common test data in helper methods if needed
- Check coverage report to find missed branches
- Test the happy path first, then edge cases and errors
- Use `toBeCloseTo()` for floating point comparisons

## Example Test Implementations

```javascript
test("should add a single item to cart", () => {
  const item = new Item("Apple", 1.5, 2);
  cart.addItem(item);

  expect(cart.isEmpty()).toBe(false);
  expect(cart.getItemCount()).toBe(2);
  expect(cart.getSubtotal()).toBeCloseTo(3.0);
});

test("should increase quantity when adding duplicate item", () => {
  const item1 = new Item("Apple", 1.5, 2);
  const item2 = new Item("Apple", 1.5, 3);

  cart.addItem(item1);
  cart.addItem(item2);

  // Should have only 1 unique item with combined quantity
  expect(cart.items.length).toBe(1);
  expect(cart.items[0].quantity).toBe(5);
  expect(cart.getItemCount()).toBe(5);
});

test("should calculate total with discount applied", () => {
  cart.addItem(new Item("Apple", 10.0, 5));
  cart.addItem(new Item("Banana", 5.0, 4));
  // Subtotal: 50 + 20 = 70

  cart.applyDiscount(20);
  const total = cart.getTotal();

  // 70 - (70 * 0.20) = 70 - 14 = 56
  expect(total).toBeCloseTo(56.0);
});
```

## Submission

Submit the following files:

- `shoppingCart.js` - Your implementation
- `shoppingCart.test.js` - Your complete test suite
- Screenshot showing 100% statement AND branch coverage

## Next Steps

After completing this exercise:

- Move on to [Exercise 3: User Service](./03-user-service.md) for integration testing and mocking
- Review [Module Theory: Branch Coverage](../theory/03-branch-coverage.md)
- Understand why branch coverage is more thorough than statement coverage
