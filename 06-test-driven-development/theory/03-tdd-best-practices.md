# TDD Best Practices

**Module**: 6 - Test-Driven Development  
**Topic**: Writing Excellent Tests with TDD  
**Reading Time**: 30 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Write clear, descriptive test names using proven conventions
- Organize tests using the AAA (Arrange-Act-Assert) pattern
- Apply the Given-When-Then format for readable tests
- Write isolated, independent tests
- Create fast tests by mocking slow dependencies
- Take baby steps for incremental progress
- Recognize and fix test smells
- Achieve natural high coverage through TDD
- Apply 10+ best practices in your daily TDD work

---

## Test Naming Conventions

### Why Names Matter

Test names are documentation. They should:

- Describe what is being tested
- Explain the scenario
- State the expected outcome
- Be readable as a sentence

### Convention 1: should_when Pattern

**Format**: `should_<expected_behavior>_when_<condition>`

**Python Examples**:

```python
def test_should_return_zero_when_input_is_empty():
    calculator = StringCalculator()
    result = calculator.add("")
    assert result == 0

def test_should_raise_error_when_password_is_too_short():
    validator = PasswordValidator()
    with pytest.raises(ValueError):
        validator.validate("abc")

def test_should_send_email_when_order_is_placed():
    mock_email = Mock()
    service = OrderService(mock_email)
    service.place_order(order)
    mock_email.send.assert_called_once()
```

**JavaScript Examples**:

```javascript
test("should return 0 when input is empty", () => {
  const calculator = new StringCalculator();
  expect(calculator.add("")).toBe(0);
});

test("should throw error when password is too short", () => {
  const validator = new PasswordValidator();
  expect(() => validator.validate("abc")).toThrow();
});

test("should send email when order is placed", () => {
  const mockEmail = jest.fn();
  const service = new OrderService(mockEmail);
  service.placeOrder(order);
  expect(mockEmail).toHaveBeenCalledTimes(1);
});
```

### Convention 2: Given-When-Then Pattern

**Format**: `given_<context>_when_<action>_then_<outcome>`

**Python Examples**:

```python
def test_given_valid_user_when_login_then_returns_token():
    user = User("alice@example.com", "password123")
    token = auth_service.login(user)
    assert token is not None

def test_given_expired_token_when_refresh_then_returns_new_token():
    expired_token = create_expired_token()
    new_token = auth_service.refresh(expired_token)
    assert new_token != expired_token

def test_given_insufficient_funds_when_withdraw_then_raises_error():
    account = Account(balance=50)
    with pytest.raises(InsufficientFundsError):
        account.withdraw(100)
```

**JavaScript Examples**:

```javascript
test("given valid credentials, when login, then returns token", () => {
  const token = authService.login("alice@example.com", "password123");
  expect(token).not.toBeNull();
});

test("given expired session, when refresh, then returns new session", () => {
  const oldSession = createExpiredSession();
  const newSession = authService.refresh(oldSession);
  expect(newSession.id).not.toBe(oldSession.id);
});
```

### Convention 3: Describe Behavior, Not Implementation

```python
# ❌ BAD: Describes implementation
def test_sets_logged_in_field_to_true():
    pass

# ✅ GOOD: Describes behavior
def test_user_is_authenticated_after_successful_login():
    pass

# ❌ BAD: Describes internal method
def test_calls_validate_and_hash_password():
    pass

# ✅ GOOD: Describes what happens
def test_stores_password_securely():
    pass
```

### Convention 4: Be Specific

```python
# ❌ BAD: Vague
def test_validation():
    pass

# ✅ GOOD: Specific
def test_validation_rejects_empty_email():
    pass

# ❌ BAD: Too generic
def test_payment_processing():
    pass

# ✅ GOOD: Specific scenario
def test_payment_processing_charges_correct_amount():
    pass
```

---

## Test Organization: AAA Pattern

### Arrange-Act-Assert

**Every test should have three clear sections:**

1. **Arrange**: Set up test data and dependencies
2. **Act**: Execute the code being tested
3. **Assert**: Verify the expected outcome

### Python Example

```python
def test_discount_calculation():
    # Arrange
    product = Product(name="Laptop", price=1000)
    discount_service = DiscountService()

    # Act
    discounted_price = discount_service.apply_discount(product, percentage=10)

    # Assert
    assert discounted_price == 900
```

### JavaScript Example

```javascript
test("calculates order total with tax", () => {
  // Arrange
  const items = [
    { name: "Book", price: 20, quantity: 2 },
    { name: "Pen", price: 5, quantity: 3 },
  ];
  const calculator = new OrderCalculator();

  // Act
  const total = calculator.calculateTotal(items, taxRate: 0.08);

  // Assert
  expect(total).toBe(59.4); // (40 + 15) * 1.08
});
```

### Why AAA?

**Benefits**:

- Clear structure
- Easy to read
- Easy to maintain
- Separates concerns
- Highlights what's being tested

### AAA with Comments (Optional)

```python
def test_user_registration():
    # Arrange: Create valid user data
    user_data = {
        "email": "alice@example.com",
        "password": "SecurePass123",
        "name": "Alice"
    }
    service = UserService()

    # Act: Register the user
    user = service.register(user_data)

    # Assert: User is created with correct data
    assert user.email == "alice@example.com"
    assert user.name == "Alice"
    assert user.is_active == True
```

---

## Given-When-Then for Readability

### BDD-Style Tests

**Given-When-Then** makes tests read like requirements:

- **Given**: The context or initial state
- **When**: The action or event
- **Then**: The expected outcome

### Python Example (Pytest-BDD Style)

```python
def test_shopping_cart():
    # Given: A user with an empty cart
    user = User("alice@example.com")
    cart = ShoppingCart(user)

    # And: Two products are available
    laptop = Product("Laptop", price=1000)
    mouse = Product("Mouse", price=20)

    # When: User adds products to cart
    cart.add(laptop, quantity=1)
    cart.add(mouse, quantity=2)

    # Then: Cart total is correct
    assert cart.total == 1040

    # And: Cart has correct number of items
    assert cart.item_count == 2
```

### JavaScript Example

```javascript
describe("Shopping Cart", () => {
  test("calculates correct total", () => {
    // Given a user with an empty cart
    const user = new User("alice@example.com");
    const cart = new ShoppingCart(user);

    // And products are available
    const laptop = new Product("Laptop", 1000);
    const mouse = new Product("Mouse", 20);

    // When user adds products to cart
    cart.add(laptop, 1);
    cart.add(mouse, 2);

    // Then cart total is correct
    expect(cart.total).toBe(1040);

    // And cart has correct item count
    expect(cart.itemCount).toBe(2);
  });
});
```

### Nested Describe Blocks (JavaScript)

```javascript
describe("PasswordValidator", () => {
  describe("when password is valid", () => {
    test("should return true for password with all requirements", () => {
      const validator = new PasswordValidator();
      const result = validator.validate("SecurePass123!");
      expect(result.isValid).toBe(true);
    });
  });

  describe("when password is invalid", () => {
    test("should return false for password without uppercase", () => {
      const validator = new PasswordValidator();
      const result = validator.validate("securepass123!");
      expect(result.isValid).toBe(false);
    });

    test("should return false for password without number", () => {
      const validator = new PasswordValidator();
      const result = validator.validate("SecurePassword!");
      expect(result.isValid).toBe(false);
    });
  });
});
```

---

## One Assertion Per Test (When Possible)

### The Principle

Each test should verify **one logical concept**.

### When to Use One Assertion

```python
# ✅ GOOD: One clear assertion
def test_returns_zero_for_empty_input():
    assert calculator.add("") == 0

def test_returns_number_for_single_digit():
    assert calculator.add("5") == 5

def test_returns_sum_for_two_numbers():
    assert calculator.add("2,3") == 5
```

### When Multiple Assertions Are OK

**Testing the same logical concept**:

```python
# ✅ GOOD: Multiple assertions about same result
def test_user_registration_creates_valid_user():
    user = service.register("alice@example.com", "password123")

    # All assertions verify the created user
    assert user.email == "alice@example.com"
    assert user.is_active == True
    assert user.created_at is not None
    assert len(user.id) > 0
```

**Triangulation (multiple examples)**:

```python
# ✅ GOOD: Multiple examples of same behavior
def test_is_even():
    assert is_even(2) == True
    assert is_even(4) == True
    assert is_even(100) == True
```

### When NOT to Use Multiple Assertions

```python
# ❌ BAD: Testing unrelated things
def test_user_service():
    service = UserService()

    # Testing registration
    user = service.register("alice@example.com", "pass")
    assert user.email == "alice@example.com"

    # Testing login (separate test!)
    token = service.login("alice@example.com", "pass")
    assert token is not None

    # Testing password reset (separate test!)
    service.reset_password(user)
    assert user.password_reset_sent == True
```

**Split into separate tests**:

```python
# ✅ GOOD: Separate tests
def test_register_creates_user():
    user = service.register("alice@example.com", "pass")
    assert user.email == "alice@example.com"

def test_login_returns_token():
    service.register("alice@example.com", "pass")
    token = service.login("alice@example.com", "pass")
    assert token is not None

def test_reset_password_sends_email():
    user = service.register("alice@example.com", "pass")
    service.reset_password(user)
    assert user.password_reset_sent == True
```

---

## Test Isolation and Independence

### The Principle

**Each test should run independently and in any order.**

### Why Independence Matters

- Tests can run in parallel
- Tests can run in any order
- One failing test doesn't break others
- Easy to debug failures

### Bad: Tests Depend on Each Other

```python
# ❌ BAD: Tests depend on order
class TestUserService:
    def test_1_register_user(self):
        self.user = service.register("alice@example.com", "pass")
        assert self.user is not None

    def test_2_login_user(self):
        # Depends on test_1 running first!
        token = service.login("alice@example.com", "pass")
        assert token is not None

    def test_3_update_user(self):
        # Depends on test_1!
        service.update(self.user, name="Alice Smith")
        assert self.user.name == "Alice Smith"
```

### Good: Independent Tests

```python
# ✅ GOOD: Each test is independent
class TestUserService:
    def test_register_user(self):
        user = service.register("alice@example.com", "pass")
        assert user is not None

    def test_login_user(self):
        # Set up its own data
        service.register("bob@example.com", "pass")
        token = service.login("bob@example.com", "pass")
        assert token is not None

    def test_update_user(self):
        # Set up its own data
        user = service.register("carol@example.com", "pass")
        service.update(user, name="Carol Smith")
        assert user.name == "Carol Smith"
```

### Using Setup/Teardown

**Python (pytest)**:

```python
class TestOrderService:
    def setup_method(self):
        # Runs before EACH test
        self.mock_db = Mock()
        self.service = OrderService(self.mock_db)

    def teardown_method(self):
        # Runs after EACH test
        self.mock_db.reset_mock()

    def test_create_order(self):
        # Fresh service for this test
        order = self.service.create_order(items)
        assert order.total == 100

    def test_cancel_order(self):
        # Fresh service for this test
        self.service.cancel_order(order_id=123)
        self.mock_db.delete.assert_called()
```

**JavaScript (Jest)**:

```javascript
describe("OrderService", () => {
  let mockDb;
  let service;

  beforeEach(() => {
    // Runs before EACH test
    mockDb = {
      create: jest.fn(),
      delete: jest.fn(),
    };
    service = new OrderService(mockDb);
  });

  afterEach(() => {
    // Runs after EACH test
    jest.clearAllMocks();
  });

  test("creates order", () => {
    const order = service.createOrder(items);
    expect(order.total).toBe(100);
  });

  test("cancels order", () => {
    service.cancelOrder(123);
    expect(mockDb.delete).toHaveBeenCalled();
  });
});
```

---

## Fast Tests

### The Principle

**Unit tests should run in milliseconds, not seconds.**

### Why Speed Matters

- Run tests frequently (every save)
- Quick feedback loop
- Developers actually run them
- CI/CD pipelines are fast

### Target Speed

- **Each unit test**: < 10ms
- **Test suite (100 tests)**: < 1 second
- **Full suite (1000 tests)**: < 10 seconds

### Make Tests Fast: Mock Slow Dependencies

**Slow dependencies to mock**:

- Database calls
- API requests
- File I/O
- Network operations
- Sleep/delays
- Email sending

**Python Example**:

```python
# ❌ SLOW: Hits real database
def test_get_user():
    # Takes 50-100ms per test
    user = database.query("SELECT * FROM users WHERE id=1")
    assert user.name == "Alice"

# ✅ FAST: Mocked database
def test_get_user():
    mock_db = Mock()
    mock_db.query.return_value = User(id=1, name="Alice")

    service = UserService(mock_db)
    user = service.get_user(1)

    assert user.name == "Alice"
    # Takes < 1ms
```

**JavaScript Example**:

```javascript
// ❌ SLOW: Makes real API call
test("fetches user data", async () => {
  // Takes 200-500ms per test
  const user = await api.fetchUser(1);
  expect(user.name).toBe("Alice");
});

// ✅ FAST: Mocked API
test("fetches user data", async () => {
  const mockApi = {
    fetchUser: jest.fn().mockResolvedValue({ id: 1, name: "Alice" }),
  };

  const service = new UserService(mockApi);
  const user = await service.getUser(1);

  expect(user.name).toBe("Alice");
  // Takes < 1ms
});
```

### Don't Mock Everything

**Do mock**:

- External APIs
- Databases
- File system
- Network
- Time

**Don't mock**:

- Your own code
- Pure functions
- Value objects
- Simple utilities

---

## Baby Steps

### The Principle

**Take the smallest possible increments.**

### Why Baby Steps?

- Easier to debug
- Less to think about
- Faster feedback
- Builds confidence
- Reduces risk

### Example: Implementing a Calculator

**Baby steps**:

```python
# Step 1: Handle zero
def test_add_zero():
    assert add(0, 0) == 0

# Step 2: Handle positive numbers
def test_add_positive():
    assert add(2, 3) == 5

# Step 3: Handle negative numbers
def test_add_negative():
    assert add(-2, 3) == 1

# Step 4: Handle mixed
def test_add_mixed():
    assert add(-5, -3) == -8
```

**NOT baby steps** (too big):

```python
# ❌ BAD: One giant test
def test_calculator():
    assert add(0, 0) == 0
    assert add(2, 3) == 5
    assert add(-2, 3) == 1
    assert subtract(5, 3) == 2
    assert multiply(2, 3) == 6
    assert divide(6, 3) == 2
    # Too much at once!
```

### How Small Is Small Enough?

**Rule of thumb**: If a test fails, you should know immediately what's wrong.

```python
# ✅ GOOD: Clear failure
def test_discount_is_10_percent():
    discount = calculate_discount(100, 10)
    assert discount == 10
    # If fails, we know discount calculation is wrong

# ❌ BAD: Unclear failure
def test_order_processing():
    order = process_order(items, user, payment)
    assert order.status == "completed"
    # If fails, what's wrong? Items? User? Payment? Status?
```

---

## Test Smells and How to Fix Them

### Smell 1: Test Too Long

**Problem**: Test is > 20 lines

```python
# ❌ BAD: Too long
def test_order_processing():
    # 50 lines of setup
    user = User(...)
    items = [Item(...), Item(...), ...]
    payment = Payment(...)
    shipping = Shipping(...)
    # ... 20 more lines ...

    order = process_order(...)

    # 20 lines of assertions
    assert ...
    # ... more assertions ...
```

**Fix**: Extract setup to helper methods

```python
# ✅ GOOD: Clean and focused
def test_order_processing():
    # Arrange
    user = create_test_user()
    items = create_test_items()
    payment = create_test_payment()

    # Act
    order = process_order(user, items, payment)

    # Assert
    assert order.status == "completed"

def create_test_user():
    return User(email="test@example.com", name="Test")

def create_test_items():
    return [Item(name="Laptop", price=1000)]

def create_test_payment():
    return Payment(card="4111111111111111")
```

### Smell 2: Duplicate Setup

**Problem**: Same setup code in multiple tests

```python
# ❌ BAD: Duplicated setup
def test_login():
    service = UserService()
    service.register("alice@example.com", "pass")
    # ...

def test_logout():
    service = UserService()
    service.register("alice@example.com", "pass")
    # ...

def test_profile():
    service = UserService()
    service.register("alice@example.com", "pass")
    # ...
```

**Fix**: Use setup method or fixtures

```python
# ✅ GOOD: Shared setup
class TestUserService:
    def setup_method(self):
        self.service = UserService()
        self.user = self.service.register("alice@example.com", "pass")

    def test_login(self):
        token = self.service.login("alice@example.com", "pass")
        assert token is not None

    def test_logout(self):
        self.service.logout(self.user)
        assert self.user.is_logged_in == False
```

### Smell 3: Magic Numbers

**Problem**: Unclear what numbers represent

```python
# ❌ BAD: Magic numbers
def test_discount():
    discount = calculate_discount(100, 0.1)
    assert discount == 10
```

**Fix**: Use named constants

```python
# ✅ GOOD: Named values
def test_discount():
    original_price = 100
    discount_percentage = 0.1
    expected_discount = 10

    discount = calculate_discount(original_price, discount_percentage)
    assert discount == expected_discount
```

### Smell 4: Testing Private Methods

**Problem**: Tests reach into internal implementation

```python
# ❌ BAD: Testing private method
def test_validate_email_format():
    validator = UserValidator()
    assert validator._validate_email_format("alice@example.com") == True
```

**Fix**: Test through public interface

```python
# ✅ GOOD: Test public behavior
def test_validates_user_with_valid_email():
    validator = UserValidator()
    user = User(email="alice@example.com")
    assert validator.validate(user) == True

def test_rejects_user_with_invalid_email():
    validator = UserValidator()
    user = User(email="not-an-email")
    assert validator.validate(user) == False
```

### Smell 5: Conditional Logic in Tests

**Problem**: Tests have if/else or loops

```python
# ❌ BAD: Conditional in test
def test_validation():
    users = get_test_users()
    for user in users:
        if user.is_admin:
            assert validate(user) == True
        else:
            assert validate(user) == False
```

**Fix**: Separate tests for each case

```python
# ✅ GOOD: Separate tests
def test_validates_admin_user():
    admin = User(role="admin")
    assert validate(admin) == True

def test_validates_regular_user():
    user = User(role="user")
    assert validate(user) == False
```

### Smell 6: Testing Too Much

**Problem**: Test verifies everything

```python
# ❌ BAD: Over-asserting
def test_user_creation():
    user = create_user("alice@example.com")

    # Testing too many implementation details
    assert user.id is not None
    assert user.email == "alice@example.com"
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.is_active == True
    assert user.is_verified == False
    assert user.login_count == 0
    assert user.last_login is None
    assert len(user.sessions) == 0
```

**Fix**: Test what matters

```python
# ✅ GOOD: Test essential behavior
def test_creates_user_with_email():
    user = create_user("alice@example.com")
    assert user.email == "alice@example.com"

def test_creates_user_as_active():
    user = create_user("alice@example.com")
    assert user.is_active == True
```

---

## Refactoring Techniques in TDD

### Extract Method

```python
# Before
def test_order():
    items = [
        Item(name="Laptop", price=1000, quantity=1),
        Item(name="Mouse", price=20, quantity=2)
    ]
    order = Order(items)
    assert order.total == 1040

# After
def test_order():
    items = create_typical_order_items()
    order = Order(items)
    assert order.total == 1040

def create_typical_order_items():
    return [
        Item(name="Laptop", price=1000, quantity=1),
        Item(name="Mouse", price=20, quantity=2)
    ]
```

### Test Data Builders

```python
# Test Data Builder Pattern
class UserBuilder:
    def __init__(self):
        self.email = "test@example.com"
        self.name = "Test User"
        self.is_admin = False

    def with_email(self, email):
        self.email = email
        return self

    def with_name(self, name):
        self.name = name
        return self

    def as_admin(self):
        self.is_admin = True
        return self

    def build(self):
        return User(
            email=self.email,
            name=self.name,
            is_admin=self.is_admin
        )

# Usage
def test_admin_access():
    admin = UserBuilder().as_admin().build()
    assert can_access_admin_panel(admin) == True

def test_user_access():
    user = UserBuilder().build()
    assert can_access_admin_panel(user) == False
```

---

## Coverage with TDD

### Natural High Coverage

**TDD naturally achieves 80-95% coverage:**

- Every line written has a test
- No untested code
- Edge cases covered incrementally

### Don't Chase 100%

```python
# Some code doesn't need tests:

# 1. Simple getters/setters
class User:
    def get_name(self):
        return self.name  # No test needed

# 2. Framework boilerplate
if __name__ == "__main__":
    app.run()  # No test needed

# 3. Trivial code
def to_string(self):
    return f"User({self.email})"  # No test needed
```

### Coverage as Safety Net, Not Goal

```python
# ✅ GOOD: High coverage from TDD
# You wrote tests first, so coverage is natural

# ❌ BAD: Writing tests to hit coverage target
# Writing tests just to increase coverage percentage
```

---

## 10 Best Practices Summary

### 1. Write Test First

Always RED before GREEN.

### 2. Test Behavior, Not Implementation

Focus on what, not how.

### 3. Keep Tests Small and Focused

One logical concept per test.

### 4. Use Descriptive Names

Test names are documentation.

### 5. Follow AAA Pattern

Arrange, Act, Assert.

### 6. Make Tests Independent

Run in any order.

### 7. Keep Tests Fast

Mock slow dependencies.

### 8. Take Baby Steps

Smallest increments possible.

### 9. Refactor Regularly

Keep code clean after each green.

### 10. Run Tests Frequently

After every change.

---

## Key Takeaways

1. **Test names** should clearly describe behavior
2. **AAA pattern** provides clear structure
3. **Given-When-Then** makes tests readable
4. **One assertion** per test when possible
5. **Independent tests** can run in any order
6. **Fast tests** provide quick feedback
7. **Baby steps** reduce risk and complexity
8. **Test smells** indicate design problems
9. **High coverage** comes naturally with TDD
10. **Refactor regularly** to keep code clean

---

## Practice Exercises

### Exercise 1: Improve Test Names

Rename these tests to be more descriptive:

```python
def test_validation():
    pass

def test_process():
    pass

def test_user():
    pass
```

### Exercise 2: Apply AAA Pattern

Refactor this test to use AAA pattern:

```python
def test_order():
    order = Order([Item("Laptop", 1000)])
    assert order.total == 1080  # with 8% tax
```

### Exercise 3: Fix Test Smells

Identify and fix the smells in this test:

```python
def test_user_operations():
    service = UserService()
    user = service.create("alice@example.com")
    if user.is_active:
        assert service.login(user.email, "pass") is not None
    service.update(user, name="Alice")
    assert user.name == "Alice"
```

### Exercise 4: Speed Up Tests

Make this test faster:

```python
def test_user_service():
    db = PostgresDatabase("production_db")
    service = UserService(db)
    user = service.get_user(1)
    assert user.email == "alice@example.com"
```

---

## Next Steps

Now that you know the best practices, learn what NOT to do:

1. **[TDD Anti-Patterns](./04-tdd-anti-patterns.md)** - Common mistakes to avoid

---

## Additional Resources

- [xUnit Test Patterns](http://xunitpatterns.com/)
- [Growing Object-Oriented Software, Guided by Tests](http://www.growing-object-oriented-software.com/)
- [Test Desiderata](https://kentbeck.github.io/TestDesiderata/) - Kent Beck's properties of good tests

---

**Remember**: Good tests are clean code. Apply the same care to test code as production code! ✨
