"""Database access layer for user operations."""


class UserRepository:
    """Simulates a database layer for user operations."""

    def __init__(self, db_connection):
        """Initialize the repository with a database connection."""
        self.db = db_connection

    def find_by_email(self, email):
        """Return the user found for ``email``, or ``None`` when absent."""
        return self.db.query(f"SELECT * FROM users WHERE email = '{email}'")

    def create_user(self, user_data):
        """Create a user unless another user already has its email address."""
        existing = self.find_by_email(user_data["email"])
        if existing:
            raise ValueError(f"User with email {user_data['email']} already exists")

        user_id = self.db.insert("users", user_data)
        user_data["id"] = user_id
        return user_data

    def update_last_login(self, user_id):
        """Record the current time as a user's most recent login."""
        self.db.update("users", user_id, {"last_login": "NOW()"})
