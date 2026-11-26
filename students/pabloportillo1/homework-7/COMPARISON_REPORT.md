# Comparison Report: Traditional vs Data-Driven Tests

Both suites test the same 10 order scenarios against `Order.calculate_total()`:

- [tests/test_order_traditional.py](tests/test_order_traditional.py): 10 test functions, each with its own
  hard-coded items, code, shipping and expected breakdown.
- [tests/test_order_data_driven.py](tests/test_order_data_driven.py): one test function, parametrized with the 10
  rows of [test_data/order_comparison.csv](test_data/order_comparison.csv).

| Scenario                     | Covers                                  |
| ---------------------------- | --------------------------------------- |
| simple_single_item           | No code, tax only                       |
| save10_at_minimum_order      | SAVE10 at exactly $50                   |
| save10_below_minimum_order   | SAVE10 at $49.99                        |
| save20_at_minimum_order      | SAVE20 at exactly $100                  |
| newuser_on_first_order       | NEWUSER for a new customer              |
| newuser_for_regular_customer | NEWUSER refused for a regular customer  |
| unknown_code_gives_no_discount | Unknown code                          |
| shipping_weight_counts_quantity | Weight x quantity plus distance      |
| express_shipping_costs_half_more | Express multiplier                  |
| freeship_removes_shipping    | FREESHIP                                |

Both versions pass, 10 tests each, and both run in 0.07 s, so speed is not a difference at this size.

## 1. Lines of Code

Counted as non-blank lines.

| What                                                        | Traditional | Data-driven |
| ----------------------------------------------------------- | ----------- | ----------- |
| Test file                                                   | 58          | 7           |
| Shared helper `tests/order_cases.py` (builds an `Order` from a row) | -   | 11          |
| Test data `order_comparison.csv` (header + 10 rows)         | -           | 11          |
| **Total written for this comparison**                       | **58**      | **29**      |

- Test code only: 58 to 7 lines, an **88% reduction**.
- Test code plus the helper: 58 to 18 lines, a **69% reduction**.
- Everything, data included: 58 to 29 lines, a **50% reduction**.

The table leaves out one real cost: `tools/data_files.py`, 282 lines that load and validate the CSV and JSON
files. It is written once and shared by all five data-driven test files in this homework, so it does not belong to
any one of them, but a project with a single small data-driven suite would pay for it alone. The loader could be
10 lines without validation; most of its size is the error reporting described in
[TEST_DATA_SPEC.md](TEST_DATA_SPEC.md#validation).

The traditional file repeats the same four steps ten times: 10 `Order(...)` calls, 10 `set_shipping` calls,
7 `apply_discount` calls and 10 dictionaries of expected amounts. The data-driven file writes those steps once.

## 2. Maintainability

**Adding a case.** Traditional: copy a function (about 9 lines with blank lines), rename it, and change the items,
the code, the shipping and five expected amounts, all inside Python. Data-driven: add one CSV line. Nothing in the
test code changes, and `python -m tools.data_files` checks the new row before the test runs, including that the
expected total adds up.

**Changing the API.** If `set_shipping` were renamed, the traditional suite needs 10 edits and the data-driven one
needs 1, in `build_order`. The same holds for any change in how an order is built.

**Changing a rule.** If the tax rate went from 8% to 10%, both suites need the tax and total of every affected
case recalculated: 10 dictionaries in Python versus 2 columns in a CSV. The data-driven version does not save the
arithmetic, but the values sit side by side in a table where they are easy to review and to check against each
other.

**Reviewing changes.** A new data-driven case is a one-line diff in a data file. A new traditional case is a new
function that the reviewer has to read in full to be sure it really follows the same steps as the others.

## 3. Readability

**One case on its own** reads better in the traditional style. Everything is in one function, with named Python
values, and a reader who has never seen the suite understands it immediately.

**The suite as a whole** reads better data-driven. The CSV is a table: the 10 scenarios line up in columns, so
it is obvious that the SAVE10 cases differ only in the price, and a missing scenario (say, SAVE20 just below $100)
is easy to spot. In the traditional file the same comparison means reading 10 functions and diffing them mentally.

**Organisation.** The data-driven suite separates the *how* (one test function, one helper) from the *what* (rows
with a category column). Failure output stays clear because each row becomes its own test with its name as the
pytest id:

```
tests/test_order_data_driven.py::test_calculate_total_returns_expected_breakdown[save10_at_minimum_order] FAILED
```

The weak spot is the items column: a JSON list inside a CSV cell is the hardest part of the file to read. Orders
with several items (see `order_calculations.csv`) make long lines, and JSON would read better for them.

## 4. Coverage

Both suites test the same 10 scenarios, so they cover the same code. The difference is how far each one scales:

| Suite                         | Test functions | Scenarios                |
| ----------------------------- | -------------- | ------------------------ |
| Traditional                   | 10             | 10                       |
| Data-driven (comparison)      | 1              | 10                       |
| `test_order_calculator.py`    | 3 (+1 unit)    | 43 rows x 1-2 checks = 76 tests |
| `test_generated_orders.py`    | 1 (+1)         | 100 generated orders     |

`test_order_calculator.py` uses the same pattern on 43 hand-calculated rows with three test functions; the
traditional style would need about 76 functions for the same checks. Writing 10 more scenarios takes about
90 lines of Python in the traditional style and 10 lines of CSV in the data-driven style; in both, most of the
time goes into calculating the expected amounts by hand, which is the same work in either style.

## 5. Conclusion

**Use data-driven tests when** many cases run the same steps and differ only in inputs and expected outputs:
calculations, validation rules, boundary values, parsers. That describes most of this homework, which is why five
of its test files are data-driven.

**Use traditional tests when** each test needs its own setup or its own kind of assertion, when there are only a
few cases, or when the scenario is easier to understand as code than as a row. In this homework that is the one
plain unit test in `test_order_calculator.py`, which checks that a rejected code keeps the code already applied:
it needs two `apply_discount` calls and an assertion on the order's state, which no CSV column describes well.

| Pros of data-driven testing                                         | Cons of data-driven testing                                       |
| ------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Far less test code; one place to change when the API changes        | A loader and a data format to design, document and maintain       |
| A new case is one row, writable by someone who does not know Python | Logic hidden behind one test function is harder to debug          |
| Cases are a table that is easy to review and compare                | Nested data (item lists) is awkward in CSV                        |
| The same data can feed other tools: the validator, the generator    | Bad data fails tests in confusing ways unless it is validated     |
| Scales to hundreds of cases (100 generated orders here)             | Branching on the data ("if this row expects an error") creeps in; here error rows get their own test function to avoid it |

The data-driven style wins clearly for this system, but it is not free: its benefit grows with the number of
cases, while its cost (the loader, the data format, the validation) is paid up front.
