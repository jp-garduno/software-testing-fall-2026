"""Unit tests for Item and ShoppingCart (exercise 2)."""

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
        assert Item("Apple", 1.50).quantity == 1

    def test_item_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Item("Apple", -1.0)

    def test_item_zero_price_raises_error(self):
        """Test that zero price raises ValueError."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Item("Apple", 0)

    def test_item_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item("Apple", 1.50, -1)

    def test_item_zero_quantity_raises_error(self):
        """Test that zero quantity raises ValueError."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item("Apple", 1.50, 0)

    def test_get_total_single_quantity(self):
        """Test total calculation for single item."""
        assert Item("Apple", 1.50).get_total() == pytest.approx(1.50)

    def test_get_total_multiple_quantity(self):
        """Test total calculation for multiple items."""
        assert Item("Apple", 1.50, 4).get_total() == pytest.approx(6.00)

    def test_item_equality(self):
        """Test that items with same name are equal."""
        assert Item("Apple", 1.50, 1) == Item("Apple", 9.99, 5)

    def test_item_inequality(self):
        """Test that items with different names are not equal."""
        assert Item("Apple", 1.50) != Item("Banana", 1.50)

    def test_item_not_equal_to_other_type(self):
        """Test that an item is never equal to a non-Item object."""
        assert Item("Apple", 1.50) != "Apple"

    def test_item_repr(self):
        """Test the string representation of an item."""
        assert repr(Item("Apple", 1.5, 2)) == "Item('Apple', $1.5, qty=2)"


class TestShoppingCart:
    """Test suite for ShoppingCart class."""

    def setup_method(self):
        """Create a fresh cart before each test."""
        self.cart = ShoppingCart()

    # initialization
    def test_cart_starts_empty(self):
        """Test that new cart is empty."""
        assert self.cart.is_empty()
        assert self.cart.get_item_count() == 0
        assert self.cart.get_total() == 0

    # add_item
    def test_add_single_item(self):
        """Test adding a single item to cart."""
        self.cart.add_item(Item("Apple", 1.50, 2))

        assert not self.cart.is_empty()
        assert self.cart.get_item_count() == 2
        assert self.cart.get_subtotal() == pytest.approx(3.00)

    def test_add_multiple_different_items(self):
        """Test adding different items to cart."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.50, 4))

        assert len(self.cart.items) == 2
        assert self.cart.get_item_count() == 6

    def test_add_duplicate_item_increases_quantity(self):
        """Test that adding duplicate item increases quantity instead of creating new entry."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Apple", 1.50, 3))

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

    # remove_item
    def test_remove_existing_item(self):
        """Test removing an item that exists in cart."""
        self.cart.add_item(Item("Apple", 1.50))

        assert self.cart.remove_item("Apple") is True
        assert self.cart.is_empty()

    def test_remove_nonexistent_item(self):
        """Test removing an item that doesn't exist returns False."""
        self.cart.add_item(Item("Apple", 1.50))

        assert self.cart.remove_item("Banana") is False
        assert len(self.cart.items) == 1

    def test_remove_from_empty_cart(self):
        """Test removing from empty cart returns False."""
        assert self.cart.remove_item("Apple") is False

    def test_remove_item_not_first(self):
        """Test removing an item located after other items keeps the rest."""
        self.cart.add_item(Item("Apple", 1.50))
        self.cart.add_item(Item("Banana", 0.50))

        assert self.cart.remove_item("Banana") is True
        assert [item.name for item in self.cart.items] == ["Apple"]

    # get_subtotal
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

    # apply_discount
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
        self.cart.add_item(Item("Apple", 10.00, 2))
        self.cart.apply_discount(100)

        assert self.cart.get_total() == pytest.approx(0)

    def test_apply_negative_discount_raises_error(self):
        """Test that negative discount raises ValueError."""
        with pytest.raises(ValueError, match="between 0 and 100"):
            self.cart.apply_discount(-1)

    def test_apply_over_100_discount_raises_error(self):
        """Test that discount over 100 raises ValueError."""
        with pytest.raises(ValueError, match="between 0 and 100"):
            self.cart.apply_discount(101)

    def test_invalid_discount_keeps_previous_value(self):
        """Test that a rejected discount does not change the current one."""
        self.cart.apply_discount(10)
        with pytest.raises(ValueError):
            self.cart.apply_discount(150)

        assert self.cart.discount_percent == 10

    # get_total
    def test_total_with_discount(self):
        """Test total calculation with discount applied."""
        self.cart.add_item(Item("Apple", 10.00, 5))
        self.cart.add_item(Item("Banana", 5.00, 4))
        self.cart.apply_discount(20)

        assert self.cart.get_total() == pytest.approx(56.00)

    def test_total_without_discount(self):
        """Test that total equals subtotal when no discount."""
        self.cart.add_item(Item("Apple", 10.00, 5))

        assert self.cart.get_total() == pytest.approx(self.cart.get_subtotal())

    # clear
    def test_clear_cart(self):
        """Test that clear removes all items and resets discount."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.apply_discount(15)
        self.cart.clear()

        assert self.cart.is_empty()
        assert self.cart.discount_percent == 0

    def test_clear_empty_cart(self):
        """Test that clearing empty cart doesn't cause errors."""
        self.cart.clear()

        assert self.cart.is_empty()

    # get_item_count
    def test_item_count_multiple_items(self):
        """Test item count sums all quantities."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.50, 3))

        assert self.cart.get_item_count() == 5

    # is_empty
    def test_is_empty_after_adding_and_removing(self):
        """Test is_empty after adding and removing all items."""
        self.cart.add_item(Item("Apple", 1.50))
        self.cart.remove_item("Apple")

        assert self.cart.is_empty()
