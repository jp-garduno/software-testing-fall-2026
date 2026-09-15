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

Create a file named `shopping_cart.py`:

```python
class Item:
    """Represents an item in the shopping cart."""

    def __init__(self, name, price, quantity=1):
        """
        Initialize an item.

        Args:
            name: Item name
            price: Item price (must be positive)
            quantity: Number of items (must be positive)

        Raises:
            ValueError: If price or quantity is invalid
        """
        if price <= 0:
            raise ValueError("Price must be positive")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.name = name
        self.price = price
        self.quantity = quantity

    def get_total(self):
        """Calculate total cost for this item."""
        return self.price * self.quantity

    def __eq__(self, other):
        """Check equality based on name."""
        if not isinstance(other, Item):
            return False
        return self.name == other.name

    def __repr__(self):
        """String representation of the item."""
        return f"Item('{self.name}', ${self.price}, qty={self.quantity})"


class ShoppingCart:
    """A shopping cart that can hold multiple items."""

    def __init__(self):
        """Initialize an empty shopping cart."""
        self.items = []
        self.discount_percent = 0

    def add_item(self, item):
        """
        Add an item to the cart. If item already exists, increase quantity.

        Args:
            item: Item object to add
        """
        # Check if item already exists
        for existing_item in self.items:
            if existing_item.name == item.name:
                existing_item.quantity += item.quantity
                return

        # Add new item
        self.items.append(item)

    def remove_item(self, item_name):
        """
        Remove an item from the cart by name.

        Args:
            item_name: Name of the item to remove

        Returns:
            True if item was removed, False if not found
        """
        for i, item in enumerate(self.items):
            if item.name == item_name:
                self.items.pop(i)
                return True
        return False

    def get_subtotal(self):
        """Calculate subtotal before discount."""
        return sum(item.get_total() for item in self.items)

    def apply_discount(self, percent):
        """
        Apply a discount percentage to the cart.

        Args:
            percent: Discount percentage (0-100)

        Raises:
            ValueError: If percent is not between 0 and 100
        """
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        self.discount_percent = percent

    def get_total(self):
        """Calculate total after discount."""
        subtotal = self.get_subtotal()
        discount_amount = subtotal * (self.discount_percent / 100)
        return subtotal - discount_amount

    def clear(self):
        """Remove all items from the cart."""
        self.items = []
        self.discount_percent = 0

    def get_item_count(self):
        """Get total number of items (sum of all quantities)."""
        return sum(item.quantity for item in self.items)

    def is_empty(self):
        """Check if cart is empty."""
        return len(self.items) == 0
```

## Part 2: Write Tests for Item Class (15 minutes)

Create `test_shopping_cart.py` and start with Item tests:

```python
import pytest
from shopping_cart import Item, ShoppingCart

class TestItem:
    """Test suite for Item class."""

    def test_item_creation_valid(self):
        """Test creating an item with valid parameters."""
        item = Item("Apple", 1.50, 3)
        assert item.name == "Apple"
        assert item.price == 1.50
        assert item.quantity == 3

    def test_item_default_quantity(self):
        """Test that default quantity is 1."""
        # TODO: Implement this test
        pass

    def test_item_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        # TODO: Implement this test
        pass

    def test_item_zero_price_raises_error(self):
        """Test that zero price raises ValueError."""
        # TODO: Implement this test
        pass

    def test_item_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        # TODO: Implement this test
        pass

    def test_item_zero_quantity_raises_error(self):
        """Test that zero quantity raises ValueError."""
        # TODO: Implement this test
        pass

    def test_get_total_single_quantity(self):
        """Test total calculation for single item."""
        # TODO: Implement this test
        pass

    def test_get_total_multiple_quantity(self):
        """Test total calculation for multiple items."""
        # TODO: Implement this test
        pass

    def test_item_equality(self):
        """Test that items with same name are equal."""
        # TODO: Implement this test
        pass

    def test_item_inequality(self):
        """Test that items with different names are not equal."""
        # TODO: Implement this test
        pass
```

## Part 3: Write Tests for ShoppingCart Class (20 minutes)

Continue in `test_shopping_cart.py`:

```python
class TestShoppingCart:
    """Test suite for ShoppingCart class."""

    def setup_method(self):
        """Create a fresh cart before each test."""
        self.cart = ShoppingCart()

    # Test initialization
    def test_cart_starts_empty(self):
        """Test that new cart is empty."""
        assert self.cart.is_empty()
        assert self.cart.get_item_count() == 0
        assert self.cart.get_total() == 0

    # Test add_item
    def test_add_single_item(self):
        """Test adding a single item to cart."""
        # TODO: Implement this test
        pass

    def test_add_multiple_different_items(self):
        """Test adding different items to cart."""
        # TODO: Implement this test
        pass

    def test_add_duplicate_item_increases_quantity(self):
        """Test that adding duplicate item increases quantity instead of creating new entry."""
        # TODO: Implement this test
        # Hint: Add same item twice and verify there's only one entry with combined quantity
        pass

    # Test remove_item
    def test_remove_existing_item(self):
        """Test removing an item that exists in cart."""
        # TODO: Implement this test
        pass

    def test_remove_nonexistent_item(self):
        """Test removing an item that doesn't exist returns False."""
        # TODO: Implement this test
        pass

    def test_remove_from_empty_cart(self):
        """Test removing from empty cart returns False."""
        # TODO: Implement this test
        pass

    # Test get_subtotal
    def test_subtotal_single_item(self):
        """Test subtotal with one item."""
        # TODO: Implement this test
        pass

    def test_subtotal_multiple_items(self):
        """Test subtotal with multiple items."""
        # TODO: Implement this test
        pass

    def test_subtotal_empty_cart(self):
        """Test subtotal of empty cart is zero."""
        # TODO: Implement this test
        pass

    # Test apply_discount
    def test_apply_valid_discount(self):
        """Test applying a valid discount percentage."""
        # TODO: Implement this test
        pass

    def test_apply_zero_discount(self):
        """Test applying 0% discount."""
        # TODO: Implement this test
        pass

    def test_apply_full_discount(self):
        """Test applying 100% discount."""
        # TODO: Implement this test
        pass

    def test_apply_negative_discount_raises_error(self):
        """Test that negative discount raises ValueError."""
        # TODO: Implement this test
        pass

    def test_apply_over_100_discount_raises_error(self):
        """Test that discount over 100 raises ValueError."""
        # TODO: Implement this test
        pass

    # Test get_total with discount
    def test_total_with_discount(self):
        """Test total calculation with discount applied."""
        # TODO: Implement this test
        # Example: Add items totaling $100, apply 20% discount, verify total is $80
        pass

    def test_total_without_discount(self):
        """Test that total equals subtotal when no discount."""
        # TODO: Implement this test
        pass

    # Test clear
    def test_clear_cart(self):
        """Test that clear removes all items and resets discount."""
        # TODO: Implement this test
        pass

    def test_clear_empty_cart(self):
        """Test that clearing empty cart doesn't cause errors."""
        # TODO: Implement this test
        pass

    # Test get_item_count
    def test_item_count_multiple_items(self):
        """Test item count sums all quantities."""
        # TODO: Implement this test
        # Example: Add item with qty 2 and item with qty 3, verify count is 5
        pass

    # Test is_empty
    def test_is_empty_after_adding_and_removing(self):
        """Test is_empty after adding and removing all items."""
        # TODO: Implement this test
        pass
```

## Part 4: Achieve Branch Coverage (5 minutes)

Run coverage and analyze branches:

```bash
# Run with branch coverage
pytest --cov=shopping_cart --cov-report=term-missing --cov-branch test_shopping_cart.py

# Generate detailed HTML report
pytest --cov=shopping_cart --cov-report=html --cov-branch test_shopping_cart.py
```

### Understanding Branch Coverage

Branch coverage checks that every decision point (if/else) executes both True and False paths:

```python
# This function has 2 branches
def divide(a, b):
    if b == 0:        # Branch 1: True path
        raise ValueError
    return a / b      # Branch 2: False path (normal case)
```

To achieve 100% branch coverage, you need tests for:

- The case where `b == 0` (True branch)
- The case where `b != 0` (False branch)

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
4. **Not testing duplicate items** - The add_item logic for duplicates needs testing
5. **Using mutable default arguments** - This is a common Python pitfall
6. **Not testing boundary values** - Test 0, 100, negative for discounts

## Tips for Success

- Test one method at a time and verify coverage increases
- Use descriptive test names that explain the scenario
- Set up common test data in helper methods if needed
- Check coverage report to find missed branches
- Test the happy path first, then edge cases and errors
- Use pytest.approx() for floating point comparisons

## Example Test Implementations

```python
def test_add_single_item(self):
    """Test adding a single item to cart."""
    item = Item("Apple", 1.50, 2)
    self.cart.add_item(item)

    assert not self.cart.is_empty()
    assert self.cart.get_item_count() == 2
    assert self.cart.get_subtotal() == pytest.approx(3.00)

def test_add_duplicate_item_increases_quantity(self):
    """Test that adding duplicate item increases quantity."""
    item1 = Item("Apple", 1.50, 2)
    item2 = Item("Apple", 1.50, 3)

    self.cart.add_item(item1)
    self.cart.add_item(item2)

    # Should have only 1 unique item with combined quantity
    assert len(self.cart.items) == 1
    assert self.cart.items[0].quantity == 5
    assert self.cart.get_item_count() == 5

def test_total_with_discount(self):
    """Test total calculation with discount applied."""
    self.cart.add_item(Item("Apple", 10.00, 5))
    self.cart.add_item(Item("Banana", 5.00, 4))
    # Subtotal: 50 + 20 = 70

    self.cart.apply_discount(20)
    total = self.cart.get_total()

    # 70 - (70 * 0.20) = 70 - 14 = 56
    assert total == pytest.approx(56.00)
```

## Submission

Submit the following files:

- `shopping_cart.py` - Your implementation
- `test_shopping_cart.py` - Your complete test suite
- Screenshot showing 100% statement AND branch coverage

## Next Steps

After completing this exercise:

- Move on to [Exercise 3: User Service](./03-user-service.md) for integration testing and mocking
- Review [Module Theory: Branch Coverage](../theory/03-branch-coverage.md)
- Understand why branch coverage is more thorough than statement coverage
