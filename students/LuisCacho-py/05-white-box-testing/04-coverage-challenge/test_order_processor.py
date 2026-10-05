"""Comprehensive test suite for OrderProcessor achieving 100% statement and branch coverage."""
import pytest
from datetime import datetime, timedelta
from order_processor import Order, OrderProcessor, OrderStatus, ShippingMethod


class TestOrderProcessor:
    """Test suite covering all branches, edge cases, and validations in order processing."""

    def setup_method(self):
        """Create processor and standard valid sample order before each test."""
        self.processor = OrderProcessor()
        self.sample_order = Order(
            order_id="ORD-001",
            customer_id="CUST-001",
            items=[
                {'name': 'Widget', 'price': 10.0, 'quantity': 2}
            ],
            shipping_address={
                'street': '123 Main St',
                'city': 'Springfield',
                'state': 'IL',
                'zip_code': '62701',
                'country': 'US'
            }
        )

    # --- Order Model Tests ---
    def test_order_subtotal_calculation(self):
        """Test subtotal calculation with regular items."""
        order = Order("O1", "C1", [{'name': 'A', 'price': 15.0, 'quantity': 2}], {})
        assert order.get_subtotal() == 30.0

    def test_order_subtotal_skips_malformed_items(self):
        """Test subtotal skips items without price or quantity without throwing exception."""
        order = Order(
            "O2",
            "C2",
            [
                {'name': 'Valid', 'price': 10.0, 'quantity': 2},
                {'name': 'NoPrice', 'quantity': 5},
                {'name': 'NoQty', 'price': 20.0},
                {'name': 'Empty'}
            ],
            {}
        )
        assert order.get_subtotal() == 20.0

    # --- Validation: Empty and Missing Items ---
    def test_validate_order_success(self):
        """Test validating an order with all valid fields."""
        is_valid, error = self.processor.validate_order(self.sample_order)
        assert is_valid is True
        assert error is None

    def test_validate_order_empty_items(self):
        """Test validation fails for order with empty items list."""
        order = Order("ORD-002", "CUST-001", [], self.sample_order.shipping_address)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert "Order must contain at least one item" in error

    def test_validate_order_none_items(self):
        """Test validation fails for order with items as None."""
        order = Order("ORD-003", "CUST-001", None, self.sample_order.shipping_address)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert "Order must contain at least one item" in error

    # --- Validation: Item Attributes ---
    def test_validate_order_missing_item_name_key(self):
        """Test validation fails when item dictionary lacks 'name' key."""
        order = Order("ORD-004", "C1", [{'price': 10.0, 'quantity': 1}], self.sample_order.shipping_address)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert "Item 0 is missing name" in error

    def test_validate_order_empty_item_name(self):
        """Test validation fails when item name is empty string."""
        order = Order("ORD-005", "C1", [{'name': '', 'price': 10.0, 'quantity': 1}], self.sample_order.shipping_address)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert "Item 0 is missing name" in error

    def test_validate_order_missing_item_price_key(self):
        """Test validation fails when item lacks 'price' key."""
        order = Order("ORD-006", "C1", [{'name': 'Pen', 'quantity': 1}], self.sample_order.shipping_address)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert "Item 0 is missing price" in error

    @pytest.mark.parametrize("invalid_price", [0, -5.0])
    def test_validate_order_invalid_price(self, invalid_price):
        """Test validation fails for zero or negative price."""
        order = Order("ORD-007", "C1", [{'name': 'Pen', 'price': invalid_price, 'quantity': 1}], self.sample_order.shipping_address)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert "Item 0 has invalid price" in error

    def test_validate_order_missing_item_quantity_key(self):
        """Test validation fails when item lacks 'quantity' key."""
        order = Order("ORD-008", "C1", [{'name': 'Pen', 'price': 10.0}], self.sample_order.shipping_address)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert "Item 0 is missing quantity" in error

    @pytest.mark.parametrize("invalid_qty", [0, -2])
    def test_validate_order_invalid_quantity(self, invalid_qty):
        """Test validation fails for zero or negative quantity."""
        order = Order("ORD-009", "C1", [{'name': 'Pen', 'price': 10.0, 'quantity': invalid_qty}], self.sample_order.shipping_address)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert "Item 0 has invalid quantity" in error

    def test_validate_order_excessive_quantity(self):
        """Test validation fails when quantity exceeds 100."""
        order = Order("ORD-010", "C1", [{'name': 'Bulk', 'price': 1.0, 'quantity': 101}], self.sample_order.shipping_address)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert "quantity exceeds maximum (100)" in error

    # --- Validation: Shipping Address ---
    def test_validate_order_missing_shipping_address(self):
        """Test validation fails when shipping address is None or empty."""
        order1 = Order("ORD-011", "C1", [{'name': 'Pen', 'price': 1.0, 'quantity': 1}], None)
        assert self.processor.validate_order(order1) == (False, "Shipping address is required")

        order2 = Order("ORD-012", "C1", [{'name': 'Pen', 'price': 1.0, 'quantity': 1}], {})
        assert self.processor.validate_order(order2) == (False, "Shipping address is required")

    @pytest.mark.parametrize("missing_field", ['street', 'city', 'state', 'zip_code', 'country'])
    def test_validate_order_missing_address_field_key(self, missing_field):
        """Test validation fails when a required address field key is omitted."""
        addr = self.sample_order.shipping_address.copy()
        del addr[missing_field]
        order = Order("ORD-013", "C1", self.sample_order.items, addr)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert f"Shipping address missing {missing_field}" in error

    @pytest.mark.parametrize("empty_field", ['street', 'city', 'state', 'zip_code', 'country'])
    def test_validate_order_empty_address_field_value(self, empty_field):
        """Test validation fails when a required address field is empty string."""
        addr = self.sample_order.shipping_address.copy()
        addr[empty_field] = ""
        order = Order("ORD-014", "C1", self.sample_order.items, addr)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert f"Shipping address missing {empty_field}" in error

    # --- Validation: ZIP Codes ---
    @pytest.mark.parametrize("invalid_zip_len", ["1234", "123456", "12345-678"])
    def test_validate_order_us_zip_invalid_length(self, invalid_zip_len):
        """Test US ZIP code must have length 5 or 10."""
        addr = self.sample_order.shipping_address.copy()
        addr['zip_code'] = invalid_zip_len
        order = Order("ORD-015", "C1", self.sample_order.items, addr)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert "Invalid US ZIP code format" in error

    def test_validate_order_us_5digit_zip_non_digits(self):
        """Test US 5-digit ZIP code containing non-digit characters fails."""
        addr = self.sample_order.shipping_address.copy()
        addr['zip_code'] = "9021A"
        order = Order("ORD-016", "C1", self.sample_order.items, addr)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert "ZIP code must be 5 digits" in error

    @pytest.mark.parametrize("malformed_zip4", [
        "1234567890",   # No hyphen
        "1234A-6789",   # Non-digit first 5
        "12345_6789",   # Underscore instead of hyphen
        "12345-678B",   # Non-digit last 4
    ])
    def test_validate_order_us_10digit_zip_malformed(self, malformed_zip4):
        """Test US ZIP+4 code format validation."""
        addr = self.sample_order.shipping_address.copy()
        addr['zip_code'] = malformed_zip4
        order = Order("ORD-017", "C1", self.sample_order.items, addr)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is False
        assert "ZIP+4 must be in format 12345-6789" in error

    def test_validate_order_us_valid_zip_plus_4(self):
        """Test valid US ZIP+4 format succeeds."""
        addr = self.sample_order.shipping_address.copy()
        addr['zip_code'] = "62701-1234"
        order = Order("ORD-018", "C1", self.sample_order.items, addr)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is True
        assert error is None

    def test_validate_order_international_address_bypasses_us_zip_rules(self):
        """Test that non-US address does not enforce US zip code rules."""
        addr = {
            'street': 'Av. Vallarta 100',
            'city': 'Guadalajara',
            'state': 'Jalisco',
            'zip_code': 'CP-44100',
            'country': 'MX'
        }
        order = Order("ORD-019", "C1", self.sample_order.items, addr)
        is_valid, error = self.processor.validate_order(order)
        assert is_valid is True
        assert error is None

    # --- Shipping Calculations ---
    def test_calculate_shipping_free_over_threshold(self):
        """Test free shipping when subtotal reaches or exceeds threshold."""
        order = Order("O3", "C1", [{'name': 'Item', 'price': 50.0, 'quantity': 1}], self.sample_order.shipping_address)
        assert self.processor.calculate_shipping(order, ShippingMethod.STANDARD) == 0.0

        order_higher = Order("O4", "C1", [{'name': 'Item', 'price': 75.0, 'quantity': 1}], self.sample_order.shipping_address)
        assert self.processor.calculate_shipping(order_higher, ShippingMethod.EXPRESS) == 0.0

    @pytest.mark.parametrize("method,base_expected", [
        (ShippingMethod.STANDARD, 5.99),
        (ShippingMethod.EXPRESS, 12.99),
        (ShippingMethod.OVERNIGHT, 24.99),
        (ShippingMethod.INTERNATIONAL, 35.99),
    ])
    def test_calculate_shipping_base_methods(self, method, base_expected):
        """Test baseline shipping rates for each ShippingMethod when under free threshold."""
        order = Order("O5", "C1", [{'name': 'Item', 'price': 10.0, 'quantity': 1}], self.sample_order.shipping_address)
        assert self.processor.calculate_shipping(order, method) == pytest.approx(base_expected)

    def test_calculate_shipping_unknown_method_fallback(self):
        """Test unknown shipping method falls back to standard base rate (5.99)."""
        order = Order("O6", "C1", [{'name': 'Item', 'price': 10.0, 'quantity': 1}], self.sample_order.shipping_address)
        assert self.processor.calculate_shipping(order, "UNKNOWN_METHOD") == pytest.approx(5.99)

    def test_calculate_shipping_weight_surcharge_between_6_and_10_items(self):
        """Test surcharge of $2.0 when item quantity is between 6 and 10."""
        order = Order("O7", "C1", [{'name': 'Item', 'price': 2.0, 'quantity': 7}], self.sample_order.shipping_address)
        # Base: 5.99 + 2.0 = 7.99
        assert self.processor.calculate_shipping(order, ShippingMethod.STANDARD) == pytest.approx(7.99)

    def test_calculate_shipping_weight_surcharge_over_10_items(self):
        """Test surcharge of $5.0 when item quantity is greater than 10."""
        order = Order("O8", "C1", [{'name': 'Item', 'price': 1.0, 'quantity': 12}], self.sample_order.shipping_address)
        # Base: 5.99 + 5.0 = 10.99
        assert self.processor.calculate_shipping(order, ShippingMethod.STANDARD) == pytest.approx(10.99)

    def test_calculate_shipping_international_non_us_surcharge(self):
        """Test international shipping to non-US country adds $15.0 surcharge."""
        non_us_addr = {
            'street': 'Gran Via 1',
            'city': 'Madrid',
            'state': 'Madrid',
            'zip_code': '28013',
            'country': 'ES'
        }
        order = Order("O9", "C1", [{'name': 'Item', 'price': 10.0, 'quantity': 2}], non_us_addr)
        # Base: 35.99 + 15.0 = 50.99
        assert self.processor.calculate_shipping(order, ShippingMethod.INTERNATIONAL) == pytest.approx(50.99)

    # --- Discounts ---
    def test_apply_discount_none_or_empty(self):
        """Test applying None or empty discount code."""
        assert self.processor.apply_discount(100.0, None) == (0.0, None)
        assert self.processor.apply_discount(100.0, "") == (0.0, None)

    def test_apply_discount_invalid_code(self):
        """Test invalid discount code returns error message."""
        discount, error = self.processor.apply_discount(100.0, "NOTREAL")
        assert discount == 0.0
        assert "Invalid discount code: NOTREAL" in error

    def test_apply_discount_freeship_code(self):
        """Test FREESHIP discount returns 0 discount amount and no error."""
        discount, error = self.processor.apply_discount(100.0, "FREESHIP")
        assert discount == 0.0
        assert error is None

    @pytest.mark.parametrize("code,rate", [
        ("SAVE10", 0.10),
        ("SAVE20", 0.20),
        ("SAVE30", 0.30),
        (" save10 ", 0.10),
        ("save20", 0.20),
    ])
    def test_apply_discount_valid_codes_case_and_whitespace(self, code, rate):
        """Test valid discount codes with trimming and case insensitivity."""
        discount, error = self.processor.apply_discount(100.0, code)
        assert discount == pytest.approx(100.0 * rate)
        assert error is None

    def test_apply_discount_capped_at_subtotal(self):
        """Test discount amount is capped at subtotal if rate exceeds 100%."""
        self.processor.discount_codes['MASSIVE'] = 1.50
        discount, error = self.processor.apply_discount(40.0, 'MASSIVE')
        assert discount == 40.0
        assert error is None

    # --- Calculate Total and Process Order ---
    def test_calculate_total_with_freeship_discount_code(self):
        """Test calculate_total with FREESHIP sets shipping cost to 0.0."""
        result = self.processor.calculate_total(
            self.sample_order,
            shipping_method=ShippingMethod.STANDARD,
            discount_code="FREESHIP"
        )
        assert result['shipping'] == 0.0
        assert result['discount'] == 0.0
        assert result['total'] == result['discounted_subtotal'] + result['tax']

    def test_calculate_total_with_save_discount(self):
        """Test calculate_total breakdown with SAVE20 discount."""
        result = self.processor.calculate_total(
            self.sample_order,
            shipping_method=ShippingMethod.STANDARD,
            discount_code="SAVE20"
        )
        assert result['subtotal'] == 20.0
        assert result['discount'] == pytest.approx(4.0)
        assert result['discounted_subtotal'] == pytest.approx(16.0)
        assert result['tax'] == pytest.approx(16.0 * 0.08)
        assert result['shipping'] == pytest.approx(5.99)
        assert result['total'] == pytest.approx(16.0 + (16.0 * 0.08) + 5.99)

    def test_process_order_success(self):
        """Test processing a valid order updates status and returns summary."""
        result = self.processor.process_order(
            self.sample_order,
            shipping_method=ShippingMethod.EXPRESS,
            discount_code="SAVE10"
        )

        assert result['order_id'] == "ORD-001"
        assert result['status'] == OrderStatus.CONFIRMED.value
        assert self.sample_order.status == OrderStatus.CONFIRMED
        assert self.sample_order.shipping_method == ShippingMethod.EXPRESS
        assert self.sample_order.discount_code == "SAVE10"
        assert 'confirmed_at' in result

    def test_process_order_invalid_raises_error(self):
        """Test process_order on invalid order raises ValueError."""
        invalid_order = Order("ORD-BAD", "C1", [], self.sample_order.shipping_address)
        with pytest.raises(ValueError, match="Order validation failed"):
            self.processor.process_order(invalid_order)

    # --- Delivery Estimation ---
    @pytest.mark.parametrize("method,days", [
        (ShippingMethod.STANDARD, 7),
        (ShippingMethod.EXPRESS, 3),
        (ShippingMethod.OVERNIGHT, 1),
        (ShippingMethod.INTERNATIONAL, 14),
    ])
    def test_estimate_delivery_date_us_destinations(self, method, days):
        """Test estimated delivery dates for domestic US orders."""
        delivery_date = self.processor.estimate_delivery_date(self.sample_order, method)
        expected = self.sample_order.created_at + timedelta(days=days)
        assert delivery_date == expected

    def test_estimate_delivery_date_international_non_us(self):
        """Test estimated delivery date adds 7 extra days for international destination outside US."""
        non_us_addr = self.sample_order.shipping_address.copy()
        non_us_addr['country'] = 'FR'
        order = Order("ORD-INT", "C1", self.sample_order.items, non_us_addr)

        delivery_date = self.processor.estimate_delivery_date(order, ShippingMethod.INTERNATIONAL)
        expected = order.created_at + timedelta(days=14 + 7)
        assert delivery_date == expected

    def test_estimate_delivery_date_unknown_shipping_method_fallback(self):
        """Test delivery date fallback for unrecognized shipping method."""
        delivery_date = self.processor.estimate_delivery_date(self.sample_order, "CUSTOM_CARRIER")
        expected = self.sample_order.created_at + timedelta(days=7)
        assert delivery_date == expected
