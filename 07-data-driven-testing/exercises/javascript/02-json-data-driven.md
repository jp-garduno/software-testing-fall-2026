# Exercise 2: JSON Data-Driven Testing (JavaScript)

## Objective

Learn to load test data from JSON files for data-driven testing in Jest.

## Part 1: Email Validation

**emailValidator.js**:

```javascript
function isValidEmail(email) {
  if (!email || email.includes(" ")) {
    return false;
  }

  const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return pattern.test(email);
}

module.exports = { isValidEmail };
```

**test-data/email-tests.json**:

```json
[
  {
    "email": "user@example.com",
    "valid": true,
    "reason": "Standard valid email"
  },
  {
    "email": "test.user@example.co.uk",
    "valid": true,
    "reason": "Multiple dots"
  },
  {
    "email": "invalid@",
    "valid": false,
    "reason": "Missing domain"
  },
  {
    "email": "@example.com",
    "valid": false,
    "reason": "Missing local part"
  },
  {
    "email": "",
    "valid": false,
    "reason": "Empty email"
  }
]
```

**emailValidator.test.js**:

```javascript
const { isValidEmail } = require("./emailValidator");
const testData = require("./test-data/email-tests.json");

test.each(testData)(
  "validates email: $email ($reason)",
  ({ email, valid, reason }) => {
    expect(isValidEmail(email)).toBe(valid);
  },
);
```

## Part 2: Product API

**productAPI.js**:

```javascript
class ProductAPI {
  constructor() {
    this.products = new Map();
    this.nextId = 1;
  }

  createProduct(name, price, category) {
    if (!name || price < 0) {
      return { status: 400, error: "Invalid input" };
    }

    const product = {
      id: this.nextId++,
      name,
      price,
      category,
    };

    this.products.set(product.id, product);
    return { status: 201, data: product };
  }

  getProduct(id) {
    if (!this.products.has(id)) {
      return { status: 404, error: "Product not found" };
    }
    return { status: 200, data: this.products.get(id) };
  }
}

module.exports = ProductAPI;
```

**test-data/product-api-tests.json**:

```json
{
  "createProductTests": [
    {
      "name": "create_valid_product",
      "input": {
        "name": "Laptop",
        "price": 999.99,
        "category": "Electronics"
      },
      "expected": {
        "status": 201,
        "dataContains": {
          "name": "Laptop",
          "price": 999.99
        }
      }
    },
    {
      "name": "create_product_negative_price",
      "input": {
        "name": "Item",
        "price": -10,
        "category": "Test"
      },
      "expected": {
        "status": 400,
        "error": "Invalid input"
      }
    }
  ]
}
```

**productAPI.test.js**:

```javascript
const ProductAPI = require("./productAPI");
const testData = require("./test-data/product-api-tests.json");

describe.each(testData.createProductTests)(
  "ProductAPI.createProduct: $name",
  ({ input, expected }) => {
    test("returns correct response", () => {
      const api = new ProductAPI();
      const result = api.createProduct(input.name, input.price, input.category);

      expect(result.status).toBe(expected.status);

      if (expected.dataContains) {
        for (const [key, value] of Object.entries(expected.dataContains)) {
          expect(result.data[key]).toBe(value);
        }
      }

      if (expected.error) {
        expect(result.error).toBe(expected.error);
      }
    });
  },
);
```

## Part 3: Validation Rules

Create JSON with validation rules and test them dynamically.

**test-data/validation-rules.json**:

```json
{
  "passwordRules": {
    "minLength": 8,
    "requireUppercase": true,
    "requireLowercase": true,
    "requireNumber": true,
    "testCases": [
      { "input": "Password123", "expected": true },
      { "input": "pass", "expected": false },
      { "input": "password123", "expected": false }
    ]
  }
}
```

## Requirements

1. Create at least 3 different validation modules
2. Each with JSON test data (10+ cases)
3. Test success and failure scenarios
4. Use descriptive test names

## Expected Output

```bash
$ npm test

 PASS  ./emailValidator.test.js
  ✓ validates email: user@example.com (Standard valid email)
  ✓ validates email: invalid@ (Missing domain)
  ...

 PASS  ./productAPI.test.js
  ProductAPI.createProduct: create_valid_product
    ✓ returns correct response
  ProductAPI.createProduct: create_product_negative_price
    ✓ returns correct response

Test Suites: 2 passed, 2 total
Tests:       15 passed, 15 total
```

## Grading

- Implementation: 35%
- JSON test data: 30%
- Test coverage: 25%
- Code quality: 10%
