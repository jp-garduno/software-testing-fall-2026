import pytest
from shopping_cart import Item, ShoppingCart

class TestItem:
    """Test suite for Item class."""

    def test_item_creation_valid(self):
        item = Item("Apple", 1.50, 3)
        assert item.name == "Apple"
        assert item.price == 1.50
        assert item.quantity == 3

    def test_item_default_quantity(self):
        item = Item("Banana", 2.00)
        assert item.quantity == 1

    def test_item_negative_price_raises_error(self):
        with pytest.raises(ValueError, match="Price must be positive"):
            Item("Apple", -1.0)

    def test_item_zero_price_raises_error(self):
        with pytest.raises(ValueError, match="Price must be positive"):
            Item("Apple", 0)

    def test_item_negative_quantity_raises_error(self):
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item("Apple", 1.50, -2)

    def test_item_zero_quantity_raises_error(self):
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item("Apple", 1.50, 0)

    def test_get_total_single_quantity(self):
        item = Item("Banana", 2.50)
        assert item.get_total() == 2.50

    def test_get_total_multiple_quantity(self):
        item = Item("Apple", 1.50, 4)
        assert item.get_total() == 6.00

    def test_item_equality(self):
        item1 = Item("Apple", 1.50, 3)
        item2 = Item("Apple", 2.00, 1) # Igualdad solo se basa en el nombre
        assert item1 == item2

    def test_item_inequality(self):
        item1 = Item("Apple", 1.50, 3)
        item2 = Item("Banana", 1.50, 3)
        assert item1 != item2

    def test_item_equality_different_type(self):
        """Branch coverage for isinstance check."""
        item1 = Item("Apple", 1.50, 3)
        assert item1 != "Apple"

    def test_item_representation(self):
        item = Item("Apple", 1.50, 3)
        assert repr(item) == "Item('Apple', $1.5, qty=3)"


class TestShoppingCart:
    """Test suite for ShoppingCart class."""

    def setup_method(self):
        self.cart = ShoppingCart()

    def test_cart_starts_empty(self):
        assert self.cart.is_empty()
        assert self.cart.get_item_count() == 0
        assert self.cart.get_total() == 0

    def test_add_single_item(self):
        item = Item("Apple", 1.50, 2)
        self.cart.add_item(item)
        assert not self.cart.is_empty()
        assert self.cart.get_item_count() == 2
        assert self.cart.get_subtotal() == pytest.approx(3.00)

    def test_add_multiple_different_items(self):
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.50, 4))
        assert self.cart.get_item_count() == 6
        assert self.cart.get_subtotal() == pytest.approx(5.00)

    def test_add_duplicate_item_increases_quantity(self):
        item1 = Item("Apple", 1.50, 2)
        item2 = Item("Apple", 1.50, 3)
        self.cart.add_item(item1)
        self.cart.add_item(item2)
        assert len(self.cart.items) == 1
        assert self.cart.items[0].quantity == 5
        assert self.cart.get_item_count() == 5

    def test_remove_existing_item(self):
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Banana", 0.50, 4))
        result = self.cart.remove_item("Apple")
        assert result is True
        assert self.cart.get_item_count() == 4
        assert len(self.cart.items) == 1

    def test_remove_nonexistent_item(self):
        self.cart.add_item(Item("Apple", 1.50, 2))
        result = self.cart.remove_item("Banana")
        assert result is False
        assert self.cart.get_item_count() == 2

    def test_remove_from_empty_cart(self):
        result = self.cart.remove_item("Apple")
        assert result is False

    def test_subtotal_empty_cart(self):
        assert self.cart.get_subtotal() == 0

    def test_apply_valid_discount(self):
        self.cart.apply_discount(20)
        assert self.cart.discount_percent == 20

    def test_apply_zero_discount(self):
        self.cart.apply_discount(0)
        assert self.cart.discount_percent == 0

    def test_apply_full_discount(self):
        self.cart.apply_discount(100)
        assert self.cart.discount_percent == 100

    def test_apply_negative_discount_raises_error(self):
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            self.cart.apply_discount(-5)

    def test_apply_over_100_discount_raises_error(self):
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            self.cart.apply_discount(105)

    def test_total_with_discount(self):
        self.cart.add_item(Item("Apple", 10.00, 5))
        self.cart.add_item(Item("Banana", 5.00, 4))
        self.cart.apply_discount(20)
        assert self.cart.get_total() == pytest.approx(56.00)

    def test_total_without_discount(self):
        self.cart.add_item(Item("Apple", 10.00, 5))
        assert self.cart.get_total() == pytest.approx(50.00)

    def test_clear_cart(self):
        self.cart.add_item(Item("Apple", 10.00, 5))
        self.cart.apply_discount(20)
        self.cart.clear()
        assert self.cart.is_empty()
        assert self.cart.discount_percent == 0

    def test_clear_empty_cart(self):
        self.cart.clear()
        assert self.cart.is_empty()

    def test_is_empty_after_adding_and_removing(self):
        self.cart.add_item(Item("Apple", 1.50, 2))
        assert not self.cart.is_empty()
        self.cart.remove_item("Apple")
        assert self.cart.is_empty()