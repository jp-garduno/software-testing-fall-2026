"""Class and branch tests for the shopping-cart exercise."""

import pytest

from shopping_cart import Item, ShoppingCart


class TestItem:
    """Test validation and behavior of individual items."""

    def test_item_creation_valid(self):
        item = Item("Apple", 1.50, 3)

        assert item.name == "Apple"
        assert item.price == pytest.approx(1.50)
        assert item.quantity == 3

    def test_item_default_quantity(self):
        assert Item("Apple", 1.50).quantity == 1

    @pytest.mark.parametrize("price", [-1, 0])
    def test_non_positive_price_raises_error(self, price):
        with pytest.raises(ValueError, match="Price must be positive"):
            Item("Apple", price)

    @pytest.mark.parametrize("quantity", [-1, 0])
    def test_non_positive_quantity_raises_error(self, quantity):
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Item("Apple", 1.50, quantity)

    def test_get_total_for_single_quantity(self):
        assert Item("Apple", 1.50).get_total() == pytest.approx(1.50)

    def test_get_total_for_multiple_quantity(self):
        assert Item("Apple", 1.50, 3).get_total() == pytest.approx(4.50)

    def test_items_with_same_name_are_equal(self):
        assert Item("Apple", 1.50) == Item("Apple", 2.00, 4)

    def test_items_with_different_names_are_not_equal(self):
        assert Item("Apple", 1.50) != Item("Pear", 1.50)

    def test_item_is_not_equal_to_another_type(self):
        assert Item("Apple", 1.50) != "Apple"

    def test_item_representation(self):
        assert repr(Item("Apple", 1.5, 2)) == "Item('Apple', $1.5, qty=2)"


class TestShoppingCart:
    """Test cart state transitions and all business-rule branches."""

    def setup_method(self):
        """Create an isolated cart for every test."""
        self.cart = ShoppingCart()

    def test_cart_starts_empty(self):
        assert self.cart.is_empty()
        assert self.cart.get_item_count() == 0
        assert self.cart.get_total() == pytest.approx(0)

    def test_add_single_item(self):
        self.cart.add_item(Item("Apple", 1.50, 2))

        assert not self.cart.is_empty()
        assert self.cart.get_item_count() == 2
        assert self.cart.get_subtotal() == pytest.approx(3.00)

    def test_add_multiple_different_items(self):
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Pear", 2.00, 3))

        assert len(self.cart.items) == 2
        assert self.cart.get_item_count() == 5

    def test_add_duplicate_item_increases_quantity(self):
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Apple", 1.50, 3))

        assert len(self.cart.items) == 1
        assert self.cart.items[0].quantity == 5

    def test_remove_existing_item(self):
        self.cart.add_item(Item("Apple", 1.50))

        assert self.cart.remove_item("Apple")
        assert self.cart.is_empty()

    def test_remove_nonexistent_item_from_nonempty_cart(self):
        self.cart.add_item(Item("Apple", 1.50))

        assert not self.cart.remove_item("Pear")
        assert self.cart.get_item_count() == 1

    def test_remove_from_empty_cart(self):
        assert not self.cart.remove_item("Apple")

    def test_subtotal_for_multiple_items(self):
        self.cart.add_item(Item("Apple", 1.50, 2))
        self.cart.add_item(Item("Pear", 2.00, 3))

        assert self.cart.get_subtotal() == pytest.approx(9.00)

    def test_apply_valid_discount(self):
        self.cart.apply_discount(25)

        assert self.cart.discount_percent == 25

    @pytest.mark.parametrize("discount", [0, 100])
    def test_apply_discount_boundaries(self, discount):
        self.cart.apply_discount(discount)

        assert self.cart.discount_percent == discount

    @pytest.mark.parametrize("discount", [-1, 101])
    def test_invalid_discount_raises_error(self, discount):
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            self.cart.apply_discount(discount)

    def test_total_with_discount(self):
        self.cart.add_item(Item("Apple", 10.00, 5))
        self.cart.add_item(Item("Banana", 5.00, 4))
        self.cart.apply_discount(20)

        assert self.cart.get_total() == pytest.approx(56.00)

    def test_total_without_discount_equals_subtotal(self):
        self.cart.add_item(Item("Apple", 10.00, 2))

        assert self.cart.get_total() == pytest.approx(self.cart.get_subtotal())

    def test_clear_cart_resets_items_and_discount(self):
        self.cart.add_item(Item("Apple", 10.00, 2))
        self.cart.apply_discount(20)

        self.cart.clear()

        assert self.cart.is_empty()
        assert self.cart.discount_percent == 0

    def test_clear_empty_cart_is_safe(self):
        self.cart.clear()

        assert self.cart.is_empty()
        assert self.cart.discount_percent == 0

    def test_item_count_sums_all_quantities(self):
        self.cart.add_item(Item("Apple", 1.00, 2))
        self.cart.add_item(Item("Pear", 1.00, 3))

        assert self.cart.get_item_count() == 5
