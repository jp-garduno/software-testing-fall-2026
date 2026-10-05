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
        item = Item("Apple", 1.50)
        assert item.quantity == 1

    def test_item_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Item("Apple", -1.00)

    def test_item_zero_price_raises_error(self):
        """Test that zero price raises ValueError."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Item("Apple", 0)

    def test_item_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item("Apple", 1.50, -2)

    def test_item_zero_quantity_raises_error(self):
        """Test that zero quantity raises ValueError."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item("Apple", 1.50, 0)

    def test_get_total_single_quantity(self):
        """Test total calculation for single item."""
        item = Item("Apple", 1.50)
        assert item.get_total() == pytest.approx(1.50)

    def test_get_total_multiple_quantity(self):
        """Test total calculation for multiple items."""
        item = Item("Apple", 1.50, 4)
        assert item.get_total() == pytest.approx(6.00)

    def test_item_equality(self):
        """Test that items with same name are equal."""
        item1 = Item("Apple", 1.50, 1)
        item2 = Item("Apple", 2.00, 5)
        assert item1 == item2

    def test_item_inequality(self):
        """Test that items with different names are not equal."""
        item1 = Item("Apple", 1.50)
        item2 = Item("Banana", 1.50)
        assert item1 != item2

    def test_item_not_equal_to_non_item(self):
        """Test that an item is never equal to an object of another type."""
        item = Item("Apple", 1.50)
        assert item != "Apple"

    def test_item_repr(self):
        """Test the string representation of an item."""
        item = Item("Apple", 1.5, 3)
        assert repr(item) == "Item('Apple', $1.5, qty=3)"


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

    def test_cart_starts_without_discount(self):
        """Test that new cart has no discount."""
        assert self.cart.discount_percent == 0

    # Test add_item
    def test_add_single_item(self):
        """Test adding a single item to cart."""
        item = Item("Apple", 1.50, 2)
        self.cart.add_item(item)

        assert not self.cart.is_empty()
        assert self.cart.get_item_count() == 2
        assert self.cart.get_subtotal() == pytest.approx(3.00)

    def test_add_multiple_different_items(self):
        """Test adding different items to cart."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.50, 3))

        assert len(self.cart.items) == 2
        assert self.cart.get_item_count() == 5

    def test_add_duplicate_item_increases_quantity(self):
        """Test that adding duplicate item increases quantity instead of creating new entry."""
        item1 = Item("Apple", 1.50, 2)
        item2 = Item("Apple", 1.50, 3)

        self.cart.add_item(item1)
        self.cart.add_item(item2)

        assert len(self.cart.items) == 1
        assert self.cart.items[0].quantity == 5
        assert self.cart.get_item_count() == 5

    def test_add_duplicate_after_different_item(self):
        """Test duplicate detection when the match is not the first item."""
        self.cart.add_item(Item("Apple", 1.50, 1))
        self.cart.add_item(Item("Banana", 0.50, 1))
        self.cart.add_item(Item("Banana", 0.50, 2))

        assert len(self.cart.items) == 2
        assert self.cart.items[1].quantity == 3

    # Test remove_item
    def test_remove_existing_item(self):
        """Test removing an item that exists in cart."""
        self.cart.add_item(Item("Apple", 1.50))

        result = self.cart.remove_item("Apple")

        assert result is True
        assert self.cart.is_empty()

    def test_remove_item_not_first_in_cart(self):
        """Test removing an item that is not the first one keeps the others."""
        self.cart.add_item(Item("Apple", 1.50))
        self.cart.add_item(Item("Banana", 0.50))

        result = self.cart.remove_item("Banana")

        assert result is True
        assert len(self.cart.items) == 1
        assert self.cart.items[0].name == "Apple"

    def test_remove_nonexistent_item(self):
        """Test removing an item that doesn't exist returns False."""
        self.cart.add_item(Item("Apple", 1.50))

        result = self.cart.remove_item("Banana")

        assert result is False
        assert len(self.cart.items) == 1

    def test_remove_from_empty_cart(self):
        """Test removing from empty cart returns False."""
        assert self.cart.remove_item("Apple") is False

    # Test get_subtotal
    def test_subtotal_single_item(self):
        """Test subtotal with one item."""
        self.cart.add_item(Item("Apple", 2.00, 3))
        assert self.cart.get_subtotal() == pytest.approx(6.00)

    def test_subtotal_multiple_items(self):
        """Test subtotal with multiple items."""
        self.cart.add_item(Item("Apple", 2.00, 3))
        self.cart.add_item(Item("Banana", 0.50, 4))
        assert self.cart.get_subtotal() == pytest.approx(8.00)

    def test_subtotal_empty_cart(self):
        """Test subtotal of empty cart is zero."""
        assert self.cart.get_subtotal() == 0

    # Test apply_discount
    def test_apply_valid_discount(self):
        """Test applying a valid discount percentage."""
        self.cart.apply_discount(25)
        assert self.cart.discount_percent == 25

    def test_apply_zero_discount(self):
        """Test applying 0% discount."""
        self.cart.add_item(Item("Apple", 10.00))
        self.cart.apply_discount(0)
        assert self.cart.get_total() == pytest.approx(10.00)

    def test_apply_full_discount(self):
        """Test applying 100% discount."""
        self.cart.add_item(Item("Apple", 10.00))
        self.cart.apply_discount(100)
        assert self.cart.get_total() == pytest.approx(0.00)

    def test_apply_negative_discount_raises_error(self):
        """Test that negative discount raises ValueError."""
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            self.cart.apply_discount(-1)

    def test_apply_over_100_discount_raises_error(self):
        """Test that discount over 100 raises ValueError."""
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            self.cart.apply_discount(101)

    def test_invalid_discount_keeps_previous_discount(self):
        """Test that a rejected discount does not change the current one."""
        self.cart.apply_discount(10)
        with pytest.raises(ValueError):
            self.cart.apply_discount(150)
        assert self.cart.discount_percent == 10

    # Test get_total with discount
    def test_total_with_discount(self):
        """Test total calculation with discount applied."""
        self.cart.add_item(Item("Apple", 10.00, 5))
        self.cart.add_item(Item("Banana", 5.00, 4))
        # Subtotal: 50 + 20 = 70

        self.cart.apply_discount(20)

        # 70 - (70 * 0.20) = 56
        assert self.cart.get_total() == pytest.approx(56.00)

    def test_total_without_discount(self):
        """Test that total equals subtotal when no discount."""
        self.cart.add_item(Item("Apple", 10.00, 2))
        assert self.cart.get_total() == pytest.approx(self.cart.get_subtotal())

    # Test clear
    def test_clear_cart(self):
        """Test that clear removes all items and resets discount."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.50))
        self.cart.apply_discount(15)

        self.cart.clear()

        assert self.cart.is_empty()
        assert self.cart.discount_percent == 0
        assert self.cart.get_total() == 0

    def test_clear_empty_cart(self):
        """Test that clearing empty cart doesn't cause errors."""
        self.cart.clear()
        assert self.cart.is_empty()

    # Test get_item_count
    def test_item_count_multiple_items(self):
        """Test item count sums all quantities."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.50, 3))
        assert self.cart.get_item_count() == 5

    # Test is_empty
    def test_is_empty_after_adding_and_removing(self):
        """Test is_empty after adding and removing all items."""
        self.cart.add_item(Item("Apple", 1.50))
        assert not self.cart.is_empty()

        self.cart.remove_item("Apple")

        assert self.cart.is_empty()
