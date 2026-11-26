import hashlib
from datetime import datetime


class UserService:
    """Business logic coordinating repository and external services."""

    def __init__(self, user_repository, email_service):
        """Initialize service dependencies."""
        self.user_repo = user_repository
        self.email_service = email_service

    def register_user(self, email, password, name):
        """Create a user and attempt to send a non-blocking welcome email."""
        if not email or not password or not name:
            raise ValueError("Email, password, and name are required")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

        user_data = {
            "email": email,
            "password_hash": self._hash_password(password),
            "name": name,
            "created_at": datetime.now().isoformat(),
        }
        user = self.user_repo.create_user(user_data)

        try:
            self.send_welcome_email(user)
        except (ConnectionError, ValueError) as e:
            print(f"Warning: Could not send welcome email: {e}")

        return user

    def login(self, email, password):
        """Authenticate a user and update their last login."""
        user = self.user_repo.find_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        password_hash = self._hash_password(password)
        if user.get("password_hash") != password_hash:
            raise ValueError("Invalid email or password")

        self.user_repo.update_last_login(user["id"])
        return user

    def send_welcome_email(self, user):
        """Send a welcome email for a newly registered user."""
        subject = "Welcome to Our Service!"
        body = f"Hello {user['name']},\n\nThank you for registering!"

        return self.email_service.send_email(user["email"], subject, body)

    def get_user_by_id(self, user_id):
        """Return a user by ID or raise ValueError if it does not exist."""
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    def _hash_password(self, password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
