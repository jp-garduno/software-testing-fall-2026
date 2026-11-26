# Test data specification

Four files in `test_data/`. Three are the contract the tests verify; the
fourth is a generated regression set.

| File | Format | Rows/cases | Brief's minimum | What it defines |
| --- | --- | --- | --- | --- |
| `order_calculations.csv` | CSV | 35 | 25 | Amounts for each order |
| `customer_validation.json` | JSON | 39 | 30 | Customer validation |
| `order_workflows.json` | JSON | 5 | 3 | End-to-end workflows |
| `generated_orders.csv` | CSV | 100 | — | Generated regression set (bonus A) |

---

## `order_calculations.csv`

One row is a complete order with its five expected amounts.

| Column | Type | What it holds |
| --- | --- | --- |
| `test_name` | text | Unique identifier; shows up in the pytest output |
| `category` | text | One of `simple`, `discount`, `tax`, `shipping`, `complex` |
| `items` | JSON | List of articles, each with `name`, `price`, `quantity`, `weight` |
| `customer_type` | text | `regular` or `new` |
| `discount_code` | text | The code, or `NONE` to attempt none |
| `distance_km` | number | Shipping distance |
| `is_express` | text | `true` or `false`, lowercase |
| `expected_subtotal` | number | Expected amounts, two decimals |
| `expected_discount` | number | |
| `expected_tax` | number | |
| `expected_shipping` | number | |
| `expected_total` | number | |
| `expected_error` | text | Expected `ValueError` message; empty when the order is valid |

**The `items` column is JSON inside a CSV cell.** Double quotes are doubled,
which is how the CSV standard escapes them:

```csv
"[{""name"": ""Notebook"", ""price"": 25.0, ""quantity"": 1, ""weight"": 0.0}]"
```

The example in the brief uses `[{name:Item1,price:50,...}]`, with unquoted
keys. That is neither valid JSON nor a valid Python literal, so it cannot be
read with `json.loads` or with `ast.literal_eval`. JSON is used here because
`csv` and `json` are both in the standard library and `json.loads` executes
nothing it reads, unlike `eval`.

**When `expected_error` carries text, the five amount columns are empty.** That
row asserts that building the order raises `ValueError` with that exact
message, and never gets as far as computing anything.

**Split by category**, against the brief's minimums:

| Category | Rows | Minimum |
| --- | --- | --- |
| `simple` | 4 | 3 |
| `discount` | 8 | 5 |
| `tax` | 5 | 4 |
| `shipping` | 8 | 6 |
| `complex` | 10 | 7 |

---

## `customer_validation.json`

```json
{
  "description": "...",
  "reference_date": "2026-11",
  "test_cases": [
    {
      "test_name": "valid_standard",
      "category": "valid_customers",
      "customer": { "email": "...", "phone": "...", "address": {...},
                    "card_number": "...", "card_expiry": "MM/YY" },
      "expected_valid": true,
      "expected_errors": [],
      "reason": "Every field well formed"
    }
  ]
}
```

`expected_errors` is the **complete list, in order**, not a subset. The order
is fixed by `validate_customer`: email, phone, street, city, state, zip, card
number, card expiry. The tests compare the whole list, so a row expecting one
error does not pass if the code returns three.

`reference_date` exists because a card's expiry depends on what day it is. If
the validator used `datetime.now()`, a `12/26` card would be valid this year
and stop being valid the next, and the suite would start failing on its own
without anyone touching it. The reference date is fixed in
`customer_validator.py` as data, not as a clock.

**Split by category**:

| Category | Cases | Minimum |
| --- | --- | --- |
| `valid_customers` | 5 | 3 |
| `invalid_emails` | 6 | 4 |
| `invalid_phones` | 5 | 4 |
| `invalid_addresses` | 7 | 5 |
| `invalid_cards` | 9 | 8 |
| `multiple_errors` | 7 | 6 |

---

## `order_workflows.json`

Each workflow chains customer validation, discount, shipping and calculation.

```json
{
  "workflow_name": "checkout_regular_with_save20",
  "description": "...",
  "customer": { ... },
  "items": [ ... ],
  "customer_type": "regular",
  "steps": [
    { "action": "validate_customer", "expected_result": true },
    { "action": "apply_discount", "code": "SAVE20", "expected_result": true },
    { "action": "set_shipping", "distance_km": 40, "is_express": false },
    { "action": "calculate_total" }
  ],
  "expected_customer_valid": true,
  "expected_discount_applied": true,
  "expected_order": { "subtotal": ..., "discount": ..., "tax": ..., "shipping": ..., "total": ... },
  "expected_outcome": "confirmed"
}
```

`expected_outcome` is `confirmed` only when the customer passes validation. A
workflow with `rejected_customer` still carries its amounts: the order is
computed but not confirmed, and one test verifies that rejecting the customer
does not change any amount.

The five workflows cover: happy path with a discount, new customer with
express, customer rejected over an invalid card, discount rejected on amount,
and `FREESHIP` over shipping that would otherwise have been expensive.

---

## `generated_orders.csv`

One hundred orders produced by `src/data_generator.py` with a seeded random.
The same seed always gives the same file, so the CSV can be regenerated and
compared byte for byte.

```bash
PYTHONPATH=src python src/data_generator.py
```

**This data is different from the other three files and the difference
matters.** Its expected values come from running the calculator itself, so they
assert *that the behaviour has not changed*, not *that the behaviour is
correct*. They are a snapshot for catching regressions. The correctness check
lives in `order_calculations.csv`, whose amounts were computed with a formula
written separately, from the text of the brief, and then cross-checked against
the implementation.

That is why the tests in `test_data_generator.py` assert no amounts: they check
that the orders are valid, that there is variety in codes and modes, and that
the file can be read back.

---

## Validating the data

`src/data_validator.py` checks the files before they are used and reports every
problem with file, line and column:

```
order_calculations.csv:14 [expected_subtotal]: 'lots' is not a number
customer_validation.json [test_cases[7]]: a valid case cannot list expected errors
```

What it checks: missing columns, duplicated names, unknown categories, badly
written booleans, numbers that are not numbers, `items` that is not JSON or is
missing fields, and in the JSON that a valid case declares no errors and an
invalid one does.

```python
from data_validator import require_valid_data
require_valid_data("test_data")   # raises DataValidationError with everything at once
```

## Adding cases

For order amounts, one line in `order_calculations.csv`. For customers, one
object in `test_cases`. In both cases no test file needs touching: the suite
walks whatever it finds.

The only file that does need touching is `tests/test_order_data_driven.py`, and
only if the new case should take part in the Part 3 comparison, because that
file picks ten scenarios by name on purpose.
