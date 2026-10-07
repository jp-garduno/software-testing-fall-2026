const crypto = require("crypto");

class UserService {
  /**
   * Business logic for user operations.
   * Coordinates between repository and external services.
   * @param {UserRepository} userRepository - Repository instance
   * @param {EmailService} emailService - Email service instance
   */
  constructor(userRepository, emailService) {
    this.userRepo = userRepository;
    this.emailService = emailService;
  }

  /**
   * Register a new user and send welcome email.
   * @param {string} email - User email address
   * @param {string} password - User password (will be hashed)
   * @param {string} name - User full name
   * @returns {Object} Created user object
   * @throws {Error} If email already exists or invalid input
   */
  registerUser(email, password, name) {
    // Validate input
    if (!email || !password || !name) {
      throw new Error("Email, password, and name are required");
    }

    if (password.length < 8) {
      throw new Error("Password must be at least 8 characters");
    }

    // Hash password
    const passwordHash = this._hashPassword(password);

    // Create user in database
    const userData = {
      email: email,
      password_hash: passwordHash,
      name: name,
      created_at: new Date().toISOString(),
    };

    const user = this.userRepo.createUser(userData);

    // Send welcome email (non-blocking)
    try {
      this.sendWelcomeEmail(user);
    } catch (error) {
      // Log error but don't fail registration
      console.log(`Warning: Could not send welcome email: ${error}`);
    }

    return user;
  }

  /**
   * Authenticate user and update last login.
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Object} User object if authentication successful
   * @throws {Error} If credentials are invalid or database fails
   */
  login(email, password) {
    // Find user
    const user = this.userRepo.findByEmail(email);
    if (!user) {
      throw new Error("Invalid email or password");
    }

    // Verify password
    const passwordHash = this._hashPassword(password);
    if (user.password_hash !== passwordHash) {
      throw new Error("Invalid email or password");
    }

    // Update last login
    this.userRepo.updateLastLogin(user.id);

    return user;
  }

  /**
   * Send welcome email to newly registered user.
   * @param {Object} user - User object with email and name
   * @returns {boolean} True if email sent successfully
   * @throws {Error} If email service fails or email is invalid
   */
  sendWelcomeEmail(user) {
    const subject = "Welcome to Our Service!";
    const body = `Hello ${user.name},\n\nThank you for registering!`;

    return this.emailService.sendEmail(user.email, subject, body);
  }

  /**
   * Retrieve user by ID.
   * @param {number} userId - User ID
   * @returns {Object} User object if found
   * @throws {Error} If user not found or database fails
   */
  getUserById(userId) {
    // This would typically call userRepo.findById()
    // Simplified for this exercise
    throw new Error("Not implemented");
  }

  /**
   * Hash password using SHA-256.
   * @private
   */
  _hashPassword(password) {
    return crypto.createHash("sha256").update(password).digest("hex");
  }
}

module.exports = UserService;
