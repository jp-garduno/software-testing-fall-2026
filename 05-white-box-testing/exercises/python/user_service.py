"""Business logic that coordinates users and welcome emails."""

import hashlib
from datetime import datetime


class UserService:
    """Business logic for user operations and service coordination."""

    def __init__(self, user_repository, email_service):
        """Initialize the service with repository and email dependencies."""
        self.user_repo = user_repository
        self.email_service = email_service

    def register_user(self, email, password, name):
        """Register a user and attempt to send a non-blocking welcome message."""
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
        except Exception as error:
            print(f"Warning: Could not send welcome email: {error}")

        return user

    def login(self, email, password):
        """Authenticate a user and update their most recent login timestamp."""
        user = self.user_repo.find_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        if user.get("password_hash") != self._hash_password(password):
            raise ValueError("Invalid email or password")

        self.user_repo.update_last_login(user["id"])
        return user

    def send_welcome_email(self, user):
        """Send a welcome email to the user."""
        subject = "Welcome to Our Service!"
        body = f"Hello {user['name']},\n\nThank you for registering!"
        return self.email_service.send_email(user["email"], subject, body)

    def get_user_by_id(self, user_id):
        """Retrieve a user by ID (not provided by this exercise's repository)."""
        raise NotImplementedError("To be implemented")

    def _hash_password(self, password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
