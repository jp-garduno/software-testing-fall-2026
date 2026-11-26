const UserService = require("../src/userService");
const UserRepository = require("../src/userRepository");

describe("UserService", () => {
  let mockRepo;
  let mockEmail;
  let service;

  beforeEach(() => {
    mockRepo = {
      findByEmail: jest.fn(),
      createUser: jest.fn(),
      updateLastLogin: jest.fn(),
    };

    mockEmail = {
      sendEmail: jest.fn(),
    };

    service = new UserService(mockRepo, mockEmail);
  });

  describe("registerUser", () => {
    test("should register user successfully", () => {
      mockRepo.createUser.mockReturnValue({
        id: 1,
        email: "test@example.com",
        name: "Test User",
        password_hash: "hashed_password",
      });
      mockEmail.sendEmail.mockReturnValue(true);

      const user = service.registerUser(
        "test@example.com",
        "password123",
        "Test User",
      );

      expect(user.email).toBe("test@example.com");
      expect(user.name).toBe("Test User");
      expect(mockRepo.createUser).toHaveBeenCalledTimes(1);
      expect(mockEmail.sendEmail).toHaveBeenCalledTimes(1);
      const emailCall = mockEmail.sendEmail.mock.calls[0];
      expect(emailCall[0]).toBe("test@example.com");
      expect(emailCall[1]).toContain("Welcome");
    });

    test("should throw error for short password", () => {
      expect(() =>
        service.registerUser("test@example.com", "short", "Test User"),
      ).toThrow(Error);

      expect(mockRepo.createUser).not.toHaveBeenCalled();
      expect(mockEmail.sendEmail).not.toHaveBeenCalled();
    });

    test("should throw error for missing email", () => {
      expect(() =>
        service.registerUser("", "password123", "Test User"),
      ).toThrow(Error);
      expect(() =>
        service.registerUser(null, "password123", "Test User"),
      ).toThrow(Error);

      expect(mockRepo.createUser).not.toHaveBeenCalled();
    });

    test("should throw error for missing password", () => {
      expect(() =>
        service.registerUser("test@example.com", "", "Test User"),
      ).toThrow(Error);
      expect(() =>
        service.registerUser("test@example.com", null, "Test User"),
      ).toThrow(Error);

      expect(mockRepo.createUser).not.toHaveBeenCalled();
    });

    test("should throw error for missing name", () => {
      expect(() =>
        service.registerUser("test@example.com", "password123", ""),
      ).toThrow(Error);
      expect(() =>
        service.registerUser("test@example.com", "password123", null),
      ).toThrow(Error);

      expect(mockRepo.createUser).not.toHaveBeenCalled();
    });

    test("should throw error for duplicate email", () => {
      mockRepo.createUser.mockImplementation(() => {
        throw new Error("Email already exists");
      });

      expect(() =>
        service.registerUser("test@example.com", "password123", "Test User"),
      ).toThrow("Email already exists");

      expect(mockEmail.sendEmail).not.toHaveBeenCalled();
    });

    test("should not fail registration if email fails", () => {
      mockRepo.createUser.mockReturnValue({
        id: 1,
        email: "test@example.com",
        name: "Test User",
        password_hash: "hashed_password",
      });
      mockEmail.sendEmail.mockImplementation(() => {
        throw new Error("SMTP unavailable");
      });

      let user;
      expect(() => {
        user = service.registerUser(
          "test@example.com",
          "password123",
          "Test User",
        );
      }).not.toThrow();

      expect(user.email).toBe("test@example.com");
      expect(mockRepo.createUser).toHaveBeenCalledTimes(1);
      expect(mockEmail.sendEmail).toHaveBeenCalledTimes(1);
    });

    test("should throw error if database fails", () => {
      mockRepo.createUser.mockImplementation(() => {
        throw new Error("Database connection failed");
      });

      expect(() =>
        service.registerUser("test@example.com", "password123", "Test User"),
      ).toThrow("Database connection failed");

      expect(mockEmail.sendEmail).not.toHaveBeenCalled();
    });
  });

  describe("login", () => {
    test("should login successfully", () => {
      const mockUser = {
        id: 1,
        email: "test@example.com",
        password_hash: service._hashPassword("password123"),
        name: "Test User",
      };
      mockRepo.findByEmail.mockReturnValue(mockUser);

      const user = service.login("test@example.com", "password123");

      expect(user.email).toBe("test@example.com");
      expect(mockRepo.findByEmail).toHaveBeenCalledWith("test@example.com");
      expect(mockRepo.updateLastLogin).toHaveBeenCalledWith(1);
    });

    test("should throw error for non-existent email", () => {
      mockRepo.findByEmail.mockReturnValue(null);

      expect(() =>
        service.login("nobody@example.com", "password123"),
      ).toThrow(Error);

      expect(mockRepo.findByEmail).toHaveBeenCalledWith("nobody@example.com");
      expect(mockRepo.updateLastLogin).not.toHaveBeenCalled();
    });

    test("should throw error for incorrect password", () => {
      mockRepo.findByEmail.mockReturnValue({
        id: 1,
        email: "test@example.com",
        password_hash: service._hashPassword("a_different_password"),
        name: "Test User",
      });

      expect(() =>
        service.login("test@example.com", "password123"),
      ).toThrow(Error);

      expect(mockRepo.updateLastLogin).not.toHaveBeenCalled();
    });

    test("should throw error if database fails", () => {
      mockRepo.findByEmail.mockImplementation(() => {
        throw new Error("Database connection failed");
      });

      expect(() =>
        service.login("test@example.com", "password123"),
      ).toThrow("Database connection failed");

      expect(mockRepo.updateLastLogin).not.toHaveBeenCalled();
    });
  });

  describe("sendWelcomeEmail", () => {
    test("should send welcome email successfully", () => {
      mockEmail.sendEmail.mockReturnValue(true);

      service.sendWelcomeEmail({ email: "test@example.com", name: "Test User" });

      expect(mockEmail.sendEmail).toHaveBeenCalledTimes(1);
      const call = mockEmail.sendEmail.mock.calls[0];
      expect(call[0]).toBe("test@example.com");
      expect(call[1]).toContain("Welcome");
    });

    test("should throw error for invalid email address", () => {
      mockEmail.sendEmail.mockImplementation(() => {
        throw new Error("Invalid email address");
      });

      expect(() =>
        service.sendWelcomeEmail({ email: "not-an-email", name: "Test User" }),
      ).toThrow(Error);
    });

    test("should throw error if email API fails", () => {
      mockEmail.sendEmail.mockImplementation(() => {
        throw new Error("Email API unavailable");
      });

      expect(() =>
        service.sendWelcomeEmail({ email: "test@example.com", name: "Test User" }),
      ).toThrow("Email API unavailable");
    });
  });
});

describe("UserService Integration Tests", () => {
  test("should complete full registration flow", () => {
    // Only mock the actual external services (DB and Email API)
    const mockDb = {
      query: jest.fn().mockReturnValue(null), // User doesn't exist
      insert: jest.fn().mockReturnValue(1), // New user ID
      update: jest.fn(),
    };

    const mockEmailApi = {
      sendEmail: jest.fn().mockReturnValue(true),
    };

    const repo = new UserRepository(mockDb);
    const emailService = { sendEmail: mockEmailApi.sendEmail };
    const service = new UserService(repo, emailService);

    // Register user
    const user = service.registerUser(
      "new@example.com",
      "password123",
      "New User",
    );

    // Verify complete flow
    expect(user.id).toBe(1);
    expect(user.email).toBe("new@example.com");
    expect(mockDb.query).toHaveBeenCalled();
    expect(mockDb.insert).toHaveBeenCalled();
    expect(mockEmailApi.sendEmail).toHaveBeenCalled();
  });

  test("should complete full login flow", () => {
    const mockDb = {
      query: jest.fn().mockReturnValue(null),
      insert: jest.fn().mockReturnValue(1),
      update: jest.fn(),
    };
    const mockEmailApi = {
      sendEmail: jest.fn().mockReturnValue(true),
    };

    const repo = new UserRepository(mockDb);
    const service = new UserService(repo, {
      sendEmail: mockEmailApi.sendEmail,
    });

    // Step 1: register
    const registered = service.registerUser(
      "new@example.com",
      "password123",
      "New User",
    );
    expect(registered.id).toBe(1);

    // Step 2: the DB now "contains" the registered user
    mockDb.query.mockReturnValue({
      id: 1,
      email: "new@example.com",
      name: "New User",
      password_hash: service._hashPassword("password123"),
    });

    // Step 3: login with the same credentials
    const loggedIn = service.login("new@example.com", "password123");

    expect(loggedIn.id).toBe(1);
    expect(loggedIn.email).toBe("new@example.com");
    expect(mockDb.update).toHaveBeenCalled();

    // Wrong password must fail against the same stored user
    expect(() => service.login("new@example.com", "wrong_password")).toThrow(
      Error,
    );
  });

  test("should handle database error during registration", () => {
    const mockDb = {
      query: jest.fn().mockReturnValue(null),
      insert: jest.fn().mockImplementation(() => {
        throw new Error("Database connection failed");
      }),
      update: jest.fn(),
    };
    const mockEmailApi = {
      sendEmail: jest.fn().mockReturnValue(true),
    };

    const repo = new UserRepository(mockDb);
    const service = new UserService(repo, {
      sendEmail: mockEmailApi.sendEmail,
    });

    expect(() =>
      service.registerUser("new@example.com", "password123", "New User"),
    ).toThrow("Database connection failed");

    // No welcome email should go out if the user was not saved
    expect(mockEmailApi.sendEmail).not.toHaveBeenCalled();
  });
});

// Covers userService.js line 105 (getUserById stub)
describe("UserService.getUserById", () => {
  test("should throw 'Not implemented'", () => {
    const service = new UserService({}, {});

    expect(() => service.getUserById(1)).toThrow("Not implemented");
  });
});

// Covers userRepository.js line 34 (duplicate email branch)
describe("UserRepository", () => {
  let mockDb;
  let repo;

  beforeEach(() => {
    mockDb = {
      query: jest.fn(),
      insert: jest.fn(),
      update: jest.fn(),
    };
    repo = new UserRepository(mockDb);
  });

  test("should throw error when creating a user with an existing email", () => {
    mockDb.query.mockReturnValue({ id: 5, email: "dup@example.com" });

    expect(() =>
      repo.createUser({ email: "dup@example.com", name: "Dup" }),
    ).toThrow("User with email dup@example.com already exists");

    expect(mockDb.insert).not.toHaveBeenCalled();
  });

  test("should create user and return it with the new ID", () => {
    mockDb.query.mockReturnValue(null);
    mockDb.insert.mockReturnValue(7);

    const user = repo.createUser({ email: "new@example.com", name: "New" });

    expect(user).toEqual({ email: "new@example.com", name: "New", id: 7 });
    expect(mockDb.insert).toHaveBeenCalledWith("users", {
      email: "new@example.com",
      name: "New",
    });
  });

  test("should update last login via the database", () => {
    repo.updateLastLogin(3);

    expect(mockDb.update).toHaveBeenCalledWith("users", 3, {
      last_login: "NOW()",
    });
  });
});

describe("UserService duplicate registration (integration)", () => {
  test("should reject duplicate email and not send welcome email", () => {
    const mockDb = {
      query: jest.fn().mockReturnValue({ id: 1, email: "dup@example.com" }),
      insert: jest.fn(),
      update: jest.fn(),
    };
    const sendEmail = jest.fn();
    const service = new UserService(new UserRepository(mockDb), { sendEmail });

    expect(() =>
      service.registerUser("dup@example.com", "password123", "Dup User"),
    ).toThrow("already exists");

    expect(mockDb.insert).not.toHaveBeenCalled();
    expect(sendEmail).not.toHaveBeenCalled();
  });
});
