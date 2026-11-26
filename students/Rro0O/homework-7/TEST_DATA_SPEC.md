# Test Data Specification

All files live in `test_data/` and are loaded by `tests/data_loader.py`.
`python src/data_validator.py` checks every rule below and reports `file:line`.

## 1. `order_calculations.csv` (and `generated_orders.csv`)

One row = one order scenario. UTF-8, `\n` line endings, header row required.

| Column              | Type    | Description                                                              |
| ------------------- | ------- | ------------------------------------------------------------------------ |
| `test_name`         | string  | Unique snake_case id; becomes the pytest id                              |
| `items`             | JSON    | List of `{name, price, quantity, weight}` using **single quotes** (quoted in CSV) |
| `customer_type`     | enum    | `new` or `regular`                                                       |
| `discount_code`     | string  | Code to apply, or `NONE`                                                 |
| `distance_km`       | number  | Shipping distance, ≥ 0                                                   |
| `is_express`        | boolean | Literal `true` or `false`                                                |
| `expected_subtotal` | number  | Dollars, 2 decimals                                                      |
| `expected_discount` | number  | Dollars, 2 decimals                                                      |
| `expected_tax`      | number  | Dollars, 2 decimals                                                      |
| `expected_shipping` | number  | Dollars, 2 decimals                                                      |
| `expected_total`    | number  | subtotal − discount + tax + shipping                                     |

Item fields: `name` string, `price` number ≥ 0, `quantity` number ≥ 0, `weight` kg per unit ≥ 0.

Example:

```csv
save10_at_exact_minimum,"[{'name':'Lamp','price':50,'quantity':1,'weight':0}]",regular,SAVE10,0,false,50.00,5.00,3.60,0.00,48.60
```

### Categories (32 cases)

| Category           | Cases | Name prefix / examples                                                       |
| ------------------ | ----- | ---------------------------------------------------------------------------- |
| Simple orders      | 3     | `simple_*`                                                                   |
| Discount validation| 9     | `save10_*`, `save20_*`, `invalid_code_*`, `expired_code_*`, `newuser_*`, `multi_item_*` |
| Tax                | 4     | `tax_*` (rounding, after discount, zero subtotal)                            |
| Shipping           | 8     | `shipping_*` (weight, distance, express, free-ship)                          |
| Complex / edges    | 8     | `complex_*` (zero quantity, empty order, maximum values, fractional weights) |

`generated_orders.csv` has the same columns; its expected values are a
regression snapshot of the calculator (see `src/data_generator.py`).

## 2. `customer_validation.json`

A JSON array of cases:

```json
{
  "test_name": "invalid_email_no_at_sign",
  "customer": { "email": "...", "phone": "...", "billing_address": {"street": "", "city": "", "state": "", "zip": ""},
                "credit_card": {"number": "", "expiration": "MM/YYYY", "cvv": ""} },
  "reference_date": "2026-01-01",
  "expected": { "is_valid": false, "errors": ["Invalid email format"] }
}
```

| Field            | Required | Notes                                                                   |
| ---------------- | -------- | ----------------------------------------------------------------------- |
| `test_name`      | yes      | Unique id                                                               |
| `customer`       | yes      | `billing_address` / `credit_card` may be `null` to test "missing"       |
| `reference_date` | no       | `YYYY-MM-DD` used as "today" for expiration (default `2026-01-01`)      |
| `expected.is_valid` | yes   | boolean; must equal `errors == []`                                      |
| `expected.errors`| yes      | Exact list, **in order**: email, phone, address, card                   |

Error messages: `Invalid email format`, `Invalid phone format`, `Missing billing address`,
`Invalid street`, `Invalid city`, `Invalid state`, `Invalid zip code`, `Missing credit card`,
`Invalid credit card number`, `Invalid expiration format`, `Credit card expired`, `Invalid CVV`.

### Categories (32 cases)

Valid customers 3 · invalid emails 4 · invalid phones 4 · invalid addresses 6 ·
invalid credit cards 8 · multiple errors 7.

## 3. `order_workflows.json`

```json
{
  "reference_date": "2026-01-01",
  "workflows": [
    { "name": "complete_order_flow",
      "steps": [ { "action": "validate_customer", "data": {}, "expected": {"valid": true} } ] }
  ]
}
```

Steps run in order against one `OrderWorkflow` instance. Every key in `expected`
must equal the matching key of the step result (numbers compared to ±$0.005);
extra keys in the result are ignored.

| Action              | `data`                                  | Result keys                                     |
| ------------------- | --------------------------------------- | ----------------------------------------------- |
| `validate_customer` | customer object                         | `valid`, `errors`                               |
| `create_order`      | `{items, customer_type}`                | `status` (`created`/`rejected`), `item_count`/`reason` |
| `apply_discount`    | `{code}`                                | `applied`                                       |
| `set_shipping`      | `{distance_km, is_express}`             | `status`                                        |
| `calculate_total`   | –                                       | subtotal, discount, tax, shipping, total (or rejection) |
| `process_payment`   | –                                       | `status` (`success`/`declined`/`failed`), `charged`/`reason`; limit $10,000 |
| `confirm_order`     | –                                       | `status`, `confirmation_id` (`ORD-000001`), `total` |

7 workflows: complete flow, invalid customer, new-user express, payment declined
over limit, free shipping, empty order, discount below minimum.

## Conventions

- File and case names: lowercase snake_case, prefix = category.
- Add a case by appending a row/object — no Python changes needed.
- Run `python src/data_validator.py` before committing data.
