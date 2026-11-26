# Test Data Specification

Every data-driven test in this homework reads its cases from `test_data/`. The files are validated when pytest
collects the tests (see [Validation](#validation)), so a malformed record stops the run with a file name and line
number instead of producing a confusing assertion failure.

| File                       | Format | Records                | Used by                                                       |
| -------------------------- | ------ | ---------------------- | ------------------------------------------------------------- |
| `order_calculations.csv`   | CSV    | 43 orders              | `tests/test_order_calculator.py`                              |
| `order_comparison.csv`     | CSV    | 10 orders              | `tests/test_order_data_driven.py` (Part 3)                    |
| `generated_orders.csv`     | CSV    | 100 orders (generated) | `tests/test_generated_orders.py` (bonus A)                    |
| `customer_validation.json` | JSON   | 42 customers           | `tests/test_customer_validator.py`                            |
| `order_workflows.json`     | JSON   | 7 workflows, 34 steps  | `tests/test_integration.py`                                   |

## Order CSV files

`order_calculations.csv`, `order_comparison.csv` and `generated_orders.csv` share one format: one order per row,
header row required, columns in any order.

| Column              | Type                        | Meaning                                                                     |
| ------------------- | --------------------------- | --------------------------------------------------------------------------- |
| `test_name`         | text, unique                | Test id shown by pytest, e.g. `save10_at_minimum_order`                     |
| `category`          | `simple` `discount` `tax` `shipping` `complex` `generated` | Groups the cases as the homework does   |
| `items`             | JSON list, single quotes    | `[{'name': 'Mug', 'price': 8.99, 'quantity': 2, 'weight': 0.4}]`            |
| `customer_type`     | `new` or `regular`          | Any other value is an error case                                            |
| `discount_code`     | text, `NONE` for no code    | Passed to `apply_discount` as written, so lowercase codes can be tested     |
| `distance_km`       | number                      | Shipping distance                                                           |
| `is_express`        | `true` or `false`           | Express shipping                                                            |
| `order_date`        | `YYYY-MM-DD` or empty       | Date used to check code expiry; empty means today                           |
| `expected_subtotal` | number with 2 decimals      | Expected `calculate_total()["subtotal"]`                                    |
| `expected_discount` | number with 2 decimals      | Expected discount                                                           |
| `expected_tax`      | number with 2 decimals      | Expected tax                                                                |
| `expected_shipping` | number with 2 decimals      | Expected shipping                                                           |
| `expected_total`    | number with 2 decimals      | Must equal subtotal - discount + tax + shipping                             |
| `expected_error`    | text or empty               | Message of the `ValueError` the order must raise                            |

A row is either a **calculation case** (the five expected amounts filled, `expected_error` empty) or an **error
case** (`expected_error` filled, the five amounts empty). In `items`, `weight` is per unit in kilograms; single
quotes keep the CSV readable and are turned into double quotes before parsing, so item names cannot contain an
apostrophe. Item values are type-checked only in calculation cases: error cases are allowed to carry a text price
or a missing field on purpose.

### Categories in `order_calculations.csv`

| Category   | Cases | What they cover                                                                                     |
| ---------- | ----- | --------------------------------------------------------------------------------------------------- |
| `simple`   | 3     | No code, no weight, no distance: one item, one item several times, two items                        |
| `discount` | 12    | Every code at and just below its minimum, unknown code, NEWUSER for new and regular customers, an expired code and its last valid day, lowercase code, several items, half-cent discount rounding |
| `tax`      | 4     | Rounding up, rounding down, tax after a discount, shipping not taxed                                |
| `shipping` | 7     | Weight only, distance only, weight times quantity, express, express rounding, FREESHIP standard and express |
| `complex`  | 17    | Several items with codes and express shipping, zero-quantity items, free items, a 10 million dollar bulk order, and 10 error cases: negative price, quantity, weight and distance, fractional quantity, unknown customer type, empty order, missing item field, blank item name, text price |

Every expected amount was calculated by hand from the rules below, not copied from the program's output.

### Rules the expected values follow

| Rule        | Value                                                                                                   |
| ----------- | ------------------------------------------------------------------------------------------------------- |
| Subtotal    | Sum of price x quantity                                                                                 |
| SAVE10      | 10% off when the subtotal is at least $50                                                               |
| SAVE20      | 20% off when the subtotal is at least $100                                                              |
| FREESHIP    | Shipping is $0                                                                                          |
| NEWUSER     | 15% off, only for `customer_type` `new`                                                                 |
| SUMMER25    | 25% off, accepted until 2026-08-31 inclusive: it stands for the "expired code" case                     |
| Tax         | 8% of subtotal - discount; shipping is not taxed                                                        |
| Shipping    | $0.50 per kg (weight x quantity) + $0.10 per km, x 1.5 for express                                      |
| Rounding    | Each amount is rounded half up to the cent; the total is the sum of the rounded amounts                 |
| Codes       | Case-insensitive, one per order; a code that does not qualify leaves the order as it was                |

Two choices where the homework statement is ambiguous:

- **Minimum order is inclusive.** The rules say "orders > $50", but the provided `apply_discount` skeleton only
  rejects `subtotal < min_order`, so an order of exactly $50.00 qualifies. `save10_at_minimum_order` and
  `save10_below_minimum_order` pin this boundary.
- **Shipping follows the stated rates.** The sample row in the statement expects $5.50 of shipping for 1 kg over
  10 km, but $0.50 x 1 + $0.10 x 10 is $1.50. The data follows the written rates.

## `customer_validation.json`

```json
{
  "reference_date": "2026-11-01",
  "cases": [
    {
      "test_name": "card_expired_last_month",
      "category": "credit_card",
      "customer": {
        "email": "john.doe@example.com",
        "phone": "(555) 123-4567",
        "billing_address": { "street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001" },
        "credit_card": { "number": "4111111111111111", "expiration": "10/2026", "cvv": "123" }
      },
      "expected": { "is_valid": false, "errors": ["Credit card is expired"] }
    }
  ]
}
```

`reference_date` is the "today" every case is validated against, so expiry results do not change as time passes
(the statement's sample card, `12/2025`, would already be expired). A field missing from `customer` is how a
missing value is tested. `expected.errors` lists every message in the order the validator reports them: email,
phone, street, city, state, ZIP, card number, expiration, CVV. `is_valid` must be `true` exactly when `errors` is
empty.

| Category      | Cases | Examples                                                                                           |
| ------------- | ----- | -------------------------------------------------------------------------------------------------- |
| `valid`       | 5     | Visa, American Express with 4-digit CVV, ZIP+4 with a spaced card number, card expiring this month, "St. Louis" |
| `email`       | 6     | No `@`, no domain, `..`, no top-level domain, a space, blank                                       |
| `phone`       | 5     | No parentheses, too few digits, letters, `+1` prefix, missing                                      |
| `address`     | 8     | Blank street, missing city, digits in city, unknown and lowercase state, short and alphabetic ZIP, no address |
| `credit_card` | 11    | Luhn failure, too short, letters, missing number, expired, month 13, 2-digit year, short CVV, 4-digit CVV on Visa, 3-digit CVV on Amex, no card |
| `multiple`    | 7     | Two errors in one section, one per section, a whole blank address or card, an empty customer       |

Validation rules: email `name@domain.tld` without consecutive dots; phone exactly `(XXX) XXX-XXXX`; city made of
letters, spaces, `.`, `'` and `-`; state one of the 50 US state codes or DC, uppercase; ZIP `12345` or
`12345-6789`; card number 13 to 19 digits (spaces and dashes ignored) passing the Luhn check; expiration `MM/YYYY`,
valid through the last day of that month; CVV 3 digits, or 4 for American Express (numbers starting with 34 or 37).

## `order_workflows.json`

```json
{
  "reference_date": "2026-11-01",
  "workflows": [
    {
      "name": "declined_payment_flow",
      "description": "The issuer declines a charge above the available credit, so no confirmation is issued.",
      "gateway": { "available_credit": 50 },
      "steps": [
        { "action": "validate_customer", "data": { "customer": { "...": "..." } }, "expected": { "valid": true, "errors": [] } },
        { "action": "process_payment", "expected": { "status": "declined", "reason": "Payment declined by the card issuer" } },
        { "action": "generate_confirmation", "expected_error": "Order has not been paid" }
      ]
    }
  ]
}
```

Each workflow runs its steps in order against one `Checkout`. `action` is one of `validate_customer`,
`create_order`, `calculate_total`, `process_payment` or `generate_confirmation`; `data` holds the keyword arguments
for that method. A step has either `expected`, the keys its result must contain with those exact values (keys
not listed are not checked), or `expected_error`, the message of the `CheckoutError` it must raise for a step
called out of order. `gateway.available_credit` configures the fake payment gateway: a charge above the remaining
credit is declined, and approved charges get the ids `TXN-0001`, `TXN-0002`, ...

| Workflow                          | What it checks                                                             |
| --------------------------------- | -------------------------------------------------------------------------- |
| `complete_order_flow`             | Validate, order with SAVE10, total, pay with exactly enough credit, confirm |
| `new_customer_express_flow`       | NEWUSER with express shipping and an American Express card                 |
| `invalid_customer_cannot_order`   | An invalid customer is rejected and there is no order to total             |
| `declined_payment_flow`           | The issuer declines the charge, so no confirmation                         |
| `paid_order_is_locked`            | A paid order can be neither paid twice nor replaced                        |
| `rejected_order_is_corrected`     | Invalid orders are rejected, then a corrected order goes through           |
| `customer_is_locked_after_order`  | The customer cannot change once an order exists                            |

## Generated data (bonus A)

`generated_orders.csv` holds 100 valid orders written by `python -m tools.generate_orders`. The generator uses a
fixed seed (2026) for both Faker, which supplies the product colour names, and Python's `random`, which picks
prices, quantities, weights, codes, distances and express shipping, so the same file comes out every time. Faker
is pinned in `requirements.txt` because a different Faker version may produce different names.

The expected amounts in this file come from the current `Order` implementation. It is a regression snapshot: it
detects any change in behaviour, but it cannot show the rules are right, which is what the hand-calculated
`order_calculations.csv` is for. If a rule changes on purpose, regenerate the file and review the diff.

## Validation

`tools/data_files.py` (bonus C) loads every file and checks, before any test runs:

- required columns or keys are present and test names are unique;
- every value has the right type: numbers, `true`/`false`, `YYYY-MM-DD` dates, allowed categories and actions;
- order rows are either calculation or error cases, and `expected_total` adds up;
- customer cases have an `is_valid` that agrees with `errors`;
- every workflow step has exactly one of `expected` or `expected_error`.

Problems are reported together, each with its file and line:

```
Invalid test data:
  order_calculations.csv:14: expected_total 72.0 does not add up to 72.9
  customer_validation.json:15: case 1: missing field 'expected'
```

Check every file without running the tests:

```bash
python -m tools.data_files
```

## Adding a case

1. Add a row (CSV) or an object (JSON) with a new, descriptive `test_name` and the right `category`.
2. Calculate the expected values by hand from the rules above.
3. Run `python -m tools.data_files`, then `python -m pytest`. No test code changes.
