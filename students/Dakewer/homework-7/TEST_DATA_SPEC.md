# Test Data Specification

All files live in `test_data/` and are loaded with paths relative to the
tests (`Path(__file__)`), so tests run from any working directory.
`python tools/validate_test_data.py` checks every rule below.

## 1. `order_calculations.csv`

One row per order scenario. UTF-8, comma separated, header required, values
containing commas or quotes are CSV-quoted (`"` doubled).

| Column | Type | Description |
|---|---|---|
| `test_name` | string | Unique id, `<category>_<scenario>`; used as the pytest id |
| `items` | JSON list | `[{"name": str, "price": number, "quantity": int, "weight": number}]` |
| `customer_type` | `new` \| `regular` | Customer kind (matters for `NEWUSER`) |
| `discount_code` | string | Code to apply, or `NONE` for no code |
| `distance_km` | number >= 0 | Shipping distance |
| `is_express` | `true` \| `false` | Express shipping flag (lower case) |
| `expected_subtotal` | number | Sum of price x quantity |
| `expected_discount` | number | Discount amount in dollars |
| `expected_tax` | number | 8% of (subtotal - discount) |
| `expected_shipping` | number | Shipping cost |
| `expected_total` | number | subtotal - discount + tax + shipping |
| `expected_error` | string, optional | Empty normally; `ValueError` when constructing the order must fail (numeric `expected_*` are then `0.00` and ignored) |

Amounts are in dollars with two decimals and compared within half a cent.

**Categories (name prefix) and counts:** `simple_` 3, `discount_` 9,
`tax_` 4, `shipping_` 8, `complex_` 10 (including 3 error cases) = 34.

**Example**

```csv
shipping_express,"[{""name"":""Item1"",""price"":50,""quantity"":1,""weight"":1}]",regular,NONE,10,true,50.00,0.00,4.00,2.25,56.25,
```

Shipping here = (1 kg x $0.50 + 10 km x $0.10) x 1.5 = $2.25.

### Derived files with the same format

- `comparison_cases.csv` - the 10 rows used in Part 3.
- `generated_orders.csv` - 100 rows from `tools/generate_orders.py`
  (names `generated_order_001` ...).

## 2. `customer_validation.json`

A JSON array of objects:

```json
{
  "test_name": "invalid_phone_digits_only",
  "category": "phone",
  "customer": { "email": "...", "phone": "5551234567",
                "billing_address": {"street": "...", "city": "...", "state": "NY", "zip": "10001"},
                "credit_card": {"number": "...", "expiration": "MM/YYYY", "cvv": "123"} },
  "expected": { "is_valid": false, "errors": ["Invalid phone format"] }
}
```

| Field | Rule |
|---|---|
| `test_name` | unique |
| `category` | `valid`, `email`, `phone`, `address`, `credit_card` or `multiple` |
| `customer` | input given to `validate_customer`; fields may be missing or wrong on purpose |
| `expected.is_valid` | boolean; must be `true` exactly when `errors` is empty |
| `expected.errors` | list of messages, **in validator order**: email, phone, street, city, state, zip, card number, expiration, CVV |

Tests use a fixed reference date, **2025-01-15**, so `12/2025` is valid and
`12/2024` is expired regardless of when the tests run.

Error messages: `Invalid email format`, `Invalid phone format`,
`Invalid street address`, `Invalid city`, `Invalid state`,
`Invalid zip code`, `Invalid credit card number`,
`Invalid expiration date` (bad format), `Credit card expired`,
`Invalid CVV`.

Counts: valid 4, email 6, phone 5, address 7, credit_card 9, multiple 6 = 37.

Format rules: email `local@domain.tld`; phone `(XXX) XXX-XXXX`; state a
2-letter US code (upper case, incl. DC); zip `12345` or `12345-6789`;
card 13-19 digits (spaces/hyphens allowed) passing Luhn; expiration `MM/YYYY`
(valid through the end of that month); CVV 3-4 digits.

## 3. `order_workflows.json`

```json
{
  "reference_date": "2025-01-15",
  "workflows": [
    { "name": "complete_order_flow",
      "description": "...",
      "steps": [ {"action": "validate_customer", "data": {...}, "expected": {...}} ] }
  ]
}
```

| Field | Rule |
|---|---|
| `reference_date` | `YYYY-MM-DD`, the "today" of the workflow engine |
| `steps[].action` | one of the actions below |
| `steps[].data` | optional input for the action |
| `steps[].expected` | **subset** of the result that must match (floats within half a cent) |

State carries from step to step (customer, order, totals, payment).

| Action | `data` | Result keys |
|---|---|---|
| `validate_customer` | customer object | `valid`, `errors` |
| `create_order` | `{customer_type, items}` | `status` (`created`/`rejected`), `item_count` or `reason` |
| `apply_discount` | `{code}` | `applied` |
| `set_shipping` | `{distance_km, is_express}` | `status` |
| `calculate_total` | - | `subtotal, discount, tax, shipping, total` |
| `process_payment` | - | `status` (`success`/`declined`/`rejected`), `amount` or `reason` |
| `generate_confirmation` | - | `status` (`confirmed`/`rejected`), `confirmation_number`, `email`, `total` |

Payments above $10,000 are declined (`amount exceeds limit`).

Workflows: `complete_order_flow`, `invalid_customer_blocks_order`,
`high_value_order_payment_declined`, `freeship_express_order`,
`discount_below_minimum_rejected`, `new_user_first_order`.

## 4. Adding new data

1. Append a row/object following the tables above.
2. Run `python tools/validate_test_data.py` - it reports problems as
   `file:line: message`.
3. Run `python -m pytest`.
