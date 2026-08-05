# Testing Guidelines

## 🎯 Testing Philosophy

**Write tests to**:

- ✅ Catch bugs before production
- ✅ Enable refactoring with confidence
- ✅ Document expected behavior
- ✅ Improve code design

**Don't write tests to**:

- ❌ Hit coverage targets artificially
- ❌ Test framework code
- ❌ Test external libraries

---

## 🏗️ Test Structure

### AAA Pattern (Arrange-Act-Assert)

Every test should follow this structure:

```python
def test_user_login_success():
    # Arrange - Set up test data and preconditions
    user = create_test_user(email="test@example.com", password="Pass123!")

    # Act - Execute the code being tested
    result = login_service.login("test@example.com", "Pass123!")

    # Assert - Verify the expected outcome
    assert result.success is True
    assert result.token is not None
    assert result.user_id == user.id
```

### Test Naming

**Format**: `test_<what>_<condition>_<expected>`

**Good names** ✅:

```python
test_login_with_valid_credentials_returns_token()
test_login_with_invalid_password_raises_error()
test_add_to_cart_when_out_of_stock_returns_error()
test_calculate_total_with_discount_applies_correctly()
```

**Bad names** ❌:

```python
test_login()
test_1()
test_cart()
test_it_works()
```

---

## 📝 Writing Good Tests

### 1. One Assertion Per Test (When Possible)

**Bad** ❌:

```python
def test_user_registration():
    user = register_user("test@example.com", "Pass123!")
    assert user is not None
    assert user.email == "test@example.com"
    assert user.password != "Pass123!"  # Should be hashed
    assert user.id is not None
    assert user.created_at is not None
    # If first assert fails, others never run!
```

**Good** ✅:

```python
def test_registration_creates_user():
    user = register_user("test@example.com", "Pass123!")
    assert user is not None

def test_registration_stores_email():
    user = register_user("test@example.com", "Pass123!")
    assert user.email == "test@example.com"

def test_registration_hashes_password():
    user = register_user("test@example.com", "Pass123!")
    assert user.password != "Pass123!"
```

### 2. Test Edge Cases

Don't just test the happy path!

```python
# Happy path
def test_divide_positive_numbers():
    assert divide(10, 2) == 5

# Edge cases
def test_divide_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_negative_numbers():
    assert divide(-10, 2) == -5

def test_divide_float_result():
    assert divide(10, 3) == pytest.approx(3.333, rel=0.001)
```

### 3. Use Fixtures for Setup

**Bad** ❌:

```python
def test_something():
    db = Database("test.db")
    db.connect()
    user = User(email="test@example.com")
    db.add(user)
    # Test code
    db.close()

def test_something_else():
    db = Database("test.db")  # Duplicated setup!
    db.connect()
    user = User(email="test@example.com")
    db.add(user)
    # Test code
    db.close()
```

**Good** ✅:

```python
@pytest.fixture
def db():
    database = Database("test.db")
    database.connect()
    yield database
    database.close()

@pytest.fixture
def test_user(db):
    user = User(email="test@example.com")
    db.add(user)
    return user

def test_something(test_user):
    # test_user is ready to use
    assert test_user.email == "test@example.com"

def test_something_else(test_user):
    # Reuse same fixture
    assert test_user.id is not None
```

### 4. Test Isolation

Each test should be independent:

**Bad** ❌:

```python
# Test 2 depends on Test 1 running first!
def test_create_user():
    global user
    user = create_user("test@example.com")

def test_login_user():
    login(user.email, "password")  # Breaks if test_create_user fails
```

**Good** ✅:

```python
@pytest.fixture
def created_user():
    return create_user("test@example.com")

def test_create_user():
    user = create_user("test@example.com")
    assert user is not None

def test_login_user(created_user):
    result = login(created_user.email, "password")
    assert result.success is True
```

---

## 🎭 Mocking

### When to Mock

**Mock**:

- ✅ External APIs (HTTP requests)
- ✅ File system operations
- ✅ Database in unit tests
- ✅ Time-dependent functions
- ✅ Random number generators
- ✅ Email services

**Don't Mock**:

- ❌ Your own code (test it for real)
- ❌ Simple data structures
- ❌ Database in integration tests

### Mocking Examples

**Python (unittest.mock)**:

```python
from unittest.mock import Mock, patch
import pytest

# Mock an external API
@patch('requests.get')
def test_fetch_user_data(mock_get):
    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "Test User"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Act
    user = fetch_user_from_api(user_id=1)

    # Assert
    assert user.name == "Test User"
    mock_get.assert_called_once_with("https://api.example.com/users/1")

# Mock time
@patch('time.time')
def test_token_expiration(mock_time):
    mock_time.return_value = 1000
    token = generate_token()

    mock_time.return_value = 2000  # 1000 seconds later
    assert is_token_expired(token) is False

    mock_time.return_value = 100000  # Way later
    assert is_token_expired(token) is True
```

**JavaScript (Jest)**:

```javascript
// Mock a module
jest.mock("../api/userService");
import { fetchUser } from "../api/userService";

test("displays user data", async () => {
  // Arrange
  fetchUser.mockResolvedValue({ id: 1, name: "Test User" });

  // Act
  const user = await getUserData(1);

  // Assert
  expect(user.name).toBe("Test User");
  expect(fetchUser).toHaveBeenCalledWith(1);
});

// Mock timer
jest.useFakeTimers();

test("calls callback after timeout", () => {
  const callback = jest.fn();
  setTimeout(callback, 1000);

  jest.advanceTimersByTime(1000);

  expect(callback).toHaveBeenCalled();
});
```

---

## 🧪 Test Types

### Unit Tests

**Purpose**: Test individual functions/methods in isolation

**Characteristics**:

- Fast (< 1ms each)
- No external dependencies
- Mock everything external
- Many tests (50+)

**Example**:

```python
def test_calculate_discount():
    # Pure function, no dependencies
    result = calculate_discount(price=100, discount_percent=20)
    assert result == 80
```

### Integration Tests

**Purpose**: Test how components work together

**Characteristics**:

- Slower (100ms - 1s each)
- Use real database (test DB)
- Test API endpoints
- Fewer tests (20+)

**Example**:

```python
def test_user_registration_flow(test_db, test_client):
    # Tests API endpoint + database + email service
    response = test_client.post('/api/register', json={
        "email": "test@example.com",
        "password": "Pass123!"
    })

    assert response.status_code == 201

    # Verify user in database
    user = test_db.query(User).filter_by(email="test@example.com").first()
    assert user is not None
```

### E2E Tests

**Purpose**: Test entire user workflows

**Characteristics**:

- Very slow (seconds each)
- Use real browser
- Test like a user would
- Few tests (5-15)

**Example**:

```python
def test_complete_purchase_flow(browser):
    # Full user journey
    browser.goto("http://localhost:3000")
    browser.click_button("Sign Up")
    browser.fill_input("email", "test@example.com")
    browser.fill_input("password", "Pass123!")
    browser.click_button("Register")

    # Should be logged in
    assert browser.is_visible("Welcome, test@example.com")

    # Add to cart and checkout
    browser.click_link("Products")
    browser.click_button("Add to Cart")
    browser.click_link("Cart")
    browser.click_button("Checkout")

    # Fill payment
    browser.fill_input("card_number", "4242424242424242")
    browser.click_button("Pay")

    # Verify order confirmation
    assert browser.is_visible("Order Confirmed")
```

---

## 📊 Test Coverage

### Coverage Goals

- **Minimum**: 80% overall
- **Critical modules**: 90%+ (auth, payments, orders)
- **Utilities**: 90%+
- **UI components**: 70%+

### What to Focus On

**High priority**:

- ✅ Business logic
- ✅ Security-critical code
- ✅ Data validation
- ✅ Error handling
- ✅ Edge cases

**Lower priority**:

- Configuration files
- Simple getters/setters
- Framework boilerplate
- Obvious code

### Running Coverage

**Python**:

```bash
# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html

# Fail if coverage below threshold
pytest --cov=src --cov-fail-under=80
```

**JavaScript**:

```bash
# Run with coverage
npm test -- --coverage

# View HTML report
open coverage/lcov-report/index.html

# Set threshold in package.json
{
  "jest": {
    "coverageThreshold": {
      "global": {
        "lines": 80,
        "branches": 80
      }
    }
  }
}
```

---

## 🚀 Test Performance

### Keep Tests Fast

**Slow tests**:

- Won't be run frequently
- Slow down CI/CD
- Frustrate developers

**Speed targets**:

- Unit tests: < 10ms each
- Integration tests: < 1s each
- Full test suite: < 5 minutes

### Making Tests Faster

1. **Use in-memory database**

   ```python
   @pytest.fixture
   def db():
       engine = create_engine("sqlite:///:memory:")
       # Much faster than disk-based DB
   ```

2. **Parallel execution**

   ```bash
   # Python
   pytest -n auto  # Use all CPU cores

   # JavaScript
   npm test -- --maxWorkers=4
   ```

3. **Skip slow tests during development**

   ```python
   @pytest.mark.slow
   def test_large_data_processing():
       pass

   # Run without slow tests
   pytest -m "not slow"
   ```

---

## 🐛 Test-Driven Debugging

When you find a bug:

1. **Write a failing test** that reproduces the bug
2. **Fix the code** to make the test pass
3. **Keep the test** to prevent regression

**Example**:

```python
# Bug reported: discount not applied correctly

# 1. Write failing test
def test_discount_applied_to_cart_total():
    cart = Cart()
    cart.add_item(Product(price=100))
    cart.apply_discount(percent=20)

    # This will fail initially
    assert cart.total == 80

# 2. Fix the bug in Cart.apply_discount()

# 3. Test now passes, bug won't come back!
```

---

## ✅ Testing Checklist

### Before Committing

- [ ] All tests pass
- [ ] New tests added for new code
- [ ] Coverage maintained or improved
- [ ] No debug statements in tests
- [ ] Tests are independent
- [ ] Tests have clear names

### Code Review

- [ ] Test edge cases
- [ ] Test error paths
- [ ] Appropriate use of mocks
- [ ] Tests are maintainable
- [ ] No flaky tests

---

## 🎓 Common Testing Mistakes

### ❌ Testing Implementation Details

**Bad**:

```python
def test_user_service_calls_database():
    # Testing HOW, not WHAT
    mock_db = Mock()
    service = UserService(mock_db)
    service.get_user(1)
    mock_db.query.assert_called_once()  # Who cares how it's implemented?
```

**Good**:

```python
def test_get_user_returns_correct_user():
    # Testing WHAT, not HOW
    user = user_service.get_user(1)
    assert user.id == 1
    assert user.email == "test@example.com"
```

### ❌ Brittle Tests

**Bad**:

```python
def test_error_message():
    with pytest.raises(ValueError) as exc:
        divide(10, 0)
    # Breaks if error message changes slightly
    assert str(exc.value) == "Error: Cannot divide by zero. Please provide a non-zero divisor."
```

**Good**:

```python
def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError):
        divide(10, 0)
    # Just verify the error type
```

### ❌ Not Testing Negative Cases

**Bad**:

```python
def test_login():
    assert login("user@example.com", "correctPassword") is not None
    # What about wrong password? Missing user? Empty strings?
```

**Good**:

```python
def test_login_success():
    assert login("user@example.com", "correctPassword") is not None

def test_login_wrong_password():
    with pytest.raises(InvalidCredentialsError):
        login("user@example.com", "wrongPassword")

def test_login_user_not_found():
    with pytest.raises(UserNotFoundError):
        login("nonexistent@example.com", "password")
```

---

## 📚 Resources

- [Python Testing Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [Jest Best Practices](https://jestjs.io/docs/tutorial-react)
- [Testing Trophy](https://kentcdodds.com/blog/write-tests)
- [Google Testing Blog](https://testing.googleblog.com/)

---

**Remember**: Tests are code too. Keep them clean, maintainable, and valuable! ✅
