"""Unit and branch coverage tests for Item and ShoppingCart classes."""
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
        item = Item("Banana", 0.75)
        assert item.name == "Banana"
        assert item.price == 0.75
        assert item.quantity == 1

    def test_item_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Item("Milk", -2.50, 1)

    def test_item_zero_price_raises_error(self):
        """Test that zero price raises ValueError."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Item("Freebie", 0, 1)

    def test_item_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item("Orange", 1.20, -5)

    def test_item_zero_quantity_raises_error(self):
        """Test that zero quantity raises ValueError."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item("Orange", 1.20, 0)

    def test_get_total_single_quantity(self):
        """Test total calculation for single item."""
        item = Item("Book", 15.99, 1)
        assert item.get_total() == pytest.approx(15.99)

    def test_get_total_multiple_quantity(self):
        """Test total calculation for multiple items."""
        item = Item("Pen", 2.50, 4)
        assert item.get_total() == pytest.approx(10.00)

    def test_item_equality(self):
        """Test that items with same name are equal regardless of price/quantity."""
        item1 = Item("Coffee", 4.50, 1)
        item2 = Item("Coffee", 5.00, 3)
        assert item1 == item2

    def test_item_inequality(self):
        """Test that items with different names are not equal."""
        item1 = Item("Coffee", 4.50, 1)
        item2 = Item("Tea", 4.50, 1)
        assert item1 != item2

    def test_item_equality_with_non_item_object(self):
        """Test equality comparison against a non-Item instance returns False."""
        item = Item("Coffee", 4.50, 1)
        assert item != "Coffee"
        assert item != 4.50
        assert item != None  # noqa: E711

    def test_item_repr(self):
        """Test string representation of Item."""
        item = Item("Laptop", 999.99, 2)
        assert repr(item) == "Item('Laptop', $999.99, qty=2)"


class TestShoppingCart:
    """Test suite for ShoppingCart class."""

    def setup_method(self):
        """Create a fresh cart before each test."""
        self.cart = ShoppingCart()

    def test_cart_starts_empty(self):
        """Test that new cart is empty."""
        assert self.cart.is_empty()
        assert self.cart.get_item_count() == 0
        assert self.cart.get_total() == 0
        assert self.cart.get_subtotal() == 0

    def test_add_single_item(self):
        """Test adding a single item to cart."""
        item = Item("Apple", 1.50, 2)
        self.cart.add_item(item)

        assert not self.cart.is_empty()
        assert self.cart.get_item_count() == 2
        assert self.cart.get_subtotal() == pytest.approx(3.00)
        assert len(self.cart.items) == 1

    def test_add_multiple_different_items(self):
        """Test adding different items to cart."""
        item1 = Item("Apple", 1.50, 2)
        item2 = Item("Orange", 2.00, 3)
        self.cart.add_item(item1)
        self.cart.add_item(item2)

        assert len(self.cart.items) == 2
        assert self.cart.get_item_count() == 5
        assert self.cart.get_subtotal() == pytest.approx(9.00)

    def test_add_duplicate_item_increases_quantity(self):
        """Test that adding duplicate item increases quantity instead of creating new entry."""
        item1 = Item("Apple", 1.50, 2)
        item2 = Item("Apple", 1.50, 3)

        self.cart.add_item(item1)
        self.cart.add_item(item2)

        assert len(self.cart.items) == 1
        assert self.cart.items[0].quantity == 5
        assert self.cart.get_item_count() == 5
        assert self.cart.get_subtotal() == pytest.approx(7.50)

    def test_remove_existing_item(self):
        """Test removing an item that exists in cart."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.80, 5))

        removed = self.cart.remove_item("Apple")
        assert removed is True
        assert len(self.cart.items) == 1
        assert self.cart.items[0].name == "Banana"

    def test_remove_nonexistent_item(self):
        """Test removing an item that doesn't exist returns False."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        removed = self.cart.remove_item("Watermelon")
        assert removed is False
        assert len(self.cart.items) == 1

    def test_remove_from_empty_cart(self):
        """Test removing from empty cart returns False."""
        assert self.cart.remove_item("Apple") is False

    def test_subtotal_single_item(self):
        """Test subtotal with one item."""
        self.cart.add_item(Item("Book", 20.0, 3))
        assert self.cart.get_subtotal() == pytest.approx(60.0)

    def test_subtotal_multiple_items(self):
        """Test subtotal with multiple items."""
        self.cart.add_item(Item("Book", 20.0, 2))
        self.cart.add_item(Item("Pen", 5.0, 4))
        assert self.cart.get_subtotal() == pytest.approx(60.0)

    def test_subtotal_empty_cart(self):
        """Test subtotal of empty cart is zero."""
        assert self.cart.get_subtotal() == 0

    def test_apply_valid_discount(self):
        """Test applying a valid discount percentage."""
        self.cart.apply_discount(25)
        assert self.cart.discount_percent == 25

    def test_apply_zero_discount(self):
        """Test applying 0% discount."""
        self.cart.apply_discount(0)
        assert self.cart.discount_percent == 0

    def test_apply_full_discount(self):
        """Test applying 100% discount."""
        self.cart.apply_discount(100)
        assert self.cart.discount_percent == 100

    def test_apply_negative_discount_raises_error(self):
        """Test that negative discount raises ValueError."""
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            self.cart.apply_discount(-10)

    def test_apply_over_100_discount_raises_error(self):
        """Test that discount over 100 raises ValueError."""
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            self.cart.apply_discount(101)

    def test_total_with_discount(self):
        """Test total calculation with discount applied."""
        self.cart.add_item(Item("Apple", 10.00, 5))
        self.cart.add_item(Item("Banana", 5.00, 4))
        self.cart.apply_discount(20)

        assert self.cart.get_total() == pytest.approx(56.00)

    def test_total_without_discount(self):
        """Test that total equals subtotal when no discount is set."""
        self.cart.add_item(Item("Coffee", 5.00, 2))
        assert self.cart.get_total() == pytest.approx(10.00)

    def test_total_with_full_discount(self):
        """Test that total is zero with 100% discount."""
        self.cart.add_item(Item("Coffee", 5.00, 2))
        self.cart.apply_discount(100)
        assert self.cart.get_total() == pytest.approx(0.0)

    def test_clear_cart(self):
        """Test that clear removes all items and resets discount."""
        self.cart.add_item(Item("Apple", 1.50, 3))
        self.cart.apply_discount(15)

        self.cart.clear()

        assert self.cart.is_empty()
        assert self.cart.discount_percent == 0
        assert len(self.cart.items) == 0

    def test_clear_empty_cart(self):
        """Test that clearing empty cart doesn't cause errors."""
        self.cart.clear()
        assert self.cart.is_empty()
        assert self.cart.discount_percent == 0

    def test_item_count_multiple_items(self):
        """Test item count sums all quantities."""
        self.cart.add_item(Item("Keyboard", 45.0, 2))
        self.cart.add_item(Item("Mouse", 25.0, 3))
        assert self.cart.get_item_count() == 5

    def test_is_empty_after_adding_and_removing(self):
        """Test is_empty after adding and removing all items."""
        item = Item("Speaker", 50.0, 1)
        self.cart.add_item(item)
        assert not self.cart.is_empty()

        self.cart.remove_item("Speaker")
        assert self.cart.is_empty()
