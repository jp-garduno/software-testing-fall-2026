# Exercise 4: CSV Data-Driven Testing (JavaScript)

## Objective

Learn to load test data from CSV files and use it in Jest data-driven tests.

## Setup

Install CSV parsing library:

```bash
npm install --save-dev csv-parse
```

## Scenario: User Registration Validation

Test a user registration system using test data stored in CSV files.

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

**test-data/emails.csv**:

```csv
email,valid,reason
user@example.com,true,Standard valid email
test.user@example.co.uk,true,Multiple dots in domain
user+tag@example.com,true,Plus sign in local part
invalid@,false,Missing domain
@example.com,false,Missing local part
user@example,false,Missing TLD
user example@test.com,false,Space in email
,false,Empty email
```

**emailValidator.test.js**:

```javascript
const { isValidEmail } = require("./emailValidator");
const fs = require("fs");
const { parse } = require("csv-parse/sync");

// Load CSV test data
function loadEmailTestData() {
  const csvData = fs.readFileSync("test-data/emails.csv", "utf8");
  const records = parse(csvData, { columns: true });

  return records.map((row) => ({
    email: row.email,
    valid: row.valid === "true",
    reason: row.reason,
  }));
}

const emailTests = loadEmailTestData();

test.each(emailTests)(
  "validates email: $email ($reason)",
  ({ email, valid, reason }) => {
    expect(isValidEmail(email)).toBe(valid);
  },
);
```

## Part 2: Password Strength Validation

**passwordValidator.js**:

```javascript
function checkPasswordStrength(password) {
  if (password.length < 8) {
    return "weak";
  }

  const hasLetter = /[a-zA-Z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  const hasSpecial = /[^a-zA-Z0-9]/.test(password);

  if (password.length >= 12 && hasLetter && hasNumber && hasSpecial) {
    return "strong";
  } else if (hasLetter && hasNumber) {
    return "medium";
  } else {
    return "weak";
  }
}

module.exports = { checkPasswordStrength };
```

**test-data/passwords.csv**:

```csv
password,strength,reason
abc,weak,Too short
password123,medium,8+ chars with letters and numbers
P@ssw0rd!2023,strong,12+ chars with all character types
12345678,weak,Only numbers
abcdefgh,weak,Only letters
Pass1234,medium,Exactly 8 chars with letters and numbers
MyP@ssw0rd123!,strong,Long with all types
VeryLongPassword123!@#,strong,Very long with all types
Pass,weak,Too short
Pass@,weak,Too short even with special
password,weak,No numbers or special chars
Password,weak,No numbers or special chars
```

**passwordValidator.test.js**:

```javascript
const { checkPasswordStrength } = require("./passwordValidator");
const fs = require("fs");
const { parse } = require("csv-parse/sync");

function loadPasswordTestData() {
  const csvData = fs.readFileSync("test-data/passwords.csv", "utf8");
  const records = parse(csvData, { columns: true });
  return records;
}

const passwordTests = loadPasswordTestData();

test.each(passwordTests)(
  "password strength: $password -> $strength ($reason)",
  ({ password, strength, reason }) => {
    expect(checkPasswordStrength(password)).toBe(strength);
  },
);
```

## Part 3: User Registration Validation

**userValidator.js**:

```javascript
function validateUserRegistration(username, email, age, country) {
  const errors = [];

  // Username validation
  if (!username || username.length < 3 || username.length > 20) {
    errors.push("Username must be 3-20 characters");
  } else if (!/^[a-zA-Z0-9]+$/.test(username)) {
    errors.push("Username must be alphanumeric");
  }

  // Email validation
  if (!email || !email.includes("@")) {
    errors.push("Invalid email format");
  }

  // Age validation
  const ageNum = parseInt(age);
  if (isNaN(ageNum) || ageNum < 13 || ageNum > 120) {
    errors.push("Age must be between 13 and 120");
  }

  // Country validation
  if (!country || country.length !== 2 || country !== country.toUpperCase()) {
    errors.push("Country must be 2-letter code (uppercase)");
  }

  return {
    isValid: errors.length === 0,
    errors: errors,
  };
}

module.exports = { validateUserRegistration };
```

**test-data/user-registrations.csv**:

```csv
username,email,age,country,valid,expected_error
alice123,alice@example.com,25,US,true,
ab,bob@example.com,30,US,false,Username must be 3-20 characters
user!@#,test@example.com,20,US,false,Username must be alphanumeric
validuser,invalid-email,25,US,false,Invalid email format
testuser,test@example.com,10,US,false,Age must be between 13 and 120
gooduser,good@example.com,25,us,false,Country must be 2-letter code (uppercase)
john_doe,john@example.com,30,US,false,Username must be alphanumeric
verylongusernamethatexceeds,test@example.com,25,US,false,Username must be 3-20 characters
user,missing-at-sign,25,US,false,Invalid email format
testuser,test@example.com,150,US,false,Age must be between 13 and 120
testuser,test@example.com,25,USA,false,Country must be 2-letter code (uppercase)
validuser,valid@example.com,13,US,true,
validuser,valid@example.com,120,US,true,
```

**userValidator.test.js**:

```javascript
const { validateUserRegistration } = require("./userValidator");
const fs = require("fs");
const { parse } = require("csv-parse/sync");

function loadUserTestData() {
  const csvData = fs.readFileSync("test-data/user-registrations.csv", "utf8");
  const records = parse(csvData, { columns: true });

  return records.map((row) => ({
    username: row.username,
    email: row.email,
    age: row.age,
    country: row.country,
    expectedValid: row.valid === "true",
    expectedError: row.expected_error,
  }));
}

const userTests = loadUserTestData();

test.each(userTests)(
  "validates user: $username",
  ({ username, email, age, country, expectedValid, expectedError }) => {
    const result = validateUserRegistration(username, email, age, country);

    expect(result.isValid).toBe(expectedValid);

    if (!expectedValid && expectedError) {
      const hasExpectedError = result.errors.some((err) =>
        err.includes(expectedError),
      );
      expect(hasExpectedError).toBe(true);
    }
  },
);
```

## Part 4: CSV Data Management Helper

**csvTestHelper.js**:

```javascript
const fs = require("fs");
const { parse } = require("csv-parse/sync");

class CSVTestDataLoader {
  constructor(dataDir = "test-data") {
    this.dataDir = dataDir;
  }

  load(filename) {
    const filepath = `${this.dataDir}/${filename}`;

    if (!fs.existsSync(filepath)) {
      throw new Error(`Test data file not found: ${filepath}`);
    }

    const csvData = fs.readFileSync(filepath, "utf8");
    return parse(csvData, { columns: true });
  }

  convertTypes(data, typeMap) {
    return data.map((row) => {
      const converted = {};

      for (const [key, targetType] of Object.entries(typeMap)) {
        const value = row[key];

        if (targetType === Boolean) {
          converted[key] = value === "true";
        } else if (targetType === Number) {
          converted[key] = parseFloat(value);
        } else if (targetType === Array) {
          converted[key] = JSON.parse(value);
        } else {
          converted[key] = value;
        }
      }

      return converted;
    });
  }
}

module.exports = CSVTestDataLoader;
```

**Usage example**:

```javascript
const CSVTestDataLoader = require("./csvTestHelper");

const loader = new CSVTestDataLoader();
const data = loader.load("emails.csv");
const typedData = loader.convertTypes(data, {
  email: String,
  valid: Boolean,
  reason: String,
});

test.each(typedData)("test $email", ({ email, valid, reason }) => {
  // test logic
});
```

## Part 5: Complex Product Data

**test-data/products.csv**:

```csv
id,name,price,category,inStock,weight,tags
1,Laptop,999.99,Electronics,true,2.5,"laptop,computer,portable"
2,Mouse,29.99,Electronics,true,0.2,"mouse,wireless,accessory"
3,Desk,399.99,Furniture,true,25.0,"desk,office,furniture"
4,Chair,199.99,Furniture,false,15.0,"chair,office,ergonomic"
5,Monitor,349.99,Electronics,true,5.5,"monitor,display,screen"
```

**productValidator.js**:

```javascript
function validateProduct(product) {
  const errors = [];

  if (!product.name || product.name.length < 3) {
    errors.push("Name must be at least 3 characters");
  }

  if (product.price <= 0) {
    errors.push("Price must be positive");
  }

  if (!["Electronics", "Furniture", "Clothing"].includes(product.category)) {
    errors.push("Invalid category");
  }

  if (typeof product.inStock !== "boolean") {
    errors.push("inStock must be boolean");
  }

  if (product.weight <= 0) {
    errors.push("Weight must be positive");
  }

  return {
    isValid: errors.length === 0,
    errors: errors,
  };
}

module.exports = { validateProduct };
```

**productValidator.test.js**:

```javascript
const { validateProduct } = require("./productValidator");
const fs = require("fs");
const { parse } = require("csv-parse/sync");

function loadProductTestData() {
  const csvData = fs.readFileSync("test-data/products.csv", "utf8");
  const records = parse(csvData, { columns: true });

  return records.map((row) => ({
    id: parseInt(row.id),
    name: row.name,
    price: parseFloat(row.price),
    category: row.category,
    inStock: row.inStock === "true",
    weight: parseFloat(row.weight),
    tags: row.tags.split(","),
  }));
}

const productTests = loadProductTestData();

test.each(productTests)(
  "validates product: $name",
  ({ name, price, category, inStock, weight, tags }) => {
    const result = validateProduct({
      name,
      price,
      category,
      inStock,
      weight,
    });

    expect(result.isValid).toBe(true);
    expect(tags.length).toBeGreaterThan(0);
  },
);
```

## Expected Output

```bash
$ npm test

 PASS  ./emailValidator.test.js
  ✓ validates email: user@example.com (Standard valid email)
  ✓ validates email: invalid@ (Missing domain)
  ...

 PASS  ./passwordValidator.test.js
  ✓ password strength: abc -> weak (Too short)
  ✓ password strength: P@ssw0rd!2023 -> strong (12+ chars with all character types)
  ...

 PASS  ./userValidator.test.js
  ✓ validates user: alice123
  ✓ validates user: ab
  ...

Test Suites: 3 passed, 3 total
Tests:       33 passed, 33 total
```

## Tips

1. Use `csv-parse/sync` for synchronous CSV parsing
2. Set `columns: true` to get objects with column names
3. Convert string types from CSV to appropriate JavaScript types
4. Handle empty values gracefully
5. Use relative paths with `__dirname` for cross-platform compatibility

## Requirements

1. Create all validator modules
2. Create CSV files with at least 10 test cases each
3. Implement tests that load data from CSV
4. Test both success and failure scenarios
5. Proper type conversion from CSV strings

## Submission

Submit:

- All JavaScript modules (`*.js`)
- All test files (`*.test.js`)
- All CSV files in `test-data/` directory
- `package.json` with dependencies
- README explaining CSV data structure
- Screenshot of passing tests

## Grading Criteria

- Implementation correctness: 30%
- CSV data quality: 30%
- Test implementation: 25%
- Code organization: 10%
- Documentation: 5%
