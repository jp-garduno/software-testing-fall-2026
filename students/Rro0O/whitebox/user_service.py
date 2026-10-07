"""Business logic layer for user operations."""

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
            ConnectionError: If database fails
        """
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

        # Welcome email is non-blocking: log the error but don't fail registration
        try:
            self.send_welcome_email(user)
        except Exception as e:  # pylint: disable=broad-except
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
        user = self.user_repo.find_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        password_hash = self._hash_password(password)
        if user.get("password_hash") != password_hash:
            raise ValueError("Invalid email or password")

        self.user_repo.update_last_login(user["id"])

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

        return self.email_service.send_email(user["email"], subject, body)

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
        raise NotImplementedError("To be implemented")

    def _hash_password(self, password):
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
