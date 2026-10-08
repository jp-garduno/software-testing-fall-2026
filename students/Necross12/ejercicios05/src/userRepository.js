class UserRepository {
  /**
   * Simulates a database layer for user operations.
   * @param {Object} dbConnection - Database connection object
   */
  constructor(dbConnection) {
    this.db = dbConnection;
  }

  /**
   * Find a user by email address.
   * @param {string} email - User email address
   * @returns {Object|null} User object if found, null otherwise
   * @throws {Error} If database connection fails
   */
  findByEmail(email) {
    // Simulate database query
    const result = this.db.query(
      `SELECT * FROM users WHERE email = '${email}'`,
    );
    return result;
  }

  /**
   * Create a new user in the database.
   * @param {Object} userData - User information
   * @returns {Object} Created user with ID
   * @throws {Error} If user already exists or database fails
   */
  createUser(userData) {
    // Check if user exists
    const existing = this.findByEmail(userData.email);
    if (existing) {
      throw new Error(`User with email ${userData.email} already exists`);
    }

    // Insert user
    const userId = this.db.insert("users", userData);
    return { ...userData, id: userId };
  }

  /**
   * Update the last login timestamp for a user.
   * @param {number} userId - User ID
   * @throws {Error} If database connection fails
   */
  updateLastLogin(userId) {
    this.db.update("users", userId, { last_login: "NOW()" });
  }
}

module.exports = UserRepository;
