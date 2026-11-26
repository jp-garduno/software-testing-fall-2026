"""Comprehensive tests for the order processing coverage challenge."""

from datetime import datetime, timedelta

import pytest
from order_processor_carloso222 import (
    Order,
    OrderProcessor,
    OrderStatus,
    ShippingMethod,
)


@pytest.fixture(name="address")
def fixture_address():
    """Return a fresh valid US address."""
    return {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip_code": "62701",
        "country": "US",
    }


@pytest.fixture(name="order")
def fixture_order(address):
    """Return a valid order below the free-shipping threshold."""
    return Order(
        "ORD-001",
        "CUST-001",
        [{"name": "Widget", "price": 10.0, "quantity": 2}],
        address,
    )


@pytest.fixture(name="processor")
def fixture_processor():
    """Return a processor with default pricing rules."""
    return OrderProcessor()


class TestOrder:
    """Tests for order state and subtotal behavior."""

    def test_initial_state(self, order):
        """A new order starts pending with no fulfillment metadata."""
        assert order.status is OrderStatus.PENDING
        assert order.shipping_method is None
        assert order.discount_code is None
        assert order.tracking_number is None
        assert isinstance(order.created_at, datetime)

    def test_subtotal_sums_only_complete_items(self, address):
        """Malformed line items do not contribute to the subtotal."""
        order = Order(
            "ORD-002",
            "CUST-001",
            [
                {"name": "Valid", "price": 4.0, "quantity": 3},
                {"name": "No price", "quantity": 5},
                {"name": "No quantity", "price": 100.0},
            ],
            address,
        )
        assert order.get_subtotal() == 12.0


class TestValidation:
    """Tests for order, item, address, and ZIP validation."""

    def test_valid_us_zip_formats(self, processor, order):
        """Both ZIP and ZIP+4 formats are accepted."""
        assert processor.validate_order(order) == (True, None)
        order.shipping_address["zip_code"] = "62701-1234"
        assert processor.validate_order(order) == (True, None)

    @pytest.mark.parametrize("items", [None, []])
    def test_empty_items_are_rejected(self, processor, address, items):
        """An order needs at least one item."""
        empty_order = Order("ORD-002", "CUST-001", items, address)
        assert processor.validate_order(empty_order) == (
            False,
            "Order must contain at least one item",
        )

    @pytest.mark.parametrize(
        "item, expected_error",
        [
            ({"price": 10.0, "quantity": 1}, "Item 0 is missing name"),
            ({"name": "", "price": 10.0, "quantity": 1}, "Item 0 is missing name"),
            ({"name": "Widget", "quantity": 1}, "Item 0 is missing price"),
            (
                {"name": "Widget", "price": 0, "quantity": 1},
                "Item 0 has invalid price",
            ),
            (
                {"name": "Widget", "price": -1, "quantity": 1},
                "Item 0 has invalid price",
            ),
            ({"name": "Widget", "price": 10.0}, "Item 0 is missing quantity"),
            (
                {"name": "Widget", "price": 10.0, "quantity": 0},
                "Item 0 has invalid quantity",
            ),
            (
                {"name": "Widget", "price": 10.0, "quantity": -1},
                "Item 0 has invalid quantity",
            ),
            (
                {"name": "Widget", "price": 10.0, "quantity": 101},
                "Item 0 quantity exceeds maximum (100)",
            ),
        ],
    )
    def test_invalid_items(self, processor, address, item, expected_error):
        """Each invalid item rule reports a specific error."""
        invalid_order = Order("ORD-002", "CUST-001", [item], address)
        assert processor.validate_order(invalid_order) == (False, expected_error)

    def test_error_identifies_item_index(self, processor, address):
        """Validation reports the index of a bad item after valid items."""
        items = [
            {"name": "Valid", "price": 1.0, "quantity": 1},
            {"name": "", "price": 2.0, "quantity": 1},
        ]
        invalid_order = Order("ORD-002", "CUST-001", items, address)
        assert processor.validate_order(invalid_order) == (
            False,
            "Item 1 is missing name",
        )

    @pytest.mark.parametrize("missing_address", [None, {}])
    def test_missing_address_is_rejected(self, processor, order, missing_address):
        """An order needs a shipping address."""
        order.shipping_address = missing_address
        assert processor.validate_order(order) == (
            False,
            "Shipping address is required",
        )

    @pytest.mark.parametrize(
        "field", ["street", "city", "state", "zip_code", "country"]
    )
    @pytest.mark.parametrize("mode", ["missing", "empty"])
    def test_required_address_fields(self, processor, order, field, mode):
        """Every required address field must exist and be nonempty."""
        if mode == "missing":
            del order.shipping_address[field]
        else:
            order.shipping_address[field] = ""

        assert processor.validate_order(order) == (
            False,
            f"Shipping address missing {field}",
        )

    @pytest.mark.parametrize(
        "zip_code, expected_error",
        [
            ("1234", "Invalid US ZIP code format"),
            ("123456", "Invalid US ZIP code format"),
            ("12A45", "ZIP code must be 5 digits"),
            ("1234A-6789", "ZIP+4 must be in format 12345-6789"),
            ("1234567890", "ZIP+4 must be in format 12345-6789"),
            ("12345-678A", "ZIP+4 must be in format 12345-6789"),
        ],
    )
    def test_invalid_us_zip_codes(self, processor, order, zip_code, expected_error):
        """Malformed US ZIP codes are rejected with useful messages."""
        order.shipping_address["zip_code"] = zip_code
        assert processor.validate_order(order) == (False, expected_error)

    def test_non_us_postal_code_is_not_us_validated(self, processor, order):
        """International postal codes bypass US-only format rules."""
        order.shipping_address.update({"country": "CA", "zip_code": "K1A 0B1"})
        assert processor.validate_order(order) == (True, None)


class TestShipping:
    """Tests for shipping rates and surcharges."""

    @pytest.mark.parametrize(
        "method, expected",
        [
            (ShippingMethod.STANDARD, 5.99),
            (ShippingMethod.EXPRESS, 12.99),
            (ShippingMethod.OVERNIGHT, 24.99),
            (ShippingMethod.INTERNATIONAL, 35.99),
            (None, 5.99),
        ],
    )
    def test_base_rates(self, processor, order, method, expected):
        """Each method has the configured base rate and a safe fallback."""
        assert processor.calculate_shipping(order, method) == expected

    def test_free_shipping_at_threshold(self, processor, order):
        """The free-shipping boundary is inclusive."""
        order.items = [{"name": "Bundle", "price": 50.0, "quantity": 1}]
        assert processor.calculate_shipping(order, ShippingMethod.OVERNIGHT) == 0.0

    @pytest.mark.parametrize(
        "quantity, expected",
        [(5, 5.99), (6, 7.99), (10, 7.99), (11, 10.99)],
    )
    def test_quantity_surcharges(self, processor, order, quantity, expected):
        """Quantity surcharges apply immediately above five and ten items."""
        order.items = [{"name": "Small", "price": 0.10, "quantity": quantity}]
        assert processor.calculate_shipping(order, ShippingMethod.STANDARD) == expected

    @pytest.mark.parametrize("country, expected", [("US", 35.99), ("MX", 50.99)])
    def test_international_country_surcharge(self, processor, order, country, expected):
        """International destinations outside the US receive a surcharge."""
        order.shipping_address["country"] = country
        assert (
            processor.calculate_shipping(order, ShippingMethod.INTERNATIONAL)
            == expected
        )


class TestDiscountsAndTotals:
    """Tests for discounts and total calculations."""

    @pytest.mark.parametrize("code", [None, ""])
    def test_no_discount_code(self, processor, code):
        """Missing discount codes are valid and worth zero."""
        assert processor.apply_discount(100.0, code) == (0.0, None)

    @pytest.mark.parametrize(
        "code, expected",
        [
            ("SAVE10", 10.0),
            ("SAVE20", 20.0),
            ("SAVE30", 30.0),
            ("save10", 10.0),
            ("  SAVE20  ", 20.0),
            ("FREESHIP", 0.0),
        ],
    )
    def test_valid_discount_codes(self, processor, code, expected):
        """Known codes are normalized and calculate the expected amount."""
        assert processor.apply_discount(100.0, code) == (expected, None)

    def test_invalid_discount_code(self, processor):
        """An unknown code returns an error without reducing the subtotal."""
        assert processor.apply_discount(100.0, "NOPE") == (
            0.0,
            "Invalid discount code: NOPE",
        )

    def test_discount_cannot_exceed_subtotal(self, processor):
        """The defensive cap prevents custom discounts from making totals negative."""
        processor.discount_codes["TOO_MUCH"] = 1.5
        assert processor.apply_discount(20.0, "TOO_MUCH") == (20.0, None)

    def test_total_with_percentage_discount(self, processor, order):
        """Tax is calculated after discount and shipping is then added."""
        result = processor.calculate_total(order, ShippingMethod.EXPRESS, "SAVE20")
        assert result == {
            "subtotal": 20.0,
            "discount": 4.0,
            "discount_code": "SAVE20",
            "discount_error": None,
            "discounted_subtotal": 16.0,
            "tax": 1.28,
            "tax_rate": 0.08,
            "shipping": 12.99,
            "shipping_method": "express",
            "total": pytest.approx(30.27),
        }

    def test_total_preserves_invalid_discount_error(self, processor, order):
        """Invalid codes leave prices unchanged and appear in the breakdown."""
        result = processor.calculate_total(order, discount_code="BAD")
        assert result["discount"] == 0.0
        assert result["discount_error"] == "Invalid discount code: BAD"
        assert result["total"] == pytest.approx(27.59)

    def test_freeship_code_skips_shipping_calculation(
        self, processor, order, monkeypatch
    ):
        """FREESHIP bypasses the normal shipping calculation after normalization."""

        def unexpected_shipping(*_args):
            raise AssertionError("shipping calculation should be skipped")

        monkeypatch.setattr(processor, "calculate_shipping", unexpected_shipping)
        result = processor.calculate_total(order, discount_code="  freeship ")
        assert result["shipping"] == 0.0
        assert result["total"] == 21.6


class TestProcessingAndDelivery:
    """Tests for the complete workflow and delivery estimates."""

    def test_invalid_order_is_not_processed(self, processor, address):
        """Processing stops at validation and leaves the order pending."""
        invalid_order = Order("ORD-002", "CUST-001", [], address)
        with pytest.raises(
            ValueError,
            match="Order validation failed: Order must contain at least one item",
        ):
            processor.process_order(invalid_order)
        assert invalid_order.status is OrderStatus.PENDING

    def test_valid_order_is_confirmed(self, processor, order):
        """Processing returns a breakdown and stores selected options."""
        result = processor.process_order(order, ShippingMethod.EXPRESS, "SAVE10")
        assert result["order_id"] == "ORD-001"
        assert result["status"] == "confirmed"
        assert result["total_breakdown"]["shipping_method"] == "express"
        assert datetime.fromisoformat(result["confirmed_at"])
        assert order.status is OrderStatus.CONFIRMED
        assert order.shipping_method is ShippingMethod.EXPRESS
        assert order.discount_code == "SAVE10"

    @pytest.mark.parametrize(
        "method, days",
        [
            (ShippingMethod.STANDARD, 7),
            (ShippingMethod.EXPRESS, 3),
            (ShippingMethod.OVERNIGHT, 1),
            (ShippingMethod.INTERNATIONAL, 14),
            (None, 7),
        ],
    )
    def test_delivery_estimates_for_us_orders(self, processor, order, method, days):
        """Each shipping method maps to its expected US delivery window."""
        expected = order.created_at + timedelta(days=days)
        assert processor.estimate_delivery_date(order, method) == expected

    def test_international_delivery_adds_seven_days(self, processor, order):
        """Non-US international orders include the additional delay."""
        order.shipping_address["country"] = "MX"
        expected = order.created_at + timedelta(days=21)
        assert (
            processor.estimate_delivery_date(order, ShippingMethod.INTERNATIONAL)
            == expected
        )
