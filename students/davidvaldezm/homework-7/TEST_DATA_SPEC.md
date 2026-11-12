# Test Data Specification

All fixtures live in `test_data/` and use UTF-8. Case names are unique within a file and become pytest parameter IDs. The loader validates the files during test collection. CSV errors identify the record's starting line. JSON schema errors identify the record's starting line and the property path when available. JSON syntax errors identify the parser's exact line.

## Order CSV files

`order_calculations.csv`, `generated_orders.csv` and `order_comparison.csv` share these columns.

| Column | Format |
| --- | --- |
| `test_name` | Nonempty descriptive case name |
| `items` | JSON array embedded in a CSV field. Each item has a string `name`, dollar `price`, `quantity` and kilogram `weight`. Double any JSON quotes within the quoted CSV field. |
| `customer_type` | `regular` or `new` |
| `discount_code` | Case-sensitive code, or `NONE` for no coupon |
| `distance_km` | Finite decimal number |
| `is_express` | `true` or `false` |
| `discount_applied` | Expected coupon result as `true` or `false`. Empty when no application is expected. |
| `expected_error` | Expected `ValueError` message for a rejected numeric input. Empty for successful calculations. |
| `expected_subtotal`, `expected_discount`, `expected_tax`, `expected_shipping`, `expected_total` | Dollar amounts to two decimal places. All five are empty for a case with an expected error. |

The schema accepts numeric quantities at fixture load time so the calculator can be tested with fractional or negative inputs. Regression rows use the fixed seed `731`, whole-cent prices and distances and weights in tenths.

## Customer JSON

`customer_validation.json` is an array of objects. Each object has `test_name`, the ISO date `as_of`, the raw `customer` input and an `expected` object with `is_valid` and the ordered list `errors`.

A valid customer supplies `email`, `phone` in US `(XXX) XXX-XXXX` format, `billing_address` with `street`, `city`, two-letter `state` and five-digit or ZIP+4 `zip`, and `credit_card` with a Luhn-valid `number`, expiration in `MM/YYYY` and three- or four-digit `cvv`. Card data is synthetic. The schema accepts any JSON value for the raw input to allow missing fields, wrong types and null values. The expected error list follows contact, address and card field order.

## Checkout workflow JSON

`order_workflows.json` has a top-level `workflows` array. Every workflow supplies `name`, `as_of`, `order_id`, `payment_responses`, `expected_charges` and an ordered `steps` array. The payment function consumes one boolean response per actual charge. `expected_charges` gives the exact amount sequence, so a duplicate charge or an unintended payment attempt fails the test.

Each step includes an `action` and an `expected` response. Steps that take parameters also supply a `data` object.

| Action | Input | Expected response |
| --- | --- | --- |
| `validate_customer` | `customer` | `valid` and ordered `errors` |
| `create_order` | `items` and optional `customer_type`, `discount_code`, `distance_km`, `is_express` | `status` and, for an invalid order, an `error` |
| `calculate_total` | None | All five amounts, or `status: no_order` |
| `process_payment` | None | `status` and `amount` when an order exists |
| `generate_confirmation` | None | `status` and, once paid, `order_id`, `email` and `total` |
