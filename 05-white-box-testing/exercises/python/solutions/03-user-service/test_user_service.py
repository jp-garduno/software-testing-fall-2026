"""Reference test suite for Exercise 3: User Service (Module 05 - White Box Testing)."""

# pylint: disable=attribute-defined-outside-init,too-many-public-methods,protected-access
import hashlib
from unittest.mock import Mock, patch

import pytest
from email_service import EmailService
from user_repository import UserRepository
from user_service import UserService

VALID_EMAIL = "test@example.com"
VALID_PASSWORD = "password123"
VALID_NAME = "Test User"


def sha256(text):
    """Independent SHA-256 helper, so tests don't rely on the code under test to compute expected hashes."""
    return hashlib.sha256(text.encode()).hexdigest()


class TestUserService:
    """Test suite for UserService with mocked dependencies."""

    def setup_method(self):
        """Create mocked dependencies and service instance."""
        # Create mock objects
        self.mock_repo = Mock(spec=UserRepository)
        self.mock_email = Mock(spec=EmailService)

        # Create service with mocked dependencies
        self.service = UserService(self.mock_repo, self.mock_email)

    def _stored_user(self, password=VALID_PASSWORD):
        """Build the user dict the repository would return."""
        return {
            "id": 1,
            "email": VALID_EMAIL,
            "name": VALID_NAME,
            "password_hash": sha256(password),
        }

    # Test register_user - Happy Path
    def test_register_user_success(self):
        """Test successful user registration."""
        # Arrange: Set up mock behavior
        self.mock_repo.create_user.return_value = self._stored_user()
        self.mock_email.send_email.return_value = True

        # Act: Call the method
        user = self.service.register_user(VALID_EMAIL, VALID_PASSWORD, VALID_NAME)

        # Assert: Verify results and interactions
        assert user["email"] == VALID_EMAIL
        assert user["name"] == VALID_NAME

        # Verify repository was called correctly
        self.mock_repo.create_user.assert_called_once()

        # Verify email was sent
        self.mock_email.send_email.assert_called_once()
        call_args = self.mock_email.send_email.call_args
        assert call_args[0][0] == VALID_EMAIL
        assert "Welcome" in call_args[0][1]

    def test_register_user_passes_hashed_password_to_repository(self):
        """Test that the repository receives a SHA-256 hash, never the plain password."""
        self.mock_repo.create_user.return_value = self._stored_user()

        self.service.register_user(VALID_EMAIL, VALID_PASSWORD, VALID_NAME)

        user_data = self.mock_repo.create_user.call_args[0][0]
        assert user_data["email"] == VALID_EMAIL
        assert user_data["name"] == VALID_NAME
        assert user_data["password_hash"] == sha256(VALID_PASSWORD)
        assert VALID_PASSWORD not in user_data.values()

    @patch("user_service.datetime")
    def test_register_user_sets_created_at_timestamp(self, mock_datetime):
        """Test that created_at comes from datetime.now() (patched global dependency)."""
        mock_datetime.now.return_value.isoformat.return_value = "2026-01-01T00:00:00"
        self.mock_repo.create_user.return_value = self._stored_user()

        self.service.register_user(VALID_EMAIL, VALID_PASSWORD, VALID_NAME)

        user_data = self.mock_repo.create_user.call_args[0][0]
        assert user_data["created_at"] == "2026-01-01T00:00:00"

    def test_register_user_with_short_password(self):
        """Test that short password raises ValueError."""
        with pytest.raises(ValueError, match="Password must be at least 8 characters"):
            self.service.register_user(VALID_EMAIL, "1234567", VALID_NAME)

        self.mock_repo.create_user.assert_not_called()

    def test_register_user_password_exactly_8_characters(self):
        """Test the password length boundary: 8 characters is accepted."""
        self.mock_repo.create_user.return_value = self._stored_user("12345678")

        user = self.service.register_user(VALID_EMAIL, "12345678", VALID_NAME)

        assert user["id"] == 1
        self.mock_repo.create_user.assert_called_once()

    def test_register_user_with_missing_email(self):
        """Test that missing email raises ValueError."""
        with pytest.raises(ValueError, match="Email, password, and name are required"):
            self.service.register_user("", VALID_PASSWORD, VALID_NAME)

        self.mock_repo.create_user.assert_not_called()

    def test_register_user_with_missing_password(self):
        """Test that missing password raises ValueError (second condition of the OR)."""
        with pytest.raises(ValueError, match="Email, password, and name are required"):
            self.service.register_user(VALID_EMAIL, "", VALID_NAME)

    def test_register_user_with_missing_name(self):
        """Test that missing name raises ValueError (third condition of the OR)."""
        with pytest.raises(ValueError, match="Email, password, and name are required"):
            self.service.register_user(VALID_EMAIL, VALID_PASSWORD, None)

    def test_register_user_duplicate_email(self):
        """Test that duplicate email raises ValueError."""
        self.mock_repo.create_user.side_effect = ValueError(
            f"User with email {VALID_EMAIL} already exists"
        )

        with pytest.raises(ValueError, match="already exists"):
            self.service.register_user(VALID_EMAIL, VALID_PASSWORD, VALID_NAME)

        self.mock_email.send_email.assert_not_called()

    def test_register_user_email_failure_does_not_block(self, capsys):
        """Test that email failure doesn't prevent registration."""
        self.mock_repo.create_user.return_value = self._stored_user()
        self.mock_email.send_email.side_effect = ConnectionError(
            "Email API unreachable"
        )

        user = self.service.register_user(VALID_EMAIL, VALID_PASSWORD, VALID_NAME)

        assert user["id"] == 1
        self.mock_email.send_email.assert_called_once()
        assert (
            "Warning: Could not send welcome email: Email API unreachable"
            in capsys.readouterr().out
        )

    def test_register_user_database_failure(self):
        """Test that database failure raises exception."""
        self.mock_repo.create_user.side_effect = ConnectionError("Database unavailable")

        with pytest.raises(ConnectionError, match="Database unavailable"):
            self.service.register_user(VALID_EMAIL, VALID_PASSWORD, VALID_NAME)

        self.mock_email.send_email.assert_not_called()

    # Test login - Happy Path
    def test_login_success(self):
        """Test successful login."""
        # Arrange
        self.mock_repo.find_by_email.return_value = self._stored_user()

        # Act
        user = self.service.login(VALID_EMAIL, VALID_PASSWORD)

        # Assert
        assert user["email"] == VALID_EMAIL
        self.mock_repo.find_by_email.assert_called_once_with(VALID_EMAIL)
        self.mock_repo.update_last_login.assert_called_once_with(1)

    def test_login_user_not_found(self):
        """Test login with non-existent email."""
        self.mock_repo.find_by_email.return_value = None

        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login("ghost@example.com", VALID_PASSWORD)

        self.mock_repo.update_last_login.assert_not_called()

    def test_login_wrong_password(self):
        """Test login with incorrect password."""
        self.mock_repo.find_by_email.return_value = self._stored_user(
            "another-password"
        )

        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login(VALID_EMAIL, VALID_PASSWORD)

        self.mock_repo.update_last_login.assert_not_called()

    def test_login_user_without_password_hash(self):
        """Test that a stored user without password_hash cannot log in."""
        self.mock_repo.find_by_email.return_value = {"id": 1, "email": VALID_EMAIL}

        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login(VALID_EMAIL, VALID_PASSWORD)

    def test_login_database_failure(self):
        """Test login when database fails."""
        self.mock_repo.find_by_email.side_effect = ConnectionError("Database timeout")

        with pytest.raises(ConnectionError, match="Database timeout"):
            self.service.login(VALID_EMAIL, VALID_PASSWORD)

        self.mock_repo.update_last_login.assert_not_called()

    def test_login_update_last_login_failure_propagates(self):
        """Test that a failure while updating last login is not swallowed."""
        self.mock_repo.find_by_email.return_value = self._stored_user()
        self.mock_repo.update_last_login.side_effect = ConnectionError(
            "Database timeout"
        )

        with pytest.raises(ConnectionError):
            self.service.login(VALID_EMAIL, VALID_PASSWORD)

    def test_login_updates_last_login_after_verification(self):
        """Test that last_login is only updated after the user is found (call order)."""
        manager = Mock()
        manager.attach_mock(self.mock_repo.find_by_email, "find")
        manager.attach_mock(self.mock_repo.update_last_login, "update")
        self.mock_repo.find_by_email.return_value = self._stored_user()

        self.service.login(VALID_EMAIL, VALID_PASSWORD)

        assert [name for name, _, _ in manager.mock_calls] == ["find", "update"]

    # Test send_welcome_email
    def test_send_welcome_email_success(self):
        """Test sending welcome email."""
        self.mock_email.send_email.return_value = True

        result = self.service.send_welcome_email(
            {"email": VALID_EMAIL, "name": VALID_NAME}
        )

        assert result is True
        self.mock_email.send_email.assert_called_once_with(
            VALID_EMAIL,
            "Welcome to Our Service!",
            f"Hello {VALID_NAME},\n\nThank you for registering!",
        )

    def test_send_welcome_email_invalid_address(self):
        """Test welcome email with invalid address."""
        self.mock_email.send_email.side_effect = ValueError(
            "Invalid email address: not-an-email"
        )

        with pytest.raises(ValueError, match="Invalid email address"):
            self.service.send_welcome_email(
                {"email": "not-an-email", "name": VALID_NAME}
            )

    def test_send_welcome_email_api_failure(self):
        """Test welcome email when API fails."""
        self.mock_email.send_email.side_effect = ConnectionError(
            "Email API unreachable"
        )

        with pytest.raises(ConnectionError, match="Email API unreachable"):
            self.service.send_welcome_email({"email": VALID_EMAIL, "name": VALID_NAME})

    # Test get_user_by_id and _hash_password
    def test_get_user_by_id_not_implemented(self):
        """Test that get_user_by_id is still a stub."""
        with pytest.raises(NotImplementedError):
            self.service.get_user_by_id(1)

    def test_hash_password_is_sha256(self):
        """Test that the password hash is the SHA-256 hex digest."""
        assert self.service._hash_password(VALID_PASSWORD) == sha256(VALID_PASSWORD)

    def test_hash_password_is_deterministic_and_unique(self):
        """Test that equal passwords hash equally and different passwords do not."""
        assert self.service._hash_password("abc12345") == self.service._hash_password(
            "abc12345"
        )
        assert self.service._hash_password("abc12345") != self.service._hash_password(
            "abc12346"
        )


class TestUserRepository:
    """Unit tests for UserRepository with a mocked database connection."""

    def setup_method(self):
        """Create a mocked database connection and repository."""
        self.mock_db = Mock()
        self.repo = UserRepository(self.mock_db)

    def test_find_by_email_returns_query_result(self):
        """Test that find_by_email queries by email and returns the result."""
        self.mock_db.query.return_value = {"id": 1, "email": VALID_EMAIL}

        result = self.repo.find_by_email(VALID_EMAIL)

        assert result == {"id": 1, "email": VALID_EMAIL}
        self.mock_db.query.assert_called_once_with(
            f"SELECT * FROM users WHERE email = '{VALID_EMAIL}'"
        )

    def test_find_by_email_not_found_returns_none(self):
        """Test that a missing user returns None."""
        self.mock_db.query.return_value = None
        assert self.repo.find_by_email(VALID_EMAIL) is None

    def test_find_by_email_database_failure(self):
        """Test that a connection error propagates."""
        self.mock_db.query.side_effect = ConnectionError("Database unavailable")

        with pytest.raises(ConnectionError):
            self.repo.find_by_email(VALID_EMAIL)

    def test_create_user_new_user_gets_id(self):
        """Test that a new user is inserted and receives the generated ID."""
        self.mock_db.query.return_value = None
        self.mock_db.insert.return_value = 42

        user = self.repo.create_user({"email": VALID_EMAIL, "name": VALID_NAME})

        assert user == {"email": VALID_EMAIL, "name": VALID_NAME, "id": 42}
        self.mock_db.insert.assert_called_once()
        assert self.mock_db.insert.call_args[0][0] == "users"

    def test_create_user_existing_user_raises_error(self):
        """Test that an existing email raises ValueError and nothing is inserted."""
        self.mock_db.query.return_value = {"id": 1, "email": VALID_EMAIL}

        with pytest.raises(
            ValueError, match=f"User with email {VALID_EMAIL} already exists"
        ):
            self.repo.create_user({"email": VALID_EMAIL, "name": VALID_NAME})

        self.mock_db.insert.assert_not_called()

    def test_create_user_insert_failure(self):
        """Test that a failure during insert propagates."""
        self.mock_db.query.return_value = None
        self.mock_db.insert.side_effect = ConnectionError("Database unavailable")

        with pytest.raises(ConnectionError):
            self.repo.create_user({"email": VALID_EMAIL})

    def test_update_last_login(self):
        """Test that update_last_login updates the right user."""
        self.repo.update_last_login(7)
        self.mock_db.update.assert_called_once_with("users", 7, {"last_login": "NOW()"})


class TestEmailService:
    """Unit tests for EmailService (it only simulates the external API, so no mocking is needed)."""

    def setup_method(self):
        """Create a fresh email service."""
        self.email_service = EmailService("test-api-key")

    def test_init_stores_api_key_and_starts_empty(self):
        """Test the initial state of the service."""
        assert self.email_service.api_key == "test-api-key"
        assert not self.email_service.sent_emails

    def test_send_email_valid_address(self):
        """Test that a valid email is recorded and returns True."""
        result = self.email_service.send_email(VALID_EMAIL, "Hi", "Body")

        assert result is True
        assert self.email_service.sent_emails == [
            {"to": VALID_EMAIL, "subject": "Hi", "body": "Body"}
        ]

    def test_send_email_missing_at_raises_error(self):
        """Test that an address without '@' is rejected (first condition of the AND)."""
        with pytest.raises(ValueError, match="Invalid email address: test.example.com"):
            self.email_service.send_email("test.example.com", "Hi", "Body")

        assert not self.email_service.sent_emails

    def test_send_email_missing_dot_raises_error(self):
        """Test that an address without '.' is rejected (second condition of the AND)."""
        with pytest.raises(ValueError, match="Invalid email address: test@example"):
            self.email_service.send_email("test@example", "Hi", "Body")


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
        user = service.register_user("new@example.com", VALID_PASSWORD, "New User")

        # Verify complete flow
        assert user["id"] == 1
        assert user["email"] == "new@example.com"
        mock_db.query.assert_called()
        mock_db.insert.assert_called()
        email_service.send_email.assert_called()

    def test_full_login_flow(self):
        """Test complete login flow: register, then log in with the stored user."""
        mock_db = Mock()
        mock_db.insert.return_value = 1
        service = UserService(UserRepository(mock_db), EmailService("test-api-key"))

        # Register: the user does not exist yet
        mock_db.query.return_value = None
        service.register_user(VALID_EMAIL, VALID_PASSWORD, VALID_NAME)

        # Login: the database now returns what was inserted
        mock_db.query.return_value = mock_db.insert.call_args[0][1]
        user = service.login(VALID_EMAIL, VALID_PASSWORD)

        assert user["id"] == 1
        assert user["name"] == VALID_NAME
        mock_db.update.assert_called_once_with("users", 1, {"last_login": "NOW()"})

    def test_registration_with_real_email_service_records_welcome_email(self):
        """Test that the real EmailService records the welcome email."""
        mock_db = Mock()
        mock_db.query.return_value = None
        mock_db.insert.return_value = 5
        email_service = EmailService("test-api-key")
        service = UserService(UserRepository(mock_db), email_service)

        service.register_user(VALID_EMAIL, VALID_PASSWORD, VALID_NAME)

        assert len(email_service.sent_emails) == 1
        assert email_service.sent_emails[0]["to"] == VALID_EMAIL
        assert email_service.sent_emails[0]["subject"] == "Welcome to Our Service!"

    def test_registration_with_invalid_email_still_creates_user(self, capsys):
        """Test that the real EmailService rejecting the address does not block registration."""
        mock_db = Mock()
        mock_db.query.return_value = None
        mock_db.insert.return_value = 9
        email_service = EmailService("test-api-key")
        service = UserService(UserRepository(mock_db), email_service)

        user = service.register_user("not-an-email", VALID_PASSWORD, VALID_NAME)

        assert user["id"] == 9
        assert not email_service.sent_emails
        assert "Invalid email address: not-an-email" in capsys.readouterr().out

    def test_registration_duplicate_email_through_repository(self):
        """Test that the repository's duplicate check stops registration end to end."""
        mock_db = Mock()
        mock_db.query.return_value = {"id": 1, "email": VALID_EMAIL}
        email_service = Mock(spec=EmailService)
        service = UserService(UserRepository(mock_db), email_service)

        with pytest.raises(ValueError, match="already exists"):
            service.register_user(VALID_EMAIL, VALID_PASSWORD, VALID_NAME)

        mock_db.insert.assert_not_called()
        email_service.send_email.assert_not_called()
