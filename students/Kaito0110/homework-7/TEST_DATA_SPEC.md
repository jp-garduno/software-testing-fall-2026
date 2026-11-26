# Test Data Specification (`TEST_DATA_SPEC.md`)

This document specifies the schema, data types, domain constraints, and conventions used across all external test data files in `test_data/`.

---

## 1. `test_data/order_calculations.csv` (and `generated_orders.csv`)

### Format Overview
- **File Type**: UTF-8 comma-separated values (`.csv`) with header row.
- **Purpose**: Drives parameterized tests in `tests/test_order_calculator.py` and `tests/test_order_data_driven.py`.
- **Total Cases**: 28 curated cases in `order_calculations.csv` (+ 100 synthetic cases in `generated_orders.csv`).

### Column Schema

| Column Name | Data Type | Required | Description & Constraints |
| --- | --- | --- | --- |
| `test_name` | `string` | Yes | Unique snake_case identifier used as the `pytest` test ID. |
| `items` | `JSON string` | Yes | JSON array of item objects: `[{"name": str, "price": float, "quantity": int, "weight": float}]`. Single quotes `'` are normalized to `"` during parsing. |
| `customer_type` | `string` | Yes | Customer tier: `"regular"` or `"new"`. Determines eligibility for `"NEWUSER"`. |
| `discount_code` | `string` | Yes | Promotional code (`"SAVE10"`, `"SAVE20"`, `"FREESHIP"`, `"NEWUSER"`, `"NONE"`, or invalid string). `"NONE"` maps to `None`. |
| `distance_km` | `float` | Yes | Shipping distance in kilometers (`$0.10` per km). Negative values are clamped to `0.0`. |
| `is_express` | `boolean string` | Yes | `"true"` or `"false"`. When `"true"`, multiplies base shipping by `1.5`. |
| `expected_subtotal` | `float` | Yes | Expected sum of `price × quantity` rounded to 2 decimal places. |
| `expected_discount` | `float` | Yes | Expected discount amount in USD rounded to 2 decimal places. |
| `expected_tax` | `float` | Yes | Expected 8% tax on `(subtotal - discount)` rounded to 2 decimal places. |
| `expected_shipping` | `float` | Yes | Expected shipping cost in USD rounded to 2 decimal places. |
| `expected_total` | `float` | Yes | Expected final total (`subtotal - discount + tax + shipping`). |

---

## 2. `test_data/customer_validation.json`

### Format Overview
- **File Type**: UTF-8 JSON array of test case objects.
- **Purpose**: Drives parameterized customer validation tests in `tests/test_customer_validator.py`.
- **Total Cases**: 32 test cases across 6 categories (valid customers, invalid emails, invalid phones, invalid addresses, invalid credit cards, and multiple simultaneous errors).

### JSON Object Schema

```json
{
  "test_name": "string (unique identifier)",
  "customer": {
    "email": "string (e.g., john@example.com)",
    "phone": "string (US format: (XXX) XXX-XXXX)",
    "billing_address": {
      "street": "string (non-empty street address)",
      "city": "string (non-empty city name)",
      "state": "string (2-letter uppercase US state code, e.g., NY, CA)",
      "zip": "string (5-digit ZIP or ZIP+4: XXXXX or XXXXX-XXXX)"
    },
    "credit_card": {
      "number": "string (13-19 digit card number validated with Luhn algorithm)",
      "expiration": "string (MM/YYYY format, compared against reference date 01/2025)",
      "cvv": "string (3 or 4 numeric digits)"
    }
  },
  "expected": {
    "is_valid": true,
    "errors": []
  }
}
```

### Possible Validation Error Messages
- `"Invalid email format"`
- `"Invalid phone format"`
- `"Invalid street address"`
- `"Invalid city"`
- `"Invalid state code"`
- `"Invalid zip code"`
- `"Invalid credit card number"`
- `"Invalid credit card expiration date"`
- `"Credit card expired"`
- `"Invalid CVV"`

---

## 3. `test_data/order_workflows.json`

### Format Overview
- **File Type**: UTF-8 JSON object containing a `"workflows"` array.
- **Purpose**: Drives end-to-end integration tests in `tests/test_integration.py`.
- **Total Workflows**: 4 multi-step workflows (`complete_standard_order_flow`, `new_user_express_order_flow`, `freeship_multi_item_workflow`, `rejected_invalid_customer_workflow`).

### Supported Workflow Step Actions
1. **`validate_customer`**: Runs `validate_customer(data)` and records whether the customer can proceed.
2. **`create_order`**: Instantiates `Order(items, customer_type)`, applies `discount_code`, and configures shipping. Returns `{"status": "created"}` or `{"status": "rejected_invalid_customer"}`.
3. **`calculate_total`**: Computes and returns the full breakdown (`subtotal`, `discount`, `tax`, `shipping`, `total`).
4. **`process_payment`**: Charges the calculated total if the customer and order are valid, returning `{"status": "success", "confirmation_id": "CONF-...", "charged_amount": ...}` or `{"status": "failed"}`.
