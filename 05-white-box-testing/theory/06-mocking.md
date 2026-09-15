# Mocking and Test Doubles

**Module**: 5 - White Box Testing  
**Topic**: Isolating Dependencies in Unit Tests  
**Reading Time**: 30 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Understand why mocking is necessary in unit tests
- Distinguish between mocks, stubs, fakes, and spies
- Use Python's `unittest.mock` library effectively
- Use Jest's mocking capabilities in JavaScript
- Mock external dependencies (files, databases, APIs, time)
- Apply mocking best practices and avoid anti-patterns
- Know when to mock and when not to mock

---

## Why Mock?

### The Problem: External Dependencies

Unit tests should be:

- **Fast**: Run in milliseconds
- **Isolated**: No external dependencies
- **Reliable**: Same result every time
- **Safe**: Don't modify real data

**But real code has dependencies**:

```python
def send_welcome_email(user):
    # Problem 1: Hits real email server (slow, requires network)
    email_client.send(
        to=user.email,
        subject="Welcome!",
        body=f"Hello {user.name}"
    )

    # Problem 2: Writes to real database (side effects)
    database.update_user(user.id, email_sent=True)

    # Problem 3: Current time (non-deterministic)
    log_event("email_sent", timestamp=datetime.now())
```

### The Solution: Mocking

**Replace real dependencies with test doubles**:

```python
def test_send_welcome_email():
    # Mock email client
    mock_email = Mock()

    # Mock database
    mock_db = Mock()

    # Mock time
    with freeze_time("2026-08-04 10:00:00"):
        send_welcome_email(user, mock_email, mock_db)

    # Verify behavior
    mock_email.send.assert_called_once()
    mock_db.update_user.assert_called_with(user.id, email_sent=True)
```

**Benefits**:

- ✅ Fast (no network, no I/O)
- ✅ Isolated (no external dependencies)
- ✅ Reliable (deterministic results)
- ✅ Safe (no side effects)

---

## Test Doubles: Types and When to Use

### 1. Dummy

**Purpose**: Fill parameter lists but never used

```python
def create_user(name, email, phone):
    # phone not used in this test
    pass

def test_create_user():
    dummy_phone = None  # Dummy - not used
    user = create_user("Alice", "alice@example.com", dummy_phone)
```

### 2. Stub

**Purpose**: Provide canned responses to calls

```python
# Stub returns fixed data
class StubDatabase:
    def get_user(self, user_id):
        return {"id": user_id, "name": "Test User"}

def test_get_user_name():
    stub_db = StubDatabase()
    service = UserService(stub_db)

    name = service.get_user_name(123)
    assert name == "Test User"
```

**Use when**: You need specific return values but don't care about interaction

### 3. Fake

**Purpose**: Working implementation, but simplified

```python
# Fake has working logic, just simpler
class FakeDatabase:
    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

def test_save_and_retrieve():
    fake_db = FakeDatabase()
    fake_db.save("user_1", {"name": "Alice"})

    user = fake_db.get("user_1")
    assert user["name"] == "Alice"
```

**Use when**: You need realistic behavior without external dependencies

### 4. Mock

**Purpose**: Verify interactions and behavior

```python
def test_user_service_calls_database():
    mock_db = Mock()
    service = UserService(mock_db)

    service.delete_user(123)

    # Verify the interaction happened
    mock_db.delete.assert_called_once_with(123)
```

**Use when**: You care about _how_ code interacts with dependencies

### 5. Spy

**Purpose**: Record information about calls while delegating to real object

```python
def test_email_service_tracks_sends():
    real_email = EmailService()
    spy_email = Spy(real_email)

    service = NotificationService(spy_email)
    service.notify_user(user)

    # Real email was sent AND we can verify
    assert spy_email.send_count == 1
    assert spy_email.last_recipient == user.email
```

**Use when**: You need both real behavior and verification

### Summary Table

| Type  | Returns Data? | Verifies Calls? | Has Logic? | Use Case                              |
| ----- | ------------- | --------------- | ---------- | ------------------------------------- |
| Dummy | ❌            | ❌              | ❌         | Unused parameters                     |
| Stub  | ✅            | ❌              | ❌         | Return fixed values                   |
| Fake  | ✅            | ❌              | ✅         | Simplified but working implementation |
| Mock  | ✅            | ✅              | ❌         | Verify interactions                   |
| Spy   | ✅            | ✅              | ✅         | Record calls to real object           |

---

## Python: unittest.mock

### Basic Mock Creation

```python
from unittest.mock import Mock

# Create a mock object
mock_obj = Mock()

# Call it however you want
mock_obj.method()
mock_obj.method(1, 2, 3)
mock_obj.attribute
mock_obj.anything.can.be.called()

# Everything succeeds (returns another Mock by default)
```

### Configuring Return Values

```python
from unittest.mock import Mock

mock_db = Mock()

# Set return value
mock_db.get_user.return_value = {"id": 1, "name": "Alice"}

# Use it
user = mock_db.get_user(1)
print(user)  # {"id": 1, "name": "Alice"}
```

### Making Mocks Raise Exceptions

```python
mock_db = Mock()

# Make it raise an exception
mock_db.connect.side_effect = ConnectionError("Database unavailable")

# This will raise
try:
    mock_db.connect()
except ConnectionError as e:
    print(e)  # Database unavailable
```

### Verifying Calls

```python
mock_email = Mock()

# Code under test
send_notification(user, mock_email)

# Verify it was called
mock_email.send.assert_called()

# Verify called once
mock_email.send.assert_called_once()

# Verify called with specific arguments
mock_email.send.assert_called_with(
    to="user@example.com",
    subject="Welcome"
)

# Verify called with any arguments containing
mock_email.send.assert_called_once_with(
    to="user@example.com",
    subject=ANY
)
```

### The `patch` Decorator

**Replace objects during test execution**:

```python
from unittest.mock import patch

# Original code
# email_service.py
import smtplib

def send_email(to, subject, body):
    server = smtplib.SMTP("smtp.gmail.com")
    server.send_message(to, subject, body)
    server.quit()

# Test with patch
from unittest.mock import patch

@patch('email_service.smtplib.SMTP')
def test_send_email(mock_smtp):
    # mock_smtp is automatically created
    mock_server = Mock()
    mock_smtp.return_value = mock_server

    send_email("user@example.com", "Hello", "Body")

    # Verify SMTP was used correctly
    mock_smtp.assert_called_once_with("smtp.gmail.com")
    mock_server.send_message.assert_called_once()
    mock_server.quit.assert_called_once()
```

### `patch` as Context Manager

```python
def test_send_email():
    with patch('email_service.smtplib.SMTP') as mock_smtp:
        mock_server = Mock()
        mock_smtp.return_value = mock_server

        send_email("user@example.com", "Hello", "Body")

        mock_server.send_message.assert_called_once()
```

---

## Python Complete Example

### Code to Test

```python
# order_service.py
import requests
from datetime import datetime
from database import Database
from email_service import EmailService

class OrderService:
    def __init__(self, db, email_service):
        self.db = db
        self.email_service = email_service

    def place_order(self, user_id, items):
        # Get user from database
        user = self.db.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        # Calculate total
        total = sum(item['price'] * item['quantity'] for item in items)

        # Check inventory via external API
        response = requests.post(
            "https://api.inventory.com/check",
            json={"items": items}
        )
        if response.status_code != 200:
            raise ValueError("Inventory check failed")

        # Create order in database
        order = {
            "user_id": user_id,
            "items": items,
            "total": total,
            "created_at": datetime.now()
        }
        order_id = self.db.create_order(order)

        # Send confirmation email
        self.email_service.send(
            to=user['email'],
            subject="Order Confirmation",
            body=f"Your order #{order_id} has been placed!"
        )

        return order_id
```

### Tests with Mocking

```python
# test_order_service.py
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from order_service import OrderService

class TestOrderService:
    def setup_method(self):
        self.mock_db = Mock()
        self.mock_email = Mock()
        self.service = OrderService(self.mock_db, self.mock_email)

    @patch('order_service.requests')
    @patch('order_service.datetime')
    def test_place_order_success(self, mock_datetime, mock_requests):
        # Arrange: Set up mocks
        fixed_time = datetime(2026, 8, 4, 10, 0, 0)
        mock_datetime.now.return_value = fixed_time

        self.mock_db.get_user.return_value = {
            "id": 1,
            "email": "user@example.com"
        }

        mock_response = Mock()
        mock_response.status_code = 200
        mock_requests.post.return_value = mock_response

        self.mock_db.create_order.return_value = 12345

        items = [
            {"name": "Laptop", "price": 1000, "quantity": 1},
            {"name": "Mouse", "price": 20, "quantity": 2}
        ]

        # Act
        order_id = self.service.place_order(user_id=1, items=items)

        # Assert
        assert order_id == 12345

        # Verify database interactions
        self.mock_db.get_user.assert_called_once_with(1)
        self.mock_db.create_order.assert_called_once()

        # Verify order data
        call_args = self.mock_db.create_order.call_args[0][0]
        assert call_args['user_id'] == 1
        assert call_args['total'] == 1040  # 1000 + 20*2
        assert call_args['created_at'] == fixed_time

        # Verify API call
        mock_requests.post.assert_called_once_with(
            "https://api.inventory.com/check",
            json={"items": items}
        )

        # Verify email sent
        self.mock_email.send.assert_called_once_with(
            to="user@example.com",
            subject="Order Confirmation",
            body="Your order #12345 has been placed!"
        )

    def test_place_order_user_not_found(self):
        # Arrange
        self.mock_db.get_user.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="User not found"):
            self.service.place_order(user_id=999, items=[])

        # Verify no other operations happened
        self.mock_db.create_order.assert_not_called()
        self.mock_email.send.assert_not_called()

    @patch('order_service.requests')
    def test_place_order_inventory_check_fails(self, mock_requests):
        # Arrange
        self.mock_db.get_user.return_value = {"id": 1, "email": "user@example.com"}

        mock_response = Mock()
        mock_response.status_code = 500
        mock_requests.post.return_value = mock_response

        # Act & Assert
        with pytest.raises(ValueError, match="Inventory check failed"):
            self.service.place_order(user_id=1, items=[{"name": "Laptop", "price": 1000, "quantity": 1}])
```

---

## JavaScript: Jest Mocking

### Basic Mock Creation

```javascript
// Create a mock function
const mockFn = jest.fn();

// Call it
mockFn("hello");
mockFn(1, 2, 3);

// Check calls
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(2);
expect(mockFn).toHaveBeenCalledWith("hello");
```

### Mock Return Values

```javascript
const mockFn = jest.fn();

// Set return value
mockFn.mockReturnValue(42);
console.log(mockFn()); // 42

// Set different values for multiple calls
mockFn.mockReturnValueOnce(1).mockReturnValueOnce(2).mockReturnValue(3);

console.log(mockFn()); // 1
console.log(mockFn()); // 2
console.log(mockFn()); // 3
console.log(mockFn()); // 3
```

### Mock Async Functions

```javascript
const mockAsyncFn = jest.fn();

// Resolve with value
mockAsyncFn.mockResolvedValue({ id: 1, name: "Alice" });

// Use it
const result = await mockAsyncFn();
console.log(result); // { id: 1, name: 'Alice' }

// Reject with error
mockAsyncFn.mockRejectedValue(new Error("Failed"));
```

### Mock Modules

```javascript
// userService.js
const axios = require("axios");

async function fetchUser(id) {
  const response = await axios.get(`https://api.example.com/users/${id}`);
  return response.data;
}

module.exports = { fetchUser };

// userService.test.js
jest.mock("axios");
const axios = require("axios");
const { fetchUser } = require("./userService");

test("fetchUser returns user data", async () => {
  // Mock axios.get
  axios.get.mockResolvedValue({
    data: { id: 1, name: "Alice" },
  });

  const user = await fetchUser(1);

  expect(user).toEqual({ id: 1, name: "Alice" });
  expect(axios.get).toHaveBeenCalledWith("https://api.example.com/users/1");
});
```

### Mock Implementation

```javascript
const mockFn = jest.fn((a, b) => a + b);

console.log(mockFn(2, 3)); // 5

// Or use mockImplementation
mockFn.mockImplementation((a, b) => a * b);
console.log(mockFn(2, 3)); // 6
```

---

## JavaScript Complete Example

### Code to Test

```javascript
// orderService.js
const axios = require("axios");

class OrderService {
  constructor(database, emailService) {
    this.db = database;
    this.emailService = emailService;
  }

  async placeOrder(userId, items) {
    // Get user from database
    const user = await this.db.getUser(userId);
    if (!user) {
      throw new Error("User not found");
    }

    // Calculate total
    const total = items.reduce((sum, item) => {
      return sum + item.price * item.quantity;
    }, 0);

    // Check inventory via external API
    const response = await axios.post("https://api.inventory.com/check", {
      items,
    });

    if (response.status !== 200) {
      throw new Error("Inventory check failed");
    }

    // Create order in database
    const order = {
      userId,
      items,
      total,
      createdAt: new Date(),
    };

    const orderId = await this.db.createOrder(order);

    // Send confirmation email
    await this.emailService.send({
      to: user.email,
      subject: "Order Confirmation",
      body: `Your order #${orderId} has been placed!`,
    });

    return orderId;
  }
}

module.exports = OrderService;
```

### Tests with Mocking

```javascript
// orderService.test.js
jest.mock("axios");
const axios = require("axios");
const OrderService = require("./orderService");

describe("OrderService", () => {
  let service;
  let mockDb;
  let mockEmailService;

  beforeEach(() => {
    // Create mocks
    mockDb = {
      getUser: jest.fn(),
      createOrder: jest.fn(),
    };

    mockEmailService = {
      send: jest.fn(),
    };

    service = new OrderService(mockDb, mockEmailService);

    // Reset axios mock
    axios.post.mockReset();
  });

  test("places order successfully", async () => {
    // Arrange
    const fixedDate = new Date("2026-08-04T10:00:00");
    jest.spyOn(global, "Date").mockImplementation(() => fixedDate);

    mockDb.getUser.mockResolvedValue({
      id: 1,
      email: "user@example.com",
    });

    axios.post.mockResolvedValue({
      status: 200,
      data: { available: true },
    });

    mockDb.createOrder.mockResolvedValue(12345);
    mockEmailService.send.mockResolvedValue(true);

    const items = [
      { name: "Laptop", price: 1000, quantity: 1 },
      { name: "Mouse", price: 20, quantity: 2 },
    ];

    // Act
    const orderId = await service.placeOrder(1, items);

    // Assert
    expect(orderId).toBe(12345);

    // Verify database interactions
    expect(mockDb.getUser).toHaveBeenCalledWith(1);
    expect(mockDb.createOrder).toHaveBeenCalledTimes(1);

    const orderArg = mockDb.createOrder.mock.calls[0][0];
    expect(orderArg.userId).toBe(1);
    expect(orderArg.total).toBe(1040); // 1000 + 20*2
    expect(orderArg.createdAt).toEqual(fixedDate);

    // Verify API call
    expect(axios.post).toHaveBeenCalledWith("https://api.inventory.com/check", {
      items,
    });

    // Verify email sent
    expect(mockEmailService.send).toHaveBeenCalledWith({
      to: "user@example.com",
      subject: "Order Confirmation",
      body: "Your order #12345 has been placed!",
    });

    // Cleanup
    global.Date.mockRestore();
  });

  test("throws error when user not found", async () => {
    // Arrange
    mockDb.getUser.mockResolvedValue(null);

    // Act & Assert
    await expect(service.placeOrder(999, [])).rejects.toThrow("User not found");

    // Verify no other operations happened
    expect(mockDb.createOrder).not.toHaveBeenCalled();
    expect(mockEmailService.send).not.toHaveBeenCalled();
  });

  test("throws error when inventory check fails", async () => {
    // Arrange
    mockDb.getUser.mockResolvedValue({
      id: 1,
      email: "user@example.com",
    });

    axios.post.mockResolvedValue({
      status: 500,
    });

    const items = [{ name: "Laptop", price: 1000, quantity: 1 }];

    // Act & Assert
    await expect(service.placeOrder(1, items)).rejects.toThrow(
      "Inventory check failed",
    );
  });
});
```

---

## Mocking Specific Scenarios

### 1. Mocking File System

**Python**:

```python
from unittest.mock import mock_open, patch

def read_config(filename):
    with open(filename) as f:
        return f.read()

def test_read_config():
    mock_file_content = "setting=value"

    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        config = read_config('config.txt')
        assert config == "setting=value"
```

**JavaScript**:

```javascript
jest.mock("fs");
const fs = require("fs");

test("reads config file", () => {
  fs.readFileSync.mockReturnValue("setting=value");

  const config = readConfig("config.txt");

  expect(config).toBe("setting=value");
});
```

### 2. Mocking Database

**Python**:

```python
def test_user_repository():
    mock_db = Mock()
    mock_db.query.return_value = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]

    repo = UserRepository(mock_db)
    users = repo.get_all_users()

    assert len(users) == 2
    mock_db.query.assert_called_once_with("SELECT * FROM users")
```

**JavaScript**:

```javascript
test("fetches all users from database", async () => {
  const mockDb = {
    query: jest.fn().mockResolvedValue([
      { id: 1, name: "Alice" },
      { id: 2, name: "Bob" },
    ]),
  };

  const repo = new UserRepository(mockDb);
  const users = await repo.getAllUsers();

  expect(users).toHaveLength(2);
  expect(mockDb.query).toHaveBeenCalledWith("SELECT * FROM users");
});
```

### 3. Mocking HTTP Requests

**Python**:

```python
@patch('requests.get')
def test_fetch_weather(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"temp": 72, "condition": "sunny"}
    mock_get.return_value = mock_response

    weather = fetch_weather("NYC")

    assert weather["temp"] == 72
    mock_get.assert_called_once_with(
        "https://api.weather.com/NYC"
    )
```

**JavaScript**:

```javascript
jest.mock("axios");
const axios = require("axios");

test("fetches weather data", async () => {
  axios.get.mockResolvedValue({
    status: 200,
    data: { temp: 72, condition: "sunny" },
  });

  const weather = await fetchWeather("NYC");

  expect(weather.temp).toBe(72);
  expect(axios.get).toHaveBeenCalledWith("https://api.weather.com/NYC");
});
```

### 4. Mocking Time

**Python**:

```python
from freezegun import freeze_time
from datetime import datetime

@freeze_time("2026-08-04 10:30:00")
def test_is_business_hours():
    # Time is frozen at 10:30 AM
    assert is_business_hours() == True

@freeze_time("2026-08-04 22:00:00")
def test_is_after_business_hours():
    # Time is frozen at 10:00 PM
    assert is_business_hours() == False
```

**JavaScript**:

```javascript
test("returns true during business hours", () => {
  // Mock Date
  const mockDate = new Date("2026-08-04T10:30:00");
  jest.spyOn(global, "Date").mockImplementation(() => mockDate);

  expect(isBusinessHours()).toBe(true);

  global.Date.mockRestore();
});

// Or use jest.useFakeTimers()
test("uses fake timers", () => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date("2026-08-04T10:30:00"));

  expect(isBusinessHours()).toBe(true);

  jest.useRealTimers();
});
```

### 5. Mocking Random Values

**Python**:

```python
from unittest.mock import patch

@patch('random.randint')
def test_dice_roll(mock_randint):
    mock_randint.return_value = 6

    result = roll_dice()

    assert result == 6
    mock_randint.assert_called_once_with(1, 6)
```

**JavaScript**:

```javascript
test("generates random number", () => {
  jest.spyOn(Math, "random").mockReturnValue(0.5);

  const result = generateRandomNumber(1, 10);

  expect(result).toBe(5);

  Math.random.mockRestore();
});
```

---

## Mocking Best Practices

### 1. Mock at the Right Level

✅ **Good**: Mock external dependencies

```python
@patch('requests.get')  # Mock external API
def test_fetch_data(mock_get):
    pass
```

❌ **Bad**: Mock internal functions

```python
@patch('my_module.calculate_total')  # Don't mock your own code!
def test_process_order(mock_calculate):
    pass
```

### 2. Don't Over-Mock

❌ **Bad**: Everything is mocked

```python
def test_complex_workflow():
    mock_a = Mock()
    mock_b = Mock()
    mock_c = Mock()
    mock_d = Mock()
    mock_e = Mock()
    # You're not testing anything real!
```

✅ **Good**: Only mock external dependencies

```python
def test_complex_workflow():
    mock_api = Mock()  # External API
    real_service = RealService()  # Your code
    real_calculator = RealCalculator()  # Your code
```

### 3. Use Real Objects When Possible

✅ **Good**: Use real value objects

```python
def test_calculate_order_total():
    items = [
        Item(name="Laptop", price=1000),  # Real objects
        Item(name="Mouse", price=20)
    ]

    total = calculate_total(items)
    assert total == 1020
```

❌ **Bad**: Mock everything

```python
def test_calculate_order_total():
    mock_item1 = Mock()
    mock_item1.price = 1000
    mock_item2 = Mock()
    mock_item2.price = 20
```

### 4. Verify Important Interactions

✅ **Good**: Verify critical calls

```python
def test_send_notification():
    mock_email = Mock()

    notify_user(user, mock_email)

    # Verify email was sent
    mock_email.send.assert_called_once_with(
        to=user.email,
        subject="Important Notification"
    )
```

### 5. Don't Test Mock Behavior

❌ **Bad**: Testing the mock

```python
def test_mock():
    mock_obj = Mock()
    mock_obj.method.return_value = 42

    result = mock_obj.method()
    assert result == 42  # You're just testing the mock!
```

✅ **Good**: Test your code with mocks

```python
def test_service_uses_repository():
    mock_repo = Mock()
    mock_repo.get_user.return_value = {"name": "Alice"}

    service = UserService(mock_repo)
    name = service.get_user_name(1)  # Testing YOUR code

    assert name == "Alice"
```

---

## When NOT to Mock

### 1. Value Objects

Don't mock simple data structures:

```python
# ❌ Bad
mock_user = Mock()
mock_user.name = "Alice"
mock_user.email = "alice@example.com"

# ✅ Good - use real object
user = User(name="Alice", email="alice@example.com")
```

### 2. Internal Functions

Don't mock your own code:

```python
# ❌ Bad
@patch('my_module.calculate_discount')
def test_process_order(mock_calculate):
    mock_calculate.return_value = 10
    # Not testing the real discount calculation!
```

### 3. Simple Utilities

Don't mock standard library or simple utilities:

```python
# ❌ Bad
@patch('json.dumps')
def test_serialize(mock_dumps):
    pass

# ✅ Good - use real json
def test_serialize():
    result = serialize(data)
    assert result == '{"key": "value"}'
```

---

## Common Mocking Mistakes

### 1. Mock Doesn't Match Real Interface

❌ **Bad**:

```python
mock_db = Mock()
mock_db.get_user.return_value = "Alice"  # Returns string

# Real database returns dict!
real_db.get_user(1)  # Returns {"id": 1, "name": "Alice"}
```

✅ **Good**: Match real interface

```python
mock_db = Mock()
mock_db.get_user.return_value = {"id": 1, "name": "Alice"}
```

### 2. Not Cleaning Up Mocks

❌ **Bad**:

```python
@patch('requests.get')
def test_one(mock_get):
    mock_get.return_value = ...

@patch('requests.get')
def test_two(mock_get):
    # Previous mock state might leak!
```

✅ **Good**: Reset in setUp/beforeEach

```python
class TestAPI:
    def setup_method(self):
        self.patcher = patch('requests.get')
        self.mock_get = self.patcher.start()

    def teardown_method(self):
        self.patcher.stop()
```

### 3. Mocking Too Broadly

❌ **Bad**:

```python
@patch('datetime.datetime')
def test_something(mock_datetime):
    # This breaks EVERYTHING using datetime in the test!
```

✅ **Good**: Mock specific usage

```python
@patch('my_module.datetime')
def test_something(mock_datetime):
    # Only mocks datetime in my_module
```

---

## Summary

**Why Mock**:

- Fast, isolated, reliable tests
- No external dependencies
- Deterministic results
- Safe (no side effects)

**Types of Test Doubles**:

- **Dummy**: Unused parameters
- **Stub**: Fixed return values
- **Fake**: Simplified working implementation
- **Mock**: Verify interactions
- **Spy**: Record calls to real object

**Python Mocking**:

- Use `unittest.mock`
- `Mock()` for objects
- `@patch` for replacing imports
- Verify with `assert_called_*` methods

**JavaScript Mocking**:

- Use Jest's built-in mocking
- `jest.fn()` for functions
- `jest.mock()` for modules
- Verify with `expect().toHaveBeenCalled*`

**Best Practices**:

- Mock external dependencies only
- Don't over-mock
- Use real objects when possible
- Verify important interactions
- Match real interfaces

**Don't Mock**:

- Value objects
- Your own internal code
- Simple utilities
- Standard library

---

## Practice Exercises

1. **Identify What to Mock**: For each scenario, decide what should be mocked and what should be real:

   - Calculating sales tax
   - Sending email confirmation
   - Validating password strength
   - Fetching user data from API
   - Generating random token

2. **Write Mocked Test**: Write a test for this function using mocks:

```python
def process_payment(user_id, amount, payment_gateway):
    user = database.get_user(user_id)
    if user.balance < amount:
        raise InsufficientFundsError()

    transaction_id = payment_gateway.charge(user.card, amount)
    database.deduct_balance(user_id, amount)
    email_service.send_receipt(user.email, transaction_id, amount)

    return transaction_id
```

3. **Fix Over-Mocking**: This test is over-mocked. Refactor it:

```python
def test_calculate_discount():
    mock_price = Mock()
    mock_price.value = 100
    mock_percentage = Mock()
    mock_percentage.value = 0.20
    mock_calculator = Mock()
    mock_calculator.multiply.return_value = 20
    # ... more mocks
```

---

## Next Steps

- Practice with [Exercise 6: Mocking](../exercises/06-mocking.md)
- Review your existing tests - are you mocking appropriately?
- Read about integration tests in [Module 6: TDD](../../06-tdd/theory/)
