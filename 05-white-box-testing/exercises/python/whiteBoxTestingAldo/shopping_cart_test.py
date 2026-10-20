import pytest
from whiteBoxTestingAldo.shopping_cart import Item, ShoppingCart

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
        item = Item("Banana", 0.75)
        assert item.quantity == 1
        

    def test_item_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        # TODO: Implement this test
        with pytest.raises(ValueError):
            Item("Apple", -1.50, 3)

    def test_item_zero_price_raises_error(self):
        """Test that zero price raises ValueError."""
        # TODO: Implement this test
        with pytest.raises(ValueError):
            Item("Apple", 0, 3)
        pass

    def test_item_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        # TODO: Implement this test
        with pytest.raises(ValueError):
            Item("Apple", 1.50, -3)

    def test_item_zero_quantity_raises_error(self):
        """Test that zero quantity raises ValueError."""
        # TODO: Implement this test
        with pytest.raises(ValueError):
            Item("Apple", 1.50, 0)

    def test_get_total_single_quantity(self):
        """Test total calculation for single item."""
        # TODO: Implement this test
        item = Item("Apple", 1.50, 3)
        assert item.get_total() == 4.50

    def test_get_total_multiple_quantity(self):
        """Test total calculation for multiple items."""
        # TODO: Implement this test
        item1 = Item("Apple", 1.50, 3)
        item2 = Item("Banana", 0.75, 2)
        assert item1.get_total() == 4.50
        assert item2.get_total() == 1.50

    def test_item_equality(self):
        """Test that items with same name are equal."""
        # TODO: Implement this test
        item1 = Item("Apple", 1.50, 3)
        item2 = Item("Apple", 2.00, 2)
        assert item1 == item2

    def test_item_inequality(self):
        """Test that items with different names are not equal."""
        # TODO: Implement this test
        item1 = Item("Apple", 1.50, 3)
        item2 = Item("Banana", 0.75, 2)
        assert item1 != item2

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
        item = Item("Apple", 1.50, 3)
        self.cart.add_item(item)
        assert not self.cart.is_empty()
        assert self.cart.get_item_count() == 3
        assert self.cart.get_subtotal() == 4.50

    def test_add_multiple_different_items(self):
        """Test adding different items to cart."""
        # TODO: Implement this test
        item1 = Item("Apple", 1.50, 3)
        item2 = Item("Banana", 0.75, 2)
        self.cart.add_item(item1)
        self.cart.add_item(item2)
        assert self.cart.get_item_count() == 5
        assert self.cart.get_subtotal() == 6.00

    def test_add_duplicate_item_increases_quantity(self):
        """Test that adding duplicate item increases quantity instead of creating new entry."""
        # TODO: Implement this test
        # Hint: Add same item twice and verify there's only one entry with combined quantity
        item1 = Item("Apple", 1.50, 3)
        item2 = Item("Apple", 1.50, 2)
        self.cart.add_item(item1)
        self.cart.add_item(item2)
        assert self.cart.get_item_count() == 5

    # Test remove_item
    def test_remove_existing_item(self):
        """Test removing an item that exists in cart."""
        # TODO: Implement this test
        item = Item("Apple", 1.50, 3)
        self.cart.add_item(item)
        assert self.cart.remove_item("Apple") == True

    def test_remove_nonexistent_item(self):
        """Test removing an item that doesn't exist returns False."""
        # TODO: Implement this test
        assert self.cart.remove_item("Banana") == False

    def test_remove_from_empty_cart(self):
        """Test removing from empty cart returns False."""
        # TODO: Implement this test
        assert self.cart.remove_item("Apple") == False

    # Test get_subtotal
    def test_subtotal_single_item(self):
        """Test subtotal with one item."""
        # TODO: Implement this test
        item = Item("Apple", 1.50, 3)
        self.cart.add_item(item)
        assert self.cart.get_subtotal() == 4.50

    def test_subtotal_multiple_items(self):
        """Test subtotal with multiple items."""
        # TODO: Implement this test
        item1 = Item("Apple", 1.50, 3)
        item2 = Item("Banana", 0.75, 2)
        self.cart.add_item(item1)
        self.cart.add_item(item2)
        assert self.cart.get_subtotal() == 6.00

    def test_subtotal_empty_cart(self):
        """Test subtotal of empty cart is zero."""
        # TODO: Implement this test
        assert self.cart.get_subtotal() == 0

    # Test apply_discount
    def test_apply_valid_discount(self):
        """Test applying a valid discount percentage."""
        # TODO: Implement this test
        item = Item("Apple", 1.50, 3)
        self.cart.add_item(item)
        self.cart.apply_discount(20)
        assert self.cart.discount_percent == 20

    def test_apply_zero_discount(self):
        """Test applying 0% discount."""
        # TODO: Implement this test
        item = Item("Apple", 1.50, 3)
        self.cart.add_item(item)
        self.cart.apply_discount(0)
        assert self.cart.discount_percent == 0

    def test_apply_full_discount(self):
        """Test applying 100% discount."""
        # TODO: Implement this test
        item = Item("Apple", 1.50, 3)
        self.cart.add_item(item)
        self.cart.apply_discount(100)
        assert self.cart.discount_percent == 100

    def test_apply_negative_discount_raises_error(self):
        """Test that negative discount raises ValueError."""
        # TODO: Implement this test
        item = Item("Apple", 1.50, 3)
        self.cart.add_item(item)
        with pytest.raises(ValueError):
            self.cart.apply_discount(-10)

    def test_apply_over_100_discount_raises_error(self):
        """Test that discount over 100 raises ValueError."""
        # TODO: Implement this test
        item = Item("Apple", 1.50, 3)
        self.cart.add_item(item)
        with pytest.raises(ValueError):
            self.cart.apply_discount(110)

    # Test get_total with discount
    def test_total_with_discount(self):
        """Test total calculation with discount applied."""
        # TODO: Implement this test
        # Example: Add items totaling $100, apply 20% discount, verify total is $80
        item1 = Item("Apple", 50, 1)
        item2 = Item("Banana", 50, 1)
        self.cart.add_item(item1)
        self.cart.add_item(item2)
        self.cart.apply_discount(20)
        assert self.cart.get_total() == 80.0

    def test_total_without_discount(self):
        """Test that total equals subtotal when no discount."""
        # TODO: Implement this test
        item = Item("Apple", 1.50, 3)
        self.cart.add_item(item)
        assert self.cart.get_total() == self.cart.get_subtotal()

    # Test clear
    def test_clear_cart(self):
        """Test that clear removes all items and resets discount."""
        # TODO: Implement this test
        item = Item("Apple", 1.50, 3)
        self.cart.add_item(item)
        self.cart.clear()
        assert self.cart.is_empty()
        assert self.cart.discount_percent == 0

    def test_clear_empty_cart(self):
        """Test that clearing empty cart doesn't cause errors."""
        # TODO: Implement this test
        self.cart.clear()
        assert self.cart.is_empty()

    # Test get_item_count
    def test_item_count_multiple_items(self):
        """Test item count sums all quantities."""
        # TODO: Implement this test
        # Example: Add item with qty 2 and item with qty 3, verify count is 5
        item1 = Item("Apple", 1.50, 2)
        item2 = Item("Banana", 0.75, 3)
        self.cart.add_item(item1)
        self.cart.add_item(item2)
        assert self.cart.get_item_count() == 5

    # Test is_empty
    def test_is_empty_after_adding_and_removing(self):
        """Test is_empty after adding and removing all items."""
        # TODO: Implement this test
        item = Item("Apple", 1.50, 3)
        self.cart.add_item(item)
        self.cart.remove_item(item)
        assert self.cart.is_empty()