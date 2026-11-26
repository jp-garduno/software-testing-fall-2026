class UserRepository:
    """Simulates a database layer for user operations."""

    def __init__(self, db_connection):
        """Initialize repository with database connection."""
        self.db = db_connection

    def find_by_email(self, email):
        """Find a user by email address."""
        result = self.db.query(f"SELECT * FROM users WHERE email = '{email}'")
        return result

    def create_user(self, user_data):
        """Create a new user in the database."""
        existing = self.find_by_email(user_data["email"])

        if existing:
            raise ValueError(f"User with email {user_data['email']} already exists")

        user_id = self.db.insert("users", user_data)
        user_data["id"] = user_id

        return user_data

    def update_last_login(self, user_id):
        """Update the last login timestamp for a user."""
        self.db.update(
            "users",
            user_id,
            {"last_login": "NOW()"},
        )
