# Exercise 6: Comprehensive Black Box Testing

**Module**: 4 - Black Box Testing  
**Difficulty**: Advanced  
**Time**: 90 minutes

---

## 🎯 Objectives

Apply all black box testing techniques to a complex, real-world scenario.

By completing this exercise, you will:

- Combine Equivalence Partitioning, BVA, Decision Tables, and State Transitions
- Know when to apply each technique
- Create comprehensive test coverage
- Build a complete test suite for a complex system
- Demonstrate mastery of black box testing

---

## The Challenge: E-Commerce Shopping Cart System

You are testing a complete e-commerce shopping cart with:

- Product catalog with categories and pricing tiers
- Shopping cart with quantity management
- Discount codes and promotional rules
- Shipping cost calculation
- Tax calculation
- Order state management
- Payment processing

This is a **comprehensive scenario** requiring all 4 black box techniques.

---

## System Requirements

### 1. Product Catalog

**Product Types**:

- **Digital** (e-books, software): No shipping, instant delivery
- **Physical Small** (books, toys): Weight 0-5 lbs, standard shipping
- **Physical Large** (furniture, appliances): Weight 5-50 lbs, special shipping
- **Perishable** (food): Expedited shipping required, no returns

**Price Ranges**:

- Budget: $0.01 - $25.00
- Standard: $25.01 - $100.00
- Premium: $100.01 - $500.00
- Luxury: $500.01+

**Stock Status**:

- In Stock (quantity > 10): Available
- Low Stock (quantity 1-10): Limited availability warning
- Out of Stock (quantity 0): Add to waitlist
- Discontinued: Cannot be ordered

### 2. Shopping Cart Rules

**Quantity Limits**:

- Digital: 1-10 per product
- Physical Small: 1-99 per product
- Physical Large: 1-20 per product
- Perishable: 1-50 per product

**Cart Limits**:

- Maximum items in cart: 100 total items
- Maximum unique products: 50
- Maximum cart value: $50,000

**Business Rules**:

- Cannot mix perishable with other types (separate orders)
- Perishable items expire in cart after 30 minutes
- Cart saved for 30 days for registered users
- Guest carts expire after 24 hours

### 3. Discount System

**Discount Types**:

**Percentage Discounts**:

- 5% off: Orders $100-$249
- 10% off: Orders $250-$499
- 15% off: Orders $500-$999
- 20% off: Orders $1000+

**Discount Codes**:

- **WELCOME10**: 10% off first order (new customers only)
- **SUMMER25**: 25% off, expires 2026-08-31
- **FREESHIP**: Free shipping on orders $50+
- **BULK20**: 20% off when buying 10+ of same item

**Discount Rules**:

- Only one discount code per order
- Percentage discounts apply before discount codes
- Discount codes cannot be combined
- Free shipping overrides calculated shipping
- Discounts apply to subtotal (before tax and shipping)

### 4. Shipping Calculation

**Shipping Methods**:

| Method          | Speed     | Base Cost | Cost per lb | Max Weight |
| --------------- | --------- | --------- | ----------- | ---------- |
| Standard Ground | 5-7 days  | $5.00     | $0.50       | 50 lbs     |
| Express         | 2-3 days  | $15.00    | $1.00       | 50 lbs     |
| Overnight       | 1 day     | $30.00    | $2.00       | 30 lbs     |
| Freight         | 7-14 days | $50.00    | $0.25       | 500 lbs    |

**Shipping Zones** (multiplier on cost):

- Zone 1 (Local): ×1.0
- Zone 2 (Regional): ×1.3
- Zone 3 (National): ×1.6
- Zone 4 (International): ×2.5

**Special Cases**:

- Digital products: $0 shipping
- Perishable: Express or Overnight only
- Free shipping with FREESHIP code or orders $100+
- Cannot ship Physical Large to International

### 5. Tax Calculation

**Tax Rates by State**:

- California: 9.5%
- New York: 8.875%
- Texas: 8.25%
- Florida: 7.0%
- Oregon: 0% (no sales tax)

**Tax Rules**:

- Tax calculated on subtotal + shipping
- Digital products: Tax only in customer state
- Physical products: Tax based on shipping destination
- No tax on international orders

### 6. Order State Machine

**States**:

1. **Empty** - No items in cart
2. **Active** - Items in cart, not checked out
3. **Checkout** - Customer on checkout page
4. **Payment** - Payment processing
5. **Confirmed** - Payment successful
6. **Failed** - Payment failed
7. **Cancelled** - Order cancelled

**Events**:

- `add_item()` - Add product to cart
- `remove_item()` - Remove product from cart
- `update_quantity()` - Change item quantity
- `apply_discount()` - Apply discount code
- `proceed_to_checkout()` - Start checkout
- `submit_payment()` - Submit payment
- `payment_success()` - Payment approved
- `payment_failure()` - Payment declined
- `cancel_order()` - Cancel order

### 7. Payment Processing

**Payment Methods**:

- Credit Card (Visa, Mastercard, Amex)
- PayPal
- Apple Pay
- Gift Card

**Payment Rules**:

- Credit Card: Min $1, Max $10,000 per transaction
- PayPal: Min $1, Max $5,000 per transaction
- Apple Pay: Min $1, Max $2,000 per transaction
- Gift Card: Can be combined with other methods

**Validation**:

- Credit card number: 13-19 digits
- CVV: 3 digits (4 for Amex)
- Expiration: Must be future date
- Billing address required

---

## Part 1: Equivalence Partitioning (20 points)

### Task

Identify equivalence classes for:

1. **Product Types** (Digital, Physical Small, Physical Large, Perishable)
2. **Price Ranges** (Budget, Standard, Premium, Luxury)
3. **Quantity per Product Type**
4. **Discount Code Validity** (valid, expired, invalid, used)
5. **Shipping Zones** (1-4)
6. **Payment Methods** (Credit Card, PayPal, Apple Pay, Gift Card)

### Deliverable

Create a table:

| Input Dimension | Partition ID | Description            | Type  | Test Value               |
| --------------- | ------------ | ---------------------- | ----- | ------------------------ |
| Product Type    | P1           | Digital product        | Valid | E-book ($15)             |
| Product Type    | P2           | Physical Small         | Valid | Book ($20, 2 lbs)        |
| Product Type    | P3           | Physical Large         | Valid | Chair ($300, 25 lbs)     |
| Product Type    | P4           | Perishable             | Valid | Fresh fruit ($10, 3 lbs) |
| Price Range     | PR1          | Budget ($0.01-$25)     | Valid | $15.00                   |
| Price Range     | PR2          | Standard ($25.01-$100) | Valid | $50.00                   |
| ...             | ...          | ...                    | ...   | ...                      |

**Complete the table** for all 6 dimensions.

---

## Part 2: Boundary Value Analysis (25 points)

### Task

Identify and test boundary values for:

1. **Product Quantity Limits** (for each product type)
2. **Cart Value Limits** ($0, $100, $250, $500, $1000, $50,000)
3. **Shipping Weight Limits** (by method)
4. **Discount Thresholds** ($100, $250, $500, $1000)
5. **Credit Card Number Length** (13-19 digits)
6. **Cart Time Limits** (30 min for perishable, 24 hrs for guest)

### Deliverable

Create boundary test cases:

| Test ID | Boundary       | Below  | At Min  | Above Min | Nominal | Below Max | At Max  | Above Max | Expected        |
| ------- | -------------- | ------ | ------- | --------- | ------- | --------- | ------- | --------- | --------------- |
| BVA_01  | Digital Qty    | 0      | 1       | 2         | 5       | 9         | 10      | 11        | Error at 0,11   |
| BVA_02  | Discount $100  | $99.99 | $100.00 | $100.01   | -       | -         | -       | -         | 5% at 100+      |
| BVA_03  | Cart Max Value | -      | -       | -         | $25,000 | $49,999   | $50,000 | $50,001   | Error at 50,001 |
| ...     | ...            | ...    | ...     | ...       | ...     | ...       | ...     | ...       | ...             |

**Create at least 20 boundary test cases.**

---

## Part 3: Decision Tables (25 points)

### Task

Create decision tables for:

1. **Shipping Method Selection**

   - Conditions: Product type, weight, zone, urgency
   - Actions: Available methods, cost calculation, restrictions

2. **Discount Application**

   - Conditions: Order value, discount code, customer type, previous orders
   - Actions: Apply percentage, apply code, deny discount, error message

3. **Order Validation**
   - Conditions: Cart value, payment method, shipping address, stock availability
   - Actions: Proceed to payment, show error, request update

### Deliverable

**Example for Shipping Method Selection**:

| Rule #               | 1   | 2   | 3   | 4   | 5   | 6   | ... |
| -------------------- | --- | --- | --- | --- | --- | --- | --- |
| **Conditions**       |
| Product = Digital    | T   | F   | F   | F   | F   | F   | ... |
| Product = Perishable | F   | T   | T   | F   | F   | F   | ... |
| Weight > 30 lbs      | -   | F   | F   | -   | T   | F   | ... |
| Zone = International | -   | -   | -   | T   | -   | F   | ... |
| Urgency = Overnight  | -   | T   | F   | -   | -   | -   | ... |
| **Actions**          |
| Offer Standard       | -   | -   | X   | -   | -   | X   | ... |
| Offer Express        | -   | X   | X   | -   | -   | X   | ... |
| Offer Overnight      | -   | X   | -   | -   | -   | X   | ... |
| Offer Freight        | -   | -   | -   | -   | X   | -   | ... |
| Show Error           | -   | -   | -   | X   | -   | -   | ... |
| Free Shipping        | X   | -   | -   | -   | -   | -   | ... |

**Create complete decision tables** for all 3 scenarios (at least 30 rules total).

---

## Part 4: State Transition Testing (30 points)

### Task

1. **Create State Diagram** for cart/order lifecycle
2. **Create State Transition Table** with all valid and invalid transitions
3. **Identify critical paths** through the state machine
4. **Test invalid transitions** that should be rejected

### Deliverable

**State Transition Table**:

| Test ID | Current State | Event                 | Next State            | Actions                         | Valid? |
| ------- | ------------- | --------------------- | --------------------- | ------------------------------- | ------ |
| ST_01   | Empty         | add_item()            | Active                | Add product, initialize cart    | Yes    |
| ST_02   | Active        | add_item()            | Active                | Add product, update totals      | Yes    |
| ST_03   | Active        | remove_item()         | Active or Empty       | Remove product, update totals   | Yes    |
| ST_04   | Active        | proceed_to_checkout() | Checkout              | Validate cart, calculate totals | Yes    |
| ST_05   | Checkout      | submit_payment()      | Payment               | Process payment                 | Yes    |
| ST_06   | Payment       | payment_success()     | Confirmed             | Create order, send confirmation | Yes    |
| ST_07   | Payment       | payment_failure()     | Failed                | Log failure, show error         | Yes    |
| ST_08   | Failed        | retry_payment()       | Payment               | Allow retry                     | Yes    |
| ST_09   | Confirmed     | cancel_order()        | Confirmed (no change) | Error: Cannot cancel            | No     |
| ST_10   | Empty         | proceed_to_checkout() | Empty (no change)     | Error: Cart is empty            | No     |
| ST_11   | Active        | payment_success()     | Active (no change)    | Error: Invalid transition       | No     |
| ...     | ...           | ...                   | ...                   | ...                             | ...    |

**Create at least 25 state transitions** (valid and invalid).

**State Diagram** (ASCII or drawn):

```
     [Empty]
        |
        | add_item()
        v
    [Active] <----+
        |         |
        | remove_item() (if items remain)
        |         |
        +---------+
        |
        | proceed_to_checkout()
        v
   [Checkout]
        |
        | submit_payment()
        v
    [Payment]
        |
        +-- payment_success() --> [Confirmed]
        |
        +-- payment_failure() --> [Failed]
                                      |
                                      | retry_payment()
                                      v
                                  [Payment]
```

---

## Part 5: Integration - Complete Test Suite (50 points)

### Task

Create a **comprehensive test suite** that combines all techniques. For the following scenario, apply the appropriate technique(s):

**Scenario**: Customer purchases multiple items with a discount code

**Test Steps**:

1. Add Digital product ($15) - quantity 2 - **Use EP for product type**
2. Add Physical Small product ($45) - quantity 5 - **Use BVA for quantity**
3. Apply discount code "WELCOME10" - **Use Decision Table for discount eligibility**
4. Verify subtotal, discount, tax, shipping - **Use BVA for calculation boundaries**
5. Proceed to checkout - **Use State Transition**
6. Enter payment information - **Use EP for payment method**
7. Submit order - **Use State Transition**
8. Verify order confirmation - **All techniques**

### Deliverable

**Implementation** (Python or JavaScript) with:

1. **Complete shopping cart system** implementing all requirements
2. **Test suite** covering all techniques
3. **Coverage report** showing:
   - Partition coverage
   - Boundary coverage
   - Decision table rule coverage
   - State transition coverage

---

## Implementation Guide

### Python Implementation

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

# ============================================================================
# Data Models
# ============================================================================

class ProductType(Enum):
    DIGITAL = "Digital"
    PHYSICAL_SMALL = "Physical Small"
    PHYSICAL_LARGE = "Physical Large"
    PERISHABLE = "Perishable"

class PriceRange(Enum):
    BUDGET = "Budget"
    STANDARD = "Standard"
    PREMIUM = "Premium"
    LUXURY = "Luxury"

class CartState(Enum):
    EMPTY = "Empty"
    ACTIVE = "Active"
    CHECKOUT = "Checkout"
    PAYMENT = "Payment"
    CONFIRMED = "Confirmed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"

@dataclass
class Product:
    id: str
    name: str
    product_type: ProductType
    price: float
    weight: float  # in pounds
    stock: int

@dataclass
class CartItem:
    product: Product
    quantity: int
    added_at: datetime

@dataclass
class DiscountCode:
    code: str
    discount_percent: float
    valid_until: Optional[datetime]
    conditions: Dict

class ShippingMethod(Enum):
    STANDARD = "Standard Ground"
    EXPRESS = "Express"
    OVERNIGHT = "Overnight"
    FREIGHT = "Freight"

# ============================================================================
# Shopping Cart Implementation
# ============================================================================

class ShoppingCart:
    def __init__(self, customer_id: Optional[str] = None):
        self.customer_id = customer_id
        self.items: List[CartItem] = []
        self.state = CartState.EMPTY
        self.discount_code: Optional[DiscountCode] = None
        self.created_at = datetime.now()
        self.shipping_zone = 1
        self.shipping_state = "CA"
        self.history = []

    # ========================================================================
    # Part 1: Equivalence Partitioning - Product Type Validation
    # ========================================================================

    def validate_product_type(self, product: Product) -> Tuple[bool, str]:
        """Validate product type constraints."""
        # Check if mixing perishable with other types
        if product.product_type == ProductType.PERISHABLE:
            for item in self.items:
                if item.product.product_type != ProductType.PERISHABLE:
                    return False, "Cannot mix perishable items with other products"
        elif any(item.product.product_type == ProductType.PERISHABLE for item in self.items):
            return False, "Cannot mix perishable items with other products"

        return True, ""

    def get_price_range(self, price: float) -> PriceRange:
        """Determine price range category (EP)."""
        if price <= 25.00:
            return PriceRange.BUDGET
        elif price <= 100.00:
            return PriceRange.STANDARD
        elif price <= 500.00:
            return PriceRange.PREMIUM
        else:
            return PriceRange.LUXURY

    # ========================================================================
    # Part 2: Boundary Value Analysis - Quantity Limits
    # ========================================================================

    def validate_quantity(self, product: Product, quantity: int) -> Tuple[bool, str]:
        """Validate quantity is within bounds (BVA)."""
        limits = {
            ProductType.DIGITAL: (1, 10),
            ProductType.PHYSICAL_SMALL: (1, 99),
            ProductType.PHYSICAL_LARGE: (1, 20),
            ProductType.PERISHABLE: (1, 50)
        }

        min_qty, max_qty = limits[product.product_type]

        if quantity < min_qty:
            return False, f"Minimum quantity is {min_qty}"
        if quantity > max_qty:
            return False, f"Maximum quantity is {max_qty}"

        # Check stock
        if quantity > product.stock:
            return False, f"Only {product.stock} in stock"

        return True, ""

    def validate_cart_limits(self) -> Tuple[bool, str]:
        """Validate cart-level limits (BVA)."""
        total_items = sum(item.quantity for item in self.items)
        unique_products = len(self.items)
        cart_value = self.calculate_subtotal()

        if total_items > 100:
            return False, "Maximum 100 items in cart"
        if unique_products > 50:
            return False, "Maximum 50 different products"
        if cart_value > 50000:
            return False, "Maximum cart value is $50,000"

        return True, ""

    # ========================================================================
    # Part 3: State Transitions
    # ========================================================================

    def add_item(self, product: Product, quantity: int) -> Tuple[bool, str]:
        """Add item to cart (state transition: Empty/Active → Active)."""
        # Validate quantity (BVA)
        valid, msg = self.validate_quantity(product, quantity)
        if not valid:
            return False, msg

        # Validate product type mixing (EP)
        valid, msg = self.validate_product_type(product)
        if not valid:
            return False, msg

        # Add item
        cart_item = CartItem(product, quantity, datetime.now())
        self.items.append(cart_item)

        # State transition
        old_state = self.state
        self.state = CartState.ACTIVE
        self.history.append((old_state, CartState.ACTIVE, "add_item"))

        # Validate cart limits (BVA)
        valid, msg = self.validate_cart_limits()
        if not valid:
            # Rollback
            self.items.pop()
            self.state = old_state
            return False, msg

        return True, f"Added {quantity}x {product.name}"

    def remove_item(self, product_id: str) -> Tuple[bool, str]:
        """Remove item from cart."""
        if self.state not in [CartState.ACTIVE, CartState.CHECKOUT]:
            return False, f"Cannot remove items in {self.state.value} state"

        self.items = [item for item in self.items if item.product.id != product_id]

        # State transition to EMPTY if no items
        if len(self.items) == 0:
            old_state = self.state
            self.state = CartState.EMPTY
            self.history.append((old_state, CartState.EMPTY, "remove_item"))

        return True, "Item removed"

    def proceed_to_checkout(self) -> Tuple[bool, str]:
        """Transition to checkout state."""
        if self.state != CartState.ACTIVE:
            return False, f"Cannot checkout from {self.state.value} state"

        if len(self.items) == 0:
            return False, "Cart is empty"

        # Check perishable expiration
        for item in self.items:
            if item.product.product_type == ProductType.PERISHABLE:
                age = datetime.now() - item.added_at
                if age > timedelta(minutes=30):
                    return False, "Perishable items have expired"

        old_state = self.state
        self.state = CartState.CHECKOUT
        self.history.append((old_state, CartState.CHECKOUT, "proceed_to_checkout"))

        return True, "Proceeding to checkout"

    def submit_payment(self, payment_method: str, amount: float) -> Tuple[bool, str]:
        """Submit payment (transition to PAYMENT state)."""
        if self.state != CartState.CHECKOUT:
            return False, f"Cannot submit payment from {self.state.value} state"

        total = self.calculate_total()
        if abs(amount - total) > 0.01:
            return False, f"Payment amount ${amount:.2f} does not match total ${total:.2f}"

        old_state = self.state
        self.state = CartState.PAYMENT
        self.history.append((old_state, CartState.PAYMENT, "submit_payment"))

        return True, "Processing payment"

    def payment_success(self) -> Tuple[bool, str]:
        """Payment approved (transition to CONFIRMED)."""
        if self.state != CartState.PAYMENT:
            return False, f"Invalid transition from {self.state.value}"

        old_state = self.state
        self.state = CartState.CONFIRMED
        self.history.append((old_state, CartState.CONFIRMED, "payment_success"))

        return True, "Order confirmed"

    def payment_failure(self, reason: str) -> Tuple[bool, str]:
        """Payment declined (transition to FAILED)."""
        if self.state != CartState.PAYMENT:
            return False, f"Invalid transition from {self.state.value}"

        old_state = self.state
        self.state = CartState.FAILED
        self.history.append((old_state, CartState.FAILED, "payment_failure"))

        return True, f"Payment failed: {reason}"

    def cancel_order(self) -> Tuple[bool, str]:
        """Cancel order."""
        if self.state in [CartState.CONFIRMED, CartState.PAYMENT]:
            return False, "Cannot cancel order in current state"

        if self.state in [CartState.ACTIVE, CartState.CHECKOUT, CartState.FAILED]:
            old_state = self.state
            self.state = CartState.CANCELLED
            self.history.append((old_state, CartState.CANCELLED, "cancel_order"))
            return True, "Order cancelled"

        return False, f"Cannot cancel from {self.state.value} state"

    # ========================================================================
    # Part 4: Decision Tables - Discount Application
    # ========================================================================

    def apply_discount_code(self, code: str) -> Tuple[bool, str]:
        """Apply discount code using decision table logic."""
        # TODO: Implement discount code lookup
        # For now, hardcode test codes

        discount_codes = {
            "WELCOME10": DiscountCode("WELCOME10", 10.0, None, {"new_customer": True}),
            "SUMMER25": DiscountCode("SUMMER25", 25.0, datetime(2026, 8, 31), {}),
            "FREESHIP": DiscountCode("FREESHIP", 0, None, {"free_shipping": True}),
            "BULK20": DiscountCode("BULK20", 20.0, None, {"min_same_item": 10})
        }

        if code not in discount_codes:
            return False, "Invalid discount code"

        discount = discount_codes[code]

        # Check expiration
        if discount.valid_until and datetime.now() > discount.valid_until:
            return False, "Discount code has expired"

        # Check conditions
        if "new_customer" in discount.conditions:
            # TODO: Check if customer is new
            pass

        if "min_same_item" in discount.conditions:
            min_qty = discount.conditions["min_same_item"]
            has_qualifying_item = any(item.quantity >= min_qty for item in self.items)
            if not has_qualifying_item:
                return False, f"Need {min_qty}+ of same item for this discount"

        self.discount_code = discount
        return True, f"Discount code applied: {discount.discount_percent}% off"

    # ========================================================================
    # Part 5: Calculations with BVA
    # ========================================================================

    def calculate_subtotal(self) -> float:
        """Calculate subtotal before discounts."""
        return sum(item.product.price * item.quantity for item in self.items)

    def calculate_volume_discount(self) -> float:
        """Calculate automatic volume discount based on order value (BVA)."""
        subtotal = self.calculate_subtotal()

        # Decision table for volume discounts
        if subtotal >= 1000:
            return 0.20
        elif subtotal >= 500:
            return 0.15
        elif subtotal >= 250:
            return 0.10
        elif subtotal >= 100:
            return 0.05
        else:
            return 0.0

    def calculate_discount(self) -> float:
        """Calculate total discount amount."""
        subtotal = self.calculate_subtotal()

        # Volume discount
        volume_discount = self.calculate_volume_discount()
        discount_amount = subtotal * volume_discount

        # Discount code
        if self.discount_code:
            code_discount = subtotal * (self.discount_code.discount_percent / 100.0)
            # Take whichever is greater (or only code discount, based on rules)
            # For now: volume discount + code discount (check requirements)
            discount_amount += code_discount

        return discount_amount

    def calculate_shipping(self) -> float:
        """Calculate shipping cost using decision table."""
        # Digital products: free shipping
        if all(item.product.product_type == ProductType.DIGITAL for item in self.items):
            return 0.0

        # Free shipping code or order over $100
        if self.discount_code and "free_shipping" in self.discount_code.conditions:
            return 0.0
        if self.calculate_subtotal() >= 100:
            return 0.0

        # Calculate based on weight and zone
        total_weight = sum(item.product.weight * item.quantity for item in self.items
                          if item.product.product_type != ProductType.DIGITAL)

        # Determine shipping method (simplified)
        # Use Standard for most, Express for perishable
        has_perishable = any(item.product.product_type == ProductType.PERISHABLE
                            for item in self.items)

        if has_perishable:
            base = 15.00
            per_lb = 1.00
        else:
            base = 5.00
            per_lb = 0.50

        shipping_cost = base + (total_weight * per_lb)

        # Apply zone multiplier
        zone_multipliers = {1: 1.0, 2: 1.3, 3: 1.6, 4: 2.5}
        shipping_cost *= zone_multipliers.get(self.shipping_zone, 1.0)

        return shipping_cost

    def calculate_tax(self) -> float:
        """Calculate tax based on state."""
        tax_rates = {
            "CA": 0.095,
            "NY": 0.08875,
            "TX": 0.0825,
            "FL": 0.07,
            "OR": 0.0
        }

        rate = tax_rates.get(self.shipping_state, 0.0)
        subtotal = self.calculate_subtotal() - self.calculate_discount()
        shipping = self.calculate_shipping()

        return (subtotal + shipping) * rate

    def calculate_total(self) -> float:
        """Calculate final total."""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        shipping = self.calculate_shipping()
        tax = self.calculate_tax()

        return subtotal - discount + shipping + tax

    def get_state(self) -> CartState:
        return self.state


# ============================================================================
# COMPREHENSIVE TEST SUITE
# ============================================================================

def test_ep_product_types():
    """EP: Test each product type equivalence class."""
    cart = ShoppingCart("customer1")

    # P1: Digital product
    digital = Product("D1", "E-book", ProductType.DIGITAL, 15.0, 0, 100)
    success, msg = cart.add_item(digital, 2)
    assert success == True

    # P2: Physical Small
    cart2 = ShoppingCart("customer2")
    physical_small = Product("PS1", "Book", ProductType.PHYSICAL_SMALL, 20.0, 2.0, 50)
    success, msg = cart2.add_item(physical_small, 5)
    assert success == True

    # P3: Physical Large
    cart3 = ShoppingCart("customer3")
    physical_large = Product("PL1", "Chair", ProductType.PHYSICAL_LARGE, 300.0, 25.0, 10)
    success, msg = cart3.add_item(physical_large, 1)
    assert success == True

    # P4: Perishable
    cart4 = ShoppingCart("customer4")
    perishable = Product("PE1", "Fruit", ProductType.PERISHABLE, 10.0, 3.0, 20)
    success, msg = cart4.add_item(perishable, 5)
    assert success == True


def test_ep_cannot_mix_perishable():
    """EP: Invalid partition - mixing perishable with other types."""
    cart = ShoppingCart("customer5")

    # Add physical product first
    physical = Product("PS1", "Book", ProductType.PHYSICAL_SMALL, 20.0, 2.0, 50)
    cart.add_item(physical, 1)

    # Try to add perishable (should fail)
    perishable = Product("PE1", "Fruit", ProductType.PERISHABLE, 10.0, 3.0, 20)
    success, msg = cart.add_item(perishable, 1)
    assert success == False
    assert "Cannot mix perishable" in msg


def test_bva_digital_quantity_boundaries():
    """BVA: Test digital product quantity boundaries (1-10)."""
    cart = ShoppingCart("customer6")
    digital = Product("D1", "Software", ProductType.DIGITAL, 50.0, 0, 100)

    # Below minimum (0)
    success, msg = cart.add_item(digital, 0)
    assert success == False

    # At minimum (1)
    success, msg = cart.add_item(digital, 1)
    assert success == True
    cart.items.clear()  # Reset

    # Above minimum (2)
    success, msg = cart.add_item(digital, 2)
    assert success == True
    cart.items.clear()

    # Below maximum (9)
    success, msg = cart.add_item(digital, 9)
    assert success == True
    cart.items.clear()

    # At maximum (10)
    success, msg = cart.add_item(digital, 10)
    assert success == True
    cart.items.clear()

    # Above maximum (11)
    success, msg = cart.add_item(digital, 11)
    assert success == False


def test_bva_discount_thresholds():
    """BVA: Test discount threshold boundaries ($100, $250, $500, $1000)."""
    cart = ShoppingCart("customer7")

    # Helper to add products worth specific amount
    def set_cart_value(value):
        cart.items.clear()
        product = Product("P1", "Item", ProductType.DIGITAL, value, 0, 100)
        cart.add_item(product, 1)

    # Below $100: 0% discount
    set_cart_value(99.99)
    assert cart.calculate_volume_discount() == 0.0

    # At $100: 5% discount
    set_cart_value(100.00)
    assert cart.calculate_volume_discount() == 0.05

    # Above $100: 5% discount
    set_cart_value(100.01)
    assert cart.calculate_volume_discount() == 0.05

    # At $250: 10% discount
    set_cart_value(250.00)
    assert cart.calculate_volume_discount() == 0.10

    # At $500: 15% discount
    set_cart_value(500.00)
    assert cart.calculate_volume_discount() == 0.15

    # At $1000: 20% discount
    set_cart_value(1000.00)
    assert cart.calculate_volume_discount() == 0.20


def test_state_transition_valid_flow():
    """State Transition: Test valid flow Empty → Active → Checkout → Payment → Confirmed."""
    cart = ShoppingCart("customer8")
    assert cart.get_state() == CartState.EMPTY

    # Empty → Active
    product = Product("P1", "Item", ProductType.DIGITAL, 50.0, 0, 100)
    success, msg = cart.add_item(product, 1)
    assert success == True
    assert cart.get_state() == CartState.ACTIVE

    # Active → Checkout
    success, msg = cart.proceed_to_checkout()
    assert success == True
    assert cart.get_state() == CartState.CHECKOUT

    # Checkout → Payment
    total = cart.calculate_total()
    success, msg = cart.submit_payment("Credit Card", total)
    assert success == True
    assert cart.get_state() == CartState.PAYMENT

    # Payment → Confirmed
    success, msg = cart.payment_success()
    assert success == True
    assert cart.get_state() == CartState.CONFIRMED


def test_state_transition_invalid_empty_to_checkout():
    """State Transition: Invalid - Empty → Checkout should fail."""
    cart = ShoppingCart("customer9")
    success, msg = cart.proceed_to_checkout()
    assert success == False
    assert cart.get_state() == CartState.EMPTY


def test_state_transition_invalid_confirmed_to_cancelled():
    """State Transition: Invalid - Confirmed → Cancelled should fail."""
    cart = ShoppingCart("customer10")

    # Get to confirmed state
    product = Product("P1", "Item", ProductType.DIGITAL, 50.0, 0, 100)
    cart.add_item(product, 1)
    cart.proceed_to_checkout()
    cart.submit_payment("Credit Card", cart.calculate_total())
    cart.payment_success()

    # Try to cancel (should fail)
    success, msg = cart.cancel_order()
    assert success == False
    assert cart.get_state() == CartState.CONFIRMED


def test_decision_table_shipping_digital():
    """Decision Table: Digital products → Free shipping."""
    cart = ShoppingCart("customer11")
    digital = Product("D1", "E-book", ProductType.DIGITAL, 15.0, 0, 100)
    cart.add_item(digital, 2)

    shipping = cart.calculate_shipping()
    assert shipping == 0.0


def test_decision_table_shipping_perishable():
    """Decision Table: Perishable → Express shipping required."""
    cart = ShoppingCart("customer12")
    perishable = Product("PE1", "Fruit", ProductType.PERISHABLE, 10.0, 3.0, 20)
    cart.add_item(perishable, 5)

    shipping = cart.calculate_shipping()
    # Should use Express rate: $15 base + ($1 × 15 lbs) = $30
    expected = 15.00 + (1.00 * 15.0)  # Zone 1 multiplier = 1.0
    assert abs(shipping - expected) < 0.01


def test_comprehensive_scenario():
    """Comprehensive: Full purchase flow with all techniques."""
    cart = ShoppingCart("customer13")

    # Step 1: Add digital product (EP: Digital type)
    digital = Product("D1", "E-book", ProductType.DIGITAL, 15.0, 0, 100)
    success, msg = cart.add_item(digital, 2)
    assert success == True

    # Step 2: Add physical product with boundary quantity (BVA: quantity = 5)
    physical = Product("PS1", "Book", ProductType.PHYSICAL_SMALL, 45.0, 2.0, 50)
    success, msg = cart.add_item(physical, 5)
    assert success == True

    # Step 3: Apply discount code (Decision Table: discount eligibility)
    success, msg = cart.apply_discount_code("WELCOME10")
    # May fail if not new customer, but let's assume it works

    # Step 4: Verify calculations (BVA: boundaries in totals)
    subtotal = cart.calculate_subtotal()
    assert subtotal == (15.0 * 2) + (45.0 * 5)  # 30 + 225 = 255

    volume_discount_rate = cart.calculate_volume_discount()
    assert volume_discount_rate == 0.10  # $255 is in $250-$499 range

    # Step 5: Proceed to checkout (State Transition)
    success, msg = cart.proceed_to_checkout()
    assert success == True
    assert cart.get_state() == CartState.CHECKOUT

    # Step 6: Submit payment (State Transition + EP: payment method)
    total = cart.calculate_total()
    success, msg = cart.submit_payment("Credit Card", total)
    assert success == True
    assert cart.get_state() == CartState.PAYMENT

    # Step 7: Payment success (State Transition)
    success, msg = cart.payment_success()
    assert success == True
    assert cart.get_state() == CartState.CONFIRMED

    # Step 8: Verify final state (All techniques applied)
    assert len(cart.history) >= 4  # Multiple state transitions recorded


# Run all tests
if __name__ == "__main__":
    print("Running comprehensive black box test suite...")
    print("\n=== Equivalence Partitioning Tests ===")
    test_ep_product_types()
    test_ep_cannot_mix_perishable()
    print("✓ EP tests passed")

    print("\n=== Boundary Value Analysis Tests ===")
    test_bva_digital_quantity_boundaries()
    test_bva_discount_thresholds()
    print("✓ BVA tests passed")

    print("\n=== State Transition Tests ===")
    test_state_transition_valid_flow()
    test_state_transition_invalid_empty_to_checkout()
    test_state_transition_invalid_confirmed_to_cancelled()
    print("✓ State transition tests passed")

    print("\n=== Decision Table Tests ===")
    test_decision_table_shipping_digital()
    test_decision_table_shipping_perishable()
    print("✓ Decision table tests passed")

    print("\n=== Comprehensive Integration Test ===")
    test_comprehensive_scenario()
    print("✓ Comprehensive test passed")

    print("\n🎉 All tests passed!")
```

---

## Deliverables

Submit:

1. **Part 1**: EP table with all partitions
2. **Part 2**: BVA table with 20+ boundary tests
3. **Part 3**: 3 complete decision tables (30+ rules total)
4. **Part 4**: State diagram + transition table (25+ transitions)
5. **Part 5**: Complete implementation with comprehensive test suite
6. **Coverage Report**:
   - Total partitions identified and tested
   - Total boundaries identified and tested
   - Total decision table rules and coverage
   - Total state transitions and coverage
   - Overall test coverage percentage

---

## Evaluation Criteria

| Criteria                     | Points | Description                                    |
| ---------------------------- | ------ | ---------------------------------------------- |
| **Equivalence Partitioning** | 20     | All partitions identified, tested              |
| **Boundary Value Analysis**  | 25     | All boundaries tested systematically           |
| **Decision Tables**          | 25     | Complete tables, all rules tested              |
| **State Transition Testing** | 30     | Complete diagram/table, all transitions tested |
| **Integration**              | 50     | Working implementation, comprehensive tests    |
| **Documentation**            | 15     | Clear analysis, technique selection rationale  |
| **Code Quality**             | 10     | Clean, maintainable, well-structured           |
| **Coverage**                 | 25     | High coverage across all techniques            |

**Total**: 200 points

---

## When to Use Which Technique

| Technique                    | Best For                                        | Example in This Exercise                                |
| ---------------------------- | ----------------------------------------------- | ------------------------------------------------------- |
| **Equivalence Partitioning** | Categorizing inputs into groups                 | Product types, payment methods, price ranges            |
| **Boundary Value Analysis**  | Testing min/max values, thresholds              | Quantity limits, discount thresholds, cart value limits |
| **Decision Tables**          | Complex business rules with multiple conditions | Shipping method selection, discount eligibility         |
| **State Transition**         | Systems with distinct states and transitions    | Cart lifecycle, order processing flow                   |

**Pro Tip**: Often you'll use multiple techniques together:

- EP to identify categories + BVA to test boundaries of each category
- Decision Table to define rules + State Transition to show when rules apply
- All techniques together for comprehensive coverage

---

## Common Mistakes to Avoid

❌ Using only one technique for the entire system  
✅ Apply the right technique for each requirement

❌ Testing features in isolation  
✅ Test integrated scenarios (like Part 5)

❌ Ignoring negative test cases  
✅ Test both valid and invalid inputs/transitions

❌ Not documenting technique selection rationale  
✅ Explain why you chose each technique

❌ Implementing before designing tests  
✅ Design test cases first, then implement

---

## Bonus Challenge

### Performance Testing Integration

Add performance considerations to your test suite:

1. **Load Testing**: Can the cart handle 1000 add_item() calls?
2. **Stress Testing**: What happens at exactly 100 items (boundary)?
3. **Timeout Testing**: Perishable items expire after 30 minutes
4. **Concurrent Access**: Multiple updates to same cart

Implement tests for these scenarios and document findings.

---

## Next Steps

After completing this exercise:

1. Review all Module 4 theory materials
2. Compare your approach with peers
3. Prepare for Module 4 assessment
4. Move to [Module 5: White Box Testing](../../05-white-box-testing/README.md)

---

## Reflection Questions

Answer these in your submission:

1. Which technique did you find most useful for this scenario? Why?
2. Where did you combine multiple techniques? What was the benefit?
3. What defects did you discover during testing?
4. If you had to reduce test count by 50%, which tests would you keep?
5. How would you prioritize these tests in a real project?

---

**Congratulations! You've completed comprehensive black box testing of a complex system. This is the level of thinking required for professional software testing.** 🎯🎉
