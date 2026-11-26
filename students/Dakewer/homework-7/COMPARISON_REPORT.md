# Comparison Report: Traditional vs Data-Driven Tests

Both suites test the **same 10 scenarios** against `Order`:

- `tests/test_order_traditional.py` - 10 functions, values hardcoded
- `tests/test_order_data_driven.py` - 1 parametrized function reading
  `test_data/comparison_cases.csv` (10 rows)

## 1. Lines of code

Counted as non-blank, non-comment lines.

| Version | Test code | Shared loader (`data_loader.py`) | Total code | Data |
|---|---|---|---|---|
| Traditional | 106 | - | 106 | 0 |
| Data-driven | 6 | 45 | 51 | 10 CSV rows |

- Reduction counting only the test module: **(106 - 6) / 106 = 94%**.
- Reduction counting the loader as well: **(106 - 51) / 106 = 52%**.

The loader is written once and reused by `test_order_calculator.py`,
`test_generated_orders.py` and this file, so the real saving grows with every
suite that shares it. The traditional cost is linear: about 10-11 lines per
scenario, forever.

## 2. Maintainability

**Adding a test case.** Traditional: copy a function, rename it, edit the
inputs and five assertions (about 11 lines, easy to leave a stale value).
Data-driven: append one CSV row, no code change.

**Updating existing tests.** If the API changes (say `set_shipping` gains a
parameter), the traditional suite needs 10 edits; the data-driven suite
needs one edit in `run_order_case`. If a *rule* changes (tax 8% -> 9%),
both approaches need their expected values updated, but in the data-driven
version they all sit in one file and can be edited or regenerated together.

## 3. Readability

- **Traditional** wins for a single case: setup, action and assertions are
  visible in one place, and a failure points at a function with a
  meaningful name.
- **Data-driven** wins for the overall picture: the CSV reads like a table
  of the rules, and gaps in coverage (e.g. no express case with a discount)
  are visible at a glance. Rows are grouped by name prefix (`simple_`,
  `discount_`, `tax_`, `shipping_`, `complex_`), and pytest ids use the same
  names, so failures still read as `test_order_scenario[shipping_express]`.
- The cost of data-driven is indirection: to understand one test you read the
  CSV row *and* the runner, and the items column holds JSON inside CSV
  quoting, which is harder on the eyes.

## 4. Coverage

| | Traditional | Data-driven |
|---|---|---|
| Scenarios in this comparison | 10 | 10 |
| Scenarios in the full suite | impractical to hand-write | 34 in `order_calculations.csv`, plus 100 generated |
| Code to add 10 more cases | about 105 lines | 10 CSV rows, 0 lines of code |

Statement coverage of `src/` is 100% with the full suite. The 10 scenarios
alone do not reach it (they have no error cases, for example); getting more
scenarios into the traditional style is exactly the point where it stops
being worth it. The 100 generated orders (bonus A) would be about 1,000
lines of traditional tests; as data they are a single 100-row file and one
short parametrized test.

(The "time to add 10 cases" row is an estimate from the line counts, not a
timed experiment.)

## 5. Conclusion

**Use traditional tests when**

- there are few cases, or each one needs bespoke setup or reasoning;
- you are exploring behaviour or writing a regression test for one bug;
- the logic of the test itself differs between cases.

**Use data-driven tests when**

- the same logic runs over many input/output combinations (calculators,
  validators, parsers, rules engines);
- non-programmers (QA, analysts) should be able to add cases;
- data can come from elsewhere (exports, generators, production samples).

**Pros of data-driven testing:** far less code, trivial to add cases,
logic and data separated, easy to generate and review cases as a table,
one fix to the runner fixes every test.

**Cons:** harder to debug a single row, less flexible for unusual setups,
test data needs its own validation (hence `tools/validate_test_data.py`),
a bug in the shared runner can hide failures in *all* cases, and expected
values copied from the implementation can make tests tautological. The
generator avoids the last problem by computing expectations with its own
independent implementation.

In this project the best structure was the mix used here: data-driven for
the calculator, validator and workflows, plus a handful of plain tests for
things that do not fit a table (return values of `apply_discount`,
malformed inputs, workflow edge cases).
