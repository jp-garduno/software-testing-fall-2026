"""Unit, mock-based, and integration tests for UserService, UserRepository, and EmailService."""
import pytest
from unittest.mock import Mock
from user_service import UserService
from user_repository import UserRepository
from email_service import EmailService


class TestUserService:
    """Test suite for UserService with mocked dependencies."""

    def setup_method(self):
        """Create mocked dependencies and service instance."""
        self.mock_repo = Mock(spec=UserRepository)
        self.mock_email = Mock(spec=EmailService)
        self.service = UserService(self.mock_repo, self.mock_email)

    def test_register_user_success(self):
        """Test successful user registration."""
        self.mock_repo.create_user.return_value = {
            'id': 1,
            'email': 'test@example.com',
            'name': 'Test User',
            'password_hash': self.service._hash_password('password123')
        }
        self.mock_email.send_email.return_value = True

        user = self.service.register_user(
            'test@example.com',
            'password123',
            'Test User'
        )

        assert user['email'] == 'test@example.com'
        assert user['name'] == 'Test User'
        assert user['id'] == 1
        self.mock_repo.create_user.assert_called_once()
        self.mock_email.send_email.assert_called_once()
        call_args = self.mock_email.send_email.call_args
        assert call_args[0][0] == 'test@example.com'
        assert 'Welcome' in call_args[0][1]

    def test_register_user_with_short_password(self):
        """Test that passwords shorter than 8 characters raise ValueError."""
        with pytest.raises(ValueError, match="Password must be at least 8 characters"):
            self.service.register_user('user@example.com', 'short1', 'Test User')

    @pytest.mark.parametrize("email,password,name", [
        ("", "password123", "Test User"),
        ("user@example.com", "", "Test User"),
        ("user@example.com", "password123", ""),
        (None, "password123", "Test User"),
        ("user@example.com", None, "Test User"),
        ("user@example.com", "password123", None),
    ])
    def test_register_user_missing_required_fields(self, email, password, name):
        """Test that missing email, password, or name raises ValueError."""
        with pytest.raises(ValueError, match="Email, password, and name are required"):
            self.service.register_user(email, password, name)

    def test_register_user_duplicate_email(self):
        """Test that duplicate email raises ValueError from repository."""
        self.mock_repo.create_user.side_effect = ValueError(
            "User with email test@example.com already exists"
        )

        with pytest.raises(ValueError, match="already exists"):
            self.service.register_user('test@example.com', 'password123', 'Test User')

    def test_register_user_email_failure_does_not_block(self):
        """Test that email failure doesn't prevent registration."""
        self.mock_repo.create_user.return_value = {
            'id': 2,
            'email': 'valid@example.com',
            'name': 'Happy User',
            'password_hash': 'somehash'
        }
        self.mock_email.send_email.side_effect = ConnectionError("SMTP server down")

        user = self.service.register_user('valid@example.com', 'password123', 'Happy User')

        assert user['id'] == 2
        assert user['email'] == 'valid@example.com'
        self.mock_repo.create_user.assert_called_once()
        self.mock_email.send_email.assert_called_once()

    def test_register_user_database_failure(self):
        """Test that database failure raises exception."""
        self.mock_repo.create_user.side_effect = ConnectionError("DB connection dropped")

        with pytest.raises(ConnectionError, match="DB connection dropped"):
            self.service.register_user('user@example.com', 'password123', 'User')

    def test_login_success(self):
        """Test successful login with password verification and last login update."""
        password = 'securepassword123'
        mock_user = {
            'id': 42,
            'email': 'user@domain.com',
            'password_hash': self.service._hash_password(password),
            'name': 'Alice'
        }
        self.mock_repo.find_by_email.return_value = mock_user

        user = self.service.login('user@domain.com', password)

        assert user['id'] == 42
        assert user['email'] == 'user@domain.com'
        self.mock_repo.find_by_email.assert_called_once_with('user@domain.com')
        self.mock_repo.update_last_login.assert_called_once_with(42)

    def test_login_user_not_found(self):
        """Test login with non-existent email raises ValueError."""
        self.mock_repo.find_by_email.return_value = None

        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login('unknown@example.com', 'password123')

        self.mock_repo.update_last_login.assert_not_called()

    def test_login_wrong_password(self):
        """Test login with incorrect password raises ValueError."""
        mock_user = {
            'id': 10,
            'email': 'user@example.com',
            'password_hash': self.service._hash_password('correct_pass123'),
            'name': 'Bob'
        }
        self.mock_repo.find_by_email.return_value = mock_user

        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login('user@example.com', 'wrong_pass123')

        self.mock_repo.update_last_login.assert_not_called()

    def test_login_database_failure(self):
        """Test login when database query fails."""
        self.mock_repo.find_by_email.side_effect = ConnectionError("Timeout querying database")

        with pytest.raises(ConnectionError, match="Timeout"):
            self.service.login('user@example.com', 'password123')

    def test_send_welcome_email_success(self):
        """Test sending welcome email calls email_service with correct parameters."""
        self.mock_email.send_email.return_value = True
        user = {'name': 'Charlie', 'email': 'charlie@example.com'}

        result = self.service.send_welcome_email(user)

        assert result is True
        self.mock_email.send_email.assert_called_once_with(
            'charlie@example.com',
            'Welcome to Our Service!',
            'Hello Charlie,\n\nThank you for registering!'
        )

    def test_send_welcome_email_invalid_address(self):
        """Test welcome email when email service raises ValueError on invalid address."""
        self.mock_email.send_email.side_effect = ValueError("Invalid email address")
        user = {'name': 'Broken', 'email': 'invalid-email'}

        with pytest.raises(ValueError, match="Invalid email address"):
            self.service.send_welcome_email(user)

    def test_send_welcome_email_api_failure(self):
        """Test welcome email when API fails with ConnectionError."""
        self.mock_email.send_email.side_effect = ConnectionError("API Unavailable")
        user = {'name': 'Eve', 'email': 'eve@example.com'}

        with pytest.raises(ConnectionError, match="API Unavailable"):
            self.service.send_welcome_email(user)

    def test_get_user_by_id_raises_not_implemented(self):
        """Test that get_user_by_id raises NotImplementedError as defined."""
        with pytest.raises(NotImplementedError, match="To be implemented"):
            self.service.get_user_by_id(1)

    def test_hash_password_deterministic(self):
        """Test that password hashing is deterministic and irreversible."""
        hash1 = self.service._hash_password("mySecret123")
        hash2 = self.service._hash_password("mySecret123")
        hash3 = self.service._hash_password("differentSecret")

        assert hash1 == hash2
        assert hash1 != hash3
        assert len(hash1) == 64


class TestUserRepository:
    """Direct unit tests for UserRepository class to guarantee comprehensive coverage."""

    def test_find_by_email_executes_query(self):
        """Test find_by_email queries database connection correctly."""
        mock_db = Mock()
        mock_db.query.return_value = {'id': 1, 'email': 'find@example.com'}
        repo = UserRepository(mock_db)

        result = repo.find_by_email('find@example.com')

        assert result == {'id': 1, 'email': 'find@example.com'}
        mock_db.query.assert_called_once_with("SELECT * FROM users WHERE email = 'find@example.com'")

    def test_find_by_email_raises_connection_error(self):
        """Test find_by_email propagates database connection errors."""
        mock_db = Mock()
        mock_db.query.side_effect = ConnectionError("DB down")
        repo = UserRepository(mock_db)

        with pytest.raises(ConnectionError):
            repo.find_by_email('find@example.com')

    def test_create_user_success(self):
        """Test create_user checks existence and inserts user record."""
        mock_db = Mock()
        mock_db.query.return_value = None
        mock_db.insert.return_value = 99
        repo = UserRepository(mock_db)

        user_data = {'email': 'new@example.com', 'name': 'New'}
        result = repo.create_user(user_data)

        assert result['id'] == 99
        assert result['email'] == 'new@example.com'
        mock_db.insert.assert_called_once_with("users", user_data)

    def test_create_user_already_exists_raises_error(self):
        """Test create_user raises ValueError if user is found."""
        mock_db = Mock()
        mock_db.query.return_value = {'id': 1, 'email': 'dup@example.com'}
        repo = UserRepository(mock_db)

        with pytest.raises(ValueError, match="already exists"):
            repo.create_user({'email': 'dup@example.com'})

    def test_update_last_login(self):
        """Test update_last_login updates user record in database."""
        mock_db = Mock()
        repo = UserRepository(mock_db)

        repo.update_last_login(7)
        mock_db.update.assert_called_once_with("users", 7, {"last_login": "NOW()"})

    def test_update_last_login_connection_error(self):
        """Test update_last_login propagates ConnectionError."""
        mock_db = Mock()
        mock_db.update.side_effect = ConnectionError("DB dropped")
        repo = UserRepository(mock_db)

        with pytest.raises(ConnectionError):
            repo.update_last_login(7)


class TestEmailService:
    """Direct unit tests for EmailService class to guarantee comprehensive coverage."""

    def test_send_email_success(self):
        """Test sending email with valid address records email and returns True."""
        service = EmailService(api_key="secret-key-123")
        assert service.api_key == "secret-key-123"

        result = service.send_email("recipient@domain.com", "Test Subject", "Test Body")

        assert result is True
        assert len(service.sent_emails) == 1
        assert service.sent_emails[0]['to'] == "recipient@domain.com"
        assert service.sent_emails[0]['subject'] == "Test Subject"
        assert service.sent_emails[0]['body'] == "Test Body"

    @pytest.mark.parametrize("invalid_email", [
        "plainaddress",
        "missingatsign.com",
        "@nodomain",
        "nodot@domain",
        ""
    ])
    def test_send_email_invalid_address_raises_value_error(self, invalid_email):
        """Test that invalid email format raises ValueError."""
        service = EmailService(api_key="key")
        with pytest.raises(ValueError, match="Invalid email address"):
            service.send_email(invalid_email, "Subject", "Body")


class TestUserServiceIntegration:
    """Integration tests connecting UserService with realistic dependencies."""

    def test_full_registration_flow(self):
        """Test complete registration flow with database query and insert."""
        mock_db = Mock()
        mock_db.query.return_value = None
        mock_db.insert.return_value = 101

        repo = UserRepository(mock_db)
        email_service = Mock(spec=EmailService)
        email_service.send_email.return_value = True

        service = UserService(repo, email_service)

        user = service.register_user('integration@test.com', 'pass12345', 'Integration User')

        assert user['id'] == 101
        assert user['email'] == 'integration@test.com'
        mock_db.query.assert_called_once()
        mock_db.insert.assert_called_once()
        email_service.send_email.assert_called_once()

    def test_full_login_flow(self):
        """Test complete registration followed by authentication."""
        database_store = {}

        class FakeDB:
            def query(self, sql_query):
                for record in database_store.values():
                    if record['email'] in sql_query:
                        return record
                return None

            def insert(self, table, data):
                new_id = len(database_store) + 1
                record = data.copy()
                record['id'] = new_id
                database_store[new_id] = record
                return new_id

            def update(self, table, record_id, updates):
                if record_id in database_store:
                    database_store[record_id].update(updates)

        fake_db = FakeDB()
        repo = UserRepository(fake_db)
        email_service = EmailService("fake-key")
        service = UserService(repo, email_service)

        registered = service.register_user("cacho@iteso.mx", "securePassword1", "Luis Cacho")
        assert registered['id'] == 1
        assert len(email_service.sent_emails) == 1

        logged_in = service.login("cacho@iteso.mx", "securePassword1")
        assert logged_in['id'] == registered['id']
        assert database_store[1]['last_login'] == "NOW()"
