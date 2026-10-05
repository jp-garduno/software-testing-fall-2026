"""Unit and branch tests for the shopping cart exercise."""

import pytest

from shopping_cart import Item, ShoppingCart


class TestItem:
    """Test suite for Item class."""

    def test_item_creation_valid(self):
        """Create an item with valid parameters."""
        item = Item("Apple", 1.50, 3)
        assert (item.name, item.price, item.quantity) == ("Apple", 1.50, 3)

    def test_item_default_quantity(self):
        """An item defaults to one unit."""
        assert Item("Apple", 1.50).quantity == 1

    @pytest.mark.parametrize("price", [-1, 0])
    def test_item_nonpositive_price_raises_error(self, price):
        """Reject negative and zero prices."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Item("Apple", price)

    @pytest.mark.parametrize("quantity", [-1, 0])
    def test_item_nonpositive_quantity_raises_error(self, quantity):
        """Reject negative and zero quantities."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item("Apple", 1.50, quantity)

    def test_get_total_single_quantity(self):
        """Calculate an item total for one unit."""
        assert Item("Apple", 1.50).get_total() == pytest.approx(1.50)

    def test_get_total_multiple_quantity(self):
        """Calculate an item total for several units."""
        assert Item("Apple", 1.50, 4).get_total() == pytest.approx(6.00)

    def test_item_equality(self):
        """Items with the same name are equal."""
        assert Item("Apple", 1.00) == Item("Apple", 2.00, 4)

    def test_item_inequality(self):
        """Items with different names are not equal."""
        assert Item("Apple", 1.00) != Item("Banana", 1.00)

    def test_item_is_not_equal_to_a_non_item(self):
        """Comparison with a different type returns False."""
        assert Item("Apple", 1.00) != "Apple"

    def test_item_representation(self):
        """The representation includes its public fields."""
        assert repr(Item("Apple", 1.50, 2)) == "Item('Apple', $1.5, qty=2)"


class TestShoppingCart:
    """Test suite for ShoppingCart class."""

    def setup_method(self):
        """Create a fresh cart before each test."""
        self.cart = ShoppingCart()

    def test_cart_starts_empty(self):
        """A new cart has no entries, count, or total."""
        assert self.cart.is_empty()
        assert self.cart.get_item_count() == 0
        assert self.cart.get_total() == 0

    def test_add_single_item(self):
        """Adding one item changes the cart state."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        assert not self.cart.is_empty()
        assert self.cart.get_item_count() == 2
        assert self.cart.get_subtotal() == pytest.approx(3.00)

    def test_add_multiple_different_items(self):
        """Different items remain distinct cart entries."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 2.00, 3))
        assert len(self.cart.items) == 2
        assert self.cart.get_subtotal() == pytest.approx(9.00)

    def test_add_duplicate_item_increases_quantity(self):
        """Duplicate names increase quantity instead of making another entry."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Apple", 9.99, 3))
        assert len(self.cart.items) == 1
        assert self.cart.items[0].quantity == 5
        assert self.cart.get_item_count() == 5

    def test_remove_existing_item(self):
        """Removing an item returns True and changes the cart."""
        self.cart.add_item(Item("Apple", 1.50))
        assert self.cart.remove_item("Apple") is True
        assert self.cart.is_empty()

    def test_remove_nonexistent_item(self):
        """Removing an absent item returns False."""
        self.cart.add_item(Item("Apple", 1.50))
        assert self.cart.remove_item("Banana") is False
        assert self.cart.get_item_count() == 1

    def test_remove_from_empty_cart(self):
        """Removing from an empty cart returns False."""
        assert self.cart.remove_item("Apple") is False

    def test_subtotal_single_item(self):
        """Subtotal is the total of a single entry."""
        self.cart.add_item(Item("Apple", 2.25, 2))
        assert self.cart.get_subtotal() == pytest.approx(4.50)

    def test_subtotal_multiple_items(self):
        """Subtotal sums all cart entries."""
        self.cart.add_item(Item("Apple", 2.00, 2))
        self.cart.add_item(Item("Banana", 3.00, 1))
        assert self.cart.get_subtotal() == pytest.approx(7.00)

    def test_subtotal_empty_cart(self):
        """An empty cart subtotal is zero."""
        assert self.cart.get_subtotal() == 0

    @pytest.mark.parametrize("discount", [0, 20, 100])
    def test_apply_valid_discount(self, discount):
        """Discount boundaries and a typical value are accepted."""
        self.cart.apply_discount(discount)
        assert self.cart.discount_percent == discount

    @pytest.mark.parametrize("discount", [-1, 101])
    def test_apply_invalid_discount_raises_error(self, discount):
        """Discounts outside the inclusive range are rejected."""
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            self.cart.apply_discount(discount)

    def test_total_with_discount(self):
        """Calculate the total after a percentage discount."""
        self.cart.add_item(Item("Apple", 10.00, 5))
        self.cart.add_item(Item("Banana", 5.00, 4))
        self.cart.apply_discount(20)
        assert self.cart.get_total() == pytest.approx(56.00)

    def test_total_without_discount(self):
        """Total equals subtotal before a discount is applied."""
        self.cart.add_item(Item("Apple", 10.00, 2))
        assert self.cart.get_total() == pytest.approx(self.cart.get_subtotal())

    def test_clear_cart(self):
        """Clear removes entries and resets the discount."""
        self.cart.add_item(Item("Apple", 2.00, 2))
        self.cart.apply_discount(25)
        self.cart.clear()
        assert self.cart.is_empty()
        assert self.cart.discount_percent == 0

    def test_clear_empty_cart(self):
        """Clearing an empty cart remains safe and idempotent."""
        self.cart.clear()
        assert self.cart.is_empty()
        assert self.cart.discount_percent == 0

    def test_item_count_multiple_items(self):
        """Item count sums the quantities of all entries."""
        self.cart.add_item(Item("Apple", 1.00, 2))
        self.cart.add_item(Item("Banana", 1.00, 3))
        assert self.cart.get_item_count() == 5

    def test_is_empty_after_adding_and_removing(self):
        """The cart is empty again after its only item is removed."""
        self.cart.add_item(Item("Apple", 1.00))
        self.cart.remove_item("Apple")
        assert self.cart.is_empty()
