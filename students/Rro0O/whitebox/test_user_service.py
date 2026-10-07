"""Unit and integration tests for UserService (exercise 3)."""

from unittest.mock import Mock, patch

import pytest

from email_service import EmailService
from user_repository import UserRepository
from user_service import UserService


class TestUserService:
    """Test suite for UserService with mocked dependencies."""

    def setup_method(self):
        """Create mocked dependencies and service instance."""
        self.mock_repo = Mock(spec=UserRepository)
        self.mock_email = Mock(spec=EmailService)
        self.service = UserService(self.mock_repo, self.mock_email)

    # register_user
    def test_register_user_success(self):
        """Test successful user registration."""
        self.mock_repo.create_user.return_value = {
            "id": 1,
            "email": "test@example.com",
            "name": "Test User",
            "password_hash": "hashed_password",
        }
        self.mock_email.send_email.return_value = True

        user = self.service.register_user("test@example.com", "password123", "Test User")

        assert user["email"] == "test@example.com"
        assert user["name"] == "Test User"
        self.mock_repo.create_user.assert_called_once()
        self.mock_email.send_email.assert_called_once()
        call_args = self.mock_email.send_email.call_args
        assert call_args[0][0] == "test@example.com"
        assert "Welcome" in call_args[0][1]

    def test_register_user_hashes_password_and_sets_timestamp(self):
        """Test that the stored data has a hashed password and a created_at timestamp."""
        self.mock_repo.create_user.side_effect = lambda data: {**data, "id": 1}

        with patch("user_service.datetime") as mock_datetime:
            mock_datetime.now.return_value.isoformat.return_value = "2026-01-01T00:00:00"
            self.service.register_user("test@example.com", "password123", "Test User")

        saved = self.mock_repo.create_user.call_args[0][0]
        assert saved["password_hash"] == self.service._hash_password("password123")
        assert saved["password_hash"] != "password123"
        assert saved["created_at"] == "2026-01-01T00:00:00"

    def test_register_user_with_short_password(self):
        """Test that short password raises ValueError."""
        with pytest.raises(ValueError, match="at least 8 characters"):
            self.service.register_user("test@example.com", "short", "Test User")
        self.mock_repo.create_user.assert_not_called()

    def test_register_user_with_seven_char_password(self):
        """Test boundary: 7 characters is rejected."""
        with pytest.raises(ValueError, match="at least 8 characters"):
            self.service.register_user("test@example.com", "1234567", "Test User")

    def test_register_user_with_eight_char_password(self):
        """Test boundary: 8 characters is accepted."""
        self.mock_repo.create_user.return_value = {"id": 1, "email": "a@b.com", "name": "N"}
        assert self.service.register_user("a@b.com", "12345678", "N")["id"] == 1

    @pytest.mark.parametrize(
        "email,password,name",
        [
            ("", "password123", "Test User"),
            (None, "password123", "Test User"),
            ("test@example.com", "", "Test User"),
            ("test@example.com", None, "Test User"),
            ("test@example.com", "password123", ""),
            ("test@example.com", "password123", None),
        ],
    )
    def test_register_user_with_missing_field(self, email, password, name):
        """Test that any missing required field raises ValueError."""
        with pytest.raises(ValueError, match="required"):
            self.service.register_user(email, password, name)
        self.mock_repo.create_user.assert_not_called()

    def test_register_user_duplicate_email(self):
        """Test that duplicate email raises ValueError."""
        self.mock_repo.create_user.side_effect = ValueError("User with email test@example.com already exists")

        with pytest.raises(ValueError, match="already exists"):
            self.service.register_user("test@example.com", "password123", "Test User")
        self.mock_email.send_email.assert_not_called()

    def test_register_user_email_failure_does_not_block(self, capsys):
        """Test that email failure doesn't prevent registration."""
        self.mock_repo.create_user.return_value = {"id": 1, "email": "test@example.com", "name": "Test User"}
        self.mock_email.send_email.side_effect = ConnectionError("API down")

        user = self.service.register_user("test@example.com", "password123", "Test User")

        assert user["id"] == 1
        assert "Could not send welcome email" in capsys.readouterr().out

    def test_register_user_database_failure(self):
        """Test that database failure raises exception."""
        self.mock_repo.create_user.side_effect = ConnectionError("DB down")

        with pytest.raises(ConnectionError, match="DB down"):
            self.service.register_user("test@example.com", "password123", "Test User")
        self.mock_email.send_email.assert_not_called()

    # login
    def test_login_success(self):
        """Test successful login."""
        mock_user = {
            "id": 1,
            "email": "test@example.com",
            "password_hash": self.service._hash_password("password123"),
            "name": "Test User",
        }
        self.mock_repo.find_by_email.return_value = mock_user

        user = self.service.login("test@example.com", "password123")

        assert user["email"] == "test@example.com"
        self.mock_repo.find_by_email.assert_called_once_with("test@example.com")
        self.mock_repo.update_last_login.assert_called_once_with(1)

    def test_login_user_not_found(self):
        """Test login with non-existent email."""
        self.mock_repo.find_by_email.return_value = None

        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login("missing@example.com", "password123")
        self.mock_repo.update_last_login.assert_not_called()

    def test_login_wrong_password(self):
        """Test login with incorrect password."""
        self.mock_repo.find_by_email.return_value = {
            "id": 1,
            "email": "test@example.com",
            "password_hash": self.service._hash_password("password123"),
        }

        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login("test@example.com", "wrongpassword")
        self.mock_repo.update_last_login.assert_not_called()

    def test_login_database_failure(self):
        """Test login when database fails."""
        self.mock_repo.find_by_email.side_effect = ConnectionError("DB down")

        with pytest.raises(ConnectionError, match="DB down"):
            self.service.login("test@example.com", "password123")

    def test_login_updates_last_login_after_verification(self):
        """Test that last_login is only updated after the user lookup."""
        manager = Mock()
        manager.attach_mock(self.mock_repo.find_by_email, "find")
        manager.attach_mock(self.mock_repo.update_last_login, "update")
        self.mock_repo.find_by_email.return_value = {
            "id": 7,
            "password_hash": self.service._hash_password("password123"),
        }

        self.service.login("test@example.com", "password123")

        assert [c[0] for c in manager.mock_calls] == ["find", "update"]

    # send_welcome_email
    def test_send_welcome_email_success(self):
        """Test sending welcome email."""
        self.mock_email.send_email.return_value = True

        result = self.service.send_welcome_email({"email": "test@example.com", "name": "Test User"})

        assert result is True
        self.mock_email.send_email.assert_called_once_with(
            "test@example.com",
            "Welcome to Our Service!",
            "Hello Test User,\n\nThank you for registering!",
        )

    def test_send_welcome_email_invalid_address(self):
        """Test welcome email with invalid address."""
        self.mock_email.send_email.side_effect = ValueError("Invalid email address: bad")

        with pytest.raises(ValueError, match="Invalid email address"):
            self.service.send_welcome_email({"email": "bad", "name": "Test User"})

    def test_send_welcome_email_api_failure(self):
        """Test welcome email when API fails."""
        self.mock_email.send_email.side_effect = ConnectionError("API down")

        with pytest.raises(ConnectionError, match="API down"):
            self.service.send_welcome_email({"email": "test@example.com", "name": "Test User"})

    # get_user_by_id
    def test_get_user_by_id_not_implemented(self):
        """Test that get_user_by_id is still a stub."""
        with pytest.raises(NotImplementedError):
            self.service.get_user_by_id(1)


class TestUserRepository:
    """Test suite for UserRepository with a mocked DB connection."""

    def setup_method(self):
        """Create mocked DB and repository."""
        self.mock_db = Mock()
        self.repo = UserRepository(self.mock_db)

    def test_find_by_email_returns_user(self):
        """Test that find_by_email returns the DB result."""
        self.mock_db.query.return_value = {"id": 1}

        assert self.repo.find_by_email("a@b.com") == {"id": 1}
        assert "a@b.com" in self.mock_db.query.call_args[0][0]

    def test_find_by_email_connection_error(self):
        """Test that DB errors propagate."""
        self.mock_db.query.side_effect = ConnectionError("DB down")

        with pytest.raises(ConnectionError):
            self.repo.find_by_email("a@b.com")

    def test_create_user_success(self):
        """Test creating a new user assigns the generated id."""
        self.mock_db.query.return_value = None
        self.mock_db.insert.return_value = 42

        user = self.repo.create_user({"email": "a@b.com"})

        assert user == {"email": "a@b.com", "id": 42}
        self.mock_db.insert.assert_called_once_with("users", {"email": "a@b.com", "id": 42})

    def test_create_user_duplicate(self):
        """Test that an existing user raises ValueError and nothing is inserted."""
        self.mock_db.query.return_value = {"id": 1}

        with pytest.raises(ValueError, match="already exists"):
            self.repo.create_user({"email": "a@b.com"})
        self.mock_db.insert.assert_not_called()

    def test_update_last_login(self):
        """Test that update_last_login delegates to the DB."""
        self.repo.update_last_login(5)

        self.mock_db.update.assert_called_once_with("users", 5, {"last_login": "NOW()"})


class TestEmailService:
    """Test suite for EmailService."""

    def setup_method(self):
        """Create email service."""
        self.email = EmailService("key")

    def test_send_email_success(self):
        """Test that a valid email is sent and recorded."""
        assert self.email.send_email("a@b.com", "Hi", "Body") is True
        assert self.email.sent_emails == [{"to": "a@b.com", "subject": "Hi", "body": "Body"}]

    @pytest.mark.parametrize("address", ["invalid", "no-at.com", "no@dot"])
    def test_send_email_invalid_address(self, address):
        """Test that invalid addresses raise ValueError."""
        with pytest.raises(ValueError, match="Invalid email address"):
            self.email.send_email(address, "Hi", "Body")
        assert not self.email.sent_emails


class TestUserServiceIntegration:
    """Integration tests with only the DB and the email API mocked."""

    def setup_method(self):
        """Wire real repository and service over a fake in-memory DB."""
        self.users = {}
        self.mock_db = Mock()
        self.mock_db.query.side_effect = lambda sql: next(
            (u for e, u in self.users.items() if f"'{e}'" in sql), None
        )

        def insert(_table, data):
            self.users[data["email"]] = data
            return len(self.users)

        self.mock_db.insert.side_effect = insert
        self.repo = UserRepository(self.mock_db)
        self.email_service = Mock(spec=EmailService)
        self.email_service.send_email.return_value = True
        self.service = UserService(self.repo, self.email_service)

    def test_full_registration_flow(self):
        """Test complete registration flow with minimal mocking."""
        user = self.service.register_user("new@example.com", "password123", "New User")

        assert user["id"] == 1
        assert user["email"] == "new@example.com"
        self.mock_db.query.assert_called()
        self.mock_db.insert.assert_called()
        self.email_service.send_email.assert_called_once()

    def test_full_login_flow(self):
        """Test registration followed by login."""
        self.service.register_user("new@example.com", "password123", "New User")

        user = self.service.login("new@example.com", "password123")

        assert user["email"] == "new@example.com"
        self.mock_db.update.assert_called_once_with("users", 1, {"last_login": "NOW()"})

    def test_duplicate_registration_fails(self):
        """Test that registering the same email twice fails."""
        self.service.register_user("new@example.com", "password123", "New User")

        with pytest.raises(ValueError, match="already exists"):
            self.service.register_user("new@example.com", "password456", "Other")

    def test_login_wrong_password_after_registration(self):
        """Test that login fails with the wrong password."""
        self.service.register_user("new@example.com", "password123", "New User")

        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login("new@example.com", "badpassword")
        self.mock_db.update.assert_not_called()
