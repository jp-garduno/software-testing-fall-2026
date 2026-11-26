class UserRepository:
    """Simulates a database layer for user operations."""

    def __init__(self, db_connection):
        """Initialize the repository with a database connection."""
        self.db = db_connection

    def find_by_email(self, email):
        """Return a user matching the email, or None when no user exists."""
        return self.db.query(f"SELECT * FROM users WHERE email = '{email}'")

    def find_by_id(self, user_id):
        """Return a user matching the ID, or None when no user exists."""
        return self.db.query(f"SELECT * FROM users WHERE id = '{user_id}'")

    def create_user(self, user_data):
        """Insert a user and return its data with the generated ID."""
        existing = self.find_by_email(user_data["email"])
        if existing:
            raise ValueError(f"User with email {user_data['email']} already exists")

        user_id = self.db.insert("users", user_data)
        user_data["id"] = user_id
        return user_data

    def update_last_login(self, user_id):
        """Update the last login timestamp for a user."""
        self.db.update("users", user_id, {"last_login": "NOW()"})
