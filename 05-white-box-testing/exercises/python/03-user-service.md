# Exercise 3: User Service with Integration Testing and Mocking

**Duration**: 75 minutes  
**Difficulty**: Advanced  
**Topics**: Integration testing, mocking, external dependencies, error handling

## Objectives

By completing this exercise, you will:

- Write integration tests for components with dependencies
- Mock external services (database, email, APIs)
- Test error handling and exception scenarios
- Use unittest.mock effectively
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

### `user_repository.py` (Database Layer)

```python
class UserRepository:
    """Simulates a database layer for user operations."""

    def __init__(self, db_connection):
        """
        Initialize repository with database connection.

        Args:
            db_connection: Database connection object
        """
        self.db = db_connection

    def find_by_email(self, email):
        """
        Find a user by email address.

        Args:
            email: User email address

        Returns:
            User dict if found, None otherwise

        Raises:
            ConnectionError: If database connection fails
        """
        # Simulate database query
        result = self.db.query(f"SELECT * FROM users WHERE email = '{email}'")
        return result

    def create_user(self, user_data):
        """
        Create a new user in the database.

        Args:
            user_data: Dictionary with user information

        Returns:
            Created user with ID

        Raises:
            ValueError: If user already exists
            ConnectionError: If database connection fails
        """
        # Check if user exists
        existing = self.find_by_email(user_data['email'])
        if existing:
            raise ValueError(f"User with email {user_data['email']} already exists")

        # Insert user
        user_id = self.db.insert("users", user_data)
        user_data['id'] = user_id
        return user_data

    def update_last_login(self, user_id):
        """
        Update the last login timestamp for a user.

        Args:
            user_id: User ID

        Raises:
            ConnectionError: If database connection fails
        """
        self.db.update("users", user_id, {"last_login": "NOW()"})
```

### `email_service.py` (External API Layer)

```python
class EmailService:
    """Simulates an external email service API."""

    def __init__(self, api_key):
        """
        Initialize email service with API key.

        Args:
            api_key: API authentication key
        """
        self.api_key = api_key
        self.sent_emails = []  # For testing purposes

    def send_email(self, to_address, subject, body):
        """
        Send an email via external API.

        Args:
            to_address: Recipient email address
            subject: Email subject
            body: Email body content

        Returns:
            True if email sent successfully

        Raises:
            ConnectionError: If API is unreachable
            ValueError: If email address is invalid
        """
        if not self._is_valid_email(to_address):
            raise ValueError(f"Invalid email address: {to_address}")

        # Simulate API call
        # In real implementation, this would make an HTTP request
        self.sent_emails.append({
            'to': to_address,
            'subject': subject,
            'body': body
        })
        return True

    def _is_valid_email(self, email):
        """Validate email format."""
        return '@' in email and '.' in email
```

### `user_service.py` (Business Logic Layer)

```python
import hashlib
from datetime import datetime

class UserService:
    """
    Business logic for user operations.
    Coordinates between repository and external services.
    """

    def __init__(self, user_repository, email_service):
        """
        Initialize service with dependencies.

        Args:
            user_repository: UserRepository instance
            email_service: EmailService instance
        """
        self.user_repo = user_repository
        self.email_service = email_service

    def register_user(self, email, password, name):
        """
        Register a new user and send welcome email.

        Args:
            email: User email address
            password: User password (will be hashed)
            name: User full name

        Returns:
            Created user object

        Raises:
            ValueError: If email already exists or invalid input
            ConnectionError: If database or email service fails
        """
        # Validate input
        if not email or not password or not name:
            raise ValueError("Email, password, and name are required")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

        # Hash password
        password_hash = self._hash_password(password)

        # Create user in database
        user_data = {
            'email': email,
            'password_hash': password_hash,
            'name': name,
            'created_at': datetime.now().isoformat()
        }

        user = self.user_repo.create_user(user_data)

        # Send welcome email (non-blocking)
        try:
            self.send_welcome_email(user)
        except Exception as e:
            # Log error but don't fail registration
            print(f"Warning: Could not send welcome email: {e}")

        return user

    def login(self, email, password):
        """
        Authenticate user and update last login.

        Args:
            email: User email
            password: User password

        Returns:
            User object if authentication successful

        Raises:
            ValueError: If credentials are invalid
            ConnectionError: If database fails
        """
        # Find user
        user = self.user_repo.find_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        # Verify password
        password_hash = self._hash_password(password)
        if user.get('password_hash') != password_hash:
            raise ValueError("Invalid email or password")

        # Update last login
        self.user_repo.update_last_login(user['id'])

        return user

    def send_welcome_email(self, user):
        """
        Send welcome email to newly registered user.

        Args:
            user: User object with email and name

        Returns:
            True if email sent successfully

        Raises:
            ConnectionError: If email service fails
            ValueError: If email is invalid
        """
        subject = "Welcome to Our Service!"
        body = f"Hello {user['name']},\n\nThank you for registering!"

        return self.email_service.send_email(
            user['email'],
            subject,
            body
        )

    def get_user_by_id(self, user_id):
        """
        Retrieve user by ID.

        Args:
            user_id: User ID

        Returns:
            User object if found

        Raises:
            ValueError: If user not found
            ConnectionError: If database fails
        """
        # This would typically call user_repo.find_by_id()
        # Simplified for this exercise
        raise NotImplementedError("To be implemented")

    def _hash_password(self, password):
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
```

## Part 2: Write Tests with Mocking (35 minutes)

Create `test_user_service.py`:

```python
import pytest
from unittest.mock import Mock, MagicMock, patch, call
from user_service import UserService
from user_repository import UserRepository
from email_service import EmailService

class TestUserService:
    """Test suite for UserService with mocked dependencies."""

    def setup_method(self):
        """Create mocked dependencies and service instance."""
        # Create mock objects
        self.mock_repo = Mock(spec=UserRepository)
        self.mock_email = Mock(spec=EmailService)

        # Create service with mocked dependencies
        self.service = UserService(self.mock_repo, self.mock_email)

    # Test register_user - Happy Path
    def test_register_user_success(self):
        """Test successful user registration."""
        # Arrange: Set up mock behavior
        self.mock_repo.create_user.return_value = {
            'id': 1,
            'email': 'test@example.com',
            'name': 'Test User',
            'password_hash': 'hashed_password'
        }
        self.mock_email.send_email.return_value = True

        # Act: Call the method
        user = self.service.register_user(
            'test@example.com',
            'password123',
            'Test User'
        )

        # Assert: Verify results and interactions
        assert user['email'] == 'test@example.com'
        assert user['name'] == 'Test User'

        # Verify repository was called correctly
        self.mock_repo.create_user.assert_called_once()

        # Verify email was sent
        self.mock_email.send_email.assert_called_once()
        call_args = self.mock_email.send_email.call_args
        assert call_args[0][0] == 'test@example.com'
        assert 'Welcome' in call_args[0][1]

    def test_register_user_with_short_password(self):
        """Test that short password raises ValueError."""
        # TODO: Implement this test
        # Verify that passwords less than 8 characters raise ValueError
        pass

    def test_register_user_with_missing_email(self):
        """Test that missing email raises ValueError."""
        # TODO: Implement this test
        pass

    def test_register_user_duplicate_email(self):
        """Test that duplicate email raises ValueError."""
        # TODO: Implement this test
        # Set mock_repo.create_user to raise ValueError
        # Verify the exception propagates
        pass

    def test_register_user_email_failure_does_not_block(self):
        """Test that email failure doesn't prevent registration."""
        # TODO: Implement this test
        # Make send_email raise an exception
        # Verify that register_user still succeeds
        pass

    def test_register_user_database_failure(self):
        """Test that database failure raises exception."""
        # TODO: Implement this test
        # Make create_user raise ConnectionError
        # Verify the exception propagates
        pass

    # Test login - Happy Path
    def test_login_success(self):
        """Test successful login."""
        # Arrange
        mock_user = {
            'id': 1,
            'email': 'test@example.com',
            'password_hash': self.service._hash_password('password123'),
            'name': 'Test User'
        }
        self.mock_repo.find_by_email.return_value = mock_user

        # Act
        user = self.service.login('test@example.com', 'password123')

        # Assert
        assert user['email'] == 'test@example.com'
        self.mock_repo.find_by_email.assert_called_once_with('test@example.com')
        self.mock_repo.update_last_login.assert_called_once_with(1)

    def test_login_user_not_found(self):
        """Test login with non-existent email."""
        # TODO: Implement this test
        # Make find_by_email return None
        # Verify ValueError is raised
        pass

    def test_login_wrong_password(self):
        """Test login with incorrect password."""
        # TODO: Implement this test
        # Return user with different password hash
        # Verify ValueError is raised
        pass

    def test_login_database_failure(self):
        """Test login when database fails."""
        # TODO: Implement this test
        # Make find_by_email raise ConnectionError
        # Verify exception propagates
        pass

    # Test send_welcome_email
    def test_send_welcome_email_success(self):
        """Test sending welcome email."""
        # TODO: Implement this test
        pass

    def test_send_welcome_email_invalid_address(self):
        """Test welcome email with invalid address."""
        # TODO: Implement this test
        # Make send_email raise ValueError
        pass

    def test_send_welcome_email_api_failure(self):
        """Test welcome email when API fails."""
        # TODO: Implement this test
        # Make send_email raise ConnectionError
        pass
```

## Part 3: Integration Tests (15 minutes)

Add integration tests that test multiple components together:

```python
class TestUserServiceIntegration:
    """Integration tests with real (or less mocked) components."""

    def test_full_registration_flow(self):
        """Test complete registration flow with minimal mocking."""
        # Only mock the actual external services (DB and Email API)
        mock_db = Mock()
        mock_db.query.return_value = None  # User doesn't exist
        mock_db.insert.return_value = 1  # New user ID

        repo = UserRepository(mock_db)
        email_service = Mock(spec=EmailService)
        email_service.send_email.return_value = True

        service = UserService(repo, email_service)

        # Register user
        user = service.register_user('new@example.com', 'password123', 'New User')

        # Verify complete flow
        assert user['id'] == 1
        assert user['email'] == 'new@example.com'
        mock_db.query.assert_called()
        mock_db.insert.assert_called()
        email_service.send_email.assert_called()

    def test_full_login_flow(self):
        """Test complete login flow."""
        # TODO: Implement this test
        # Test registration followed by login
        pass
```

## Part 4: Measure Coverage (5 minutes)

```bash
# Run tests with coverage
pytest --cov=. --cov-report=term-missing --cov-branch test_user_service.py

# Generate HTML report
pytest --cov=. --cov-report=html --cov-branch test_user_service.py
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
3. **Not verifying mock calls** - Use assert_called_once(), assert_called_with()
4. **Testing implementation details** - Test behavior, not internals
5. **Not testing error paths** - Test what happens when dependencies fail
6. **Not cleaning up mocks** - Use setup_method to create fresh mocks

## Tips for Success

- Mock at the boundary (database, API) not internal logic
- Use `spec=` parameter to catch attribute errors
- Verify not just that methods were called, but with correct arguments
- Test exception handling thoroughly
- Use `side_effect` to simulate errors
- Keep mocks simple and focused

## Advanced Mocking Techniques

### Using side_effect for Multiple Calls

```python
def test_retry_logic(self):
    """Test that service retries on failure."""
    # First call fails, second succeeds
    self.mock_repo.find_by_email.side_effect = [
        ConnectionError("Database timeout"),
        {'id': 1, 'email': 'test@example.com'}
    ]

    # Your retry logic here
```

### Using patch for Global Dependencies

```python
@patch('user_service.datetime')
def test_user_creation_timestamp(self, mock_datetime):
    """Test that timestamp is set correctly."""
    mock_datetime.now.return_value.isoformat.return_value = '2026-01-01T00:00:00'

    # Your test here
```

### Verifying Call Order

```python
def test_login_updates_last_login_after_verification(self):
    """Test that last_login is only updated after successful auth."""
    manager = Mock()
    manager.attach_mock(self.mock_repo.find_by_email, 'find')
    manager.attach_mock(self.mock_repo.update_last_login, 'update')

    # ... perform login ...

    # Verify find was called before update
    assert manager.mock_calls[0][0] == 'find'
    assert manager.mock_calls[1][0] == 'update'
```

## Submission

Submit the following files:

- `user_repository.py`
- `email_service.py`
- `user_service.py`
- `test_user_service.py` - Complete test suite
- Screenshot showing >90% coverage

## Next Steps

After completing this exercise:

- Move on to [Exercise 4: Coverage Challenge](./04-coverage-challenge.md)
- Review [Module Theory: Mock-up Testing](../theory/06-mocking.md)
- Learn about different types of test doubles (mocks, stubs, fakes, spies)
