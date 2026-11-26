from datetime import datetime, timedelta

import pytest
from order_processor import Order, OrderProcessor, OrderStatus, ShippingMethod


class TestOrderProcessor:
    """Test suite for OrderProcessor."""

    def setup_method(self):
        """Create processor and sample order before each test."""
        self.processor = OrderProcessor()
        self.sample_order = Order(
            order_id="ORD-001",
            customer_id="CUST-001",
            items=[{"name": "Widget", "price": 10.0, "quantity": 2}],
            shipping_address={
                "street": "123 Main St",
                "city": "Springfield",
                "state": "IL",
                "zip_code": "62701",
                "country": "US",
            },
        )

    def test_validate_order_success(self):
        """Test validating a valid order."""
        is_valid, error = self.processor.validate_order(self.sample_order)
        assert is_valid is True
        assert error is None

    def test_calculate_total_no_discount(self):
        """Test calculating total without discount."""
        result = self.processor.calculate_total(self.sample_order)
        assert result["subtotal"] == 20.0
        assert result["discount"] == 0.0
        assert result["tax"] > 0

    def make_order(self, items=None, shipping_address=None):
        """Create an order with configurable items and address."""
        if items is None:
            items = [{"name": "Widget", "price": 10.0, "quantity": 2}]
        if shipping_address is None:
            shipping_address = {
                "street": "123 Main St",
                "city": "Springfield",
                "state": "IL",
                "zip_code": "62701",
                "country": "US",
            }
        return Order("ORD-TEST", "CUST-TEST", items, shipping_address)

    def test_get_subtotal_ignores_items_missing_price_or_quantity(self):
        order = self.make_order(
            items=[
                {"name": "No price", "quantity": 2},
                {"name": "No quantity", "price": 5.0},
                {"name": "Complete", "price": 3.0, "quantity": 4},
            ]
        )

        assert order.get_subtotal() == 12.0

    @pytest.mark.parametrize(
        "items, expected_error",
        [
            ([], "at least one item"),
            ([{}], "missing name"),
            ([{"name": "", "price": 1, "quantity": 1}], "missing name"),
            ([{"name": "Widget"}], "missing price"),
            ([{"name": "Widget", "price": 0, "quantity": 1}], "invalid price"),
            ([{"name": "Widget", "price": -1, "quantity": 1}], "invalid price"),
            ([{"name": "Widget", "price": 1}], "missing quantity"),
            ([{"name": "Widget", "price": 1, "quantity": 0}], "invalid quantity"),
            ([{"name": "Widget", "price": 1, "quantity": -1}], "invalid quantity"),
            ([{"name": "Widget", "price": 1, "quantity": 101}], "exceeds maximum"),
        ],
    )
    def test_validate_order_rejects_invalid_items(self, items, expected_error):
        order = self.make_order(items=items)

        is_valid, error = self.processor.validate_order(order)

        assert is_valid is False
        assert expected_error in error

    def test_validate_order_rejects_missing_shipping_address(self):
        order = self.make_order()
        order.shipping_address = None

        is_valid, error = self.processor.validate_order(order)

        assert is_valid is False
        assert error == "Shipping address is required"

    @pytest.mark.parametrize(
        "field, field_value",
        [
            ("street", None),
            ("city", ""),
            ("state", None),
            ("zip_code", None),
            ("country", None),
        ],
    )
    def test_validate_order_rejects_missing_address_fields(self, field, field_value):
        address = {
            "street": "123 Main St",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62701",
            "country": "US",
        }
        if field_value is None:
            del address[field]
        else:
            address[field] = field_value

        is_valid, error = self.processor.validate_order(
            self.make_order(shipping_address=address)
        )

        assert is_valid is False
        assert error == f"Shipping address missing {field}"

    @pytest.mark.parametrize(
        "zip_code, expected_error",
        [
            ("1234", "Invalid US ZIP code format"),
            ("12A45", "ZIP code must be 5 digits"),
            ("1234A-6789", "ZIP+4 must be in format 12345-6789"),
            ("1234567890", "ZIP+4 must be in format 12345-6789"),
            ("12345-678A", "ZIP+4 must be in format 12345-6789"),
        ],
    )
    def test_validate_order_rejects_invalid_us_zip_codes(
        self, zip_code, expected_error
    ):
        address = dict(self.sample_order.shipping_address, zip_code=zip_code)

        is_valid, error = self.processor.validate_order(
            self.make_order(shipping_address=address)
        )

        assert is_valid is False
        assert error == expected_error

    @pytest.mark.parametrize(
        "country, zip_code", [("US", "12345-6789"), ("CA", "postal code")]
    )
    def test_validate_order_accepts_valid_zip_formats(self, country, zip_code):
        address = dict(
            self.sample_order.shipping_address, country=country, zip_code=zip_code
        )

        is_valid, error = self.processor.validate_order(
            self.make_order(shipping_address=address)
        )

        assert is_valid is True
        assert error is None

    @pytest.mark.parametrize(
        "method, expected_rate",
        [
            (ShippingMethod.STANDARD, 5.99),
            (ShippingMethod.EXPRESS, 12.99),
            (ShippingMethod.OVERNIGHT, 24.99),
            (ShippingMethod.INTERNATIONAL, 35.99),
            (None, 5.99),
        ],
    )
    def test_calculate_shipping_rates(self, method, expected_rate):
        assert (
            self.processor.calculate_shipping(self.sample_order, method)
            == expected_rate
        )

    @pytest.mark.parametrize(
        "quantity, expected_rate", [(5, 5.99), (6, 7.99), (10, 7.99), (11, 10.99)]
    )
    def test_calculate_shipping_item_count_surcharges(self, quantity, expected_rate):
        order = self.make_order(
            items=[{"name": "Widget", "price": 1.0, "quantity": quantity}]
        )

        assert (
            self.processor.calculate_shipping(order, ShippingMethod.STANDARD)
            == expected_rate
        )

    def test_calculate_shipping_free_at_threshold(self):
        order = self.make_order(
            items=[{"name": "Widget", "price": 10.0, "quantity": 5}]
        )

        assert self.processor.calculate_shipping(order, ShippingMethod.OVERNIGHT) == 0.0

    def test_calculate_shipping_adds_international_surcharge_for_non_us(self):
        address = dict(self.sample_order.shipping_address, country="CA")
        order = self.make_order(shipping_address=address)

        assert (
            self.processor.calculate_shipping(order, ShippingMethod.INTERNATIONAL)
            == 50.99
        )

    @pytest.mark.parametrize(
        "code, expected_discount",
        [("SAVE10", 10.0), ("SAVE20", 20.0), ("SAVE30", 30.0), (" save10 ", 10.0)],
    )
    def test_apply_discount_codes_and_normalization(self, code, expected_discount):
        discount, error = self.processor.apply_discount(100.0, code)

        assert discount == expected_discount
        assert error is None

    @pytest.mark.parametrize("code", [None, ""])
    def test_apply_discount_without_code(self, code):
        assert self.processor.apply_discount(100.0, code) == (0.0, None)

    def test_apply_discount_freeship_code(self):
        assert self.processor.apply_discount(100.0, "FREESHIP") == (0.0, None)

    def test_apply_discount_invalid_code_reports_original_value(self):
        code = " invalid "

        discount, error = self.processor.apply_discount(100.0, code)

        assert discount == 0.0
        assert error == f"Invalid discount code: {code}"

    def test_apply_discount_caps_discount_at_negative_subtotal(self):
        discount, error = self.processor.apply_discount(-100.0, "SAVE10")

        assert discount == -100.0
        assert error is None

    def test_calculate_total_applies_discount_before_tax(self):
        result = self.processor.calculate_total(
            self.sample_order, ShippingMethod.EXPRESS, "SAVE20"
        )

        assert result["subtotal"] == 20.0
        assert result["discount"] == 4.0
        assert result["discounted_subtotal"] == 16.0
        assert result["tax"] == 1.28
        assert result["shipping"] == 12.99
        assert result["total"] == pytest.approx(30.27)

    def test_calculate_total_invalid_discount_keeps_shipping_and_error(self):
        result = self.processor.calculate_total(
            self.sample_order, discount_code="BAD-CODE"
        )

        assert result["discount"] == 0.0
        assert result["discount_error"] == "Invalid discount code: BAD-CODE"
        assert result["shipping"] == 5.99

    def test_calculate_total_freeship_code_waives_shipping(self):
        result = self.processor.calculate_total(
            self.sample_order, discount_code=" freeship "
        )

        assert result["discount"] == 0.0
        assert result["shipping"] == 0.0
        assert result["discount_error"] is None

    def test_process_order_rejects_invalid_order_without_changing_status(self):
        order = self.make_order(items=[])

        with pytest.raises(
            ValueError,
            match="Order validation failed: Order must contain at least one item",
        ):
            self.processor.process_order(order)

        assert order.status is OrderStatus.PENDING

    def test_process_order_confirms_valid_order_and_records_options(self):
        result = self.processor.process_order(
            self.sample_order, ShippingMethod.EXPRESS, "SAVE10"
        )

        assert result["order_id"] == self.sample_order.order_id
        assert result["status"] == "confirmed"
        assert datetime.fromisoformat(result["confirmed_at"])
        assert result["total_breakdown"]["discount_code"] == "SAVE10"
        assert self.sample_order.status is OrderStatus.CONFIRMED
        assert self.sample_order.shipping_method is ShippingMethod.EXPRESS
        assert self.sample_order.discount_code == "SAVE10"

    @pytest.mark.parametrize(
        "method, expected_days",
        [
            (ShippingMethod.STANDARD, 7),
            (ShippingMethod.EXPRESS, 3),
            (ShippingMethod.OVERNIGHT, 1),
            (ShippingMethod.INTERNATIONAL, 14),
            (None, 7),
        ],
    )
    def test_estimate_delivery_date_by_shipping_method(self, method, expected_days):
        order = self.make_order()
        order.created_at = datetime(2026, 1, 1)

        assert self.processor.estimate_delivery_date(order, method) == (
            order.created_at + timedelta(days=expected_days)
        )

    def test_estimate_delivery_date_adds_time_for_non_us_international_order(self):
        address = dict(self.sample_order.shipping_address, country="CA")
        order = self.make_order(shipping_address=address)
        order.created_at = datetime(2026, 1, 1)

        assert self.processor.estimate_delivery_date(
            order, ShippingMethod.INTERNATIONAL
        ) == order.created_at + timedelta(days=21)
