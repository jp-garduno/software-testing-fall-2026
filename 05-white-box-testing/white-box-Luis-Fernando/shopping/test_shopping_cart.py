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
        with pytest.raises(ValueError, match="^Price must be positive$"):
            Item("Apple", -1.50)

    def test_item_zero_price_raises_error(self):
        """Test that zero price raises ValueError."""
        with pytest.raises(ValueError, match="^Price must be positive$"):
            Item("Apple", 0)

    def test_item_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        with pytest.raises(ValueError, match="^Quantity must be positive$"):
            Item("Apple", 1.50, -1)

    def test_item_zero_quantity_raises_error(self):
        """Test that zero quantity raises ValueError."""
        with pytest.raises(ValueError, match="^Quantity must be positive$"):
            Item("Apple", 1.50, 0)

    def test_get_total_single_quantity(self):
        """Test total calculation for single item."""
        item = Item("Apple", 1.50, 1)
        assert item.get_total() == pytest.approx(1.50)

    def test_get_total_multiple_quantity(self):
        """Test total calculation for multiple items."""
        item = Item("Apple", 0.10, 3)
        assert item.get_total() == pytest.approx(0.30)

    def test_item_equality(self):
        """Test that items with same name are equal."""
        assert Item("Apple", 1.50, 2) == Item("Apple", 2.00, 3)

    def test_item_inequality(self):
        """Test that items with different names are not equal."""
        assert Item("Apple", 1.50, 2) != Item("Banana", 1.50, 2)

    def test_item_inequality_with_other_type(self):
        """Test that an item is not equal to a non-Item object."""
        assert Item("Apple", 1.50) != "Apple"

    def test_item_repr(self):
        """Test that the representation includes name, price, and quantity."""
        assert repr(Item("Apple", 1.50, 3)) == "Item('Apple', $1.5, qty=3)"


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
        assert self.cart.items == []
        assert self.cart.discount_percent == 0

    # Test add_item
    def test_add_single_item(self):
        """Test adding a single item to cart."""
        item = Item("Apple", 1.50, 2)
        self.cart.add_item(item)

        assert len(self.cart.items) == 1
        assert self.cart.items[0] is item
        assert not self.cart.is_empty()
        assert self.cart.get_item_count() == 2
        assert self.cart.get_subtotal() == pytest.approx(3.00)

    def test_add_multiple_different_items(self):
        """Test adding different items to cart."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.75, 3))

        assert [item.name for item in self.cart.items] == ["Apple", "Banana"]
        assert [item.quantity for item in self.cart.items] == [2, 3]
        assert self.cart.get_item_count() == 5
        assert self.cart.get_subtotal() == pytest.approx(5.25)

    def test_add_duplicate_item_increases_quantity(self):
        """Test that adding duplicate item increases quantity instead of creating new entry."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Apple", 1.50, 3))

        assert len(self.cart.items) == 1
        assert self.cart.items[0].name == "Apple"
        assert self.cart.items[0].quantity == 5
        assert self.cart.get_item_count() == 5
        assert self.cart.get_subtotal() == pytest.approx(7.50)

    # Test remove_item
    def test_remove_existing_item(self):
        """Test removing an item that exists in cart."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.75, 3))

        assert self.cart.remove_item("Banana") is True
        assert [item.name for item in self.cart.items] == ["Apple"]
        assert self.cart.get_item_count() == 2
        assert self.cart.get_subtotal() == pytest.approx(3.00)

    def test_remove_nonexistent_item(self):
        """Test removing an item that doesn't exist returns False."""
        self.cart.add_item(Item("Apple", 1.50, 2))

        assert self.cart.remove_item("Banana") is False
        assert [item.name for item in self.cart.items] == ["Apple"]
        assert self.cart.get_item_count() == 2
        assert self.cart.get_subtotal() == pytest.approx(3.00)

    def test_remove_from_empty_cart(self):
        """Test removing from empty cart returns False."""
        assert self.cart.remove_item("Apple") is False
        assert self.cart.is_empty()
        assert self.cart.get_item_count() == 0

    # Test get_subtotal
    def test_subtotal_single_item(self):
        """Test subtotal with one item."""
        self.cart.add_item(Item("Apple", 1.50, 3))
        assert self.cart.get_subtotal() == pytest.approx(4.50)

    def test_subtotal_multiple_items(self):
        """Test subtotal with multiple items."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.75, 3))
        self.cart.apply_discount(20)

        assert self.cart.get_subtotal() == pytest.approx(5.25)

    def test_subtotal_empty_cart(self):
        """Test subtotal of empty cart is zero."""
        assert self.cart.get_subtotal() == 0

    # Test apply_discount
    def test_apply_valid_discount(self):
        """Test applying a valid discount percentage."""
        self.cart.add_item(Item("Apple", 10.00, 2))
        self.cart.apply_discount(12.5)

        assert self.cart.discount_percent == 12.5
        assert self.cart.get_total() == pytest.approx(17.50)

    def test_apply_zero_discount(self):
        """Test applying 0% discount."""
        self.cart.add_item(Item("Apple", 10.00, 2))
        self.cart.apply_discount(20)
        self.cart.apply_discount(0)

        assert self.cart.discount_percent == 0
        assert self.cart.get_total() == pytest.approx(20.00)

    def test_apply_full_discount(self):
        """Test applying 100% discount."""
        self.cart.add_item(Item("Apple", 10.00, 2))
        self.cart.apply_discount(100)

        assert self.cart.discount_percent == 100
        assert self.cart.get_total() == pytest.approx(0.00)

    def test_apply_negative_discount_raises_error(self):
        """Test that negative discount raises ValueError."""
        self.cart.apply_discount(20)

        with pytest.raises(ValueError, match="^Discount must be between 0 and 100$"):
            self.cart.apply_discount(-1)

        assert self.cart.discount_percent == 20

    def test_apply_over_100_discount_raises_error(self):
        """Test that discount over 100 raises ValueError."""
        self.cart.apply_discount(20)

        with pytest.raises(ValueError, match="^Discount must be between 0 and 100$"):
            self.cart.apply_discount(101)

        assert self.cart.discount_percent == 20

    # Test get_total with discount
    def test_total_with_discount(self):
        """Test total calculation with discount applied."""
        self.cart.add_item(Item("Apple", 10.00, 5))
        self.cart.add_item(Item("Banana", 5.00, 10))
        self.cart.apply_discount(20)

        assert self.cart.get_subtotal() == pytest.approx(100.00)
        assert self.cart.get_total() == pytest.approx(80.00)

    def test_total_without_discount(self):
        """Test that total equals subtotal when no discount."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.75, 3))

        assert self.cart.get_total() == pytest.approx(5.25)
        assert self.cart.get_total() == pytest.approx(self.cart.get_subtotal())

    # Test clear
    def test_clear_cart(self):
        """Test that clear removes all items and resets discount."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.75, 3))
        self.cart.apply_discount(20)

        self.cart.clear()

        assert self.cart.items == []
        assert self.cart.is_empty()
        assert self.cart.get_item_count() == 0
        assert self.cart.get_subtotal() == 0
        assert self.cart.get_total() == 0
        assert self.cart.discount_percent == 0

    def test_clear_empty_cart(self):
        """Test that clearing empty cart doesn't cause errors."""
        self.cart.clear()

        assert self.cart.items == []
        assert self.cart.is_empty()
        assert self.cart.get_item_count() == 0
        assert self.cart.get_total() == 0
        assert self.cart.discount_percent == 0

    # Test get_item_count
    def test_item_count_multiple_items(self):
        """Test item count sums all quantities."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.75, 3))

        assert self.cart.get_item_count() == 5

    # Test is_empty
    def test_is_empty_after_adding_and_removing(self):
        """Test is_empty after adding and removing all items."""
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.75, 3))
        assert not self.cart.is_empty()

        assert self.cart.remove_item("Apple") is True
        assert not self.cart.is_empty()

        assert self.cart.remove_item("Banana") is True
        assert self.cart.is_empty()
        assert self.cart.get_item_count() == 0
        assert self.cart.get_total() == 0
