# Test Data Specification

All test data lives in `test_data/`. The tests never hardcode these cases. They
load them through `src/data_loader.py`, which first runs the checks in
`src/data_validation.py` and stops with a line-numbered report if a file is
broken. To check the files without running the tests:

```bash
python -m src.data_validation
```

| File | Format | Cases | Used by |
| --- | --- | ---: | --- |
| `order_calculations.csv` | CSV | 42 | `tests/test_order_calculator.py` |
| `order_comparison.csv` | CSV (same schema) | 10 | `tests/test_order_data_driven.py` |
| `generated_orders.csv` | CSV (same schema) | 100 | `tests/test_data_generator.py` |
| `customer_validation.json` | JSON | 45 | `tests/test_customer_validator.py` |
| `order_workflows.json` | JSON | 6 workflows, 37 steps | `tests/test_integration.py` |

---

## 1. `order_calculations.csv`

One row per order. The first line is the header. Text that contains commas,
such as the `items` column, is wrapped in double quotes.

| Column | Type | Rules |
| --- | --- | --- |
| `test_name` | text | Required and unique. Used as the pytest id. Format: `<category>_<what is tested>`. |
| `category` | enum | `simple`, `discount`, `tax`, `shipping`, `complex` (`generated` is only used in `generated_orders.csv`). |
| `items` | JSON list | `[{'name':str,'price':number,'quantity':int,'weight':number}]`. Single quotes are used so the CSV stays readable; the loader turns them into `"` before parsing. `weight` is **per unit**, in kg. `[]` is an empty cart. |
| `customer_type` | enum | `new` or `regular`. |
| `discount_code` | text | A code as the customer would type it (case-insensitive), or `NONE`. Unknown and expired codes are allowed on purpose. |
| `distance_km` | number | Shipping distance. Decimals are allowed. |
| `is_express` | bool | Exactly `true` or `false`. |
| `expected_subtotal` … `expected_total` | number | The five amounts of the breakdown, in dollars with 2 decimals. They must satisfy `subtotal - discount + tax + shipping = total` (±0.005). |
| `expected_error` | text | Empty for a normal case. Otherwise, part of the `ValueError` message the order must raise, and the five expected columns must be empty. |

Example:

```csv
test_name,category,items,customer_type,discount_code,distance_km,is_express,expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total,expected_error
discount_save10_at_threshold,discount,"[{'name':'Headphones','price':50,'quantity':1,'weight':0}]",regular,SAVE10,0,false,50.00,5.00,3.60,0.00,48.60,
complex_negative_price,complex,"[{'name':'Refund','price':-10,'quantity':1,'weight':1}]",regular,NONE,10,false,,,,,,price cannot be negative
```

### Calculation rules used to compute the expected values

| Rule | Detail |
| --- | --- |
| Subtotal | Σ price × quantity |
| SAVE10 | 10% off when the subtotal is **at least** $50.00 (exactly $50.00 qualifies) |
| SAVE20 | 20% off when the subtotal is at least $100.00 |
| NEWUSER | 15% off, only for `customer_type = new` |
| FREESHIP | Shipping becomes $0, even for express |
| `SUMMER25`, `BLACKFRIDAY` | Expired campaign codes (2025), so no discount |
| Codes | Codes do not stack. A rejected code keeps the code already applied. |
| Tax | 8% of (subtotal − discount) |
| Shipping | ($0.50 × total kg + $0.10 × km) × 1.5 when express |
| Rounding | Each amount is rounded to cents, half up. The total is the sum of the rounded parts. |
| Invalid input | A negative price, quantity, weight or distance, or a non-integer quantity, raises `ValueError` |

The expected values were calculated by hand from these rules. They were then
checked with a separate script that uses Python fractions and does not use the
project code.

**Note about the assignment's sample row.** The sample in the assignment
(`simple_order`: 1 kg, 10 km, `expected_shipping 5.50`) does not match the
stated rules: $0.50 × 1 + $0.10 × 10 = **$1.50**. This data follows the rules,
so that scenario appears as `simple_with_standard_shipping` with shipping 1.50
and total 55.50.

### Categories and minimums

| Category | Required | Present | What it covers |
| --- | ---: | ---: | --- |
| simple | 3 | 4 | Single item, quantity > 1, several items, plain shipping |
| discount | 5 | 12 | Each code at and below its threshold, NEWUSER for the wrong customer type, invalid, expired and lowercase codes, several items |
| tax | 4 | 5 | Rounding up and down, tax after a discount, empty order, large amounts |
| shipping | 6 | 9 | Weight only, distance only, both, express, express rounding half up (two cases, one where binary floats would round down), FREESHIP, FREESHIP with express, decimal distance |
| complex | 7 | 12 | Carts with several items and a discount, zero quantity, all quantities zero, free item, maximum values, negative price, quantity, weight and distance, fractional quantity |

---

## 2. `customer_validation.json`

A JSON **list** of test cases:

```json
{
  "test_name": "invalid_card_expired_last_month",
  "category": "invalid_card",
  "description": "Boundary: expired the month before the reference date",
  "reference_date": "2026-06-15",
  "customer": {
    "email": "john@example.com",
    "phone": "(555) 123-4567",
    "billing_address": {"street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001"},
    "credit_card": {"number": "4532015112830366", "expiration": "05/2026", "cvv": "123"}
  },
  "expected": {"is_valid": false, "errors": ["Credit card is expired"]}
}
```

| Field | Rules |
| --- | --- |
| `test_name` | Required and unique |
| `category` | `valid`, `invalid_email`, `invalid_phone`, `invalid_address`, `invalid_card`, `multiple_errors` |
| `description` | Optional, free text. It is shown in the assertion message. |
| `reference_date` | Optional ISO date used as "today" for the expiration check, so the results do not depend on the day the tests run. If it is missing, the real date is used. |
| `customer` | The object given to `validate_customer`. Keys can be missing or `null` on purpose. |
| `expected.is_valid` | Boolean. It must be `true` exactly when `errors` is empty. |
| `expected.errors` | The **exact, ordered** list of messages |

### Validation rules and error messages

Errors are reported in this order: email, phone, address, card.

| Field | Rule | Message |
| --- | --- | --- |
| email | missing or blank | `Email is required` |
| email | `local@domain.tld`: no spaces, no `..`, a top-level domain of 2 or more letters, at most 254 characters | `Invalid email format` |
| phone | missing or blank | `Phone is required` |
| phone | exactly `(XXX) XXX-XXXX`, area code starting with 2-9 | `Invalid phone format` |
| billing_address | missing or not an object | `Billing address is required` |
| street | missing or blank | `Street is required` |
| city | missing or blank / letters, spaces and `.'-` only | `City is required` / `Invalid city` |
| state | one of the 50 state codes or `DC`, in upper case | `Invalid state` |
| zip | `12345` or `12345-6789` | `Invalid ZIP code` |
| credit_card | missing or not an object | `Credit card is required` |
| number | 13-19 digits (spaces and dashes allowed) that pass the Luhn check | `Invalid credit card number` |
| expiration | `MM/YYYY` with a month from 01 to 12 | `Invalid expiration date format` |
| expiration | earlier than the reference month (a card is good through its expiration month) | `Credit card is expired` |
| cvv | 4 digits for American Express (34/37), 3 for all other cards | `Invalid CVV` |

### Categories and minimums

| Category | Required | Present |
| --- | ---: | ---: |
| valid | 3 | 7 |
| invalid_email | 4 | 6 |
| invalid_phone | 4 | 5 |
| invalid_address | 5 | 8 |
| invalid_card | 8 | 12 |
| multiple_errors | 6 | 7 |

Card numbers are published test numbers: Visa `4532015112830366`, Mastercard
`5555555555554444`, Amex `378282246310005`, Discover `6011111111111117`. The
"too short" and "too long" cases use numbers that **pass** the Luhn check, so
they fail only because of their length.

---

## 3. `order_workflows.json`

```json
{
  "reference_date": "2026-06-15",
  "workflows": [
    {
      "name": "complete_order_flow",
      "description": "...",
      "steps": [
        {"action": "create_order", "data": {"items": [...], "discount_code": "SAVE10"}, "expected": {"status": "created"}}
      ]
    }
  ]
}
```

- `reference_date` is optional and is passed to `OrderProcessor(today=...)`.
- Each `action` is an `OrderProcessor` method. `data` holds its keyword
  arguments and can be left out when there are none.
- `expected` lists **only the fields that matter at that step**. Other fields
  in the result are ignored. Numbers are compared to the cent.

| Action | `data` | Result fields |
| --- | --- | --- |
| `validate_customer` | `customer` | `valid`, `errors` |
| `create_order` | `items`, `customer_type`, `discount_code`, `distance_km`, `is_express` | `status` (`created`/`rejected`), `order_id`, `discount_applied`, `error` |
| `apply_discount` | `code` | `applied`, `discount_code`, `error` |
| `calculate_total` | — | `status` (`calculated`/`error`), `subtotal`, `discount`, `tax`, `shipping`, `total` |
| `process_payment` | `amount` (optional) | `status` (`success`/`declined`/`failed`), `transaction_id`, `amount`, `error` |
| `generate_confirmation` | — | `status` (`confirmed`/`error`), `confirmation_number`, `email`, `total`, `items` |

Card numbers `4000000000000002` and `5105105105105100` are valid but are
declined by the simulated payment gateway.

| Workflow | Scenario |
| --- | --- |
| `complete_order_flow` | Happy path with SAVE10, payment and confirmation |
| `new_user_express_flow` | NEWUSER with express shipping, and paying twice is refused |
| `invalid_customer_blocks_checkout` | A customer with 3 errors cannot order, pay or get a confirmation |
| `declined_card_flow` | A well-formed card is declined, so there is no confirmation |
| `retry_discount_and_payment_amount` | An invalid code, then FREESHIP (which requires recalculating), then a wrong amount, then a correct one |
| `invalid_order_data_rejected` | Negative quantity and negative distance are rejected, then a corrected order goes through |

---

## 4. `generated_orders.csv` (bonus)

This file is produced by `python -m src.data_generator` (Faker, seed 2026). It
uses the same schema as `order_calculations.csv` with `category = generated`.
Its expected values were calculated by the `Order` class when the file was
created, so it works as a **golden master**: the regression test fails if a
later change to the calculator changes any amount. The invariant test also
checks properties that do not depend on the implementation, such as tax being
8% of the net amount and FREESHIP meaning free shipping.

Only regenerate this file when a pricing change is intended, and review the
diff before committing it.
