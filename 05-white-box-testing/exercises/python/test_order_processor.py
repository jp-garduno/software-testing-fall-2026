"""Comprehensive unit tests for the order-processing coverage challenge."""

from datetime import datetime, timedelta

import pytest

from order_processor import Order, OrderProcessor, OrderStatus, ShippingMethod


def make_order(items=None, address=None):
    """Create a valid order that individual tests may adjust."""
    return Order(
        "ORD-001",
        "CUST-001",
        items
        if items is not None
        else [{"name": "Widget", "price": 10.0, "quantity": 2}],
        address
        if address is not None
        else {
            "street": "123 Main St",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62701",
            "country": "US",
        },
    )


class TestOrderAndValidation:
    """Tests for order initialization, subtotals, and validation outcomes."""

    def setup_method(self):
        """Create a processor for every independent test."""
        self.processor = OrderProcessor()

    def test_order_initializes_pending_and_subtotal_ignores_incomplete_items(self):
        """A new order starts pending and totals only complete line items."""
        order = make_order(
            [
                {"name": "Complete", "price": 4.0, "quantity": 3},
                {"name": "No price", "quantity": 1},
                {"name": "No quantity", "price": 2.0},
            ]
        )

        assert order.status is OrderStatus.PENDING
        assert order.shipping_method is None
        assert order.discount_code is None
        assert order.tracking_number is None
        assert order.get_subtotal() == 12.0

    def test_validate_order_success_and_us_zip_plus_four(self):
        """Both five-digit ZIP codes and ZIP+4 values are accepted."""
        assert self.processor.validate_order(make_order()) == (True, None)
        plus_four = make_order(
            address={**make_order().shipping_address, "zip_code": "62701-1234"}
        )
        assert self.processor.validate_order(plus_four) == (True, None)

    @pytest.mark.parametrize("items", [[], None])
    def test_validate_order_rejects_empty_items(self, items):
        """Orders need at least one item."""
        order = make_order(items=items)
        order.items = items
        assert self.processor.validate_order(order) == (
            False,
            "Order must contain at least one item",
        )

    @pytest.mark.parametrize(
        "item,message",
        [
            ({"price": 1, "quantity": 1}, "missing name"),
            ({"name": "", "price": 1, "quantity": 1}, "missing name"),
            ({"name": "Widget", "quantity": 1}, "missing price"),
            ({"name": "Widget", "price": 0, "quantity": 1}, "invalid price"),
            ({"name": "Widget", "price": -1, "quantity": 1}, "invalid price"),
            ({"name": "Widget", "price": 1}, "missing quantity"),
            ({"name": "Widget", "price": 1, "quantity": 0}, "invalid quantity"),
            ({"name": "Widget", "price": 1, "quantity": -1}, "invalid quantity"),
            ({"name": "Widget", "price": 1, "quantity": 101}, "exceeds maximum"),
        ],
    )
    def test_validate_order_rejects_invalid_item_fields(self, item, message):
        """Every item validation branch returns a useful error."""
        valid, error = self.processor.validate_order(make_order(items=[item]))
        assert valid is False
        assert message in error

    @pytest.mark.parametrize(
        "field", ["street", "city", "state", "zip_code", "country"]
    )
    def test_validate_order_rejects_missing_address_fields(self, field):
        """All required address fields are required and non-empty."""
        address = make_order().shipping_address.copy()
        address[field] = ""
        valid, error = self.processor.validate_order(make_order(address=address))
        assert valid is False
        assert error == f"Shipping address missing {field}"

    def test_validate_order_rejects_absent_address(self):
        """A completely absent shipping address cannot be used."""
        order = make_order()
        order.shipping_address = None
        assert self.processor.validate_order(order) == (
            False,
            "Shipping address is required",
        )

    @pytest.mark.parametrize(
        "zip_code,message",
        [
            ("1234", "Invalid US ZIP code format"),
            ("12A45", "ZIP code must be 5 digits"),
            ("12345-67A9", "ZIP+4 must be in format 12345-6789"),
        ],
    )
    def test_validate_order_rejects_invalid_us_zip_codes(self, zip_code, message):
        """US ZIP-format length, digit, and ZIP+4 checks are exercised."""
        address = make_order().shipping_address.copy()
        address["zip_code"] = zip_code
        assert self.processor.validate_order(make_order(address=address)) == (
            False,
            message,
        )

    def test_validate_order_allows_non_us_addresses(self):
        """International addresses do not use US ZIP-format rules."""
        address = make_order().shipping_address.copy()
        address.update({"country": "CA", "zip_code": "A1A 1A1"})
        assert self.processor.validate_order(make_order(address=address)) == (
            True,
            None,
        )


class TestShippingDiscountsAndTotals:
    """Tests for every pricing and shipping decision branch."""

    def setup_method(self):
        """Use a default processor and a low-value valid order."""
        self.processor = OrderProcessor()
        self.order = make_order()

    @pytest.mark.parametrize(
        "method,expected",
        [
            (ShippingMethod.STANDARD, 5.99),
            (ShippingMethod.EXPRESS, 12.99),
            (ShippingMethod.OVERNIGHT, 24.99),
            (ShippingMethod.INTERNATIONAL, 35.99),
            (None, 5.99),
        ],
    )
    def test_calculate_shipping_base_rates(self, method, expected):
        """Each known method, plus the fallback, selects its base rate."""
        assert self.processor.calculate_shipping(self.order, method) == expected

    def test_calculate_shipping_is_free_at_threshold(self):
        """Subtotals at the free-shipping threshold do not incur shipping."""
        order = make_order(items=[{"name": "Expensive", "price": 50.0, "quantity": 1}])
        assert self.processor.calculate_shipping(order, ShippingMethod.EXPRESS) == 0.0

    @pytest.mark.parametrize("quantity,expected", [(6, 7.99), (11, 10.99)])
    def test_calculate_shipping_adds_quantity_surcharges(self, quantity, expected):
        """Orders over five and ten items take the appropriate surcharge branch."""
        order = make_order(
            items=[{"name": "Small", "price": 1.0, "quantity": quantity}]
        )
        assert (
            self.processor.calculate_shipping(order, ShippingMethod.STANDARD) == expected
        )

    def test_calculate_shipping_adds_non_us_international_surcharge(self):
        """International shipping outside the US adds the destination surcharge."""
        address = make_order().shipping_address.copy()
        address["country"] = "MX"
        assert (
            self.processor.calculate_shipping(
                make_order(address=address), ShippingMethod.INTERNATIONAL
            )
            == 50.99
        )

    @pytest.mark.parametrize(
        "code,expected",
        [
            (None, 0.0),
            ("", 0.0),
            ("SAVE10", 10.0),
            ("save20", 20.0),
            ("  SAVE30  ", 30.0),
            ("FREESHIP", 0.0),
        ],
    )
    def test_apply_discount_valid_codes(self, code, expected):
        """Blank, normalized, and free-shipping codes return expected discounts."""
        discount, error = self.processor.apply_discount(100.0, code)
        assert discount == expected
        assert error is None

    def test_apply_discount_invalid_and_capped_codes(self):
        """Unknown codes report errors and configured rates cannot over-discount."""
        assert self.processor.apply_discount(100.0, "NOPE") == (
            0.0,
            "Invalid discount code: NOPE",
        )
        self.processor.discount_codes["OVER"] = 2.0
        assert self.processor.apply_discount(10.0, "OVER") == (10.0, None)

    def test_calculate_total_covers_discount_tax_shipping_and_free_ship_code(self):
        """Totals apply discounts before tax and FREESHIP overrides normal shipping."""
        discounted = self.processor.calculate_total(
            self.order, ShippingMethod.EXPRESS, "SAVE10"
        )
        assert discounted["subtotal"] == 20.0
        assert discounted["discount"] == 2.0
        assert discounted["discounted_subtotal"] == 18.0
        assert discounted["tax"] == pytest.approx(1.44)
        assert discounted["shipping"] == 12.99
        assert discounted["total"] == pytest.approx(32.43)

        free_ship = self.processor.calculate_total(
            self.order, discount_code="  freeship "
        )
        assert free_ship["shipping"] == 0.0
        assert free_ship["shipping_method"] == "standard"


class TestProcessAndDelivery:
    """Tests for order lifecycle changes and delivery estimates."""

    def setup_method(self):
        """Create a processor used by lifecycle tests."""
        self.processor = OrderProcessor()

    def test_process_order_confirms_valid_order(self):
        """Processing a valid order returns a breakdown and mutates lifecycle fields."""
        order = make_order()
        result = self.processor.process_order(order, ShippingMethod.EXPRESS, "SAVE10")

        assert result["order_id"] == "ORD-001"
        assert result["status"] == "confirmed"
        assert result["total_breakdown"]["shipping_method"] == "express"
        assert datetime.fromisoformat(result["confirmed_at"])
        assert order.status is OrderStatus.CONFIRMED
        assert order.shipping_method is ShippingMethod.EXPRESS
        assert order.discount_code == "SAVE10"

    def test_process_order_rejects_invalid_order(self):
        """Invalid orders fail before lifecycle fields are changed."""
        order = make_order(items=[])
        with pytest.raises(ValueError, match="Order validation failed"):
            self.processor.process_order(order)
        assert order.status is OrderStatus.PENDING

    @pytest.mark.parametrize(
        "method,days",
        [
            (ShippingMethod.STANDARD, 7),
            (ShippingMethod.EXPRESS, 3),
            (ShippingMethod.OVERNIGHT, 1),
            (ShippingMethod.INTERNATIONAL, 14),
            (None, 7),
        ],
    )
    def test_estimate_delivery_dates_for_all_methods(self, method, days):
        """Each shipping method uses its documented number of calendar days."""
        order = make_order()
        order.created_at = datetime(2026, 1, 1, 9, 0, 0)
        assert self.processor.estimate_delivery_date(
            order, method
        ) == order.created_at + timedelta(days=days)

    def test_estimate_delivery_date_adds_international_days(self):
        """Non-US international orders add seven extra delivery days."""
        address = make_order().shipping_address.copy()
        address["country"] = "MX"
        order = make_order(address=address)
        order.created_at = datetime(2026, 1, 1)
        assert self.processor.estimate_delivery_date(
            order, ShippingMethod.INTERNATIONAL
        ) == datetime(2026, 1, 22)
