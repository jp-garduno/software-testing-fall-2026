import hashlib
from unittest.mock import Mock

import pytest
from email_service import EmailService
from user_repository import UserRepository
from user_service import UserService


class TestUserService:  # pylint: disable=attribute-defined-outside-init
    """Unit tests for UserService with mocked dependencies."""

    def setup_method(self):
        self.mock_repo = Mock(spec=UserRepository)
        self.mock_email = Mock(spec=EmailService)
        self.service = UserService(self.mock_repo, self.mock_email)

    def test_register_user_success(self):
        self.mock_repo.create_user.return_value = {
            "id": 1,
            "email": "test@example.com",
            "name": "Test User",
            "password_hash": hashlib.sha256(b"password123").hexdigest(),
        }
        self.mock_email.send_email.return_value = True

        user = self.service.register_user(
            "test@example.com", "password123", "Test User"
        )

        assert user["email"] == "test@example.com"
        assert user["name"] == "Test User"
        created_data = self.mock_repo.create_user.call_args.args[0]
        assert (
            created_data["password_hash"] == hashlib.sha256(b"password123").hexdigest()
        )
        assert created_data["created_at"]
        self.mock_repo.create_user.assert_called_once_with(created_data)
        self.mock_email.send_email.assert_called_once_with(
            "test@example.com",
            "Welcome to Our Service!",
            "Hello Test User,\n\nThank you for registering!",
        )

    def test_register_user_with_short_password(self):
        with pytest.raises(ValueError, match="at least 8 characters"):
            self.service.register_user("test@example.com", "short", "Test User")

        self.mock_repo.create_user.assert_not_called()
        self.mock_email.send_email.assert_not_called()

    @pytest.mark.parametrize(
        ("email", "password", "name"),
        [
            ("", "password123", "Test User"),
            ("test@example.com", "", "Test User"),
            ("test@example.com", "password123", ""),
        ],
    )
    def test_register_user_with_missing_required_input(self, email, password, name):
        with pytest.raises(ValueError, match="are required"):
            self.service.register_user(email, password, name)

        self.mock_repo.create_user.assert_not_called()

    def test_register_user_duplicate_email(self):
        self.mock_repo.create_user.side_effect = ValueError("already exists")

        with pytest.raises(ValueError, match="already exists"):
            self.service.register_user("test@example.com", "password123", "Test User")

        self.mock_email.send_email.assert_not_called()

    def test_register_user_email_failure_does_not_block(self, capsys):
        self.mock_repo.create_user.return_value = {
            "id": 1,
            "email": "test@example.com",
            "name": "Test User",
        }
        self.mock_email.send_email.side_effect = ConnectionError("email down")

        user = self.service.register_user(
            "test@example.com", "password123", "Test User"
        )

        assert user["id"] == 1
        assert "Could not send welcome email: email down" in capsys.readouterr().out

    def test_register_user_database_failure(self):
        self.mock_repo.create_user.side_effect = ConnectionError("database down")

        with pytest.raises(ConnectionError, match="database down"):
            self.service.register_user("test@example.com", "password123", "Test User")

        self.mock_email.send_email.assert_not_called()

    def test_login_success(self):
        mock_user = {
            "id": 1,
            "email": "test@example.com",
            "password_hash": hashlib.sha256(b"password123").hexdigest(),
            "name": "Test User",
        }
        self.mock_repo.find_by_email.return_value = mock_user

        user = self.service.login("test@example.com", "password123")

        assert user == mock_user
        self.mock_repo.find_by_email.assert_called_once_with("test@example.com")
        self.mock_repo.update_last_login.assert_called_once_with(1)

    def test_login_user_not_found(self):
        self.mock_repo.find_by_email.return_value = None

        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login("missing@example.com", "password123")

        self.mock_repo.update_last_login.assert_not_called()

    def test_login_wrong_password(self):
        self.mock_repo.find_by_email.return_value = {
            "id": 1,
            "password_hash": hashlib.sha256(b"other-password").hexdigest(),
        }

        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login("test@example.com", "password123")

        self.mock_repo.update_last_login.assert_not_called()

    def test_login_database_failure(self):
        self.mock_repo.find_by_email.side_effect = ConnectionError("database down")

        with pytest.raises(ConnectionError, match="database down"):
            self.service.login("test@example.com", "password123")

    def test_send_welcome_email_success(self):
        self.mock_email.send_email.return_value = True
        user = {"email": "test@example.com", "name": "Test User"}

        result = self.service.send_welcome_email(user)

        assert result is True
        self.mock_email.send_email.assert_called_once_with(
            "test@example.com",
            "Welcome to Our Service!",
            "Hello Test User,\n\nThank you for registering!",
        )

    @pytest.mark.parametrize(
        ("error", "message"),
        [
            (ValueError("invalid address"), "invalid address"),
            (ConnectionError("api down"), "api down"),
        ],
    )
    def test_send_welcome_email_propagates_service_errors(self, error, message):
        self.mock_email.send_email.side_effect = error

        with pytest.raises(type(error), match=message):
            self.service.send_welcome_email(
                {"email": "bad-address", "name": "Test User"}
            )

    def test_get_user_by_id_success(self):
        expected_user = {"id": 1, "email": "test@example.com"}
        self.mock_repo.find_by_id.return_value = expected_user

        user = self.service.get_user_by_id(1)

        assert user is expected_user
        self.mock_repo.find_by_id.assert_called_once_with(1)

    def test_get_user_by_id_not_found(self):
        self.mock_repo.find_by_id.return_value = None

        with pytest.raises(ValueError, match="User not found"):
            self.service.get_user_by_id(99)

    def test_get_user_by_id_database_failure(self):
        self.mock_repo.find_by_id.side_effect = ConnectionError("database down")

        with pytest.raises(ConnectionError, match="database down"):
            self.service.get_user_by_id(1)


class TestUserRepository:  # pylint: disable=attribute-defined-outside-init
    """Tests for repository behavior using a mocked database connection."""

    def setup_method(self):
        self.db = Mock()
        self.repository = UserRepository(self.db)

    def test_find_by_email_returns_query_result(self):
        expected_user = {"id": 1, "email": "test@example.com"}
        self.db.query.return_value = expected_user

        result = self.repository.find_by_email("test@example.com")

        assert result is expected_user
        self.db.query.assert_called_once_with(
            "SELECT * FROM users WHERE email = 'test@example.com'"
        )

    def test_find_by_id_returns_query_result(self):
        expected_user = {"id": 7, "email": "test@example.com"}
        self.db.query.return_value = expected_user

        result = self.repository.find_by_id(7)

        assert result is expected_user
        self.db.query.assert_called_once_with("SELECT * FROM users WHERE id = '7'")

    def test_create_user_inserts_when_email_is_new(self):
        user_data = {"email": "test@example.com", "name": "Test User"}
        self.db.query.return_value = None
        self.db.insert.return_value = 42

        result = self.repository.create_user(user_data)

        assert result == {**user_data, "id": 42}
        self.db.insert.assert_called_once_with("users", user_data)

    def test_create_user_rejects_duplicate_email(self):
        self.db.query.return_value = {"id": 1, "email": "test@example.com"}
        user_data = {"email": "test@example.com"}

        with pytest.raises(ValueError, match="already exists"):
            self.repository.create_user(user_data)

        self.db.insert.assert_not_called()

    def test_update_last_login(self):
        self.repository.update_last_login(7)

        self.db.update.assert_called_once_with("users", 7, {"last_login": "NOW()"})

    @pytest.mark.parametrize(
        "method_name,args",
        [
            ("find_by_email", ("test@example.com",)),
            ("find_by_id", (7,)),
            ("create_user", ({"email": "test@example.com"},)),
            ("update_last_login", (7,)),
        ],
    )
    def test_database_failures_propagate(self, method_name, args):
        self.db.query.side_effect = ConnectionError("database down")
        self.db.insert.side_effect = ConnectionError("database down")
        self.db.update.side_effect = ConnectionError("database down")
        method = getattr(self.repository, method_name)

        with pytest.raises(ConnectionError, match="database down"):
            method(*args)


class TestEmailService:  # pylint: disable=attribute-defined-outside-init
    """Tests for the simulated email API."""

    def setup_method(self):
        self.service = EmailService("test-api-key")

    def test_send_email_success(self):
        result = self.service.send_email("test@example.com", "Subject", "Body")

        assert result is True
        assert self.service.sent_emails == [
            {
                "to": "test@example.com",
                "subject": "Subject",
                "body": "Body",
            }
        ]

    @pytest.mark.parametrize("address", ["invalid", "user@domain"])
    def test_send_email_rejects_invalid_address(self, address):
        with pytest.raises(ValueError, match="Invalid email address"):
            self.service.send_email(address, "Subject", "Body")

        assert not self.service.sent_emails


class TestUserServiceIntegration:
    """Integration tests using the real repository and service layers."""

    def test_full_registration_flow(self):
        mock_db = Mock()
        mock_db.query.return_value = None
        mock_db.insert.return_value = 1
        repo = UserRepository(mock_db)
        email_service = Mock(spec=EmailService)
        email_service.send_email.return_value = True
        service = UserService(repo, email_service)

        user = service.register_user("new@example.com", "password123", "New User")

        assert user["id"] == 1
        assert user["email"] == "new@example.com"
        assert user["password_hash"] == hashlib.sha256(b"password123").hexdigest()
        mock_db.query.assert_called_once_with(
            "SELECT * FROM users WHERE email = 'new@example.com'"
        )
        mock_db.insert.assert_called_once_with("users", user)
        email_service.send_email.assert_called_once()

    def test_full_login_flow_after_registration(self):
        mock_db = Mock()
        mock_db.insert.return_value = 1
        repo = UserRepository(mock_db)
        email_service = Mock(spec=EmailService)
        email_service.send_email.return_value = True
        service = UserService(repo, email_service)
        stored_user = {
            "id": 1,
            "email": "new@example.com",
            "password_hash": hashlib.sha256(b"password123").hexdigest(),
            "name": "New User",
        }
        mock_db.query.side_effect = [None, stored_user]

        registered_user = service.register_user(
            "new@example.com", "password123", "New User"
        )
        logged_in_user = service.login("new@example.com", "password123")

        assert registered_user["id"] == 1
        assert logged_in_user == stored_user
        assert mock_db.query.call_count == 2
        mock_db.update.assert_called_once_with("users", 1, {"last_login": "NOW()"})
