# Introduction to White Box Testing

**Module**: 5 - White Box Testing  
**Topic**: Unit & Integration Testing Fundamentals  
**Reading Time**: 30 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Distinguish between white box and black box testing approaches
- Understand when to use each testing approach
- Write effective unit tests using the AAA pattern
- Apply test isolation principles
- Create meaningful test names
- Understand integration testing fundamentals
- Apply the test pyramid concept to your testing strategy

---

## White Box vs Black Box Testing

### Black Box Testing

**Black box testing** treats the system as a "black box" - you cannot see inside. You only have access to:

- Inputs
- Outputs
- Requirements/specifications

**Focus**: Does the system do what it's supposed to do?

```
┌─────────────────┐
│                 │
│  Input  →  ?  → Output
│                 │
└─────────────────┘
```

**Example**: Testing a login function

```python
# Black box approach - don't care how it works internally
def test_login_with_valid_credentials():
    result = login("user@example.com", "password123")
    assert result.success == True
    assert result.user_id is not None
```

### White Box Testing

**White box testing** (also called **glass box** or **clear box** testing) looks inside the system. You have access to:

- Source code
- Internal structure
- Logic flow
- Data structures

**Focus**: Does the internal implementation work correctly?

```
┌─────────────────────────────┐
│ if user_exists():           │
│   if password_match():      │
│     create_session()        │
│     return success          │
│   else:                     │
│     return error            │
│ else:                       │
│   return error              │
└─────────────────────────────┘
```

**Example**: Testing internal logic paths

```python
# White box approach - test internal logic branches
def test_login_creates_session_on_success():
    user = create_test_user("user@example.com", "password123")
    result = login("user@example.com", "password123")

    # Verify internal behavior
    assert session_exists(user.id)
    assert get_session(user.id).expires_at > datetime.now()

def test_login_returns_specific_error_for_wrong_password():
    user = create_test_user("user@example.com", "password123")
    result = login("user@example.com", "wrong_password")

    assert result.error_code == "INVALID_PASSWORD"
    assert not session_exists(user.id)
```

---

## When to Use Each Approach

### Use Black Box Testing When:

1. **Testing from user perspective**: UI testing, API testing
2. **Requirements-based testing**: Validating specifications
3. **You don't have source code access**: Third-party libraries, external services
4. **Testing the contract**: Public API behavior

### Use White Box Testing When:

1. **Testing internal logic**: Algorithms, business rules
2. **Ensuring code coverage**: All branches, paths tested
3. **Unit testing**: Individual functions, classes
4. **Finding hidden bugs**: Edge cases in internal logic
5. **Refactoring**: Ensuring internal changes don't break behavior

### Best Practice: Use Both!

```
┌──────────────────────────────────────┐
│  Black Box Tests (User Perspective)  │
│  ↓                                    │
│  Integration Tests (Module Level)    │
│  ↓                                    │
│  White Box Tests (Code Level)        │
└──────────────────────────────────────┘
```

---

## Unit Testing Fundamentals

### What is a Unit Test?

A **unit test** verifies a small piece of code (a "unit") in isolation:

- A single function
- A single method
- A single class

### Characteristics of Good Unit Tests

1. **Fast**: Runs in milliseconds
2. **Isolated**: No dependencies on external systems
3. **Repeatable**: Same result every time
4. **Self-validating**: Pass or fail, no manual verification
5. **Timely**: Written close to when the code is written

### The AAA Pattern

**AAA** stands for **Arrange-Act-Assert**, a standard structure for writing clear unit tests.

```python
def test_calculate_discount():
    # Arrange - Set up test data
    original_price = 100
    discount_percentage = 20

    # Act - Execute the function being tested
    final_price = calculate_discount(original_price, discount_percentage)

    # Assert - Verify the result
    assert final_price == 80
```

```javascript
// JavaScript/Jest example
describe("calculate_discount", () => {
  test("applies 20% discount correctly", () => {
    // Arrange
    const originalPrice = 100;
    const discountPercentage = 20;

    // Act
    const finalPrice = calculateDiscount(originalPrice, discountPercentage);

    // Assert
    expect(finalPrice).toBe(80);
  });
});
```

### Breaking Down the AAA Pattern

#### 1. Arrange (Setup)

Prepare everything needed for the test:

```python
# Arrange
user = User(email="test@example.com", age=25)
product = Product(name="Laptop", price=1000)
cart = ShoppingCart(user=user)
cart.add_item(product)
```

#### 2. Act (Execute)

Call the function/method being tested:

```python
# Act
total = cart.calculate_total()
```

#### 3. Assert (Verify)

Check that the result matches expectations:

```python
# Assert
assert total == 1000
assert cart.item_count() == 1
```

### Complete Example: Python

```python
import pytest
from datetime import datetime, timedelta

class Subscription:
    def __init__(self, start_date, duration_days):
        self.start_date = start_date
        self.duration_days = duration_days

    def is_active(self, check_date):
        end_date = self.start_date + timedelta(days=self.duration_days)
        return self.start_date <= check_date <= end_date

# Unit tests using AAA pattern
def test_subscription_is_active_on_start_date():
    # Arrange
    start = datetime(2026, 1, 1)
    subscription = Subscription(start_date=start, duration_days=30)

    # Act
    is_active = subscription.is_active(start)

    # Assert
    assert is_active == True

def test_subscription_is_active_during_period():
    # Arrange
    start = datetime(2026, 1, 1)
    subscription = Subscription(start_date=start, duration_days=30)
    check_date = datetime(2026, 1, 15)

    # Act
    is_active = subscription.is_active(check_date)

    # Assert
    assert is_active == True

def test_subscription_is_not_active_before_start():
    # Arrange
    start = datetime(2026, 1, 1)
    subscription = Subscription(start_date=start, duration_days=30)
    check_date = datetime(2025, 12, 31)

    # Act
    is_active = subscription.is_active(check_date)

    # Assert
    assert is_active == False

def test_subscription_is_not_active_after_end():
    # Arrange
    start = datetime(2026, 1, 1)
    subscription = Subscription(start_date=start, duration_days=30)
    check_date = datetime(2026, 2, 1)  # Day 32

    # Act
    is_active = subscription.is_active(check_date)

    # Assert
    assert is_active == False
```

### Complete Example: JavaScript

```javascript
// subscription.js
class Subscription {
  constructor(startDate, durationDays) {
    this.startDate = startDate;
    this.durationDays = durationDays;
  }

  isActive(checkDate) {
    const endDate = new Date(this.startDate);
    endDate.setDate(endDate.getDate() + this.durationDays);

    return checkDate >= this.startDate && checkDate <= endDate;
  }
}

// subscription.test.js
describe("Subscription", () => {
  test("is active on start date", () => {
    // Arrange
    const start = new Date("2026-01-01");
    const subscription = new Subscription(start, 30);

    // Act
    const isActive = subscription.isActive(start);

    // Assert
    expect(isActive).toBe(true);
  });

  test("is active during subscription period", () => {
    // Arrange
    const start = new Date("2026-01-01");
    const subscription = new Subscription(start, 30);
    const checkDate = new Date("2026-01-15");

    // Act
    const isActive = subscription.isActive(checkDate);

    // Assert
    expect(isActive).toBe(true);
  });

  test("is not active before start date", () => {
    // Arrange
    const start = new Date("2026-01-01");
    const subscription = new Subscription(start, 30);
    const checkDate = new Date("2025-12-31");

    // Act
    const isActive = subscription.isActive(checkDate);

    // Assert
    expect(isActive).toBe(false);
  });

  test("is not active after end date", () => {
    // Arrange
    const start = new Date("2026-01-01");
    const subscription = new Subscription(start, 30);
    const checkDate = new Date("2026-02-01");

    // Act
    const isActive = subscription.isActive(checkDate);

    // Assert
    expect(isActive).toBe(false);
  });
});
```

---

## Test Isolation

### Why Isolation Matters

Tests should be **independent** - they should not affect each other.

**Problem**: Tests that depend on execution order

```python
# ❌ BAD - Tests depend on shared state
user_count = 0

def test_create_user():
    global user_count
    create_user("alice@example.com")
    user_count += 1
    assert user_count == 1

def test_create_another_user():
    global user_count
    create_user("bob@example.com")
    user_count += 1
    assert user_count == 2  # Fails if run alone!
```

**Solution**: Each test sets up its own data

```python
# ✅ GOOD - Tests are independent
def test_create_user():
    # Fresh setup for this test
    db = create_test_database()
    create_user("alice@example.com", db)
    assert db.user_count() == 1
    db.teardown()

def test_create_another_user():
    # Fresh setup for this test
    db = create_test_database()
    create_user("bob@example.com", db)
    assert db.user_count() == 1  # Always expects 1
    db.teardown()
```

### Using Fixtures for Isolation

**Python (pytest fixtures)**:

```python
import pytest

@pytest.fixture
def database():
    """Create a fresh database for each test"""
    db = create_test_database()
    yield db
    db.teardown()

@pytest.fixture
def user(database):
    """Create a test user"""
    return create_user("test@example.com", database)

def test_user_can_login(database, user):
    # Each test gets fresh database and user
    result = login(user.email, "password123", database)
    assert result.success == True

def test_user_can_update_profile(database, user):
    # Completely independent from previous test
    update_profile(user.id, name="New Name", database=database)
    updated_user = get_user(user.id, database)
    assert updated_user.name == "New Name"
```

**JavaScript (Jest setup/teardown)**:

```javascript
describe("User operations", () => {
  let database;
  let user;

  // Run before each test
  beforeEach(() => {
    database = createTestDatabase();
    user = createUser("test@example.com", database);
  });

  // Run after each test
  afterEach(() => {
    database.teardown();
  });

  test("user can login", () => {
    const result = login(user.email, "password123", database);
    expect(result.success).toBe(true);
  });

  test("user can update profile", () => {
    updateProfile(user.id, { name: "New Name" }, database);
    const updatedUser = getUser(user.id, database);
    expect(updatedUser.name).toBe("New Name");
  });
});
```

---

## Test Naming Conventions

Good test names clearly describe what is being tested and what the expected outcome is.

### Pattern 1: `test_<what>_<condition>_<expected>`

```python
def test_calculate_discount_with_valid_percentage_returns_reduced_price():
    pass

def test_calculate_discount_with_negative_percentage_raises_value_error():
    pass

def test_calculate_discount_with_zero_percentage_returns_original_price():
    pass
```

### Pattern 2: `test_should_<expected>_when_<condition>`

```python
def test_should_return_true_when_user_is_admin():
    pass

def test_should_raise_exception_when_input_is_none():
    pass

def test_should_send_email_when_order_is_confirmed():
    pass
```

### Pattern 3: BDD Style - `test_<Given>_<When>_<Then>`

```javascript
describe("ShoppingCart", () => {
  test("given empty cart, when item added, then count is one", () => {
    // Test implementation
  });

  test("given item in cart, when same item added, then quantity increases", () => {
    // Test implementation
  });
});
```

### Bad vs Good Names

| Bad             | Good                                           |
| --------------- | ---------------------------------------------- |
| `test_login()`  | `test_login_with_valid_credentials_succeeds()` |
| `test_case_1()` | `test_discount_applies_to_orders_over_100()`   |
| `test_error()`  | `test_division_by_zero_raises_value_error()`   |
| `test_works()`  | `test_email_validation_accepts_valid_format()` |
| `test_add()`    | `test_add_item_increases_cart_count()`         |

---

## Integration Testing Fundamentals

### What is Integration Testing?

**Integration tests** verify that multiple units work together correctly:

- Multiple functions
- Multiple classes
- Multiple modules
- Module + database
- Module + external API

### Unit vs Integration

```
Unit Test:
┌─────────┐
│Function │ → Test in isolation
└─────────┘

Integration Test:
┌─────────┐   ┌──────────┐   ┌────────┐
│Function │ → │Database  │ → │Email   │
│         │   │          │   │Service │
└─────────┘   └──────────┘   └────────┘
     Test them working together
```

### Example: Unit vs Integration

**Code to Test**:

```python
class OrderService:
    def __init__(self, db, email_service):
        self.db = db
        self.email_service = email_service

    def place_order(self, user_id, items):
        # Validate items
        if not items:
            raise ValueError("Cannot place empty order")

        # Calculate total
        total = sum(item.price * item.quantity for item in items)

        # Save to database
        order = self.db.create_order(user_id, items, total)

        # Send confirmation email
        self.email_service.send_order_confirmation(user_id, order.id)

        return order
```

**Unit Test** (isolated, uses mocks):

```python
from unittest.mock import Mock

def test_place_order_calculates_total_correctly():
    # Arrange
    mock_db = Mock()
    mock_email = Mock()
    service = OrderService(mock_db, mock_email)

    items = [
        Mock(price=10, quantity=2),  # 20
        Mock(price=5, quantity=3)     # 15
    ]

    # Act
    service.place_order(user_id=1, items=items)

    # Assert - verify total was calculated correctly
    mock_db.create_order.assert_called_once()
    call_args = mock_db.create_order.call_args
    assert call_args[0][2] == 35  # Third argument is total
```

**Integration Test** (uses real database and email service):

```python
def test_place_order_integration():
    # Arrange - use real implementations
    db = create_test_database()
    email_service = create_test_email_service()
    service = OrderService(db, email_service)

    user = db.create_user("test@example.com")
    items = [
        db.create_product("Laptop", price=1000),
        db.create_product("Mouse", price=20)
    ]

    # Act
    order = service.place_order(user.id, items)

    # Assert - verify end-to-end behavior
    assert order.id is not None
    assert order.total == 1020

    # Verify database state
    saved_order = db.get_order(order.id)
    assert saved_order.user_id == user.id
    assert len(saved_order.items) == 2

    # Verify email was sent
    emails = email_service.get_sent_emails()
    assert len(emails) == 1
    assert emails[0].to == "test@example.com"
    assert "Order Confirmation" in emails[0].subject
```

### Integration Test Example: JavaScript

```javascript
// orderService.js
class OrderService {
  constructor(db, emailService) {
    this.db = db;
    this.emailService = emailService;
  }

  async placeOrder(userId, items) {
    if (!items || items.length === 0) {
      throw new Error("Cannot place empty order");
    }

    const total = items.reduce((sum, item) => {
      return sum + item.price * item.quantity;
    }, 0);

    const order = await this.db.createOrder(userId, items, total);
    await this.emailService.sendOrderConfirmation(userId, order.id);

    return order;
  }
}

// orderService.integration.test.js
describe("OrderService Integration", () => {
  let db;
  let emailService;
  let orderService;

  beforeEach(async () => {
    // Use real test implementations
    db = await createTestDatabase();
    emailService = createTestEmailService();
    orderService = new OrderService(db, emailService);
  });

  afterEach(async () => {
    await db.teardown();
  });

  test("place order saves to database and sends email", async () => {
    // Arrange
    const user = await db.createUser("test@example.com");
    const items = [
      { id: 1, name: "Laptop", price: 1000, quantity: 1 },
      { id: 2, name: "Mouse", price: 20, quantity: 2 },
    ];

    // Act
    const order = await orderService.placeOrder(user.id, items);

    // Assert
    expect(order.id).toBeDefined();
    expect(order.total).toBe(1040);

    // Verify database state
    const savedOrder = await db.getOrder(order.id);
    expect(savedOrder.userId).toBe(user.id);
    expect(savedOrder.items).toHaveLength(2);

    // Verify email
    const emails = emailService.getSentEmails();
    expect(emails).toHaveLength(1);
    expect(emails[0].to).toBe("test@example.com");
  });
});
```

---

## The Test Pyramid

The **Test Pyramid** is a strategy for balancing different types of tests.

```
        /\
       /  \
      / UI \          Few - Slow - Expensive
     /Tests\
    /────────\
   /          \
  /Integration\      Some - Medium Speed
 /    Tests    \
/────────────────\
/                \
/   Unit Tests    \   Many - Fast - Cheap
/                  \
──────────────────────
```

### Pyramid Layers

#### Layer 1: Unit Tests (70-80%)

- **Many**: Majority of your tests
- **Fast**: Milliseconds
- **Focused**: Single function/class
- **Cheap**: Easy to write and maintain

#### Layer 2: Integration Tests (15-20%)

- **Some**: Test module interactions
- **Medium**: Seconds
- **Broader**: Multiple components
- **Moderate**: More complex setup

#### Layer 3: End-to-End/UI Tests (5-10%)

- **Few**: Test critical user flows
- **Slow**: Minutes
- **Wide**: Entire system
- **Expensive**: Brittle, hard to maintain

### Why This Shape?

**Unit tests are fast and pinpoint problems**:

```python
# Runs in <1ms
def test_calculate_tax():
    assert calculate_tax(100, 0.08) == 8.0
```

**E2E tests are slow and catch integration issues**:

```python
# Runs in ~30 seconds
def test_complete_checkout_flow():
    browser.goto("/products")
    browser.click("Add to Cart")
    browser.goto("/checkout")
    browser.fill("card_number", "4111111111111111")
    browser.click("Place Order")
    assert browser.is_visible("Order Confirmation")
```

### Anti-Pattern: Ice Cream Cone

```
──────────────────────
\                  /
 \   UI Tests    /     Many - Most time here
  \            /
   \──────────/
    \        /
     \ Integ /        Few
      \    /
       \──/
        \/            Almost none - Bad!
     Unit Tests
```

**Problems with Ice Cream Cone**:

- Tests are slow
- Hard to maintain
- Failures are hard to debug
- Expensive to run

---

## Putting It All Together

### Example: Testing a User Registration System

**1. Unit Tests** (fast, many):

```python
def test_validate_email_accepts_valid_format():
    assert validate_email("user@example.com") == True

def test_validate_email_rejects_missing_at_symbol():
    assert validate_email("userexample.com") == False

def test_hash_password_returns_different_value():
    password = "secret123"
    hashed = hash_password(password)
    assert hashed != password
    assert len(hashed) > 20
```

**2. Integration Tests** (medium, some):

```python
def test_register_user_creates_database_record():
    db = create_test_database()
    auth_service = AuthService(db)

    user = auth_service.register_user(
        email="newuser@example.com",
        password="ValidPass123!"
    )

    assert user.id is not None
    saved_user = db.get_user_by_email("newuser@example.com")
    assert saved_user is not None
    assert saved_user.email == "newuser@example.com"
```

**3. E2E Tests** (slow, few):

```python
def test_user_can_register_and_login_through_ui():
    browser.goto("/register")
    browser.fill("email", "test@example.com")
    browser.fill("password", "ValidPass123!")
    browser.click("Register")

    assert browser.is_visible("Registration Successful")

    browser.goto("/login")
    browser.fill("email", "test@example.com")
    browser.fill("password", "ValidPass123!")
    browser.click("Login")

    assert browser.url() == "/dashboard"
```

---

## Common Mistakes to Avoid

### 1. Testing Implementation Details

❌ **Bad**: Testing internal variable names

```python
def test_internal_variable():
    calc = Calculator()
    calc.add(5)
    assert calc._internal_sum == 5  # Testing private variable
```

✅ **Good**: Testing public behavior

```python
def test_public_behavior():
    calc = Calculator()
    calc.add(5)
    assert calc.get_total() == 5  # Testing public API
```

### 2. Tests That Are Too Large

❌ **Bad**: Testing everything in one test

```python
def test_entire_user_flow():
    # 100 lines testing registration, login, profile update, logout...
    pass
```

✅ **Good**: Separate focused tests

```python
def test_user_registration():
    # 10 lines testing just registration
    pass

def test_user_login():
    # 10 lines testing just login
    pass
```

### 3. No Assertions

❌ **Bad**: Test that doesn't verify anything

```python
def test_create_user():
    create_user("test@example.com")  # No assertion!
```

✅ **Good**: Always assert something

```python
def test_create_user():
    user = create_user("test@example.com")
    assert user is not None
    assert user.email == "test@example.com"
```

### 4. Ignoring Test Failures

❌ **Bad**: Commenting out failing tests

```python
# def test_broken_feature():
#     # TODO: Fix this later
#     pass
```

✅ **Good**: Fix or mark as expected to fail

```python
@pytest.mark.xfail(reason="Known bug #123")
def test_broken_feature():
    # Test stays, marked as expected failure
    pass
```

---

## Summary

**White Box Testing**:

- Looks inside the code
- Tests internal logic
- Ensures code coverage
- Used for unit and integration tests

**Unit Testing Best Practices**:

- Use AAA pattern (Arrange-Act-Assert)
- Keep tests isolated and independent
- Use clear, descriptive test names
- Test one thing per test

**Integration Testing**:

- Tests multiple units working together
- Uses real implementations (not mocks)
- Verifies module interactions

**Test Pyramid**:

- Many unit tests (fast, cheap)
- Some integration tests (medium)
- Few E2E tests (slow, expensive)

---

## Practice Exercises

1. **Convert Black Box to White Box**: Take a black box test you've written and convert it to a white box test that verifies internal logic.

2. **Write Unit Tests**: Write unit tests for a calculator class with methods: `add()`, `subtract()`, `multiply()`, `divide()`. Follow AAA pattern.

3. **Write Integration Test**: Write an integration test for a blog system that verifies creating a post, saving to database, and retrieving it.

4. **Test Isolation**: Fix this broken test suite where tests depend on each other:

```python
balance = 0

def test_deposit():
    global balance
    balance += 100
    assert balance == 100

def test_withdraw():
    global balance
    balance -= 50
    assert balance == 50  # Fails if run alone!
```

5. **Test Pyramid**: For a shopping cart system, list 10 unit tests, 3 integration tests, and 1 E2E test you would write.

---

## Next Steps

- Read [02-statement-coverage.md](./02-statement-coverage.md) to learn about measuring code coverage
- Practice writing unit tests with [Exercise 1: Unit Testing Basics](../exercises/01-unit-testing-basics.md)
- Review the AAA pattern in your existing tests
