"""Reference test suite for Exercise 2: Shopping Cart Class Testing (Module 05 - White Box Testing)."""

# pylint: disable=attribute-defined-outside-init,too-many-public-methods
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
            Item("Apple", -1.50)

    def test_item_zero_price_raises_error(self):
        """Test that zero price raises ValueError (boundary value)."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Item("Apple", 0)

    def test_item_smallest_positive_price_is_valid(self):
        """Test the boundary just above zero for price."""
        item = Item("Gum", 0.01)
        assert item.price == 0.01

    def test_item_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item("Apple", 1.50, -1)

    def test_item_zero_quantity_raises_error(self):
        """Test that zero quantity raises ValueError (boundary value)."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item("Apple", 1.50, 0)

    def test_item_invalid_price_checked_before_quantity(self):
        """Test that price is validated first when both values are invalid."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Item("Apple", 0, 0)

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
        assert Item("Apple", 1.50, 1) == Item("Apple", 2.00, 5)

    def test_item_inequality(self):
        """Test that items with different names are not equal."""
        assert Item("Apple", 1.50) != Item("Banana", 1.50)

    def test_item_not_equal_to_non_item(self):
        """Test the isinstance branch of __eq__: comparing with a non-Item returns False."""
        assert Item("Apple", 1.50) != "Apple"

    def test_item_repr(self):
        """Test the string representation of an item."""
        assert repr(Item("Apple", 1.5, 3)) == "Item('Apple', $1.5, qty=3)"


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

    def test_carts_do_not_share_items(self):
        """Test that each cart has its own item list (no shared mutable state)."""
        other_cart = ShoppingCart()
        self.cart.add_item(Item("Apple", 1.50))
        assert other_cart.is_empty()

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
        self.cart.add_item(Item("Apple", 1.50))
        self.cart.add_item(Item("Banana", 0.50))

        assert len(self.cart.items) == 2
        assert [item.name for item in self.cart.items] == ["Apple", "Banana"]

    def test_add_duplicate_item_increases_quantity(self):
        """Test that adding duplicate item increases quantity instead of creating new entry."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Apple", 1.50, 3))

        # Should have only 1 unique item with combined quantity
        assert len(self.cart.items) == 1
        assert self.cart.items[0].quantity == 5
        assert self.cart.get_item_count() == 5

    def test_add_duplicate_after_other_items_skips_non_matching(self):
        """Test the loop's False branch: non-matching items are skipped before the duplicate is found."""
        self.cart.add_item(Item("Apple", 1.50))
        self.cart.add_item(Item("Banana", 0.50))
        self.cart.add_item(Item("Banana", 0.50, 2))

        assert len(self.cart.items) == 2
        assert self.cart.items[0].quantity == 1
        assert self.cart.items[1].quantity == 3

    def test_add_duplicate_keeps_original_price(self):
        """Test that a duplicate with a different price keeps the price of the first item added."""
        self.cart.add_item(Item("Apple", 1.00, 1))
        self.cart.add_item(Item("Apple", 5.00, 1))

        assert self.cart.get_subtotal() == pytest.approx(2.00)

    # Test remove_item
    def test_remove_existing_item(self):
        """Test removing an item that exists in cart."""
        self.cart.add_item(Item("Apple", 1.50))

        assert self.cart.remove_item("Apple") is True
        assert self.cart.is_empty()

    def test_remove_item_after_non_matching_items(self):
        """Test removing an item that is not first, leaving the others untouched."""
        self.cart.add_item(Item("Apple", 1.50))
        self.cart.add_item(Item("Banana", 0.50))
        self.cart.add_item(Item("Cherry", 3.00))

        assert self.cart.remove_item("Banana") is True
        assert [item.name for item in self.cart.items] == ["Apple", "Cherry"]

    def test_remove_nonexistent_item(self):
        """Test removing an item that doesn't exist returns False."""
        self.cart.add_item(Item("Apple", 1.50))

        assert self.cart.remove_item("Banana") is False
        assert len(self.cart.items) == 1

    def test_remove_from_empty_cart(self):
        """Test removing from empty cart returns False."""
        assert self.cart.remove_item("Apple") is False

    def test_remove_same_item_twice(self):
        """Test that the second removal of the same item returns False."""
        self.cart.add_item(Item("Apple", 1.50))
        self.cart.remove_item("Apple")

        assert self.cart.remove_item("Apple") is False

    # Test get_subtotal
    def test_subtotal_single_item(self):
        """Test subtotal with one item."""
        self.cart.add_item(Item("Apple", 2.50, 2))
        assert self.cart.get_subtotal() == pytest.approx(5.00)

    def test_subtotal_multiple_items(self):
        """Test subtotal with multiple items."""
        self.cart.add_item(Item("Apple", 10.00, 5))
        self.cart.add_item(Item("Banana", 5.00, 4))
        assert self.cart.get_subtotal() == pytest.approx(70.00)

    def test_subtotal_empty_cart(self):
        """Test subtotal of empty cart is zero."""
        assert self.cart.get_subtotal() == 0

    def test_subtotal_ignores_discount(self):
        """Test that subtotal is calculated before discount."""
        self.cart.add_item(Item("Apple", 10.00, 10))
        self.cart.apply_discount(50)
        assert self.cart.get_subtotal() == pytest.approx(100.00)

    # Test apply_discount
    def test_apply_valid_discount(self):
        """Test applying a valid discount percentage."""
        self.cart.apply_discount(25)
        assert self.cart.discount_percent == 25

    def test_apply_zero_discount(self):
        """Test applying 0% discount (lower boundary)."""
        self.cart.apply_discount(0)
        assert self.cart.discount_percent == 0

    def test_apply_full_discount(self):
        """Test applying 100% discount (upper boundary)."""
        self.cart.add_item(Item("Apple", 10.00))
        self.cart.apply_discount(100)

        assert self.cart.discount_percent == 100
        assert self.cart.get_total() == pytest.approx(0.00)

    def test_apply_negative_discount_raises_error(self):
        """Test that negative discount raises ValueError (first condition of the OR)."""
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            self.cart.apply_discount(-1)

    def test_apply_over_100_discount_raises_error(self):
        """Test that discount over 100 raises ValueError (second condition of the OR)."""
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            self.cart.apply_discount(101)

    def test_invalid_discount_keeps_previous_discount(self):
        """Test that a rejected discount does not change the current discount."""
        self.cart.apply_discount(10)
        with pytest.raises(ValueError):
            self.cart.apply_discount(150)
        assert self.cart.discount_percent == 10

    def test_apply_discount_replaces_previous_discount(self):
        """Test that discounts are not cumulative: the last one wins."""
        self.cart.apply_discount(10)
        self.cart.apply_discount(30)
        assert self.cart.discount_percent == 30

    # Test get_total with discount
    def test_total_with_discount(self):
        """Test total calculation with discount applied."""
        self.cart.add_item(Item("Apple", 10.00, 5))
        self.cart.add_item(Item("Banana", 5.00, 4))
        # Subtotal: 50 + 20 = 70

        self.cart.apply_discount(20)

        # 70 - (70 * 0.20) = 70 - 14 = 56
        assert self.cart.get_total() == pytest.approx(56.00)

    def test_total_without_discount(self):
        """Test that total equals subtotal when no discount."""
        self.cart.add_item(Item("Apple", 10.00, 3))
        assert self.cart.get_total() == pytest.approx(self.cart.get_subtotal())

    def test_total_with_fractional_discount(self):
        """Test a non-integer discount percentage."""
        self.cart.add_item(Item("Apple", 100.00))
        self.cart.apply_discount(12.5)
        assert self.cart.get_total() == pytest.approx(87.50)

    def test_total_empty_cart_with_discount(self):
        """Test that a discount on an empty cart still yields zero."""
        self.cart.apply_discount(50)
        assert self.cart.get_total() == 0

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

    def test_cart_is_reusable_after_clear(self):
        """Test that items can be added again after clearing."""
        self.cart.add_item(Item("Apple", 1.50))
        self.cart.clear()
        self.cart.add_item(Item("Banana", 0.50, 2))

        assert self.cart.get_item_count() == 2
        assert self.cart.get_total() == pytest.approx(1.00)

    # Test get_item_count
    def test_item_count_multiple_items(self):
        """Test item count sums all quantities."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.50, 3))
        assert self.cart.get_item_count() == 5

    def test_item_count_after_removal(self):
        """Test item count drops by the full quantity of the removed item."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.50, 3))
        self.cart.remove_item("Banana")
        assert self.cart.get_item_count() == 2

    # Test is_empty
    def test_is_empty_after_adding_and_removing(self):
        """Test is_empty after adding and removing all items."""
        self.cart.add_item(Item("Apple", 1.50))
        self.cart.add_item(Item("Banana", 0.50))
        assert not self.cart.is_empty()

        self.cart.remove_item("Apple")
        self.cart.remove_item("Banana")
        assert self.cart.is_empty()
