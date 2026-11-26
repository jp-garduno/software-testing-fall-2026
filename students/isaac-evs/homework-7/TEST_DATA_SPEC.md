# Test Data Specification

All scenarios live in `test_data/`. The test code only loads and interprets them (`tests/data_loader.py`), so
adding a case means adding a row or an object, not writing a test.

| File                                | Format | Cases | Used by                                                          |
| ----------------------------------- | ------ | ----- | ---------------------------------------------------------------- |
| `order_calculations.csv`            | CSV    | 38    | `test_order_calculator.py`                                       |
| `order_calculations.xlsx`           | Excel  | 38    | `test_order_excel.py` (same cases as the CSV, 6 sheets)          |
| `customer_validation.json`          | JSON   | 48    | `test_customer_validator.py`                                     |
| `order_workflows.json`              | JSON   | 5     | `test_integration.py`                                            |
| `comparison_orders.csv`             | CSV    | 10    | `test_order_data_driven.py` (the Part 3 comparison)              |

Expected values were calculated by hand, not by running the code under test.

## 1. `order_calculations.csv`

One row per order. UTF-8, comma separated, standard CSV quoting.

| Column                                                                 | Type            | Meaning |
| ---------------------------------------------------------------------- | --------------- | ------- |
| `test_name`                                                            | text, unique    | Becomes the pytest id, e.g. `save10_at_minimum_threshold` |
| `category`                                                             | text            | `simple`, `discount`, `tax`, `shipping`, `complex` or `error` |
| `items`                                                                | JSON list       | `[{"name": str, "price": number, "quantity": int, "weight": number}]`; quotes are doubled inside the CSV cell |
| `customer_type`                                                        | text            | `new` or `regular` (anything else must be an `error` row) |
| `discount_code`                                                        | text            | A code, or `NONE` for no code |
| `distance_km`                                                          | number          | Shipping distance |
| `is_express`                                                           | `true`/`false`  | Express shipping |
| `expected_subtotal` ... `expected_total`                               | number, 2 dp    | Expected breakdown (5 columns). Empty on `error` rows |
| `expected_error`                                                       | text            | Empty for normal rows. For `error` rows, a substring of the `ValueError` message |

Compared with the column list in the assignment text, this file adds `category` and `expected_error`.

Cases per category: simple 3, discount 10, tax 5, shipping 7, complex 6, error 7.

### Business rules the data relies on

| Rule | Decision |
| ---- | -------- |
| Minimum order for a code | **Inclusive.** `SAVE10` applies at exactly $50.00, `SAVE20` at exactly $100.00. The assignment text says "> $50" but its starter code rejects only subtotals *below* the minimum; I followed the code, and `save10_at_minimum_threshold` / `save20_at_minimum_threshold` pin this. |
| `NEWUSER` | Valid only when `customer_type` is `new` ("15% off first order"). Rejected for `regular` customers. |
| Code matching | Exact and case sensitive: `save10` is invalid. |
| Several codes | The last *valid* code replaces the earlier one. An invalid code changes nothing. Only one code is active. |
| `FREESHIP` | $0 price discount, shipping is $0 even when express is selected. |
| Tax | 8% of (subtotal - discount), rounded half-up to cents. |
| Shipping | (total weight in kg x $0.50 + km x $0.10), times 1.5 if express, rounded half-up to cents. Total weight = sum of weight x quantity. |
| Total | subtotal - discount + tax + shipping, built from the already-rounded parts, so the breakdown adds up exactly. |
| Zero quantity | Allowed; the item contributes nothing to price or weight. |
| Invalid input | Negative price, quantity or weight, a non-integer quantity, a negative distance, an empty item list, or an unknown customer type raise `ValueError` (the `error` rows). |

### Where this differs from the assignment text

| Assignment text | What I did |
| --------------- | ---------- |
| Sample row: 1 kg, 10 km, standard shipping, `expected_shipping` = 5.50 | The written rules give 0.50 + 1.00 = **1.50**. The sample row is inconsistent with the rules, so it is not used. |
| Sample `items` cell: `[{name:Item1,price:50,...}]` | Not valid JSON (unquoted keys), so the sample loader's `json.loads` would fail on it. The data uses real JSON. |
| Sample loader: `row['items'].replace("'", '"')` | Breaks any item name containing an apostrophe (checked with `Men's shirt`). Not needed with valid JSON, so it is not used. |
| Sample test: `pytest.approx(x, rel=1e-2)` | A 1% tolerance accepts a total of 100.99 for 100.00. Tests use `abs=0.005`, i.e. exact to the cent. |
| Sample customer: card expiring `12/2025` | Already expired today (2026-11-12), so the sample would fail depending on the run date. The tests validate cards as of a fixed reference date (2026-06-15), so results never depend on when they run. |

## 2. `order_calculations.xlsx`

Generated from the CSV by `python tools/csv_to_xlsx.py`. Same columns, one sheet per category (`simple`, `discount`,
`tax`, `shipping`, `complex`, `error`). Numbers are numeric cells, `is_express` is a boolean cell, `items` stays JSON text.
`test_excel_and_csv_describe_the_same_cases` fails if the two files drift apart, so after editing the CSV regenerate the workbook.

## 3. `customer_validation.json`

A list of objects:

```json
{
  "test_name": "email_missing_at_sign",
  "category": "invalid_email",
  "customer": { "email": "...", "phone": "...", "billing_address": {"street": "", "city": "", "state": "", "zip": ""},
                "credit_card": {"number": "", "expiration": "MM/YYYY", "cvv": ""} },
  "as_of": "2027-01-01",
  "expected": { "is_valid": false, "errors": ["Invalid email format"] }
}
```

`as_of` is optional (ISO date). Without it the tests validate as of the fixed reference date **2026-06-15**, so card
expiry results never depend on the real date. Categories: valid 6, invalid_email 6, invalid_phone 6, invalid_address 8,
invalid_credit_card 12, multiple_errors 8, reference_date 2.

### Validation rules

| Field | Valid when | Error message |
| ----- | ---------- | ------------- |
| `email` | `local@domain.tld`; no leading/trailing/consecutive dots in the local part, no spaces, TLD of 2+ letters, at most 254 characters | `Invalid email format` |
| `phone` | exactly `(XXX) XXX-XXXX` | `Invalid phone format` |
| `street` | non-blank, at most 100 characters, with at least one letter and one digit | `Invalid street` |
| `city` | starts with a letter, 2-50 characters of letters, spaces, `.`, `'`, `-` | `Invalid city` |
| `state` | uppercase US state or DC code | `Invalid state` |
| `zip` | `12345` or `12345-6789` | `Invalid zip code` |
| `credit_card.number` | 13-19 digits (single spaces and hyphens allowed) passing the Luhn check | `Invalid credit card number` |
| `credit_card.expiration` | `MM/YYYY`, month 01-12 | `Invalid expiration date` |
| (expiration, continued) | not earlier than the current month; a card is valid through the end of its month | `Credit card expired` |
| `credit_card.cvv` | 3 digits, or 4 digits for cards starting 34 or 37 (American Express) | `Invalid CVV` |

Errors are listed in the order of this table (email, phone, street, city, state, zip, number, expiration, CVV).
A missing section or field counts as invalid, so `{}` produces all nine errors.

## 4. `order_workflows.json`

```json
{
  "customers": { "standard": { ...customer record... } },
  "workflows": [
    { "name": "complete_order_flow", "description": "...",
      "steps": [ { "action": "validate_customer", "data": {"customer": "standard"}, "expected": {"valid": true} } ] }
  ]
}
```

`data.customer` is a key into `customers`. `expected` lists only the keys to check; numbers are compared to the cent,
everything else exactly. A fresh engine is used per workflow, so confirmation numbers start at `ORD-000001`.

| Action | `data` | Result keys |
| ------ | ------ | ----------- |
| `validate_customer` | `customer` | `valid`, `errors` |
| `create_order` | `items`, optional `customer_type` | `status` (`created`) or rejected |
| `apply_discount` | `code` | `applied` |
| `set_shipping` | `distance_km`, optional `express` | `status` |
| `calculate_total` | - | the five breakdown amounts |
| `process_payment` | - | `status` (`success` / `declined`), `amount` |
| `generate_confirmation` | - | `status`, `confirmation_number`, `total` |

A step whose prerequisite is missing returns `{"status": "rejected", "error": ...}`. The simulated payment processor
declines card `4000000000000002`.

## 5. `comparison_orders.csv`

Ten rows copied from `order_calculations.csv`; the same ten scenarios are hard-coded in `test_order_traditional.py`.

## Validating the data files

`src/data_validator.py` checks all of the files above and reports problems with line numbers (columns present, JSON
types, `is_valid` consistent with `errors`, duplicate names, unknown workflow actions or customers, and the minimum case
counts the assignment requires). `test_data_validation.py` runs it on the shipped files and on deliberately broken ones.

## Adding a case

1. Add a row (CSV) or an object (JSON) with a unique `test_name` and hand-calculated expectations.
2. For an order case, regenerate the workbook: `python tools/csv_to_xlsx.py`.
3. Run `pytest`. `test_shipped_data_files_have_no_problems` points at the line of any malformed entry.
