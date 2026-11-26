# Comparison Report: Traditional vs Data-Driven Tests

This report compares two suites that test the **same ten order scenarios**:

| Suite | File | Where the data lives |
| --- | --- | --- |
| Traditional | `tests/test_order_traditional.py` | Hardcoded inside 10 test functions |
| Data-driven | `tests/test_order_data_driven.py` | `test_data/order_comparison.csv`, run by 1 parameterized test |

The ten scenarios are: `simple_single_item`, `simple_with_standard_shipping`,
`discount_save10_at_threshold`, `discount_save10_below_threshold`,
`discount_save20_at_threshold`, `discount_newuser_new_customer`,
`discount_invalid_code`, `tax_after_discount`, `shipping_express_multiplier` and
`shipping_freeship_code`. Both suites check all five values of every breakdown
(subtotal, discount, tax, shipping, total), so both make 50 checks and both
report 10 test results.

## 1. Lines of Code

The counts were measured with Python's `tokenize` module. "Code lines" leaves
out blank lines, comments and docstrings.

| Metric | Traditional | Data-driven (test file) | Data-driven (test file + CSV) |
| --- | ---: | ---: | ---: |
| Total lines | 127 | 22 | 33 |
| Code lines | 99 | 13 | 24 (13 code + 11 CSV) |
| Test functions | 10 | 1 | 1 |
| `assert` statements written | 50 | 1 (in a loop) | 1 |

**Reduction:**

- Test code: 99 → 13 code lines, **86.9% less**.
- Counting the CSV as part of the cost: 99 → 24 lines, **75.8% less**.

To be fair to the traditional suite, the data-driven file is short partly
because the CSV reading lives in `src/data_loader.py`. That loader is shared by
every data-driven suite in the project (calculator, validator, comparison and
generated orders), so its cost is paid once and not again for each suite.

Each traditional test is about 10 lines and 80% of them are the same in every
test: build the order, apply the code, set shipping, then five `assert` lines.
Only the input values and the five expected numbers change. That repeated
setup is what the data-driven version removes.

## 2. Maintainability

**Adding a new test case**

- *Traditional:* copy one function (about 10 lines), rename it, then edit the
  items, the code, the shipping and five expected numbers. It is easy to forget
  one of the five, and the copied value still passes if it happens to match.
- *Data-driven:* add one CSV row. The validator (`src/data_validation.py`)
  checks the row before any test runs. It rejects a missing column, a value of
  the wrong type, a `test_name` used twice, and a row whose parts do not add up
  to its total. Each problem is reported with its line number, for example
  `order_comparison.csv:7: [expected_total] parts add up to 86.40, not 86.04`.

**Updating existing tests**

- If a business rule changes (for example the tax rate goes from 8% to 9%),
  both suites need new expected values. In the traditional suite they are
  spread over ten functions. In the data-driven suite they are in one column of
  one file, which can be edited in a spreadsheet or regenerated with a script.
- If the API changes (for example `set_shipping` gets a new parameter), the
  traditional suite needs ten edits and the data-driven suite needs one.

## 3. Readability

- **A single scenario** is easier to read in the traditional suite. Everything
  is in one place and written as ordinary Python, and a failure points straight
  at a named function with literal values.
- **The whole set of scenarios** is easier to read in the data-driven suite. The
  CSV is a table, so it is easy to see that SAVE10 is tested at $50.00 and at
  $49.99, or that no case combines NEWUSER with express shipping. In the
  traditional file you have to read ten functions to see that.
- **Failure reports** are equally clear in both. The data-driven suite uses
  `ids=lambda case: case.test_name`, so a failure shows up as
  `test_order_total[discount_save10_at_threshold]` and the assertion message
  names the component that was wrong.
- **Organization:** in the data-driven suite the `category` column groups the
  cases. The full suite has 42 cases in 5 categories, and
  `load_order_cases(category="tax")` selects one group. The traditional suite
  can only group cases by function names or separate files.

## 4. Coverage

| | Traditional | Data-driven |
| --- | --- | --- |
| Scenarios in the comparison | 10 | 10 |
| Scenarios in the whole project | 10 | 42 calculation + 45 customer + 6 workflows + 100 generated orders |
| Time to add 10 more cases | ~100 lines of code, ~15-20 min | 10 CSV rows, ~5 min, no code change |
| Run time (10 cases, measured 3 times) | 0.19-0.20 s | 0.20-0.21 s |

The run times are the same. Most of the time is pytest starting up and
importing modules; ten more parameter sets cost almost nothing. The data-driven
suite also reads and validates a small CSV file, which does not show in the
measurement.

Once the data is external, it is cheap to get much more of it. The project's
own numbers show this:

- `order_calculations.csv` has 42 cases, including 5 negative and invalid inputs
  that must raise `ValueError`. They all run through the same three test
  functions.
- `generated_orders.csv` has **100 orders produced by Faker**. Writing those as
  100 traditional functions would take about 1,000 lines. Here they are covered
  by one regression test and one invariant test.
- Generated data also found a real mismatch. Faker's `state_abbr()` returns
  freely associated states such as `PW` (Palau) and `FM` (Micronesia). The
  validator correctly rejects them because they are not US states. A
  hand-written suite would probably never have tried those values.

## 5. Conclusion

**When to use data-driven tests**

- The same behaviour is checked with many inputs: calculations, validators,
  parsers, business rules or boundary values.
- The expected values come from someone else, such as an analyst's spreadsheet
  or a product specification, and that person should be able to read the cases
  or add new ones without writing Python.
- Large volumes are needed: generated, regression or production-like data.

**When to use traditional tests**

- Each test has its own setup or its own way of asserting, for example "a
  rejected code keeps the previous one" or "the order cannot be paid twice".
  Forcing these into a table means adding columns that only one row uses.
- A very small number of cases, where the extra files and loader cost more than
  they save.
- Tests that document behaviour and should read like an example in the code.

**Pros of data-driven testing**

- Much less duplicated code: 87% fewer lines here.
- Adding a case means adding data, with no code to change.
- The scenarios can be reviewed as a table, so missing cases are easy to spot.
- One validator checks all the data, and the same data can be reused by other
  suites or tools.

**Cons of data-driven testing**

- Data and logic are in two places, so understanding a failure means reading
  both.
- It needs extra infrastructure: a loader, parsing, and ideally validation of
  the data files.
- Data files have no type checking. Without the validator, a typo such as
  `ture` in `is_express` would silently become `False`.
- Cases with unusual setup do not fit the table and need separate tests anyway.
  `test_order_calculator.py` has 79 test runs that come from the CSV. Next to
  them it has two plain tests (a rejected code keeps the previous one, an
  accepted code replaces it) and three small tables kept in the test file:
  `apply_discount` return values, expiration dates and malformed items.

In this project both styles are used together. Data-driven tests cover anything
that is "the same check with different numbers", and plain tests cover the few
behaviours that are about the sequence of events rather than the values.
