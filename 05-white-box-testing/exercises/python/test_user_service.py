"""Unit and integration tests for the user-service exercise."""

from unittest.mock import Mock

import pytest

from email_service import EmailService
from user_repository import UserRepository
from user_service import UserService


class TestUserService:
    """Unit tests that mock UserService dependencies at their boundaries."""

    def setup_method(self):
        """Create isolated mocked dependencies for every test."""
        self.mock_repo = Mock(spec=UserRepository)
        self.mock_email = Mock(spec=EmailService)
        self.service = UserService(self.mock_repo, self.mock_email)

    def test_register_user_success(self):
        """A valid registration stores the user and sends a welcome email."""
        self.mock_repo.create_user.return_value = {
            "id": 1,
            "email": "test@example.com",
            "name": "Test User",
        }

        user = self.service.register_user(
            "test@example.com", "password123", "Test User"
        )

        assert user["email"] == "test@example.com"
        created_data = self.mock_repo.create_user.call_args.args[0]
        assert created_data["password_hash"] == self.service._hash_password(
            "password123"
        )
        self.mock_email.send_email.assert_called_once()

    @pytest.mark.parametrize(
        "email,password,name",
        [("", "password123", "Name"), ("a@b.c", "", "Name"), ("a@b.c", "password123", "")],
    )
    def test_register_user_requires_all_fields(self, email, password, name):
        """Each required field rejects an otherwise incomplete registration."""
        with pytest.raises(ValueError, match="Email, password, and name are required"):
            self.service.register_user(email, password, name)
        self.mock_repo.create_user.assert_not_called()

    def test_register_user_with_short_password(self):
        """Passwords shorter than eight characters are rejected."""
        with pytest.raises(ValueError, match="at least 8"):
            self.service.register_user("test@example.com", "short", "Test User")
        self.mock_repo.create_user.assert_not_called()

    def test_register_user_duplicate_email(self):
        """A repository duplicate-email error propagates to the caller."""
        self.mock_repo.create_user.side_effect = ValueError("already exists")

        with pytest.raises(ValueError, match="already exists"):
            self.service.register_user("test@example.com", "password123", "Test User")
        self.mock_email.send_email.assert_not_called()

    def test_register_user_email_failure_does_not_block(self, capsys):
        """Email failure is warned about but does not undo registration."""
        created_user = {"id": 2, "email": "new@example.com", "name": "New User"}
        self.mock_repo.create_user.return_value = created_user
        self.mock_email.send_email.side_effect = ConnectionError("email unavailable")

        assert (
            self.service.register_user("new@example.com", "password123", "New User")
            == created_user
        )
        assert "Could not send welcome email" in capsys.readouterr().out

    def test_register_user_database_failure(self):
        """Database failures stop registration and are not swallowed."""
        self.mock_repo.create_user.side_effect = ConnectionError("database unavailable")

        with pytest.raises(ConnectionError, match="database unavailable"):
            self.service.register_user("test@example.com", "password123", "Test User")

    def test_login_success(self):
        """Correct credentials return the user and update its last-login value."""
        user = {
            "id": 1,
            "email": "test@example.com",
            "password_hash": self.service._hash_password("password123"),
        }
        self.mock_repo.find_by_email.return_value = user

        assert self.service.login("test@example.com", "password123") == user
        self.mock_repo.find_by_email.assert_called_once_with("test@example.com")
        self.mock_repo.update_last_login.assert_called_once_with(1)

    def test_login_user_not_found(self):
        """Unknown users get the same credentials error as a wrong password."""
        self.mock_repo.find_by_email.return_value = None

        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login("missing@example.com", "password123")
        self.mock_repo.update_last_login.assert_not_called()

    def test_login_wrong_password(self):
        """A mismatched password does not update the login timestamp."""
        self.mock_repo.find_by_email.return_value = {
            "id": 1,
            "password_hash": self.service._hash_password("different-password"),
        }

        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login("test@example.com", "password123")
        self.mock_repo.update_last_login.assert_not_called()

    def test_login_database_failure(self):
        """Database failures during lookup propagate unchanged."""
        self.mock_repo.find_by_email.side_effect = ConnectionError(
            "database unavailable"
        )

        with pytest.raises(ConnectionError, match="database unavailable"):
            self.service.login("test@example.com", "password123")

    def test_send_welcome_email_success(self):
        """A welcome message has the expected recipient, subject, and body."""
        self.mock_email.send_email.return_value = True

        assert self.service.send_welcome_email(
            {"email": "test@example.com", "name": "Test"}
        )
        self.mock_email.send_email.assert_called_once_with(
            "test@example.com",
            "Welcome to Our Service!",
            "Hello Test,\n\nThank you for registering!",
        )

    @pytest.mark.parametrize(
        "error", [ValueError("invalid address"), ConnectionError("api unavailable")]
    )
    def test_send_welcome_email_propagates_email_errors(self, error):
        """Direct welcome-email callers can react to external-service failures."""
        self.mock_email.send_email.side_effect = error

        with pytest.raises(type(error)):
            self.service.send_welcome_email({"email": "bad", "name": "Test"})

    def test_get_user_by_id_is_not_implemented(self):
        """The documented unimplemented operation communicates that fact clearly."""
        with pytest.raises(NotImplementedError, match="To be implemented"):
            self.service.get_user_by_id(1)


class TestUserRepositoryAndEmailService:
    """Tests for the concrete repository and email boundary classes."""

    def test_repository_create_find_and_update(self):
        """Repository delegates queries, inserts, and updates to its database."""
        database = Mock()
        database.query.return_value = None
        database.insert.return_value = 7
        repository = UserRepository(database)
        data = {"email": "test@example.com", "name": "Test"}

        assert repository.create_user(data)["id"] == 7
        database.query.assert_called_once_with(
            "SELECT * FROM users WHERE email = 'test@example.com'"
        )
        database.insert.assert_called_once_with("users", data)
        repository.update_last_login(7)
        database.update.assert_called_once_with("users", 7, {"last_login": "NOW()"})

    def test_repository_rejects_duplicate_email(self):
        """Repository prevents an insert when a matching record already exists."""
        database = Mock()
        database.query.return_value = {"id": 1}

        with pytest.raises(ValueError, match="already exists"):
            UserRepository(database).create_user({"email": "test@example.com"})
        database.insert.assert_not_called()

    def test_email_service_stores_valid_messages_and_rejects_invalid_addresses(self):
        """Email validation controls whether an email is recorded as sent."""
        service = EmailService("key")

        assert service.send_email("test@example.com", "Hello", "Body") is True
        assert service.sent_emails == [
            {"to": "test@example.com", "subject": "Hello", "body": "Body"}
        ]
        with pytest.raises(ValueError, match="Invalid email address"):
            service.send_email("invalid-address", "Hello", "Body")


class TestUserServiceIntegration:
    """Integration tests using a real repository with a mocked database boundary."""

    def test_full_registration_flow(self):
        """Registration coordinates the repository, database, and email service."""
        database = Mock()
        database.query.return_value = None
        database.insert.return_value = 1
        email = Mock(spec=EmailService)
        email.send_email.return_value = True
        service = UserService(UserRepository(database), email)

        user = service.register_user("new@example.com", "password123", "New User")

        assert user["id"] == 1
        assert user["email"] == "new@example.com"
        database.query.assert_called_once()
        database.insert.assert_called_once()
        email.send_email.assert_called_once()

    def test_full_login_flow(self):
        """Login works through the real repository once the database returns a user."""
        database = Mock()
        email = Mock(spec=EmailService)
        service = UserService(UserRepository(database), email)
        password_hash = service._hash_password("password123")
        database.query.return_value = {
            "id": 3,
            "email": "member@example.com",
            "password_hash": password_hash,
        }

        user = service.login("member@example.com", "password123")

        assert user["id"] == 3
        database.update.assert_called_once_with("users", 3, {"last_login": "NOW()"})
