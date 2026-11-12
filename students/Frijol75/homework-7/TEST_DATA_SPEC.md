# Test Data Specification: E-Commerce Order Processing

This document outlines the data schemas, validation criteria, and file conventions for the external datasets utilized in Homework 7.

---

## 1. `test_data/order_calculations.csv`

Used by `tests/test_order_calculator.py` to validate pricing, discount policies, tax calculations, and shipping tariffs.

### 1.1 Column Definitions

| Column Name | Type | Allowed Values | Description |
| :--- | :--- | :--- | :--- |
| `test_name` | String | Alphanumeric snake_case | Unique identifier for the test case scenario. |
| `items` | JSON Array (string) | Valid JSON list of objects | Items in the order: `{"name": str, "price": float, "quantity": int, "weight": float}`. |
| `customer_type` | String | `"regular"`, `"new"` | Type of customer placing the order. |
| `discount_code` | String | `"NONE"`, `"SAVE10"`, `"SAVE20"`, `"FREESHIP"`, `"NEWUSER"` (or arbitrary invalid code) | Promo code submitted during checkout. |
| `distance_km` | Float | $\ge 0.0$ | Shipping distance in kilometers. |
| `is_express` | Boolean | `"true"`, `"false"` | Delivery speed preference (express applies 1.5× shipping multiplier). |
| `expected_subtotal` | Float | $\ge 0.0$ | Sum of `price * quantity` across all items. |
| `expected_discount` | Float | $\ge 0.0$ | Calculated discount amount deducted from subtotal. |
| `expected_tax` | Float | $\ge 0.0$ | 8% tax applied to `(subtotal - discount)`. |
| `expected_shipping` | Float | $\ge 0.0$ | Weight and distance shipping tariff ($0 if FREESHIP applied). |
| `expected_total` | Float | $\ge 0.0$ | `subtotal - discount + tax + shipping`. |

### 1.2 Test Categories Covered (30 cases total)
- **Simple Orders**: Single items, multiple quantities, empty cart (boundary).
- **Discount Codes**: Threshold boundaries for SAVE10 ($50) and SAVE20 ($100), NEWUSER customer restrictions, invalid codes.
- **Tax Calculations**: Standard 8%, after-discount tax, rounding fractions.
- **Shipping Rates**: Weight-only, distance-only, combined, express multiplier (1.5×), FREESHIP override, cross-country distances (1000km).
- **Complex Orders**: Bundles combining multiple promotions, express options, and boundary conditions.

---

## 2. `test_data/customer_validation.json`

Used by `tests/test_customer_validator.py` to validate customer registration, contact info, billing addresses, and payment credentials.

### 2.1 JSON Schema

Each entry in the root array has the following structure:

```json
{
  "test_name": "string (unique test case ID)",
  "customer": {
    "email": "string | null",
    "phone": "string (US format: (XXX) XXX-XXXX) | null",
    "billing_address": {
      "street": "string",
      "city": "string",
      "state": "string (2-letter uppercase US state)",
      "zip": "string (5 digits or 5+4 format: 12345 or 12345-6789)"
    } | null,
    "credit_card": {
      "number": "string (13-19 digits, Luhn valid)",
      "expiration": "string (MM/YYYY format)",
      "cvv": "string (3-4 digits)"
    } | null
  },
  "expected": {
    "is_valid": true | false,
    "errors": [
      "string (exact error message)"
    ]
  }
}
```

### 2.2 Standard Error Messages (in validation order)
1. **Email**: `"Missing email"`, `"Invalid email format"`
2. **Phone**: `"Missing phone"`, `"Invalid phone format"`
3. **Address**: `"Missing billing address"`, `"Missing street"`, `"Missing city"`, `"Invalid state"`, `"Invalid zip code"`
4. **Credit Card**: `"Missing credit card"`, `"Invalid credit card number"`, `"Invalid expiration format"`, `"Credit card expired"`, `"Invalid CVV"`

### 2.3 Test Categories Covered (35 cases total)
- Valid customer profiles (Visa, Mastercard, Amex with 4-digit CVV, zip+4).
- Invalid email scenarios (missing `@`, consecutive dots `..`, empty string, missing domain).
- Invalid phone scenarios (plain digits, dashes only, short length, missing).
- Invalid billing addresses (missing street/city, unknown state code, lowercase state, invalid zip, null address).
- Invalid credit cards (Luhn checksum failures, length < 13 or > 19, non-digits, expired date, invalid month, invalid CVV, null card).
- Multi-error combinations (all sections failing simultaneously).

---

## 3. `test_data/order_workflows.json`

Used by `tests/test_integration.py` to validate multi-step stateful workflows.

### 3.1 Structure
An array of workflows, each specifying sequential steps:
- `validate_customer`: Verifies customer payload.
- `create_order`: Instantiates order with items and customer type.
- `apply_discount`: Tests discount rule.
- `set_shipping`: Configures distance and express flag.
- `calculate_total`: Verifies total breakdown.
- `process_payment`: Finalizes transaction.
- `order_aborted`: Handles expected rejection on customer validation failure.

### 3.2 Workflows Implemented
1. `complete_standard_order_flow`: Happy path with regular customer and SAVE10.
2. `new_customer_express_order_flow`: New customer onboarding with NEWUSER and express delivery.
3. `freeship_heavy_order_flow`: Heavy industrial order with FREESHIP coupon.
4. `customer_validation_rejection_flow`: Negative flow where corrupted customer data halts the workflow.

---

## 4. `test_data/generated_orders.csv` (Bonus Option A)

Generated programmatically by `src/data_generator.py`:
- Contains **100 synthetic orders** with computed expected values for stress/regression testing.
- Uses identical schema to `order_calculations.csv`.

