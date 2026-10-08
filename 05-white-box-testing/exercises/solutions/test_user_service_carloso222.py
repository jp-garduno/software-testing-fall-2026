# pylint: disable=too-many-public-methods
# pylint: disable=attribute-defined-outside-init
# pylint: disable=protected-access

from unittest.mock import Mock, patch

import pytest
from email_service_carloso222 import EmailService
from user_repository_carloso222 import UserRepository
from user_service_carloso222 import UserService


class TestUserService:
    """Test suite for UserService with mocked dependencies."""

    def setup_method(self):
        """Create fresh mocked dependencies."""
        self.mock_repo = Mock(spec=UserRepository)
        self.mock_email = Mock(spec=EmailService)

        self.service = UserService(
            self.mock_repo,
            self.mock_email,
        )

    def test_register_user_success(self):
        """Test successful user registration."""
        self.mock_repo.create_user.return_value = {
            "id": 1,
            "email": "test@example.com",
            "name": "Test User",
            "password_hash": "hashed_password",
        }

        self.mock_email.send_email.return_value = True

        user = self.service.register_user(
            "test@example.com",
            "password123",
            "Test User",
        )

        assert user["email"] == "test@example.com"
        assert user["name"] == "Test User"

        self.mock_repo.create_user.assert_called_once()
        self.mock_email.send_email.assert_called_once()

        call_args = self.mock_email.send_email.call_args

        assert call_args[0][0] == "test@example.com"
        assert "Welcome" in call_args[0][1]

    def test_register_user_hashes_password(self):
        """Test that plain password is not stored."""
        self.mock_repo.create_user.side_effect = lambda user_data: {
            "id": 1,
            **user_data,
        }
        self.mock_email.send_email.return_value = True

        self.service.register_user(
            "test@example.com",
            "password123",
            "Test User",
        )

        user_data = self.mock_repo.create_user.call_args[0][0]

        assert user_data["password_hash"] != "password123"
        assert user_data["password_hash"] == (
            self.service._hash_password("password123")
        )

    @patch("user_service_carloso222.datetime")
    def test_register_user_creation_timestamp(
        self,
        mock_datetime,
    ):
        """Test registration timestamp."""
        mock_datetime.now.return_value.isoformat.return_value = "2026-01-01T00:00:00"

        self.mock_repo.create_user.side_effect = lambda user_data: {
            "id": 1,
            **user_data,
        }
        self.mock_email.send_email.return_value = True

        self.service.register_user(
            "test@example.com",
            "password123",
            "Test User",
        )

        user_data = self.mock_repo.create_user.call_args[0][0]

        assert user_data["created_at"] == "2026-01-01T00:00:00"

    def test_register_user_with_short_password(self):
        """Test that short password raises ValueError."""
        with pytest.raises(
            ValueError,
            match="Password must be at least 8 characters",
        ):
            self.service.register_user(
                "test@example.com",
                "short",
                "Test User",
            )

        self.mock_repo.create_user.assert_not_called()

    @pytest.mark.parametrize(
        "email,password,name",
        [
            ("", "password123", "Test User"),
            ("test@example.com", "", "Test User"),
            ("test@example.com", "password123", ""),
        ],
    )
    def test_register_user_with_missing_fields(
        self,
        email,
        password,
        name,
    ):
        """Test required registration fields."""
        with pytest.raises(
            ValueError,
            match="Email, password, and name are required",
        ):
            self.service.register_user(
                email,
                password,
                name,
            )

        self.mock_repo.create_user.assert_not_called()

    def test_register_user_duplicate_email(self):
        """Test duplicate email error."""
        self.mock_repo.create_user.side_effect = ValueError("User already exists")

        with pytest.raises(
            ValueError,
            match="User already exists",
        ):
            self.service.register_user(
                "test@example.com",
                "password123",
                "Test User",
            )

        self.mock_email.send_email.assert_not_called()

    def test_register_user_email_failure_does_not_block(
        self,
        capsys,
    ):
        """Test that email failure doesn't stop registration."""
        created_user = {
            "id": 1,
            "email": "test@example.com",
            "name": "Test User",
            "password_hash": "hash",
        }

        self.mock_repo.create_user.return_value = created_user
        self.mock_email.send_email.side_effect = ConnectionError(
            "Email API unavailable"
        )

        user = self.service.register_user(
            "test@example.com",
            "password123",
            "Test User",
        )

        assert user == created_user

        captured = capsys.readouterr()

        assert "Warning: Could not send welcome email" in (captured.out)

    def test_register_user_database_failure(self):
        """Test database failure during registration."""
        self.mock_repo.create_user.side_effect = ConnectionError("Database unavailable")

        with pytest.raises(
            ConnectionError,
            match="Database unavailable",
        ):
            self.service.register_user(
                "test@example.com",
                "password123",
                "Test User",
            )

        self.mock_email.send_email.assert_not_called()

    def test_login_success(self):
        """Test successful login."""
        mock_user = {
            "id": 1,
            "email": "test@example.com",
            "password_hash": self.service._hash_password("password123"),
            "name": "Test User",
        }

        self.mock_repo.find_by_email.return_value = mock_user

        user = self.service.login(
            "test@example.com",
            "password123",
        )

        assert user["email"] == "test@example.com"

        self.mock_repo.find_by_email.assert_called_once_with("test@example.com")
        self.mock_repo.update_last_login.assert_called_once_with(1)

    def test_login_user_not_found(self):
        """Test login with non-existent user."""
        self.mock_repo.find_by_email.return_value = None

        with pytest.raises(
            ValueError,
            match="Invalid email or password",
        ):
            self.service.login(
                "missing@example.com",
                "password123",
            )

        self.mock_repo.update_last_login.assert_not_called()

    def test_login_wrong_password(self):
        """Test login with incorrect password."""
        mock_user = {
            "id": 1,
            "email": "test@example.com",
            "password_hash": self.service._hash_password("correctpassword"),
            "name": "Test User",
        }

        self.mock_repo.find_by_email.return_value = mock_user

        with pytest.raises(
            ValueError,
            match="Invalid email or password",
        ):
            self.service.login(
                "test@example.com",
                "wrongpassword",
            )

        self.mock_repo.update_last_login.assert_not_called()

    def test_login_database_failure(self):
        """Test login when database fails."""
        self.mock_repo.find_by_email.side_effect = ConnectionError(
            "Database unavailable"
        )

        with pytest.raises(
            ConnectionError,
            match="Database unavailable",
        ):
            self.service.login(
                "test@example.com",
                "password123",
            )

    def test_send_welcome_email_success(self):
        """Test welcome email success."""
        user = {
            "email": "test@example.com",
            "name": "Test User",
        }

        self.mock_email.send_email.return_value = True

        result = self.service.send_welcome_email(user)

        assert result is True

        self.mock_email.send_email.assert_called_once_with(
            "test@example.com",
            "Welcome to Our Service!",
            "Hello Test User,\n\nThank you for registering!",
        )

    def test_send_welcome_email_invalid_address(self):
        """Test invalid email address."""
        user = {
            "email": "invalid",
            "name": "Test User",
        }

        self.mock_email.send_email.side_effect = ValueError("Invalid email address")

        with pytest.raises(
            ValueError,
            match="Invalid email address",
        ):
            self.service.send_welcome_email(user)

    def test_send_welcome_email_api_failure(self):
        """Test email API failure."""
        user = {
            "email": "test@example.com",
            "name": "Test User",
        }

        self.mock_email.send_email.side_effect = ConnectionError("API unavailable")

        with pytest.raises(
            ConnectionError,
            match="API unavailable",
        ):
            self.service.send_welcome_email(user)

    def test_get_user_by_id_not_implemented(self):
        """Test unimplemented user lookup."""
        with pytest.raises(
            NotImplementedError,
            match="not implemented",
        ):
            self.service.get_user_by_id(1)


class TestUserRepository:
    """Tests for real UserRepository behavior."""

    def test_find_by_email(self):
        """Test database query."""
        mock_db = Mock()

        expected_user = {
            "id": 1,
            "email": "test@example.com",
        }

        mock_db.query.return_value = expected_user

        repository = UserRepository(mock_db)

        result = repository.find_by_email("test@example.com")

        assert result == expected_user

        mock_db.query.assert_called_once_with(
            "SELECT * FROM users WHERE email = 'test@example.com'"
        )

    def test_create_user_success(self):
        """Test repository user creation."""
        mock_db = Mock()
        mock_db.query.return_value = None
        mock_db.insert.return_value = 10

        repository = UserRepository(mock_db)

        user_data = {
            "email": "new@example.com",
            "name": "New User",
        }

        user = repository.create_user(user_data)

        assert user["id"] == 10

        mock_db.insert.assert_called_once_with(
            "users",
            user_data,
        )

    def test_create_duplicate_user(self):
        """Test duplicate repository user."""
        mock_db = Mock()

        mock_db.query.return_value = {
            "id": 1,
            "email": "test@example.com",
        }

        repository = UserRepository(mock_db)

        with pytest.raises(
            ValueError,
            match="already exists",
        ):
            repository.create_user(
                {
                    "email": "test@example.com",
                    "name": "Test User",
                }
            )

        mock_db.insert.assert_not_called()

    def test_update_last_login(self):
        """Test last login database update."""
        mock_db = Mock()
        repository = UserRepository(mock_db)

        repository.update_last_login(1)

        mock_db.update.assert_called_once_with(
            "users",
            1,
            {"last_login": "NOW()"},
        )


class TestEmailService:
    """Tests for EmailService."""

    def test_send_email_success(self):
        """Test successful email."""
        service = EmailService("test-api-key")

        result = service.send_email(
            "test@example.com",
            "Test Subject",
            "Test Body",
        )

        assert result is True
        assert len(service.sent_emails) == 1

        assert service.sent_emails[0] == {
            "to": "test@example.com",
            "subject": "Test Subject",
            "body": "Test Body",
        }

    @pytest.mark.parametrize(
        "invalid_email",
        [
            "invalid-email",
            "user@example",
        ],
    )
    def test_send_email_invalid_address(
        self,
        invalid_email,
    ):
        """Test invalid email formats."""
        service = EmailService("test-api-key")

        with pytest.raises(
            ValueError,
            match="Invalid email address",
        ):
            service.send_email(
                invalid_email,
                "Subject",
                "Body",
            )

        assert not service.sent_emails


class TestUserServiceIntegration:
    """Integration tests with real internal components."""

    def test_full_registration_flow(self):
        """Test complete registration flow."""
        mock_db = Mock()
        mock_db.query.return_value = None
        mock_db.insert.return_value = 1

        repository = UserRepository(mock_db)

        email_service = Mock(spec=EmailService)
        email_service.send_email.return_value = True

        service = UserService(
            repository,
            email_service,
        )

        user = service.register_user(
            "new@example.com",
            "password123",
            "New User",
        )

        assert user["id"] == 1
        assert user["email"] == "new@example.com"

        mock_db.query.assert_called()
        mock_db.insert.assert_called_once()
        email_service.send_email.assert_called_once()

    def test_full_login_flow(self):
        """Test registration followed by login."""
        mock_db = Mock()

        mock_db.query.return_value = None
        mock_db.insert.return_value = 1

        repository = UserRepository(mock_db)

        email_service = Mock(spec=EmailService)
        email_service.send_email.return_value = True

        service = UserService(
            repository,
            email_service,
        )

        registered_user = service.register_user(
            "new@example.com",
            "password123",
            "New User",
        )

        mock_db.query.return_value = registered_user

        logged_user = service.login(
            "new@example.com",
            "password123",
        )

        assert logged_user["id"] == 1
        assert logged_user["email"] == "new@example.com"

        mock_db.update.assert_called_once_with(
            "users",
            1,
            {"last_login": "NOW()"},
        )
