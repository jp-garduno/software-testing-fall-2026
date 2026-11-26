# Test Data Specification

This document outlines the exact format and structural requirements for the external test data files used in the E-Commerce Order Processing test suite.

## 1. Order Calculations Data (`test_data/order_calculations.csv`)
This CSV file drives the parameterized tests for the `order_calculator.py` module. 

**Format Rules:**
* **File type:** Comma-Separated Values (.csv)
* **Header row:** Strictly required.
* **JSON Encoding:** The `items` column must contain a valid JSON string wrapped in double quotes. Single quotes inside the JSON string are automatically converted to double quotes by the parsing script.

**Columns Definition:**
1. `test_name` (string): Unique identifier for the test case.
2. `items` (JSON string): Array of objects representing cart items. Schema: `[{name: str, price: float, quantity: int, weight: float}]`
3. `customer_type` (string): Either "regular" or "new".
4. `discount_code` (string): The promotional code (e.g., "SAVE10", "FREESHIP"). Use "NONE" if no discount applies.
5. `distance_km` (float): The shipping distance in kilometers.
6. `is_express` (boolean): "true" or "false".
7. `expected_subtotal` (float): The exact expected subtotal.
8. `expected_discount` (float): The exact expected discount amount.
9. `expected_tax` (float): The expected calculated tax (8% of subtotal after discount).
10. `expected_shipping` (float): The expected shipping cost.
11. `expected_total` (float): The expected final total.

## 2. Customer Validation Data (`test_data/customer_validation.json`)
This JSON file drives the parameterized tests for the `customer_validator.py` module.

**Format Rules:**
* **File type:** JSON array of objects.
* **Root Structure:** Each object must represent a single test scenario.

**Object Schema:**

    {
      "test_name": "string",
      "customer": {
        "email": "string",
        "phone": "string",
        "billing_address": {
          "street": "string",
          "city": "string",
          "state": "string",
          "zip": "string"
        },
        "credit_card": {
          "number": "string",
          "expiration": "string (MM/YYYY)",
          "cvv": "string"
        }
      },
      "expected": {
        "is_valid": boolean,
        "errors": ["array", "of", "expected", "error", "messages"]
      }
    }

## 3. Integration Workflows Data (`test_data/order_workflows.json`)
This JSON file drives the end-to-end integration tests, simulating a sequence of actions.

**Format Rules:**
* **Root Structure:** A single JSON object containing a `workflows` array.
* **Workflow Schema:** Each workflow contains a `name` and an ordered array of `steps`.
* **Step Actions Supported:** `validate_customer`, `create_order`, `calculate_total`, `process_payment`.
* **Flow Control:** If a step's action results in a state contrary to its `expected` block, the test fails immediately.