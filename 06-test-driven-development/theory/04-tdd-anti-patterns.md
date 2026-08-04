# TDD Anti-Patterns

**Module**: 6 - Test-Driven Development  
**Topic**: Common TDD Mistakes and How to Avoid Them  
**Reading Time**: 25 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Recognize and avoid testing implementation details
- Understand the dangers of over-mocking
- Identify when tests are too large or complex
- Speed up slow test suites
- Eliminate flaky tests
- Ensure test independence
- Avoid skipping the refactor phase
- Write tests before code (not after)
- Test at the right level of abstraction
- Balance test coverage with diminishing returns

---

## Anti-Pattern 1: Testing Implementation Details

### The Problem

**Tests that depend on HOW code works, not WHAT it does.**

When implementation details change, tests break even though behavior is correct.

### Example: The Problem (Python)

```python
# ❌ BAD: Testing implementation
def test_user_service_calls_database_query():
    mock_db = Mock()
    service = UserService(mock_db)

    service.get_user(1)

    # Coupled to implementation
    mock_db.execute.assert_called_with("SELECT * FROM users WHERE id=?", (1,))

# Now if we change from raw SQL to ORM, test breaks!

def get_user(self, user_id):
    # Changed implementation
    return self.db.query(User).filter_by(id=user_id).first()
    # Test FAILS even though behavior is same!
```

### Example: The Problem (JavaScript)

```javascript
// ❌ BAD: Testing implementation
test("user service fetches from cache first", () => {
  const mockCache = { get: jest.fn(), set: jest.fn() };
  const mockDb = { query: jest.fn() };
  const service = new UserService(mockCache, mockDb);

  service.getUser(1);

  // Coupled to implementation detail (caching)
  expect(mockCache.get).toHaveBeenCalledWith("user:1");

  // If we remove caching, test breaks even though getUser still works!
});
```

### The Solution: Test Behavior

```python
# ✅ GOOD: Testing behavior
def test_get_user_returns_user_with_correct_id():
    mock_db = Mock()
    mock_db.get_user.return_value = User(id=1, name="Alice")
    service = UserService(mock_db)

    user = service.get_user(1)

    # Test the result, not how we got it
    assert user.id == 1
    assert user.name == "Alice"
```

```javascript
// ✅ GOOD: Testing behavior
test("getUser returns user with correct data", async () => {
  const mockDb = {
    getUser: jest.fn().mockResolvedValue({ id: 1, name: "Alice" }),
  };
  const service = new UserService(mockDb);

  const user = await service.getUser(1);

  // Test the result
  expect(user.id).toBe(1);
  expect(user.name).toBe("Alice");
});
```

### Signs You're Testing Implementation

- Test breaks when you refactor
- Test verifies internal method calls
- Test checks private methods
- Test verifies order of operations
- Test mocks your own code

### How to Avoid

**Ask yourself**: "If I change HOW this works but keep WHAT it does the same, will my test break?"

If yes, you're testing implementation.

---

## Anti-Pattern 2: Over-Mocking

### The Problem

**Mocking everything, including your own code.**

Tests become meaningless because nothing real is tested.

### Example: The Problem (Python)

```python
# ❌ BAD: Mocking everything
def test_order_service():
    mock_calculator = Mock()
    mock_calculator.calculate_total.return_value = 100

    mock_validator = Mock()
    mock_validator.validate.return_value = True

    mock_formatter = Mock()
    mock_formatter.format.return_value = "Order #123"

    mock_db = Mock()
    mock_db.save.return_value = 123

    service = OrderService(mock_calculator, mock_validator, mock_formatter, mock_db)

    order_id = service.create_order(items)

    assert order_id == 123

# What did we actually test? Just that mocks return what we told them to!
```

### Example: The Problem (JavaScript)

```javascript
// ❌ BAD: Everything is mocked
test("processes order", () => {
  const mockCalculator = { calculate: jest.fn().mockReturnValue(100) };
  const mockValidator = { validate: jest.fn().mockReturnValue(true) };
  const mockFormatter = { format: jest.fn().mockReturnValue("Order #123") };
  const mockDb = { save: jest.fn().mockReturnValue(123) };

  const service = new OrderService(
    mockCalculator,
    mockValidator,
    mockFormatter,
    mockDb,
  );

  const orderId = service.createOrder(items);

  expect(orderId).toBe(123);

  // We're testing that mocks work, not that our code works!
});
```

### The Solution: Mock Only External Dependencies

```python
# ✅ GOOD: Only mock external dependencies
def test_order_service_creates_order():
    # Real instances of our code
    calculator = OrderCalculator()
    validator = OrderValidator()
    formatter = OrderFormatter()

    # Mock external dependency (database)
    mock_db = Mock()
    mock_db.save.return_value = 123

    service = OrderService(calculator, validator, formatter, mock_db)

    items = [Item("Laptop", price=1000, quantity=1)]
    order_id = service.create_order(items)

    # Now we're testing real logic
    assert order_id == 123
    mock_db.save.assert_called_once()
```

### What to Mock vs What to Keep Real

**Mock (external dependencies)**:

- Database
- APIs
- File system
- Network
- Email service
- Payment gateway
- Current time

**Keep Real (your code)**:

- Business logic
- Calculations
- Validators
- Formatters
- Value objects
- Domain models

### Signs of Over-Mocking

- More mock setup than actual test
- Mocking your own classes
- Tests always pass (not testing real behavior)
- Can't tell what's actually being tested
- Changing code doesn't fail tests

---

## Anti-Pattern 3: Large Tests

### The Problem

**Testing too much in one test.**

When test fails, you don't know what's wrong. Tests are hard to read and maintain.

### Example: The Problem (Python)

```python
# ❌ BAD: Testing entire user flow
def test_user_registration_and_login_and_profile():
    # 1. Registration
    service = UserService()
    user = service.register("alice@example.com", "password123")
    assert user is not None
    assert user.email == "alice@example.com"

    # 2. Email verification
    token = service.generate_verification_token(user)
    service.verify_email(token)
    assert user.is_verified == True

    # 3. Login
    session = service.login("alice@example.com", "password123")
    assert session is not None

    # 4. Profile update
    service.update_profile(user, name="Alice Smith", bio="Hello")
    assert user.name == "Alice Smith"

    # 5. Password change
    service.change_password(user, "password123", "newpassword456")

    # 6. Logout
    service.logout(session)
    assert session.is_active == False

# If this fails, where is the problem?
```

### Example: The Problem (JavaScript)

```javascript
// ❌ BAD: One giant test
test("complete e-commerce flow", async () => {
  const user = await register("alice@example.com", "pass123");
  await verifyEmail(user.verificationToken);

  const products = await searchProducts("laptop");
  expect(products.length).toBeGreaterThan(0);

  const cart = new ShoppingCart(user);
  cart.add(products[0], 1);

  const order = await checkout(cart, paymentInfo);
  expect(order.status).toBe("pending");

  await processPayment(order);
  expect(order.status).toBe("paid");

  await shipOrder(order);
  expect(order.status).toBe("shipped");

  // 50 more lines...

  // Where's the bug if this fails?
});
```

### The Solution: Small, Focused Tests

```python
# ✅ GOOD: Small, focused tests
def test_register_creates_user_with_email():
    service = UserService()
    user = service.register("alice@example.com", "password123")
    assert user.email == "alice@example.com"

def test_register_creates_unverified_user():
    service = UserService()
    user = service.register("alice@example.com", "password123")
    assert user.is_verified == False

def test_verify_email_marks_user_as_verified():
    service = UserService()
    user = service.register("alice@example.com", "password123")
    token = service.generate_verification_token(user)

    service.verify_email(token)

    assert user.is_verified == True

def test_login_returns_session_for_verified_user():
    service = UserService()
    user = create_verified_user()

    session = service.login("alice@example.com", "password123")

    assert session is not None
    assert session.user_id == user.id

# Each test is clear and focused
```

### Rule of Thumb

**If your test has more than one "Act" step, it's too big.**

```python
# ❌ BAD: Multiple actions
def test_user_flow():
    user = service.register(...)  # Act 1
    service.verify(...)           # Act 2
    session = service.login(...)  # Act 3
    service.update(...)           # Act 4

# ✅ GOOD: One action
def test_registration():
    user = service.register(...)  # Act
    assert user.email == "..."
```

---

## Anti-Pattern 4: Slow Tests

### The Problem

**Tests take too long to run.**

Developers stop running tests. CI/CD takes forever. Feedback loop is slow.

### Example: The Problem (Python)

```python
# ❌ BAD: Slow tests
def test_user_service():
    # Connects to real database (100ms)
    db = PostgresDatabase("postgres://localhost/testdb")
    service = UserService(db)

    # Makes real API call (500ms)
    user_data = fetch_user_from_api("https://api.example.com/users/1")

    # Saves to real database (100ms)
    user = service.create_user(user_data)

    # Waits for real email (2000ms)
    time.sleep(2)  # Wait for email to send

    assert user.email_sent == True

# Total: 2700ms per test!
# 100 tests = 4.5 minutes!
```

### Example: The Problem (JavaScript)

```javascript
// ❌ BAD: Slow tests
test("creates user and sends welcome email", async () => {
  // Real database connection (100ms)
  const db = new Database("mongodb://localhost/test");

  // Real API call (500ms)
  const emailService = new SendGridEmailService(API_KEY);

  const service = new UserService(db, emailService);

  // Real operations (600ms)
  await service.createUser("alice@example.com", "pass123");

  // Wait for async email (2000ms)
  await new Promise((resolve) => setTimeout(resolve, 2000));

  const user = await db.findUser("alice@example.com");
  expect(user.welcomeEmailSent).toBe(true);

  // Total: 3200ms per test!
});
```

### The Solution: Mock Slow Dependencies

```python
# ✅ GOOD: Fast tests
def test_user_service_sends_welcome_email():
    # Mock database (<1ms)
    mock_db = Mock()

    # Mock email service (<1ms)
    mock_email = Mock()

    service = UserService(mock_db, mock_email)

    # Fast operation (<1ms)
    service.create_user("alice@example.com", "pass123")

    # Verify behavior (<1ms)
    mock_email.send_welcome.assert_called_once_with("alice@example.com")

# Total: <5ms per test!
# 100 tests = 0.5 seconds!
```

```javascript
// ✅ GOOD: Fast tests
test("sends welcome email when user is created", () => {
  // Mock dependencies
  const mockDb = { save: jest.fn() };
  const mockEmail = { sendWelcome: jest.fn() };

  const service = new UserService(mockDb, mockEmail);

  service.createUser("alice@example.com", "pass123");

  expect(mockEmail.sendWelcome).toHaveBeenCalledWith("alice@example.com");

  // Total: <5ms
});
```

### Speed Targets

- **Unit test**: < 10ms
- **100 unit tests**: < 1 second
- **1000 unit tests**: < 10 seconds

If slower, mock more dependencies.

---

## Anti-Pattern 5: Flaky Tests

### The Problem

**Tests that sometimes pass, sometimes fail, without code changes.**

Destroys confidence. Wastes time investigating. Developers start ignoring failures.

### Common Causes

1. **Race conditions**
2. **Dependency on time**
3. **Random values**
4. **External dependencies**
5. **Test order dependencies**
6. **Shared state**

### Example: Flaky Test (Python)

```python
# ❌ BAD: Depends on current time
def test_is_business_hours():
    # Flaky! Depends on when test runs
    result = is_business_hours()
    assert result == True  # Fails after 5pm

# ❌ BAD: Random values
def test_generate_id():
    id1 = generate_random_id()
    id2 = generate_random_id()
    assert id1 != id2  # Might fail (1 in a billion chance)

# ❌ BAD: Race condition
def test_async_operation():
    start_background_task()
    time.sleep(0.1)  # Hope it's done!
    result = get_result()
    assert result == "completed"  # Might fail if task takes longer
```

### Example: Flaky Test (JavaScript)

```javascript
// ❌ BAD: Depends on time
test("session expires after 1 hour", () => {
  const session = createSession();

  // Wait 1 hour (flaky in CI environments)
  setTimeout(() => {
    expect(session.isValid()).toBe(false);
  }, 3600000);
});

// ❌ BAD: Race condition
test("fetches data asynchronously", (done) => {
  fetchData().then((data) => {
    expect(data).toBeDefined();
    done();
  });

  // If fetchData is slow, test might timeout
});
```

### The Solution: Make Tests Deterministic

```python
# ✅ GOOD: Mock time
from freezegun import freeze_time

@freeze_time("2026-08-04 14:00:00")  # 2 PM
def test_is_business_hours_during_work():
    result = is_business_hours()
    assert result == True

@freeze_time("2026-08-04 22:00:00")  # 10 PM
def test_is_business_hours_after_work():
    result = is_business_hours()
    assert result == False

# ✅ GOOD: Seed random
import random

def test_generate_id():
    random.seed(42)  # Deterministic
    id1 = generate_random_id()

    random.seed(42)
    id2 = generate_random_id()

    assert id1 == id2  # Always passes

# ✅ GOOD: Mock async
def test_background_task():
    mock_task = Mock()
    mock_task.get_result.return_value = "completed"

    process_with_task(mock_task)

    mock_task.get_result.assert_called_once()
```

```javascript
// ✅ GOOD: Mock time
test("session expires after 1 hour", () => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date("2026-08-04T10:00:00"));

  const session = createSession();

  // Fast forward 1 hour
  jest.advanceTimersByTime(3600000);

  expect(session.isValid()).toBe(false);

  jest.useRealTimers();
});

// ✅ GOOD: Proper async handling
test("fetches data asynchronously", async () => {
  const mockFetch = jest.fn().mockResolvedValue({ id: 1, name: "Alice" });

  const data = await fetchData(mockFetch);

  expect(data).toBeDefined();
});
```

### Prevention Checklist

- [ ] Mock current time
- [ ] Seed random generators
- [ ] Mock external dependencies
- [ ] Use proper async/await
- [ ] Ensure test independence
- [ ] Avoid shared state
- [ ] Don't use sleep/setTimeout

---

## Anti-Pattern 6: Test Interdependence

### The Problem

**Tests depend on each other or on execution order.**

Can't run tests in isolation. Hard to debug. Parallel execution fails.

### Example: The Problem (Python)

```python
# ❌ BAD: Tests depend on order
class TestUserService:
    def test_1_create_user(self):
        self.user = service.register("alice@example.com", "pass")
        assert self.user is not None

    def test_2_login_user(self):
        # Depends on test_1 creating user!
        token = service.login("alice@example.com", "pass")
        assert token is not None

    def test_3_delete_user(self):
        # Depends on test_1!
        service.delete(self.user)
        assert service.get_user(self.user.id) is None

# If test_1 fails, test_2 and test_3 also fail (cascading failures)
# If tests run in random order, tests fail
```

### Example: The Problem (JavaScript)

```javascript
// ❌ BAD: Shared state
let sharedUser;

test("creates user", () => {
  sharedUser = createUser("alice@example.com");
  expect(sharedUser).toBeDefined();
});

test("updates user", () => {
  // Depends on previous test!
  updateUser(sharedUser, { name: "Alice Smith" });
  expect(sharedUser.name).toBe("Alice Smith");
});

test("deletes user", () => {
  // Depends on previous tests!
  deleteUser(sharedUser);
  expect(findUser(sharedUser.id)).toBeNull();
});
```

### The Solution: Independent Tests

```python
# ✅ GOOD: Each test is independent
class TestUserService:
    def test_create_user(self):
        user = service.register("alice@example.com", "pass")
        assert user is not None

    def test_login_with_valid_credentials(self):
        # Create its own test data
        service.register("bob@example.com", "pass")
        token = service.login("bob@example.com", "pass")
        assert token is not None

    def test_delete_user_removes_from_system(self):
        # Create its own test data
        user = service.register("carol@example.com", "pass")
        service.delete(user)
        assert service.get_user(user.id) is None

# Can run in any order
# One failure doesn't affect others
```

```javascript
// ✅ GOOD: Independent tests
describe("UserService", () => {
  test("creates user", () => {
    const user = createUser("alice@example.com");
    expect(user).toBeDefined();
  });

  test("updates user", () => {
    // Create own data
    const user = createUser("bob@example.com");
    updateUser(user, { name: "Bob Smith" });
    expect(user.name).toBe("Bob Smith");
  });

  test("deletes user", () => {
    // Create own data
    const user = createUser("carol@example.com");
    deleteUser(user);
    expect(findUser(user.id)).toBeNull();
  });
});
```

### Test Independence Rules

1. **Each test creates its own data**
2. **Each test cleans up after itself**
3. **No shared state between tests**
4. **Tests can run in any order**
5. **Tests can run in parallel**

---

## Anti-Pattern 7: Ignoring Refactor Phase

### The Problem

**Skipping the refactor step in Red-Green-Refactor.**

Technical debt accumulates. Code becomes messy. Tests become hard to maintain.

### Example: The Problem (Python)

```python
# ❌ BAD: Never refactored
def calculate_total(items, discount_code, tax_rate, shipping_country):
    total = 0
    for item in items:
        total += item.price * item.quantity
    if discount_code == "SAVE10":
        total = total * 0.9
    elif discount_code == "SAVE20":
        total = total * 0.8
    elif discount_code == "SAVE30":
        total = total * 0.7
    elif discount_code == "VIP":
        total = total * 0.5
    if shipping_country == "US":
        shipping = 10
    elif shipping_country == "Canada":
        shipping = 15
    elif shipping_country == "International":
        shipping = 25
    else:
        shipping = 0
    total += shipping
    total = total * (1 + tax_rate)
    return total

# Passes tests but is a mess!
```

### The Solution: Refactor After Each Green

```python
# ✅ GOOD: Refactored for clarity
class OrderCalculator:
    def calculate_total(self, items, discount_code, tax_rate, shipping_country):
        subtotal = self._calculate_subtotal(items)
        discounted = self._apply_discount(subtotal, discount_code)
        with_shipping = self._add_shipping(discounted, shipping_country)
        final_total = self._apply_tax(with_shipping, tax_rate)
        return final_total

    def _calculate_subtotal(self, items):
        return sum(item.price * item.quantity for item in items)

    def _apply_discount(self, amount, discount_code):
        discounts = {
            "SAVE10": 0.9,
            "SAVE20": 0.8,
            "SAVE30": 0.7,
            "VIP": 0.5
        }
        multiplier = discounts.get(discount_code, 1.0)
        return amount * multiplier

    def _add_shipping(self, amount, country):
        shipping_rates = {
            "US": 10,
            "Canada": 15,
            "International": 25
        }
        shipping = shipping_rates.get(country, 0)
        return amount + shipping

    def _apply_tax(self, amount, tax_rate):
        return amount * (1 + tax_rate)

# Same behavior, much cleaner!
# Tests still pass!
```

### Signs You Need to Refactor

- Duplicated code
- Long methods (> 20 lines)
- Magic numbers
- Complex conditionals
- Unclear variable names
- Too many parameters

---

## Anti-Pattern 8: Writing Tests After Code

### The Problem

**Writing tests after implementation (defeating the purpose of TDD).**

Loses all TDD benefits: design feedback, confidence, documentation.

### Why It's Bad

```python
# ❌ BAD: Code written first
def calculate_discount(price, customer_type, is_holiday, items_count):
    # Complex implementation written without tests
    # Hard to test after the fact
    # Tightly coupled
    # No design feedback
    pass

# Now trying to write tests...
def test_calculate_discount():
    # How do I test this?
    # Too many parameters!
    # Not sure what edge cases exist!
    pass
```

### The Solution: Always Test First

```python
# ✅ GOOD: Test first
def test_calculate_discount_for_regular_customer():
    discount = calculate_discount(price=100, customer_type="regular")
    assert discount == 0

# Now write minimal code
def calculate_discount(price, customer_type):
    return 0

# Next test
def test_calculate_discount_for_vip_customer():
    discount = calculate_discount(price=100, customer_type="vip")
    assert discount == 10

# Improve code
def calculate_discount(price, customer_type):
    if customer_type == "vip":
        return price * 0.1
    return 0

# Continue TDD cycle...
```

---

## Anti-Pattern 9: Testing Private Methods

### The Problem

**Writing tests for private/internal methods.**

Tests become fragile. Refactoring breaks tests. Testing implementation, not behavior.

### Example: The Problem (Python)

```python
# ❌ BAD: Testing private methods
class OrderProcessor:
    def _validate_items(self, items):
        # private method
        return all(item.price > 0 for item in items)

    def _calculate_subtotal(self, items):
        # private method
        return sum(item.price * item.quantity for item in items)

# Tests for private methods
def test_validate_items():
    processor = OrderProcessor()
    items = [Item("Laptop", 1000)]
    assert processor._validate_items(items) == True  # Testing private!

def test_calculate_subtotal():
    processor = OrderProcessor()
    items = [Item("Laptop", 1000)]
    assert processor._calculate_subtotal(items) == 1000  # Testing private!
```

### The Solution: Test Public Interface

```python
# ✅ GOOD: Test through public interface
class OrderProcessor:
    def process_order(self, items):
        if not self._validate_items(items):
            raise ValueError("Invalid items")
        return self._calculate_subtotal(items)

    def _validate_items(self, items):
        return all(item.price > 0 for item in items)

    def _calculate_subtotal(self, items):
        return sum(item.price * item.quantity for item in items)

# Test public behavior
def test_process_order_with_valid_items():
    processor = OrderProcessor()
    items = [Item("Laptop", 1000)]
    total = processor.process_order(items)
    assert total == 1000
    # Private methods tested indirectly!

def test_process_order_with_invalid_items():
    processor = OrderProcessor()
    items = [Item("Laptop", -100)]  # Invalid price
    with pytest.raises(ValueError):
        processor.process_order(items)
    # Validation method tested indirectly!
```

### Rule

**If it's private, don't test it directly. It's an implementation detail.**

---

## Anti-Pattern 10: Chasing 100% Coverage

### The Problem

**Obsessing over 100% code coverage.**

Diminishing returns. Waste of time. Focus on metrics instead of quality.

### Example: The Problem

```python
# ❌ BAD: Testing trivial code for coverage
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_name(self):
        return self.name  # Do we really need to test this?

    def get_email(self):
        return self.email  # Or this?

    def __str__(self):
        return f"User({self.name})"  # Or this?

# Tests just for coverage
def test_get_name():
    user = User("Alice", "alice@example.com")
    assert user.get_name() == "Alice"  # Waste of time

def test_get_email():
    user = User("Alice", "alice@example.com")
    assert user.get_email() == "alice@example.com"  # Waste of time

def test_str():
    user = User("Alice", "alice@example.com")
    assert str(user) == "User(Alice)"  # Waste of time
```

### The Solution: Focus on Meaningful Coverage

```python
# ✅ GOOD: Test business logic, skip trivial code
class UserService:
    def register(self, email, password):
        # Test this! Has business logic
        if len(password) < 8:
            raise ValueError("Password too short")

        if self.email_exists(email):
            raise ValueError("Email already registered")

        hashed = self._hash_password(password)
        return User(email, hashed)

    def _hash_password(self, password):
        # Don't test directly, tested through register()
        return bcrypt.hash(password)

# Focus tests on business logic
def test_register_rejects_short_password():
    service = UserService()
    with pytest.raises(ValueError, match="Password too short"):
        service.register("alice@example.com", "pass")

def test_register_rejects_duplicate_email():
    service = UserService()
    service.register("alice@example.com", "password123")
    with pytest.raises(ValueError, match="already registered"):
        service.register("alice@example.com", "password123")
```

### Coverage Guidelines

**Target**: 80-90% coverage

**Don't test**:

- Getters/setters
- Simple properties
- toString/repr methods
- Framework boilerplate
- Trivial code

**Do test**:

- Business logic
- Calculations
- Validation
- Edge cases
- Error handling

---

## Summary of Anti-Patterns

| Anti-Pattern            | Problem                     | Solution                              |
| ----------------------- | --------------------------- | ------------------------------------- |
| Testing Implementation  | Tests break on refactor     | Test behavior, not how                |
| Over-Mocking            | Not testing real code       | Mock only external dependencies       |
| Large Tests             | Hard to debug failures      | Small, focused tests                  |
| Slow Tests              | Developers don't run them   | Mock slow dependencies                |
| Flaky Tests             | Random failures             | Make tests deterministic              |
| Test Interdependence    | Can't run in isolation      | Each test is independent              |
| Ignoring Refactor       | Technical debt accumulates  | Refactor after each green             |
| Writing Tests After     | Loses TDD benefits          | Always write tests first              |
| Testing Private Methods | Fragile, coupled tests      | Test through public interface         |
| Chasing 100% Coverage   | Waste time on trivial tests | Focus on meaningful coverage (80-90%) |

---

## Quick Checklist: Is My Test Good?

Before committing, ask:

- [ ] Does test describe behavior, not implementation?
- [ ] Are only external dependencies mocked?
- [ ] Is test small and focused (one thing)?
- [ ] Does test run in < 10ms?
- [ ] Does test always produce same result?
- [ ] Can test run independently?
- [ ] Did I refactor after green?
- [ ] Was test written before code?
- [ ] Am I testing public interface?
- [ ] Is this test worth the effort?

---

## Key Takeaways

1. **Test behavior**, not implementation
2. **Mock only external** dependencies
3. **Keep tests small** and focused
4. **Make tests fast** (< 10ms)
5. **Eliminate flakiness** with determinism
6. **Ensure independence** (run in any order)
7. **Always refactor** after green
8. **Write tests first** (never after)
9. **Test public interface**, not private
10. **Aim for 80-90%** coverage, not 100%

---

## Practice Exercises

### Exercise 1: Identify Anti-Patterns

Find the anti-patterns in this test:

```python
def test_user_service():
    service = UserService()

    # Create user
    user = service._create_user_object("alice@example.com")
    assert user.email == "alice@example.com"

    # Validate
    result = service._validate_user(user)
    assert result == True

    # Save
    time.sleep(0.5)  # Wait for DB
    service._save_to_database(user)

    # Login
    token = service._authenticate(user.email, "pass")
    assert token is not None
```

### Exercise 2: Fix Over-Mocking

Refactor this test to use fewer mocks:

```python
def test_order_calculation():
    mock_adder = Mock()
    mock_adder.add.return_value = 100

    mock_multiplier = Mock()
    mock_multiplier.multiply.return_value = 108

    mock_rounder = Mock()
    mock_rounder.round.return_value = 108.00

    calculator = OrderCalculator(mock_adder, mock_multiplier, mock_rounder)
    total = calculator.calculate(items)
    assert total == 108.00
```

### Exercise 3: Make Test Independent

Fix these interdependent tests:

```python
shared_cart = None

def test_create_cart():
    global shared_cart
    shared_cart = ShoppingCart()
    assert shared_cart is not None

def test_add_to_cart():
    shared_cart.add(Item("Laptop", 1000))
    assert len(shared_cart.items) == 1

def test_calculate_total():
    total = shared_cart.calculate_total()
    assert total == 1000
```

---

## Next Steps

You've completed the TDD theory module! Continue with:

1. **[Module 7: Data-Driven Testing](../../07-data-driven-testing/theory/)** - Testing with multiple inputs
2. **[TDD Practice Exercises](../exercises/)** - Apply what you've learned

---

## Additional Resources

- [Test Smells Catalog](http://xunitpatterns.com/Test%20Smells.html)
- [TDD Anti-Patterns](https://blog.james-carr.org/2006/11/03/tdd-anti-patterns/)
- [Google Testing Blog](https://testing.googleblog.com/)
- [Test Desiderata - Kent Beck](https://kentbeck.github.io/TestDesiderata/)

---

**Remember**: Knowing what NOT to do is just as important as knowing what to do! Avoid these anti-patterns and your TDD practice will be excellent! 🚫
