# Comparison Report: Traditional vs Data-Driven Testing

Both suites cover the **same 10 scenarios** of the order calculator:
`tests/test_order_traditional.py` hard-codes inputs and expected values in 10
functions; `tests/test_order_data_driven.py` is one parametrized test that
reads the 10 scenarios by name from `test_data/order_calculations.csv`.

## 1. Lines of Code

Counted as non-blank, non-comment lines (`wc -l` totals in parentheses).

| Suite                  | Code LOC | Total lines | Notes                                          |
| ---------------------- | -------- | ----------- | ---------------------------------------------- |
| Traditional (10 tests) | 52       | 79          | data inline, shared `calc`/`check` helpers     |
| Data-driven (10 cases) | 30       | 36          | plus 10 rows in the CSV                        |
| Shared `data_loader.py`| 54       | 69          | written once, reused by all 5 data-driven files |

**Reduction:** (52 − 30) / 52 ≈ **42%** fewer lines of test code. Counting the
loader the single 10-scenario suite is *not* smaller (84 vs 52) — the loader
is an up-front cost. It pays off because it is shared: the same suite design
runs 32 CSV rows, 32 customer cases, 7 workflows and 100 generated orders
(**171 data rows** from 4 small test bodies), whereas the traditional style
needs one function per row — roughly 171 × 5 lines ≈ 850 lines.

## 2. Maintainability

- **Add a case:** traditional = write a new function (about 5 lines of
  hard-coded values and an assertion call). Data-driven = append one CSV row; no
  Python edit and the case appears in the report with its own id.
- **Update a rule:** if the tax rate changes, traditional tests need every
  expected number edited inside code; data-driven needs only data edits (or a
  regeneration), while the assertion logic stays untouched. When the *API*
  changes (e.g. `calculate_total` signature) the opposite is true: one place
  to fix in the data-driven suite, ten in the traditional one.
- **Data reuse:** the same CSV is consumed by three suites (full run, 10-case
  run, regression); non-programmers can review or extend it in a spreadsheet.
- **Risk:** data files need validation (typos, wrong types). `src/data_validator.py`
  reports `file:line` problems and runs inside the suite.

## 3. Readability

- Traditional wins for *one* scenario: the story (input → expectation) sits
  inside the test and the failure points to a function with a meaningful name.
- Data-driven wins for *many* scenarios: a table lets you scan coverage at a
  glance and spot gaps (e.g. no express + FREESHIP row). Good ids
  (`save10_at_exact_minimum`) and an assertion message with the failing
  component keep failures as readable as named functions.
- Organisation: traditional groups by function name, data-driven by data
  category (simple, discount, tax, shipping, complex), which maps directly to
  the requirements list.
- Downsides of data-driven: logic that differs per case is awkward to express
  in a table (we kept negative-value and `ValueError` tests as normal unit
  tests), and the reader must open two files.

## 4. Coverage and Effort

| Metric                           | Traditional | Data-driven                       |
| -------------------------------- | ----------- | --------------------------------- |
| Scenarios in the 10-test suites  | 10          | 10                                |
| Scenarios available to same logic| 10          | 32 (CSV) + 100 (generated)        |
| Time to run (10 tests, pytest)   | 0.47 s      | 0.19 s (both dominated by ~4 s start-up/coverage plugin load) |
| Time to add 10 more cases        | ≈ 10–15 min (10 functions, ~50 lines) | ≈ 2–3 min (10 CSV rows) |

Raw calculation speed is not a differentiator: running 10 / 50 / 100 / 500 CSV
cases through `Order` takes 0.1 / 2.0 / 3.9 / 12 ms respectively (linear). The
measured wall-clock difference between the two suites is within start-up noise.
The real gain is effort per extra case, not CPU time.

The full suite — 281 tests, 99% statement coverage of `src/` — would have
required many hundred lines in the traditional style.

## 5. Conclusion

**Use data-driven tests when** the logic is the same and only inputs/outputs
vary: calculators, validators, parsers, boundary-value and equivalence-class
tables, regression baselines, and anything business people should review.

**Use traditional tests when** a scenario needs unique setup, mocking, rich
interaction, or when the test *is* the documentation of one important
behaviour (error handling, state transitions).

| Pros of data-driven                          | Cons of data-driven                                   |
| -------------------------------------------- | ----------------------------------------------------- |
| Far less duplicated code                     | Up-front cost: loaders, formats, validation           |
| Adding cases is cheap and low-risk           | Data errors become test errors (needs a validator)    |
| Data reusable across suites and by non-devs  | Harder to express per-case logic                      |
| Coverage gaps visible as missing rows        | Failure points to a row, not a hand-written story     |
| Scales to hundreds of generated cases        | Expected values copied from the code defeat the test  |

Takeaway: use both. This homework keeps traditional tests for error handling
(negative values, unknown actions) and data-driven tests for the 170+ value
tables, which gives breadth without sacrificing clarity.

One caveat learned while generating expected values: the CSV `expected_*`
columns must be computed independently of the implementation (here with a
separate `Decimal` reference calculation), otherwise the data only proves the
code agrees with itself. `generated_orders.csv` is explicitly a *regression
snapshot*, not an oracle.
