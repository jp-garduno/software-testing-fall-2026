# Traditional vs Data-Driven Testing: Comparison Report

Both suites test the same 10 order scenarios (simple order, SAVE10 and SAVE20 at their thresholds, an invalid code,
NEWUSER, tax after discount, weight + distance shipping, express shipping, FREESHIP overriding express, and a complex
SAVE20 + express order). The traditional version, `tests/test_order_traditional.py`, has 10 test functions with every
input and expected value in the body. The data-driven version, `tests/test_order_data_driven.py`, is one parametrized
function reading the same 10 scenarios from `test_data/comparison_orders.csv`. Both pass (10 tests each).

## 1. Lines of Code

Counted with `python tools/count_loc.py` (non-blank, non-comment lines; docstrings count).

| What is counted                                                          | Lines | Reduction vs traditional |
| ------------------------------------------------------------------------ | ----- | ------------------------ |
| Traditional test file                                                    | 151   | -                        |
| Data-driven test file only                                               | 8     | 94.7%                    |
| Data-driven test file + its CSV (10 rows + header)                       | 19    | 87.4%                    |
| Data-driven test file + CSV + the CSV-order loader functions it relies on | 57    | 62.3%                    |

The loader (38 lines of functions in `tests/data_loader.py`) is shared by the order, Excel and comparison suites, so
its cost is paid once, not per test file. The honest per-suite figure is the second or third row. The fair general
statement is that code grows with the number of *kinds* of test, while data grows with the number of *cases*.

Scaling: the traditional file costs about 15 lines per scenario ((151 - 3 header lines) / 10). The full order suite has
38 scenarios; written the traditional way it would be roughly 560 lines, against 38 CSV rows and the same 8-line test.
That figure is an estimate from the 15-line average, not a measurement.

## 2. Maintainability

**Adding a case.** Traditional: copy a 15-line test, rename it, edit the items and five expected numbers; the data
and the logic are interleaved, so a typo in an expected value is easy to make. Data-driven: add one CSV row. The row has
a unique name that becomes the test id, and `test_shipped_data_files_have_no_problems` reports the line number if the
row is malformed.

**Updating an existing case.** Both need the expected numbers changed when a business rule changes (for example, a 9%
tax rate makes the `tax` and `total` values wrong in every scenario). The numbers are the same either way; the
difference is where they live. In the traditional suite they are scattered over 150 lines of code, in the data-driven
one they are two columns of one file that can be reviewed as a table.

**Changing how a check is made** (say, also asserting a new field of the result). Traditional: edit 10 test bodies.
Data-driven: edit one function (plus a column). This is where data-driven helps most.

**Costs of the data-driven approach that I hit:**

- The test body is no longer self-contained. To understand a failure you open the CSV, and a failure in
  `test_order_calculation[save10_at_minimum_threshold]` tells you the case name, not which hard-coded number was wrong.
- The data needs its own validation. A malformed row fails with a parsing error rather than an assertion, which is
  why I added `src/data_validator.py`, which reports problems with line numbers.
- Data files need the same discipline as code. The assignment's own sample row had a shipping value (5.50 for 1 kg and
  10 km) that contradicts its written rules (1.50), and its `items` cell was not valid JSON; see `TEST_DATA_SPEC.md`.
- Two copies of the same data drift apart. The Excel workbook is generated from the CSV, and a test fails if they
  disagree.

## 3. Readability

The traditional tests read well one at a time: the scenario, the inputs and the answer are all in view, and the test name
describes it. That also makes them tedious in bulk; 10 near-identical 15-line bodies hide the one line that differs.
The data-driven version is the reverse: the logic is readable at a glance (build order, apply code, set shipping, compare
five numbers) and the scenarios read as a table, where differences between rows are obvious. Organisation is better too:
a `category` column groups scenarios, and in the Excel version each category has its own sheet. For readers who need
to see the whole scenario in the failing test itself, traditional is easier.

## 4. Coverage

- **Scenarios**: the comparison suites cover 10 scenarios each. The full data-driven order suite covers 38 (including 7
  invalid-input cases), plus the same data re-run from Excel; customer validation covers 48 scenarios and the workflows
  5. Producing the 38 order scenarios in the traditional style would have been impractical to review.
- **Code coverage**: all suites together reach 100% statement and 100% branch coverage of `src/` (384 statements, 132
  branches). Each 10-scenario comparison suite alone reaches 79% of `order_calculator.py` and 17% of `src/` overall; the
  paths it misses are the input-validation errors, which the 7 `error` rows and the other suites add.
- **Time to add 10 more cases**: by my line counts, about 150 lines of new test code in the traditional style, against
  10 new CSV rows (10 lines) with no new code in the data-driven style. I did not time this with a stopwatch.
- **Run time**: both comparison suites take 0.01 s (10 tests). My first data-driven run was about ten times slower
  (0.06-0.15 s), but the cause was not the technique: `data_loader.py` imported `openpyxl` at the top, which costs more
  than the tests themselves even when only a CSV is read. Importing it lazily inside the Excel reader removed the
  difference. Data-driven testing adds no per-test overhead here; loading data can, so keep loaders light.

## 5. Conclusion

**Use traditional tests** for a few distinct behaviours, for scenarios that need setup the data cannot express (mocks,
state, ordering), and when a failing test should explain itself without opening another file.

**Use data-driven tests** when the same logic must be checked against many input/expected pairs: calculators,
validators, parsers, boundary tables. In this project that is the order calculator (38 rows) and the customer
validator (48 objects).

| Pros of data-driven                                              | Cons of data-driven                                              |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| Adding scenarios is cheap and needs no new code                  | Test body is separated from its data                             |
| Logic changes in one place                                       | Data files need validation and review like code                  |
| Scenarios read as a table, so gaps and duplicates stand out      | Failures point to a case name, not to the offending line         |
| Non-programmers can contribute or review cases                   | Complex setup does not fit in a row                              |
| The same data can drive other formats (CSV, JSON, Excel)         | Expected values are still only as good as whoever calculated them |

The last row matters most. Data-driven testing makes it easy to add many cases, not to make them correct. I calculated
the expected values by hand instead of generating them from the code under test; had I generated them from the
calculator, every test would have passed and proved nothing. As a check that the data really catches defects, I changed
eight single values or operators in `src/` (tax rate, weight rate, express multiplier, rounding mode, the inclusive
minimum order, the Luhn parity, the expiry boundary, the CVV length) and the suite failed for every one.
