"""Reference solution for Exercise 3: User Service (Module 05 - White Box Testing) - database layer."""


class UserRepository:
    """Simulates a database layer for user operations."""

    def __init__(self, db_connection):
        """
        Initialize repository with database connection.

        Args:
            db_connection: Database connection object
        """
        self.db = db_connection

    def find_by_email(self, email):
        """
        Find a user by email address.

        Args:
            email: User email address

        Returns:
            User dict if found, None otherwise

        Raises:
            ConnectionError: If database connection fails
        """
        # Simulate database query
        result = self.db.query(f"SELECT * FROM users WHERE email = '{email}'")
        return result

    def create_user(self, user_data):
        """
        Create a new user in the database.

        Args:
            user_data: Dictionary with user information

        Returns:
            Created user with ID

        Raises:
            ValueError: If user already exists
            ConnectionError: If database connection fails
        """
        # Check if user exists
        existing = self.find_by_email(user_data["email"])
        if existing:
            raise ValueError(f"User with email {user_data['email']} already exists")

        # Insert user
        user_id = self.db.insert("users", user_data)
        user_data["id"] = user_id
        return user_data

    def update_last_login(self, user_id):
        """
        Update the last login timestamp for a user.

        Args:
            user_id: User ID

        Raises:
            ConnectionError: If database connection fails
        """
        self.db.update("users", user_id, {"last_login": "NOW()"})
