# Test Data Specification (`TEST_DATA_SPEC.md`)

This document specifies the schema, data types, validation rules, and category breakdown for all external test data files in `test_data/`.

---

## 1. `test_data/order_calculations.csv` (and `generated_orders.csv`)

### Format
UTF-8 encoded CSV file with a header row. The `items` column stores a JSON-encoded array of item objects.

### Schema Definition

| Column Name | Data Type | Constraints / Allowed Values | Description |
| :--- | :--- | :--- | :--- |
| `test_name` | `string` | Unique identifier, non-empty (`snake_case`) | Descriptive test case ID used by `pytest` |
| `items` | `JSON array` | Array of `{"name": str, "price": float, "quantity": int, "weight": float}` | Line items in the shopping cart |
| `customer_type` | `string` | `"regular"` or `"new"` | Customer tier (determines eligibility for `NEWUSER`) |
| `discount_code` | `string` | `"NONE"`, `"SAVE10"`, `"SAVE20"`, `"FREESHIP"`, `"NEWUSER"`, or invalid code | Promotional code to apply |
| `distance_km` | `float` | Real number (`>= 0` for standard cases; negative tested as edge case) | Shipping distance in kilometers |
| `is_express` | `boolean` | `"true"` or `"false"` (case-insensitive string) | Whether express shipping (`1.5x` multiplier) is selected |
| `expected_subtotal` | `float` | Rounded to 2 decimal places | Expected sum of `price × quantity` |
| `expected_discount` | `float` | Rounded to 2 decimal places | Expected discount dollar amount |
| `expected_tax` | `float` | Rounded to 2 decimal places | Expected 8% tax on `(subtotal - discount)` |
| `expected_shipping` | `float` | Rounded to 2 decimal places | Expected shipping cost |
| `expected_total` | `float` | Rounded to 2 decimal places | Expected final total (`subtotal - discount + tax + shipping`) |

### Coverage Breakdown in `order_calculations.csv` (30 Cases)
1. **Simple orders (`simple_*`)**: 4 cases (single item, multiple quantities, multiple items, decimal prices).
2. **Discount validation (`discount_*`)**: 8 cases (`SAVE10` at $50 and $49.99, `SAVE20` at $100 and $99.99, `NEWUSER` for `"new"` vs `"regular"` customer, invalid code `EXPIRED50`, multi-item discount).
3. **Tax calculations (`tax_*`)**: 4 cases (small order rounding, high-value order, post-`SAVE10` tax, post-`NEWUSER` tax).
4. **Shipping calculations (`shipping_*`)**: 6 cases (light/short standard, heavy/long standard, express `1.5x`, `FREESHIP` override, zero-weight distance-only, weight-only local pickup).
5. **Complex & edge cases (`complex_*`, `edge_*`)**: 8 cases (multi-item + discount + express, empty cart, zero quantity, negative values clamped to zero, maximum enterprise bulk order, fractional weights).

---

## 2. `test_data/customer_validation.json`

### Format
UTF-8 JSON array of test case objects.

### Schema Definition

```json
{
  "test_name": "string (unique identifier)",
  "customer": {
    "email": "string (user@domain.tld)",
    "phone": "string ((XXX) XXX-XXXX)",
    "billing_address": {
      "street": "string (>= 3 non-whitespace chars)",
      "city": "string (>= 2 non-whitespace chars)",
      "state": "string (2 uppercase letters: ^[A-Z]{2}$)",
      "zip": "string (5 digits or ZIP+4: ^\\d{5}(-\\d{4})?$)"
    },
    "credit_card": {
      "number": "string (13-19 digits passing Luhn checksum)",
      "expiration": "string (MM/YYYY, not expired relative to 01/2025)",
      "cvv": "string (3 or 4 digits: ^\\d{3,4}$)"
    }
  },
  "expected": {
    "is_valid": true,
    "errors": []
  }
}
```

### Error Messages Verified
- `"Invalid email format"`
- `"Invalid phone format"`
- `"Invalid billing address"` / `"Invalid street address"` / `"Invalid city"` / `"Invalid state code"` / `"Invalid zip code"`
- `"Invalid credit card information"` / `"Invalid credit card number"` / `"Invalid expiration date"` / `"Invalid CVV"`

### Coverage Breakdown in `customer_validation.json` (34 Cases)
1. **Valid customers (`valid_customer_*`)**: 4 cases (Visa, Mastercard, Amex 15-digit + 4-digit CVV, ZIP+4).
2. **Invalid emails (`invalid_email_*`)**: 5 cases (missing `@`, missing domain, spaces, double dots, empty).
3. **Invalid phones (`invalid_phone_*`)**: 5 cases (no parentheses, missing space, letters, too short, empty).
4. **Invalid addresses (`invalid_address_*`)**: 6 cases (short street, short city, lowercase state, 3-letter state, 4-digit zip, alphanumeric zip).
5. **Invalid credit cards (`invalid_card_*`)**: 8 cases (Luhn checksum failure, too short, non-digits, expired year, expired month, month `13`, short CVV, non-digit CVV).
6. **Multiple validation errors (`multiple_errors_*`)**: 6 cases combining 2 to 8 simultaneous validation failures.

---

## 3. `test_data/order_workflows.json`

### Format
UTF-8 JSON object with a top-level `"workflows"` list. Each workflow has a `"name"` and an ordered array of `"steps"`.

### Supported Workflow Actions
1. `"validate_customer"`: Runs `validate_customer(step["data"])` and checks `expected["valid"]`.
2. `"create_order"`: Instantiates `Order`, applies optional `discount_code`, configures shipping, and checks `expected["status"] == "created"`.
3. `"calculate_total"`: Computes breakdown (`subtotal`, `discount`, `tax`, `shipping`, `total`) and compares against `expected`.
4. `"process_payment"`: Approves payment (`"success"`) if and only if customer validation passed and order total > 0; otherwise returns `"failed"`.
