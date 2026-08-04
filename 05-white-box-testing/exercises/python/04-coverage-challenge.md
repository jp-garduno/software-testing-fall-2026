# Exercise 4: Coverage Challenge

**Duration**: 90 minutes  
**Difficulty**: Advanced  
**Topics**: High coverage, complex code paths, edge cases, comprehensive testing

## Objectives

By completing this exercise, you will:

- Analyze existing code to identify untested paths
- Write tests to achieve >95% coverage
- Handle complex branching logic and nested conditions
- Test loops, error handling, and edge cases
- Understand the limitations of coverage metrics
- Balance coverage goals with test quality

## Background

You've been given a partially tested codebase with low coverage (~40%). Your mission is to analyze the code, identify untested paths, and write comprehensive tests to achieve >95% statement and branch coverage. This exercise simulates real-world scenarios where you inherit legacy code that needs testing.

## Part 1: Analyze the Code (15 minutes)

You are provided with `order_processor.py` - a complex order processing system with validation, calculations, and business rules.

### `order_processor.py`

```python
from datetime import datetime, timedelta
from enum import Enum

class OrderStatus(Enum):
    """Order status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class ShippingMethod(Enum):
    """Shipping method enumeration."""
    STANDARD = "standard"
    EXPRESS = "express"
    OVERNIGHT = "overnight"
    INTERNATIONAL = "international"

class Order:
    """Represents a customer order."""

    def __init__(self, order_id, customer_id, items, shipping_address):
        """Initialize an order."""
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.shipping_address = shipping_address
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()
        self.shipping_method = None
        self.discount_code = None
        self.tracking_number = None

    def get_subtotal(self):
        """Calculate order subtotal."""
        total = 0
        for item in self.items:
            if 'price' in item and 'quantity' in item:
                total += item['price'] * item['quantity']
        return total

class OrderProcessor:
    """Processes and validates orders."""

    def __init__(self, tax_rate=0.08, free_shipping_threshold=50.0):
        """
        Initialize order processor.

        Args:
            tax_rate: Sales tax rate (default 8%)
            free_shipping_threshold: Minimum order amount for free shipping
        """
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.discount_codes = {
            'SAVE10': 0.10,
            'SAVE20': 0.20,
            'SAVE30': 0.30,
            'FREESHIP': 0.0
        }

    def validate_order(self, order):
        """
        Validate an order before processing.

        Args:
            order: Order object

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if order has items
        if not order.items or len(order.items) == 0:
            return False, "Order must contain at least one item"

        # Validate each item
        for i, item in enumerate(order.items):
            if 'name' not in item or not item['name']:
                return False, f"Item {i} is missing name"

            if 'price' not in item:
                return False, f"Item {i} is missing price"

            if item['price'] <= 0:
                return False, f"Item {i} has invalid price"

            if 'quantity' not in item:
                return False, f"Item {i} is missing quantity"

            if item['quantity'] <= 0:
                return False, f"Item {i} has invalid quantity"

            # Check for excessive quantity (potential fraud)
            if item['quantity'] > 100:
                return False, f"Item {i} quantity exceeds maximum (100)"

        # Validate shipping address
        if not order.shipping_address:
            return False, "Shipping address is required"

        required_fields = ['street', 'city', 'state', 'zip_code', 'country']
        for field in required_fields:
            if field not in order.shipping_address or not order.shipping_address[field]:
                return False, f"Shipping address missing {field}"

        # Validate ZIP code format (US only for simplicity)
        zip_code = order.shipping_address['zip_code']
        if order.shipping_address['country'] == 'US':
            if not (len(zip_code) == 5 or len(zip_code) == 10):
                return False, "Invalid US ZIP code format"

            # Check if it's all digits (for 5-digit) or has hyphen (for ZIP+4)
            if len(zip_code) == 5:
                if not zip_code.isdigit():
                    return False, "ZIP code must be 5 digits"
            elif len(zip_code) == 10:
                if not (zip_code[:5].isdigit() and zip_code[5] == '-' and zip_code[6:].isdigit()):
                    return False, "ZIP+4 must be in format 12345-6789"

        return True, None

    def calculate_shipping(self, order, shipping_method):
        """
        Calculate shipping cost based on method and order details.

        Args:
            order: Order object
            shipping_method: ShippingMethod enum

        Returns:
            Shipping cost as float
        """
        subtotal = order.get_subtotal()

        # Free shipping for orders over threshold
        if subtotal >= self.free_shipping_threshold:
            return 0.0

        # Base shipping rates
        if shipping_method == ShippingMethod.STANDARD:
            base_rate = 5.99
        elif shipping_method == ShippingMethod.EXPRESS:
            base_rate = 12.99
        elif shipping_method == ShippingMethod.OVERNIGHT:
            base_rate = 24.99
        elif shipping_method == ShippingMethod.INTERNATIONAL:
            base_rate = 35.99
        else:
            base_rate = 5.99

        # Additional charges based on weight (estimated by item count)
        item_count = sum(item['quantity'] for item in order.items)
        if item_count > 10:
            base_rate += 5.0
        elif item_count > 5:
            base_rate += 2.0

        # International shipping surcharge for non-US
        if (shipping_method == ShippingMethod.INTERNATIONAL and
            order.shipping_address.get('country') != 'US'):
            base_rate += 15.0

        return base_rate

    def apply_discount(self, subtotal, discount_code):
        """
        Apply discount code to subtotal.

        Args:
            subtotal: Order subtotal
            discount_code: Discount code string

        Returns:
            Tuple of (discount_amount, error_message)
        """
        if not discount_code:
            return 0.0, None

        # Normalize code
        code = discount_code.upper().strip()

        if code not in self.discount_codes:
            return 0.0, f"Invalid discount code: {discount_code}"

        discount_percent = self.discount_codes[code]

        # Special handling for FREESHIP code
        if code == 'FREESHIP':
            return 0.0, None  # Handled separately in shipping calculation

        # Calculate discount
        discount_amount = subtotal * discount_percent

        # Cap discount at subtotal (can't be negative)
        if discount_amount > subtotal:
            discount_amount = subtotal

        return discount_amount, None

    def calculate_total(self, order, shipping_method=ShippingMethod.STANDARD, discount_code=None):
        """
        Calculate order total including tax, shipping, and discounts.

        Args:
            order: Order object
            shipping_method: ShippingMethod enum
            discount_code: Optional discount code

        Returns:
            Dictionary with breakdown of costs
        """
        subtotal = order.get_subtotal()

        # Apply discount
        discount_amount, discount_error = self.apply_discount(subtotal, discount_code)
        discounted_subtotal = subtotal - discount_amount

        # Calculate tax on discounted subtotal
        tax = discounted_subtotal * self.tax_rate

        # Calculate shipping (free shipping for FREESHIP code)
        if discount_code and discount_code.upper().strip() == 'FREESHIP':
            shipping = 0.0
        else:
            shipping = self.calculate_shipping(order, shipping_method)

        # Calculate total
        total = discounted_subtotal + tax + shipping

        return {
            'subtotal': subtotal,
            'discount': discount_amount,
            'discount_code': discount_code,
            'discount_error': discount_error,
            'discounted_subtotal': discounted_subtotal,
            'tax': tax,
            'tax_rate': self.tax_rate,
            'shipping': shipping,
            'shipping_method': shipping_method.value,
            'total': total
        }

    def process_order(self, order, shipping_method=ShippingMethod.STANDARD, discount_code=None):
        """
        Process an order: validate, calculate total, and update status.

        Args:
            order: Order object
            shipping_method: ShippingMethod enum
            discount_code: Optional discount code

        Returns:
            Dictionary with order result

        Raises:
            ValueError: If order validation fails
        """
        # Validate order
        is_valid, error = self.validate_order(order)
        if not is_valid:
            raise ValueError(f"Order validation failed: {error}")

        # Calculate total
        total_breakdown = self.calculate_total(order, shipping_method, discount_code)

        # Update order
        order.status = OrderStatus.CONFIRMED
        order.shipping_method = shipping_method
        order.discount_code = discount_code

        return {
            'order_id': order.order_id,
            'status': order.status.value,
            'total_breakdown': total_breakdown,
            'confirmed_at': datetime.now().isoformat()
        }

    def estimate_delivery_date(self, order, shipping_method):
        """
        Estimate delivery date based on shipping method.

        Args:
            order: Order object
            shipping_method: ShippingMethod enum

        Returns:
            Estimated delivery date
        """
        business_days = {
            ShippingMethod.STANDARD: 7,
            ShippingMethod.EXPRESS: 3,
            ShippingMethod.OVERNIGHT: 1,
            ShippingMethod.INTERNATIONAL: 14
        }

        days = business_days.get(shipping_method, 7)

        # Add extra days for international
        if (shipping_method == ShippingMethod.INTERNATIONAL and
            order.shipping_address.get('country') != 'US'):
            days += 7

        # Calculate delivery date (simplified, doesn't account for weekends)
        delivery_date = order.created_at + timedelta(days=days)

        return delivery_date
```

## Part 2: Run Initial Coverage Report (5 minutes)

You're provided with minimal existing tests in `test_order_processor.py`:

```python
import pytest
from datetime import datetime
from order_processor import Order, OrderProcessor, OrderStatus, ShippingMethod

class TestOrderProcessor:
    """Test suite for OrderProcessor."""

    def setup_method(self):
        """Create processor and sample order before each test."""
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

    def test_validate_order_success(self):
        """Test validating a valid order."""
        is_valid, error = self.processor.validate_order(self.sample_order)
        assert is_valid is True
        assert error is None

    def test_calculate_total_no_discount(self):
        """Test calculating total without discount."""
        result = self.processor.calculate_total(self.sample_order)
        assert result['subtotal'] == 20.0
        assert result['discount'] == 0.0
        assert result['tax'] > 0
```

### Run Coverage

```bash
pytest --cov=order_processor --cov-report=term-missing --cov-branch test_order_processor.py
```

You should see coverage around 40%. Your goal is to get it above 95%.

## Part 3: Achieve >95% Coverage (60 minutes)

Analyze the coverage report and write tests to cover untested code. Consider:

### Areas to Test

1. **Validation Edge Cases**

   - Empty order (no items)
   - Missing item fields (name, price, quantity)
   - Invalid prices (zero, negative)
   - Invalid quantities (zero, negative, >100)
   - Missing address fields
   - Invalid ZIP codes (wrong length, non-digit, invalid ZIP+4 format)
   - International addresses

2. **Shipping Calculations**

   - All shipping methods (STANDARD, EXPRESS, OVERNIGHT, INTERNATIONAL)
   - Free shipping threshold
   - Item count surcharges (>5 items, >10 items)
   - International surcharges
   - Different combinations

3. **Discount Logic**

   - All discount codes (SAVE10, SAVE20, SAVE30, FREESHIP)
   - Invalid discount codes
   - Null/empty discount codes
   - Case sensitivity and whitespace
   - FREESHIP special handling

4. **Total Calculations**

   - Various combinations of items, shipping, discounts
   - Edge case: discount larger than subtotal
   - Tax calculations

5. **Process Order**

   - Invalid orders (validation failures)
   - Valid orders with various configurations
   - Status updates

6. **Delivery Estimation**
   - All shipping methods
   - US vs international addresses
   - Date calculations

### Your Tasks

1. **Analyze coverage gaps** - Identify which lines and branches aren't covered
2. **Write comprehensive tests** - Cover all paths through the code
3. **Test edge cases** - Don't just test happy paths
4. **Verify behavior** - Make sure the code does what it should
5. **Achieve >95% coverage** - Both statement and branch coverage

### Example Tests to Get You Started

```python
def test_validate_order_empty_items(self):
    """Test validation fails for order with no items."""
    order = Order("ORD-002", "CUST-001", [], self.sample_order.shipping_address)
    is_valid, error = self.processor.validate_order(order)
    assert is_valid is False
    assert "at least one item" in error

def test_validate_order_missing_item_name(self):
    """Test validation fails for item without name."""
    order = Order(
        "ORD-002",
        "CUST-001",
        [{'price': 10.0, 'quantity': 1}],
        self.sample_order.shipping_address
    )
    is_valid, error = self.processor.validate_order(order)
    assert is_valid is False
    assert "missing name" in error

def test_calculate_shipping_free_over_threshold(self):
    """Test free shipping for orders over threshold."""
    # Create order with items totaling > $50
    order = Order(
        "ORD-003",
        "CUST-001",
        [{'name': 'Expensive Widget', 'price': 60.0, 'quantity': 1}],
        self.sample_order.shipping_address
    )

    shipping = self.processor.calculate_shipping(order, ShippingMethod.STANDARD)
    assert shipping == 0.0

def test_apply_discount_save20(self):
    """Test applying SAVE20 discount code."""
    discount, error = self.processor.apply_discount(100.0, 'SAVE20')
    assert discount == 20.0
    assert error is None

def test_apply_discount_invalid_code(self):
    """Test invalid discount code returns error."""
    discount, error = self.processor.apply_discount(100.0, 'INVALID')
    assert discount == 0.0
    assert "Invalid discount code" in error
```

## Part 4: Verify and Analyze (10 minutes)

### Check Your Coverage

```bash
pytest --cov=order_processor --cov-report=html --cov-branch test_order_processor.py
```

Open `htmlcov/index.html` and verify:

- Statement coverage >95%
- Branch coverage >95%
- No critical paths left untested

### Reflect on Coverage

Consider these questions:

1. Did you achieve high coverage without sacrificing test quality?
2. Are there any branches that are hard or impossible to test?
3. Would you feel confident deploying this code?
4. What's the difference between high coverage and good testing?

## Evaluation Criteria

Your solution will be evaluated on:

- **Coverage Achievement**: >95% statement and branch coverage
- **Test Quality**: Tests are meaningful, not just coverage padding
- **Edge Case Coverage**: All edge cases identified and tested
- **Code Organization**: Tests are well-organized and readable
- **Test Independence**: Tests don't depend on each other
- **Assertion Quality**: Tests verify correct behavior, not just execution

## Common Mistakes to Avoid

1. **Writing tests just for coverage** - Tests should verify behavior
2. **Not testing error paths** - Validation and error handling need testing
3. **Ignoring branch coverage** - Statement coverage alone is insufficient
4. **Not testing edge cases** - Boundaries and special values are critical
5. **Copy-paste tests** - Use parametrize or helper functions for similar tests
6. **Over-complicated tests** - Keep tests simple and focused

## Tips for Success

- Use coverage report to guide your testing, not dictate it
- Test one method at a time to see coverage increase
- Use pytest.mark.parametrize for testing multiple similar cases
- Group related tests in classes
- Use descriptive test names
- Write tests for behavior, not implementation
- Don't obsess over 100% - focus on meaningful coverage

## Advanced: Using Parametrize

```python
@pytest.mark.parametrize("code,expected_discount", [
    ('SAVE10', 10.0),
    ('SAVE20', 20.0),
    ('SAVE30', 30.0),
    ('save10', 10.0),  # Test case insensitivity
    ('  SAVE10  ', 10.0),  # Test whitespace handling
])
def test_discount_codes(code, expected_discount):
    """Test various discount codes."""
    processor = OrderProcessor()
    discount, error = processor.apply_discount(100.0, code)
    assert discount == expected_discount
    assert error is None
```

## Submission

Submit the following files:

- `test_order_processor.py` - Your comprehensive test suite
- Screenshot showing >95% statement and branch coverage
- Brief reflection (200 words): What did you learn about coverage metrics? Are there diminishing returns?

## Reflection Questions

1. How many tests did you write to achieve >95% coverage?
2. Were there any paths that were difficult to test? Why?
3. Is high coverage the same as good testing?
4. What percentage of coverage do you think is reasonable for production code?
5. Can you have high coverage but poor tests? How?

## Next Steps

After completing this exercise:

- Complete [Homework 5](../homework/homework-5.md)
- Review all Module 5 theory materials
- Prepare for [Module 6: Test Driven Development](../../06-test-driven-development/README.md)
- Consider: When is 95% coverage too much? When is it not enough?
