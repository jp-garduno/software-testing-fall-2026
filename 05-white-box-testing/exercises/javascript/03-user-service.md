# Exercise 3: User Service with Integration Testing and Mocking

**Duration**: 75 minutes  
**Difficulty**: Advanced  
**Topics**: Integration testing, mocking, external dependencies, error handling

## Objectives

By completing this exercise, you will:

- Write integration tests for components with dependencies
- Mock external services (database, email, APIs)
- Test error handling and exception scenarios
- Use Jest mocking effectively
- Understand when to use mocks vs real implementations
- Achieve high coverage with proper mocking

## Background

Real applications depend on external services like databases, APIs, and third-party libraries. Testing these components requires mocking external dependencies to:

- Avoid hitting real databases or APIs during tests
- Simulate error conditions
- Make tests fast and reliable
- Test edge cases that are hard to reproduce

## Part 1: Implementation (20 minutes)

Create the following files:

### `userRepository.js` (Database Layer)

```javascript
class UserRepository {
  /**
   * Simulates a database layer for user operations.
   * @param {Object} dbConnection - Database connection object
   */
  constructor(dbConnection) {
    this.db = dbConnection;
  }

  /**
   * Find a user by email address.
   * @param {string} email - User email address
   * @returns {Object|null} User object if found, null otherwise
   * @throws {Error} If database connection fails
   */
  findByEmail(email) {
    // Simulate database query
    const result = this.db.query(
      `SELECT * FROM users WHERE email = '${email}'`,
    );
    return result;
  }

  /**
   * Create a new user in the database.
   * @param {Object} userData - User information
   * @returns {Object} Created user with ID
   * @throws {Error} If user already exists or database fails
   */
  createUser(userData) {
    // Check if user exists
    const existing = this.findByEmail(userData.email);
    if (existing) {
      throw new Error(`User with email ${userData.email} already exists`);
    }

    // Insert user
    const userId = this.db.insert("users", userData);
    return { ...userData, id: userId };
  }

  /**
   * Update the last login timestamp for a user.
   * @param {number} userId - User ID
   * @throws {Error} If database connection fails
   */
  updateLastLogin(userId) {
    this.db.update("users", userId, { last_login: "NOW()" });
  }
}

module.exports = UserRepository;
```

### `emailService.js` (External API Layer)

```javascript
class EmailService {
  /**
   * Simulates an external email service API.
   * @param {string} apiKey - API authentication key
   */
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.sentEmails = []; // For testing purposes
  }

  /**
   * Send an email via external API.
   * @param {string} toAddress - Recipient email address
   * @param {string} subject - Email subject
   * @param {string} body - Email body content
   * @returns {boolean} True if email sent successfully
   * @throws {Error} If API is unreachable or email is invalid
   */
  sendEmail(toAddress, subject, body) {
    if (!this._isValidEmail(toAddress)) {
      throw new Error(`Invalid email address: ${toAddress}`);
    }

    // Simulate API call
    this.sentEmails.push({
      to: toAddress,
      subject: subject,
      body: body,
    });
    return true;
  }

  /**
   * Validate email format.
   * @private
   */
  _isValidEmail(email) {
    return email.includes("@") && email.includes(".");
  }
}

module.exports = EmailService;
```

### `userService.js` (Business Logic Layer)

```javascript
const crypto = require("crypto");

class UserService {
  /**
   * Business logic for user operations.
   * Coordinates between repository and external services.
   * @param {UserRepository} userRepository - Repository instance
   * @param {EmailService} emailService - Email service instance
   */
  constructor(userRepository, emailService) {
    this.userRepo = userRepository;
    this.emailService = emailService;
  }

  /**
   * Register a new user and send welcome email.
   * @param {string} email - User email address
   * @param {string} password - User password (will be hashed)
   * @param {string} name - User full name
   * @returns {Object} Created user object
   * @throws {Error} If email already exists or invalid input
   */
  registerUser(email, password, name) {
    // Validate input
    if (!email || !password || !name) {
      throw new Error("Email, password, and name are required");
    }

    if (password.length < 8) {
      throw new Error("Password must be at least 8 characters");
    }

    // Hash password
    const passwordHash = this._hashPassword(password);

    // Create user in database
    const userData = {
      email: email,
      password_hash: passwordHash,
      name: name,
      created_at: new Date().toISOString(),
    };

    const user = this.userRepo.createUser(userData);

    // Send welcome email (non-blocking)
    try {
      this.sendWelcomeEmail(user);
    } catch (error) {
      // Log error but don't fail registration
      console.log(`Warning: Could not send welcome email: ${error}`);
    }

    return user;
  }

  /**
   * Authenticate user and update last login.
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Object} User object if authentication successful
   * @throws {Error} If credentials are invalid or database fails
   */
  login(email, password) {
    // Find user
    const user = this.userRepo.findByEmail(email);
    if (!user) {
      throw new Error("Invalid email or password");
    }

    // Verify password
    const passwordHash = this._hashPassword(password);
    if (user.password_hash !== passwordHash) {
      throw new Error("Invalid email or password");
    }

    // Update last login
    this.userRepo.updateLastLogin(user.id);

    return user;
  }

  /**
   * Send welcome email to newly registered user.
   * @param {Object} user - User object with email and name
   * @returns {boolean} True if email sent successfully
   * @throws {Error} If email service fails or email is invalid
   */
  sendWelcomeEmail(user) {
    const subject = "Welcome to Our Service!";
    const body = `Hello ${user.name},\n\nThank you for registering!`;

    return this.emailService.sendEmail(user.email, subject, body);
  }

  /**
   * Retrieve user by ID.
   * @param {number} userId - User ID
   * @returns {Object} User object if found
   * @throws {Error} If user not found or database fails
   */
  getUserById(userId) {
    // This would typically call userRepo.findById()
    // Simplified for this exercise
    throw new Error("Not implemented");
  }

  /**
   * Hash password using SHA-256.
   * @private
   */
  _hashPassword(password) {
    return crypto.createHash("sha256").update(password).digest("hex");
  }
}

module.exports = UserService;
```

## Part 2: Write Tests with Mocking (35 minutes)

Create `userService.test.js`:

```javascript
const UserService = require("./userService");
const UserRepository = require("./userRepository");
const EmailService = require("./emailService");

describe("UserService", () => {
  let mockRepo;
  let mockEmail;
  let service;

  beforeEach(() => {
    // Create mock objects
    mockRepo = {
      findByEmail: jest.fn(),
      createUser: jest.fn(),
      updateLastLogin: jest.fn(),
    };

    mockEmail = {
      sendEmail: jest.fn(),
    };

    // Create service with mocked dependencies
    service = new UserService(mockRepo, mockEmail);
  });

  // Test registerUser - Happy Path
  describe("registerUser", () => {
    test("should register user successfully", () => {
      // Arrange: Set up mock behavior
      mockRepo.createUser.mockReturnValue({
        id: 1,
        email: "test@example.com",
        name: "Test User",
        password_hash: "hashed_password",
      });
      mockEmail.sendEmail.mockReturnValue(true);

      // Act: Call the method
      const user = service.registerUser(
        "test@example.com",
        "password123",
        "Test User",
      );

      // Assert: Verify results and interactions
      expect(user.email).toBe("test@example.com");
      expect(user.name).toBe("Test User");

      // Verify repository was called correctly
      expect(mockRepo.createUser).toHaveBeenCalledTimes(1);

      // Verify email was sent
      expect(mockEmail.sendEmail).toHaveBeenCalledTimes(1);
      const emailCall = mockEmail.sendEmail.mock.calls[0];
      expect(emailCall[0]).toBe("test@example.com");
      expect(emailCall[1]).toContain("Welcome");
    });

    test("should throw error for short password", () => {
      // TODO: Implement this test
      // Verify that passwords less than 8 characters throw Error
    });

    test("should throw error for missing email", () => {
      // TODO: Implement this test
    });

    test("should throw error for missing password", () => {
      // TODO: Implement this test
    });

    test("should throw error for missing name", () => {
      // TODO: Implement this test
    });

    test("should throw error for duplicate email", () => {
      // TODO: Implement this test
      // Set mockRepo.createUser to throw Error
      // Verify the exception propagates
    });

    test("should not fail registration if email fails", () => {
      // TODO: Implement this test
      // Make sendEmail throw an exception
      // Verify that registerUser still succeeds
    });

    test("should throw error if database fails", () => {
      // TODO: Implement this test
      // Make createUser throw Error
      // Verify the exception propagates
    });
  });

  // Test login - Happy Path
  describe("login", () => {
    test("should login successfully", () => {
      // Arrange
      const mockUser = {
        id: 1,
        email: "test@example.com",
        password_hash: service._hashPassword("password123"),
        name: "Test User",
      };
      mockRepo.findByEmail.mockReturnValue(mockUser);

      // Act
      const user = service.login("test@example.com", "password123");

      // Assert
      expect(user.email).toBe("test@example.com");
      expect(mockRepo.findByEmail).toHaveBeenCalledWith("test@example.com");
      expect(mockRepo.updateLastLogin).toHaveBeenCalledWith(1);
    });

    test("should throw error for non-existent email", () => {
      // TODO: Implement this test
      // Make findByEmail return null
      // Verify Error is thrown
    });

    test("should throw error for incorrect password", () => {
      // TODO: Implement this test
      // Return user with different password hash
      // Verify Error is thrown
    });

    test("should throw error if database fails", () => {
      // TODO: Implement this test
      // Make findByEmail throw Error
      // Verify exception propagates
    });
  });

  // Test sendWelcomeEmail
  describe("sendWelcomeEmail", () => {
    test("should send welcome email successfully", () => {
      // TODO: Implement this test
    });

    test("should throw error for invalid email address", () => {
      // TODO: Implement this test
      // Make sendEmail throw Error
    });

    test("should throw error if email API fails", () => {
      // TODO: Implement this test
      // Make sendEmail throw Error
    });
  });
});
```

## Part 3: Integration Tests (15 minutes)

Add integration tests that test multiple components together:

```javascript
describe("UserService Integration Tests", () => {
  test("should complete full registration flow", () => {
    // Only mock the actual external services (DB and Email API)
    const mockDb = {
      query: jest.fn().mockReturnValue(null), // User doesn't exist
      insert: jest.fn().mockReturnValue(1), // New user ID
      update: jest.fn(),
    };

    const mockEmailApi = {
      sendEmail: jest.fn().mockReturnValue(true),
    };

    const repo = new UserRepository(mockDb);
    const emailService = { sendEmail: mockEmailApi.sendEmail };
    const service = new UserService(repo, emailService);

    // Register user
    const user = service.registerUser(
      "new@example.com",
      "password123",
      "New User",
    );

    // Verify complete flow
    expect(user.id).toBe(1);
    expect(user.email).toBe("new@example.com");
    expect(mockDb.query).toHaveBeenCalled();
    expect(mockDb.insert).toHaveBeenCalled();
    expect(mockEmailApi.sendEmail).toHaveBeenCalled();
  });

  test("should complete full login flow", () => {
    // TODO: Implement this test
    // Test registration followed by login
  });

  test("should handle database error during registration", () => {
    // TODO: Implement this test
    // Simulate database error
  });
});
```

## Part 4: Measure Coverage (5 minutes)

```bash
# Run tests with coverage
npm run test:coverage

# Or with Jest directly
jest --coverage
```

## Evaluation Criteria

Your solution will be evaluated on:

- **Test Coverage**: >90% statement and branch coverage
- **Proper Mocking**: External dependencies correctly mocked
- **Error Handling**: All error conditions tested
- **Integration Tests**: Multiple components tested together
- **Test Quality**: Clear, maintainable, well-documented tests
- **Mock Verification**: Verify mocks were called correctly

## Common Mistakes to Avoid

1. **Over-mocking** - Don't mock the class under test
2. **Under-mocking** - Don't hit real databases or APIs
3. **Not verifying mock calls** - Use `toHaveBeenCalled()`, `toHaveBeenCalledWith()`
4. **Testing implementation details** - Test behavior, not internals
5. **Not testing error paths** - Test what happens when dependencies fail
6. **Not cleaning up mocks** - Use `beforeEach` to create fresh mocks

## Tips for Success

- Mock at the boundary (database, API) not internal logic
- Verify not just that methods were called, but with correct arguments
- Test exception handling thoroughly
- Use `mockImplementation()` or `mockReturnValue()` for simple cases
- Use `mockRejectedValue()` for async errors
- Keep mocks simple and focused

## Advanced Mocking Techniques

### Using mockImplementation for Custom Logic

```javascript
test("should retry on failure", () => {
  // First call fails, second succeeds
  mockRepo.findByEmail
    .mockImplementationOnce(() => {
      throw new Error("Database timeout");
    })
    .mockImplementationOnce(() => ({
      id: 1,
      email: "test@example.com",
    }));

  // Your retry logic here
});
```

### Spying on Console

```javascript
test("should log warning when email fails", () => {
  const consoleSpy = jest.spyOn(console, "log").mockImplementation();
  mockEmail.sendEmail.mockImplementation(() => {
    throw new Error("Email API down");
  });

  // Register user (should succeed despite email failure)
  service.registerUser("test@example.com", "password123", "Test");

  // Verify warning was logged
  expect(consoleSpy).toHaveBeenCalledWith(
    expect.stringContaining("Could not send welcome email"),
  );

  consoleSpy.mockRestore();
});
```

### Verifying Call Order

```javascript
test("should update last login after verification", () => {
  const mockUser = {
    id: 1,
    email: "test@example.com",
    password_hash: service._hashPassword("password123"),
  };
  mockRepo.findByEmail.mockReturnValue(mockUser);

  service.login("test@example.com", "password123");

  // Verify find was called before update
  const findCall = mockRepo.findByEmail.mock.invocationCallOrder[0];
  const updateCall = mockRepo.updateLastLogin.mock.invocationCallOrder[0];
  expect(findCall).toBeLessThan(updateCall);
});
```

## Submission

Submit the following files:

- `userRepository.js`
- `emailService.js`
- `userService.js`
- `userService.test.js` - Complete test suite
- Screenshot showing >90% coverage

## Next Steps

After completing this exercise:

- Move on to [Exercise 4: Coverage Challenge](./04-coverage-challenge.md)
- Review [Module Theory: Mock-up Testing](../theory/06-mocking.md)
- Learn about different types of test doubles (mocks, stubs, fakes, spies)
