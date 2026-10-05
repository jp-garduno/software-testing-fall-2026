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
        name = "Apple"
        price = 1.50
        expected_quantity = 1
        item = Item(name, price)
        assert item.quantity == expected_quantity

    def test_item_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        name = "Apple"
        price = -1.50
        with pytest.raises(ValueError, match="Price must be positive"):
            Item(name, price)

    def test_item_zero_price_raises_error(self):
        """Test that zero price raises ValueError."""
        name = "Apple"
        price = 0
        with pytest.raises(ValueError, match="Price must be positive"):
            Item(name, price)

    def test_item_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        name = "Apple"
        price = 1.50
        quantity = -1
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item(name, price, quantity)

    def test_item_zero_quantity_raises_error(self):
        """Test that zero quantity raises ValueError."""
        name = "Apple"
        price = 1.50
        quantity = 0
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item(name, price, quantity)

    def test_get_total_single_quantity(self):
        """Test total calculation for single item."""
        item = Item("Apple", 1.50)
        expected_total = 1.50
        total = item.get_total()
        assert total == pytest.approx(expected_total)

    def test_get_total_multiple_quantity(self):
        """Test total calculation for multiple items."""
        item = Item("Apple", 1.50, 3)
        expected_total = 4.50
        total = item.get_total()
        assert total == pytest.approx(expected_total)

    def test_item_equality(self):
        """Test that items with same name are equal."""
        first_item = Item("Apple", 1.50)
        second_item = Item("Apple", 2.00)
        are_equal = first_item == second_item
        assert are_equal is True

    def test_item_inequality(self):
        """Test that items with different names are not equal."""
        first_item = Item("Apple", 1.50)
        second_item = Item("Banana", 1.50)
        are_equal = first_item == second_item
        assert are_equal is False

    def test_item_inequality_with_non_item(self):
        """Test that an item is not equal to an object of another type."""
        item = Item("Apple", 1.50)
        other = "Apple"
        are_equal = item == other
        assert are_equal is False

    def test_item_representation(self):
        """Test the string representation of an item."""
        item = Item("Apple", 1.50, 2)
        expected_representation = "Item('Apple', $1.5, qty=2)"
        representation = repr(item)
        assert representation == expected_representation


class TestShoppingCart:  # pylint: disable=attribute-defined-outside-init,too-many-public-methods
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
        item = Item("Apple", 1.50, 2)
        self.cart.add_item(item)
        assert not self.cart.is_empty()
        assert self.cart.get_item_count() == 2
        assert self.cart.get_subtotal() == pytest.approx(3.00)

    def test_add_multiple_different_items(self):
        """Test adding different items to cart."""
        apple = Item("Apple", 1.50, 2)
        banana = Item("Banana", 2.00, 3)
        self.cart.add_item(apple)
        self.cart.add_item(banana)
        assert len(self.cart.items) == 2
        assert self.cart.get_item_count() == 5
        assert self.cart.get_subtotal() == pytest.approx(9.00)

    def test_add_duplicate_item_increases_quantity(self):
        """Test that adding duplicate item increases quantity instead of creating new entry."""
        first_item = Item("Apple", 1.50, 2)
        second_item = Item("Apple", 1.50, 3)
        self.cart.add_item(first_item)
        self.cart.add_item(second_item)
        assert len(self.cart.items) == 1
        assert self.cart.items[0].quantity == 5
        assert self.cart.get_item_count() == 5

    # Test remove_item
    def test_remove_existing_item(self):
        """Test removing an item that exists in cart."""
        item = Item("Apple", 1.50)
        self.cart.add_item(item)
        was_removed = self.cart.remove_item("Apple")
        assert was_removed is True
        assert self.cart.is_empty()

    def test_remove_nonexistent_item(self):
        """Test removing an item that doesn't exist returns False."""
        item = Item("Apple", 1.50)
        self.cart.add_item(item)
        was_removed = self.cart.remove_item("Banana")
        assert was_removed is False
        assert self.cart.items == [item]

    def test_remove_from_empty_cart(self):
        """Test removing from empty cart returns False."""
        item_name = "Apple"
        was_removed = self.cart.remove_item(item_name)
        assert was_removed is False
        assert self.cart.is_empty()

    # Test get_subtotal
    def test_subtotal_single_item(self):
        """Test subtotal with one item."""
        item = Item("Apple", 1.50, 3)
        self.cart.add_item(item)
        expected_subtotal = 4.50
        subtotal = self.cart.get_subtotal()
        assert subtotal == pytest.approx(expected_subtotal)

    def test_subtotal_multiple_items(self):
        """Test subtotal with multiple items."""
        apple = Item("Apple", 1.50, 2)
        banana = Item("Banana", 2.00, 3)
        self.cart.add_item(apple)
        self.cart.add_item(banana)
        expected_subtotal = 9.00
        subtotal = self.cart.get_subtotal()
        assert subtotal == pytest.approx(expected_subtotal)

    def test_subtotal_empty_cart(self):
        """Test subtotal of empty cart is zero."""
        expected_subtotal = 0
        subtotal = self.cart.get_subtotal()
        assert subtotal == expected_subtotal

    # Test apply_discount
    def test_apply_valid_discount(self):
        """Test applying a valid discount percentage."""
        item = Item("Apple", 10.00)
        discount_percent = 25
        self.cart.add_item(item)
        self.cart.apply_discount(discount_percent)
        assert self.cart.discount_percent == discount_percent
        assert self.cart.get_total() == pytest.approx(7.50)

    def test_apply_zero_discount(self):
        """Test applying 0% discount."""
        item = Item("Apple", 10.00)
        discount_percent = 0
        self.cart.add_item(item)
        self.cart.apply_discount(discount_percent)
        assert self.cart.get_total() == pytest.approx(10.00)

    def test_apply_full_discount(self):
        """Test applying 100% discount."""
        item = Item("Apple", 10.00)
        discount_percent = 100
        self.cart.add_item(item)
        self.cart.apply_discount(discount_percent)
        assert self.cart.get_total() == pytest.approx(0)

    def test_apply_negative_discount_raises_error(self):
        """Test that negative discount raises ValueError."""
        discount_percent = -1
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            self.cart.apply_discount(discount_percent)

    def test_apply_over_100_discount_raises_error(self):
        """Test that discount over 100 raises ValueError."""
        discount_percent = 101
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            self.cart.apply_discount(discount_percent)

    # Test get_total with discount
    def test_total_with_discount(self):
        """Test total calculation with discount applied."""
        first_item = Item("Apple", 10.00, 5)
        second_item = Item("Banana", 5.00, 10)
        discount_percent = 20
        self.cart.add_item(first_item)
        self.cart.add_item(second_item)
        self.cart.apply_discount(discount_percent)
        expected_total = 80.00
        total = self.cart.get_total()
        assert total == pytest.approx(expected_total)

    def test_total_without_discount(self):
        """Test that total equals subtotal when no discount."""
        item = Item("Apple", 10.00, 2)
        self.cart.add_item(item)
        total = self.cart.get_total()
        assert total == pytest.approx(self.cart.get_subtotal())

    # Test clear
    def test_clear_cart(self):
        """Test that clear removes all items and resets discount."""
        item = Item("Apple", 10.00, 2)
        self.cart.add_item(item)
        self.cart.apply_discount(20)
        self.cart.clear()
        assert self.cart.is_empty()
        assert self.cart.get_item_count() == 0
        assert self.cart.discount_percent == 0
        assert self.cart.get_total() == 0

    def test_clear_empty_cart(self):
        """Test that clearing empty cart doesn't cause errors."""
        self.cart.clear()
        assert self.cart.is_empty()
        assert self.cart.discount_percent == 0

    # Test get_item_count
    def test_item_count_multiple_items(self):
        """Test item count sums all quantities."""
        apple = Item("Apple", 1.50, 2)
        banana = Item("Banana", 2.00, 3)
        self.cart.add_item(apple)
        self.cart.add_item(banana)
        expected_count = 5
        item_count = self.cart.get_item_count()
        assert item_count == expected_count

    # Test is_empty
    def test_is_empty_after_adding_and_removing(self):
        """Test is_empty after adding and removing all items."""
        item = Item("Apple", 1.50)
        self.cart.add_item(item)
        self.cart.remove_item("Apple")
        is_empty = self.cart.is_empty()
        assert is_empty is True
