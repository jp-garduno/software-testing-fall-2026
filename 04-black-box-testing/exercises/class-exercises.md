# Black Box Testing - Class Exercises

These exercises are designed for in-class practice and discussion. Work through them step-by-step, applying the techniques you've learned.

---

## 📋 Exercise Set 1: Equivalence Partitioning

### Exercise 1.1: Number Classification

**Requirement**: Function that checks if a given number is positive, negative, or zero.

**Task**:

1. Identify equivalence classes
2. Design test cases (one per class minimum)
3. Implement in Python and JavaScript

**Equivalence Classes**:

```
Valid Classes:
- [ ] Positive numbers (n > 0)
- [ ] Negative numbers (n < 0)
- [ ] Zero (n = 0)

Invalid Classes:
- [ ] Non-numeric input (if applicable)
```

**Sample Test Cases**:
| Test ID | Input | Expected Output | Equivalence Class |
|---------|-------|-----------------|-------------------|
| TC1 | 5 | "Positive" | Positive numbers |
| TC2 | -3 | "Negative" | Negative numbers |
| TC3 | 0 | "Zero" | Zero |

---

### Exercise 1.2: Password Validator

**Requirement**: Function that validates user passwords with the following rules:

- The password must be at least 8 characters long
- The password must contain at least one uppercase letter
- The password must contain at least one lowercase letter
- The password must contain at least one digit
- The password must contain at least one special character (!, @, #, $, %, or &)

**Task**:

1. Identify all equivalence classes (valid and invalid)
2. Design comprehensive test cases
3. Implement the validator and tests

**Equivalence Classes Template**:

```
Valid Classes:
- [ ] Passwords meeting all criteria

Invalid Classes (for each violated rule):
- [ ] Too short (< 8 characters)
- [ ] No uppercase letter
- [ ] No lowercase letter
- [ ] No digit
- [ ] No special character
- [ ] Multiple rules violated
```

**Hint**: You can have one valid equivalence class and multiple invalid ones.

---

### Exercise 1.3: Credit Card Validation

**Requirement**: Function that validates credit card numbers.

- Valid card numbers: Length between 13 and 16 digits, containing only numeric digits

**Task**:

1. Identify equivalence classes
2. Design test cases
3. Consider what makes this different from simple numeric validation

**Think About**:

- What are the valid length ranges?
- What about non-numeric characters?
- What about empty or null input?

---

### Exercise 1.4: Date Validation

**Requirement**: Function that validates dates with the following rules:

- Valid years: Between 1900 and 2100
- Valid months: Between 1 and 12
- Valid days: Between 1 and 31

**Task**:

1. Identify equivalence classes for each component (year, month, day)
2. Design test cases
3. What additional validation might be needed? (e.g., February 30th)

---

### Exercise 1.5: Flight Booking Eligibility

**Requirement**: Function that checks the eligibility of a passenger to book a flight.

- Eligible ages: Between 18 and 65
- Frequent flyers: True or False
- **Special rule**: Frequent flyers can be any age

**Task**:

1. Identify equivalence classes considering the combination of age and frequent flyer status
2. Design test cases covering all combinations
3. This combines two input dimensions - how many classes do you need?

---

### Exercise 1.6: URL Validation

**Requirement**: Function that validates URLs.

- Valid URLs: Length less than or equal to 255 characters, starting with "http://" or "https://"

**Task**:

1. Identify equivalence classes
2. Consider protocol variations
3. What about edge cases with exactly 255 characters?

---

## 📋 Exercise Set 2: Boundary Value Analysis

### Exercise 2.1: Discount Calculator

**Requirement**: Function that calculates the discount for a customer's purchase based on the total amount.

**Discount Rules**:

- If the total amount is **less than 100**, no discount is applied
- If the total amount is **between 100 and 500 (inclusive)**, a 10% discount is applied
- If the total amount is **greater than 500**, a 20% discount is applied

**Task**:

1. Identify boundaries in the requirements
2. For each boundary, identify test values (below, at, above)
3. Create a complete test case table
4. Implement the function and tests

**Boundary Analysis Template**:

```
Boundary 1: 100
- Below: 99
- At: 100
- Above: 101

Boundary 2: 500
- Below: 499
- At: 500
- Above: 501

Additional considerations:
- Minimum value: 0 or negative?
- Maximum value: Any limit?
```

---

### Exercise 2.2: Loan Eligibility Calculator

**Requirement**: Function that calculates the eligibility of a person for a loan based on their income and credit score.

**Eligibility Rules**:

- If the income is **less than $30,000**, the person is not eligible for a loan
- If the income is **between $30,000 and $60,000 (inclusive)** and the credit score is **above 700**, the person is eligible for a standard loan
- If the income is **between $30,000 and $60,000 (inclusive)** and the credit score is **below or equal to 700**, the person is eligible for a secured loan
- If the income is **greater than $60,000** and the credit score is **above 750**, the person is eligible for a premium loan
- If the income is **greater than $60,000** and the credit score is **between 700 and 750 (inclusive)**, the person is eligible for a standard loan

**Task**:

1. Identify all boundaries (both income and credit score)
2. Create a test case matrix covering boundary combinations
3. This is a two-dimensional problem - how do you handle it?

**Boundaries to Consider**:

```
Income boundaries: 30,000 and 60,000
Credit score boundaries: 700 and 750
```

---

### Exercise 2.3: E-Commerce Product Categorization

**Requirement**: Function that determines the category of a product in an e-commerce system based on its price.

**Product Categories**:

- **Category A**: Products priced between $10 and $50 (inclusive)
- **Category B**: Products priced between $51 and $100 (inclusive)
- **Category C**: Products priced between $101 and $200 (inclusive)
- **Category D**: Products priced above $200

**Task**:

1. Identify all boundaries
2. Design boundary value tests
3. What happens to products under $10?

---

### Exercise 2.4: Shipping Cost Calculator

**Requirement**: Function that calculates the cost of shipping for packages based on their weight and dimensions.

**Shipping Cost Rules**:

- If the weight of the package is **≤ 1 kg** and the dimensions (length, width, and height) are each **≤ 10 cm**, the cost is **$5**
- If the weight is **between 1 and 5 kg (inclusive)** and the dimensions are each **between 11 and 30 cm (inclusive)**, the cost is **$10**
- If the weight is **> 5 kg** or any of the dimensions is **> 30 cm**, the cost is **$20**

**Task**:

1. This has multiple dimensions (weight, length, width, height) - identify all boundaries
2. How do you handle the "or" condition in the last rule?
3. Design a comprehensive boundary test suite

---

## 📋 Exercise Set 3: Decision Tables

### Exercise 3.1: Weather Advisory System

**Requirement**: Create the decision table for a system that provides weather advisories based on temperature and humidity.

**Rules**:

- Weather recommendation **"High temperature and humidity. Stay hydrated."** for temperature **> 30** and humidity **> 70**
- Weather recommendation **"Low temperature. Don't forget your jacket!"** for temperature **< 0** and **any humidity**
- **No weather recommendation** for any other temperature and humidity combination

**Task**:

1. Create a complete decision table
2. Identify all possible combinations of conditions
3. Simplify if possible (combine redundant rules)
4. Implement the system and tests

**Decision Table Template**:

```
| Rule | R1 | R2 | R3 | R4 | ... |
|------|----|----|----|----|-----|
| Temperature > 30 | T | F | ... |
| Humidity > 70 | T | F | ... |
| Temperature < 0 | F | T | ... |
|------|----|----|----|----|-----|
| Action | "High temp..." | "Low temp..." | "No advisory" | ... |
```

---

### Exercise 3.2: User Authentication System

**Requirement**: Create the decision table for a system that authenticates users based on their username and password.

**Rules**:

- Returns **"Admin"** for username **"admin"** and password **"admin123"**
- Returns **"User"** for any other username with **at least 5 characters** and password with **at least 8 characters**
- Returns **"Invalid"** if the username or password length requirements are not met

**Task**:

1. Create decision table
2. What are all the combinations of conditions?
3. How do you handle the length requirements?

---

### Exercise 3.3: Insurance Premium Calculator

**Requirement**: An insurance company calculates premiums based on:

- Age: < 25, 25-60, > 60
- Coverage level: Basic, Standard, Premium
- Accident history: Yes/No

**Rules**:

- Age < 25 with accidents: Premium + 50%
- Age < 25 without accidents: Premium + 25%
- Age 25-60 with accidents: Premium + 20%
- Age 25-60 without accidents: Standard Premium
- Age > 60 with accidents: Premium + 30%
- Age > 60 without accidents: Premium + 15%
- All percentages apply to the base coverage premium

**Task**:

1. Create comprehensive decision table
2. Implement the calculator
3. Design tests covering all rules

---

## 📋 Exercise Set 4: Combined Techniques

### Exercise 4.1: E-Commerce Order Processor

**Requirement**: Function that processes user orders in an e-commerce system. The function calculates the total price of the items in the order, applying different discounts based on the quantity of each item.

**Discount Rules**:

- If the quantity of a single item is **between 1 and 5 (inclusive)**, no discount is applied
- If the quantity of a single item is **between 6 and 10 (inclusive)**, a **5% discount** is applied
- If the quantity of a single item is **greater than 10**, a **10% discount** is applied

**Task**:

1. Apply **Equivalence Partitioning** to identify quantity ranges
2. Apply **Boundary Value Analysis** for the quantity boundaries
3. Create comprehensive test cases
4. Implement and test with multiple items in an order

---

### Exercise 4.2: Shipping Cost Calculator (Advanced)

**Requirement**: Function that calculates shipping costs for an online shopping system. The function calculates shipping costs based on the total weight of the items in the order and the shipping method chosen by the customer.

**Shipping Cost Rules**:

**For standard shipping**:

- If the total weight is **≤ 5 kg**, the cost is **$10**
- If the total weight is **between 5 and 10 kg (inclusive)**, the cost is **$15**
- If the total weight is **> 10 kg**, the cost is **$20**

**For express shipping**:

- If the total weight is **≤ 5 kg**, the cost is **$20**
- If the total weight is **between 5 and 10 kg (inclusive)**, the cost is **$30**
- If the total weight is **> 10 kg**, the cost is **$40**

**Task**:

1. Use **Decision Tables** to handle the combination of shipping method and weight
2. Use **Boundary Value Analysis** for weight boundaries
3. Create comprehensive test suite
4. Implement both shipping methods

---

## 🎯 Challenge Exercise: ATM State Machine

**Requirement**: Design tests for an ATM system with the following states and transitions:

**States**:

- Idle
- Card Inserted
- PIN Entry
- Authenticated
- Transaction in Progress
- Ejecting Card

**Valid Transitions**:

- Idle → Card Inserted (user inserts card)
- Card Inserted → PIN Entry (system prompts for PIN)
- PIN Entry → Authenticated (correct PIN entered)
- PIN Entry → Card Inserted (wrong PIN, retries remaining)
- PIN Entry → Ejecting Card (3 wrong PINs)
- Authenticated → Transaction in Progress (user selects transaction)
- Transaction in Progress → Authenticated (transaction complete, user wants more)
- Transaction in Progress → Ejecting Card (transaction complete, user done)
- Authenticated → Ejecting Card (user cancels)
- Ejecting Card → Idle (card ejected)

**Task**:

1. Draw a state transition diagram
2. Identify all valid transitions
3. Identify invalid transitions (test that they're rejected)
4. Design test cases covering:
   - All valid transitions
   - All states
   - Invalid transitions from each state
5. Implement a simple state machine and tests

---

## 📊 Summary: When to Use Each Technique

| **Scenario**                                    | **Recommended Technique(s)**       |
| ----------------------------------------------- | ---------------------------------- |
| Input validation with categories                | Equivalence Partitioning           |
| Numeric ranges or limits                        | BVA + Equivalence Partitioning     |
| Complex business rules with multiple conditions | Decision Tables                    |
| System with distinct states                     | State Transition                   |
| Payment/checkout logic                          | Decision Tables + BVA              |
| Form validation                                 | Equivalence Partitioning + BVA     |
| User authentication                             | Decision Tables                    |
| Order processing workflow                       | State Transition + Decision Tables |

---

## 🚀 Next Steps

After completing these exercises:

1. Implement solutions in both Python and JavaScript
2. Compare your test cases with classmates
3. Discuss which techniques worked best for each scenario
4. Start working on [Homework 4](../homework/homework-4.md)

---

**Remember**: The goal is not just to create tests, but to create **effective** tests that find bugs efficiently! 🎯
