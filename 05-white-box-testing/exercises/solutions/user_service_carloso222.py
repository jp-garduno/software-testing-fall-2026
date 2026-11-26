# pylint: disable=broad-exception-caught

import hashlib
from datetime import datetime


class UserService:
    """Business logic for user operations."""

    def __init__(self, user_repository, email_service):
        """Initialize service with dependencies."""
        self.user_repo = user_repository
        self.email_service = email_service

    def register_user(self, email, password, name):
        """Register a new user and send welcome email."""
        if not email or not password or not name:
            raise ValueError("Email, password, and name are required")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

        password_hash = self._hash_password(password)

        user_data = {
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "created_at": datetime.now().isoformat(),
        }

        user = self.user_repo.create_user(user_data)

        try:
            self.send_welcome_email(user)
        except Exception as exc:
            print(f"Warning: Could not send welcome email: {exc}")

        return user

    def login(self, email, password):
        """Authenticate user and update last login."""
        user = self.user_repo.find_by_email(email)

        if not user:
            raise ValueError("Invalid email or password")

        password_hash = self._hash_password(password)

        if user.get("password_hash") != password_hash:
            raise ValueError("Invalid email or password")

        self.user_repo.update_last_login(user["id"])

        return user

    def send_welcome_email(self, user):
        """Send welcome email to newly registered user."""
        subject = "Welcome to Our Service!"
        body = f"Hello {user['name']},\n\n" "Thank you for registering!"

        return self.email_service.send_email(
            user["email"],
            subject,
            body,
        )

    def get_user_by_id(self, user_id):
        """Retrieve user by ID."""
        raise NotImplementedError(f"User lookup by ID {user_id} is not implemented")

    def _hash_password(self, password):
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
