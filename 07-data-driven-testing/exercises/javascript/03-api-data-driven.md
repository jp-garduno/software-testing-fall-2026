# Exercise 3: API Data-Driven Testing (JavaScript)

## Objective

Apply data-driven testing to REST API testing with complex scenarios.

## Scenario: RESTful API Testing

Test a complete REST API with various endpoints using data-driven approach.

## Setup

**Install dependencies**:

```bash
npm install --save-dev supertest express
```

**api-server.js**:

```javascript
const express = require("express");
const app = express();

app.use(express.json());

// In-memory database
const users = new Map();
let userId = 1;

app.post("/api/users", (req, res) => {
  const { username, email, age } = req.body;

  if (!username || !email) {
    return res.status(400).json({ error: "Missing required fields" });
  }

  if (age && (age < 13 || age > 120)) {
    return res.status(400).json({ error: "Invalid age" });
  }

  const user = { id: userId++, username, email, age };
  users.set(user.id, user);

  res.status(201).json(user);
});

app.get("/api/users/:id", (req, res) => {
  const id = parseInt(req.params.id);
  const user = users.get(id);

  if (!user) {
    return res.status(404).json({ error: "User not found" });
  }

  res.status(200).json(user);
});

app.put("/api/users/:id", (req, res) => {
  const id = parseInt(req.params.id);
  const user = users.get(id);

  if (!user) {
    return res.status(404).json({ error: "User not found" });
  }

  Object.assign(user, req.body);
  res.status(200).json(user);
});

app.delete("/api/users/:id", (req, res) => {
  const id = parseInt(req.params.id);

  if (!users.has(id)) {
    return res.status(404).json({ error: "User not found" });
  }

  users.delete(id);
  res.status(200).json({ message: "User deleted" });
});

module.exports = app;
```

## Part 1: CRUD Operations Testing

**test-data/user-api-tests.json**:

```json
{
  "createUserTests": [
    {
      "name": "create_user_success",
      "method": "POST",
      "endpoint": "/api/users",
      "body": {
        "username": "alice",
        "email": "alice@example.com",
        "age": 25
      },
      "expected": {
        "status": 201,
        "hasKeys": ["id", "username", "email", "age"],
        "matches": {
          "username": "alice",
          "email": "alice@example.com"
        }
      }
    },
    {
      "name": "create_user_missing_username",
      "method": "POST",
      "endpoint": "/api/users",
      "body": {
        "email": "test@example.com"
      },
      "expected": {
        "status": 400,
        "error": "Missing required fields"
      }
    },
    {
      "name": "create_user_invalid_age",
      "method": "POST",
      "endpoint": "/api/users",
      "body": {
        "username": "younguser",
        "email": "young@example.com",
        "age": 10
      },
      "expected": {
        "status": 400,
        "error": "Invalid age"
      }
    }
  ],
  "getUserTests": [
    {
      "name": "get_existing_user",
      "setup": {
        "createUser": {
          "username": "bob",
          "email": "bob@example.com",
          "age": 30
        }
      },
      "method": "GET",
      "endpoint": "/api/users/1",
      "expected": {
        "status": 200,
        "matches": {
          "username": "bob"
        }
      }
    },
    {
      "name": "get_nonexistent_user",
      "method": "GET",
      "endpoint": "/api/users/999",
      "expected": {
        "status": 404,
        "error": "User not found"
      }
    }
  ],
  "updateUserTests": [
    {
      "name": "update_user_success",
      "setup": {
        "createUser": {
          "username": "charlie",
          "email": "charlie@example.com",
          "age": 35
        }
      },
      "method": "PUT",
      "endpoint": "/api/users/1",
      "body": {
        "age": 36
      },
      "expected": {
        "status": 200,
        "matches": {
          "age": 36
        }
      }
    }
  ],
  "deleteUserTests": [
    {
      "name": "delete_user_success",
      "setup": {
        "createUser": {
          "username": "david",
          "email": "david@example.com"
        }
      },
      "method": "DELETE",
      "endpoint": "/api/users/1",
      "expected": {
        "status": 200,
        "message": "User deleted"
      }
    }
  ]
}
```

**api-server.test.js**:

```javascript
const request = require("supertest");
const app = require("./api-server");
const testData = require("./test-data/user-api-tests.json");

describe("User API - Create User", () => {
  test.each(testData.createUserTests)(
    "$name",
    async ({ method, endpoint, body, expected }) => {
      const response = await request(app).post(endpoint).send(body);

      expect(response.status).toBe(expected.status);

      if (expected.hasKeys) {
        expected.hasKeys.forEach((key) => {
          expect(response.body).toHaveProperty(key);
        });
      }

      if (expected.matches) {
        for (const [key, value] of Object.entries(expected.matches)) {
          expect(response.body[key]).toBe(value);
        }
      }

      if (expected.error) {
        expect(response.body.error).toBe(expected.error);
      }
    },
  );
});

describe("User API - Get User", () => {
  test.each(testData.getUserTests)(
    "$name",
    async ({ setup, method, endpoint, expected }) => {
      // Setup: Create user if needed
      if (setup && setup.createUser) {
        await request(app).post("/api/users").send(setup.createUser);
      }

      // Execute test
      const response = await request(app).get(endpoint);

      expect(response.status).toBe(expected.status);

      if (expected.matches) {
        for (const [key, value] of Object.entries(expected.matches)) {
          expect(response.body[key]).toBe(value);
        }
      }

      if (expected.error) {
        expect(response.body.error).toBe(expected.error);
      }
    },
  );
});

// TODO: Implement tests for updateUserTests and deleteUserTests
```

## Part 2: Authentication API Testing

**test-data/auth-api-tests.json**:

```json
{
  "loginTests": [
    {
      "name": "login_success",
      "credentials": {
        "username": "admin",
        "password": "admin123"
      },
      "expected": {
        "status": 200,
        "hasKeys": ["token", "userId"],
        "tokenPattern": "^[A-Za-z0-9-_]+\\.[A-Za-z0-9-_]+\\.[A-Za-z0-9-_]+$"
      }
    },
    {
      "name": "login_invalid_password",
      "credentials": {
        "username": "admin",
        "password": "wrongpass"
      },
      "expected": {
        "status": 401,
        "error": "Invalid credentials"
      }
    },
    {
      "name": "login_missing_username",
      "credentials": {
        "password": "admin123"
      },
      "expected": {
        "status": 400,
        "error": "Missing username"
      }
    }
  ],
  "protectedEndpointTests": [
    {
      "name": "access_with_valid_token",
      "endpoint": "/api/profile",
      "headers": {
        "Authorization": "Bearer valid_token"
      },
      "expected": {
        "status": 200
      }
    },
    {
      "name": "access_without_token",
      "endpoint": "/api/profile",
      "expected": {
        "status": 401,
        "error": "Authentication required"
      }
    }
  ]
}
```

## Part 3: Complex Scenarios

**test-data/complex-scenarios.json**:

```json
{
  "userWorkflowTests": [
    {
      "name": "complete_user_lifecycle",
      "steps": [
        {
          "description": "Create user",
          "method": "POST",
          "endpoint": "/api/users",
          "body": {
            "username": "testuser",
            "email": "test@example.com",
            "age": 25
          },
          "expected": {
            "status": 201
          }
        },
        {
          "description": "Get created user",
          "method": "GET",
          "endpoint": "/api/users/1",
          "expected": {
            "status": 200,
            "matches": {
              "username": "testuser"
            }
          }
        },
        {
          "description": "Update user",
          "method": "PUT",
          "endpoint": "/api/users/1",
          "body": {
            "age": 26
          },
          "expected": {
            "status": 200,
            "matches": {
              "age": 26
            }
          }
        },
        {
          "description": "Delete user",
          "method": "DELETE",
          "endpoint": "/api/users/1",
          "expected": {
            "status": 200
          }
        },
        {
          "description": "Verify user deleted",
          "method": "GET",
          "endpoint": "/api/users/1",
          "expected": {
            "status": 404
          }
        }
      ]
    }
  ]
}
```

**workflow.test.js**:

```javascript
const request = require("supertest");
const app = require("./api-server");
const testData = require("./test-data/complex-scenarios.json");

describe("User Workflows", () => {
  test.each(testData.userWorkflowTests)("$name", async ({ steps }) => {
    for (const step of steps) {
      const req = request(app)[step.method.toLowerCase()](step.endpoint);

      if (step.body) {
        req.send(step.body);
      }

      if (step.headers) {
        for (const [key, value] of Object.entries(step.headers)) {
          req.set(key, value);
        }
      }

      const response = await req;

      expect(response.status).toBe(step.expected.status);

      if (step.expected.matches) {
        for (const [key, value] of Object.entries(step.expected.matches)) {
          expect(response.body[key]).toBe(value);
        }
      }
    }
  });
});
```

## Requirements

1. Implement all CRUD endpoints
2. Create comprehensive test data (25+ test cases)
3. Test success and error scenarios
4. Implement workflow tests (multi-step)
5. Test authentication if implementing auth
6. Clean database between tests

## Tips

1. Use `beforeEach()` to reset state
2. Use `supertest` for API testing
3. Test both happy path and edge cases
4. Validate response structure
5. Test error messages

## Expected Output

```bash
$ npm test

 PASS  ./api-server.test.js
  User API - Create User
    ✓ create_user_success (45ms)
    ✓ create_user_missing_username (12ms)
    ✓ create_user_invalid_age (10ms)
  User API - Get User
    ✓ get_existing_user (15ms)
    ✓ get_nonexistent_user (8ms)
  ...

Test Suites: 1 passed, 1 total
Tests:       15 passed, 15 total
```

## Submission

Submit:

- `api-server.js`
- All test files
- All JSON test data files
- `package.json` with dependencies
- README with API documentation
- Screenshot of passing tests

## Grading Criteria

- API implementation: 25%
- Test data quality: 30%
- Test implementation: 30%
- Code quality: 10%
- Documentation: 5%
