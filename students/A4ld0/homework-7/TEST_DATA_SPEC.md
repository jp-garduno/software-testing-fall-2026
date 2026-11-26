# Test data specification

All fixtures use UTF-8. Paths are resolved relative to the project files so tests can load data from any working directory.

## Order calculations CSV

Each row has a unique `test_name`. Put each case on one physical line. The `items` column contains a JSON array inside a quoted CSV cell. Escape each internal double quote as two double quotes.

| Field | Type and meaning |
|---|---|
| `items` | Array of objects containing a string `name`, numeric `price`, integer `quantity`, and numeric `weight` in kilograms per unit |
| `customer_type` | `new` or `regular` |
| `discount_code` | Coupon string or `NONE` |
| `distance_km` | Numeric shipping distance in kilometers |
| `is_express` | Literal `true` or `false` |
| `expected_subtotal`, `expected_discount`, `expected_tax`, `expected_shipping`, `expected_total` | Expected dollar amounts |
| `expected_error` | Empty on success or `RangeError` for an invalid input. Leave all five expected amounts empty for an error case. |

The first ten CSV rows are also used by the comparison suite. If you change that set, update the hardcoded traditional scenarios to match.

## Customer validation JSON

The root is an array. Each record contains a unique string `test_name`, a `customer` object, and an `expected` object with a Boolean `is_valid` and an array of error strings. A valid record has an empty error array. Errors follow this order: email, phone, billing address, card number, card expiration.

| Customer field | Valid input |
|---|---|
| `email` | String with a local part, an at sign, and a dotted domain |
| `phone` | String in the form `(XXX) XXX-XXXX` |
| `billing_address` | Object with nonblank `street` and `city`, a two-letter US state or DC, and a five-digit ZIP or ZIP+4 |
| `credit_card` | Object with a `number` string of 13–19 digits passing Luhn and an `expiration` string in `MM/YYYY` format. The optional `cvv` is fixture data. |

Negative scenarios can supply invalid types or missing customer fields to exercise the application validator. Dates are checked against June 15, 2026 in the tests.

## Workflow JSON

The root has a `workflows` array. Each workflow has a unique string `name` and an ordered `steps` array. Each step supplies an `action` and an `expected` object. Input steps also supply `data`.

| Action | Input | Expected keys |
|---|---|---|
| `validate_customer` | Customer object | `valid` |
| `create_order` | Order object with the same input fields as the CSV | `status` |
| `calculate_total` | None | `total` or `status` on rejection |
| `process_payment` | None | `status` |
| `confirm_order` | None | `status` and `total` on success, or `status` on rejection |

Fixture validation runs before the suite. CSV errors report their physical row. For JSON schema errors, keep each scenario name on its own line to obtain a scenario line number. The workflow error also identifies the step number.
