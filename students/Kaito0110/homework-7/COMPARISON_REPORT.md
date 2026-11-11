# Traditional vs. Data-Driven Testing — Comparison Report

## Executive Summary

To evaluate the effectiveness of **Data-Driven Testing (DDT)** against **Traditional Hardcoded Testing**, we implemented the exact same 10 order calculation scenarios in two separate test modules:

1. **`tests/test_order_traditional.py`**: 10 individual test functions (`test_traditional_01_*` through `test_traditional_10_*`), each containing hardcoded item lists, shipping settings, discount codes, and 5 assertions.
2. **`tests/test_order_data_driven.py`**: 1 parameterized test function (`test_order_data_driven_ten_cases`) decorated with `@pytest.mark.parametrize` that loads the same 10 cases from `test_data/order_calculations.csv`.

---

## 1. Lines of Code (LOC) Analysis

| Metric | Traditional (`test_order_traditional.py`) | Data-Driven (`test_order_data_driven.py`) | Reduction / Difference |
| --- | --- | --- | --- |
| **Total Lines (including blanks/comments)** | 191 lines | 66 lines | **-65.4% fewer lines** |
| **Executable Python Lines (SLOC)** | 133 lines | 38 lines | **-71.4% SLOC reduction** |
| **Test Functions Required** | 10 functions | 1 function | **-90.0% function count** |
| **Assertions Written in Code** | 50 assertions (`5 × 10`) | 5 assertions (`5 × 1`) | **-90.0% assertion duplication** |

### Scaling Projection
- In the **traditional approach**, each new test case adds approximately **18–20 lines of Python code**. Scaling from 10 to 100 test cases would require **~1,900 lines** of repetitive Python code.
- In the **data-driven approach**, the Python test file remains fixed at **66 lines** regardless of whether we run 10, 28, or 100+ cases—each new scenario is just **1 row in a CSV file**.

---

## 2. Maintainability

### How Easy Is It to Add New Test Cases?
- **Traditional**: Requires writing a new `def test_...()` function, copying the setup boilerplate (`Order(...)`, `apply_discount(...)`, `set_shipping(...)`, `calculate_total()`), and writing 5 `pytest.approx` assertions.
- **Data-Driven**: Requires appending a single line to `test_data/order_calculations.csv` (or one JSON object in `customer_validation.json`). Zero Python code changes are required. Even non-developers (QA analysts, product managers) can contribute test cases directly in CSV/spreadsheet tools.

### How Easy Is It to Update Existing Tests?
- **Traditional**: If the `Order` API changes (for example, renaming `set_shipping(distance, is_express)` to `configure_shipping(distance_km=..., express=...)` or adding a `"handling_fee"` key to `calculate_total()`), every single test function (**10 functions** in the benchmark, or **28+ functions** in the full suite) must be edited manually.
- **Data-Driven**: Any API or assertion change is updated in **one single place** inside the parameterized test body.

---

## 3. Readability and Organization

- **Traditional Approach**:
  - *Strengths*: Each test function is self-contained; a developer can inspect inputs and expected outputs in one place without opening an external file.
  - *Weaknesses*: High visual noise. Because 90% of every function is identical boilerplate, it is difficult to spot the subtle difference between `test_traditional_04_save10_at_threshold` (\$50.00) and `test_traditional_05_save10_below_threshold` (\$49.99).
- **Data-Driven Approach**:
  - *Strengths*: Clean separation of **test logic** (how to test) from **test data** (what values to test). Comparing boundary values across rows in `order_calculations.csv` is immediate because inputs and expected outputs are aligned in tabular columns.Descriptive `test_name` IDs (`ids=...`) ensure `pytest -v` output remains clear (`test_order_calculation[discount_save10_at_min_threshold]`).
  - *Weaknesses*: Requires jumping between the test script and the CSV/JSON file when debugging a single case, and requires a small loader/parser function.

---

## 4. Coverage and Speed of Expansion

| Dimension | Traditional Suite | Data-Driven Suite |
| --- | --- | --- |
| **Scenarios Tested in Homework 7** | 10 benchmark cases | 28 CSV orders + 100 generated orders + 32 JSON customers + 4 workflows |
| **Time to Add 10 More Test Cases** | ~12–15 minutes (copy/paste, rename functions, formatwith Black/Pylint) | ~2 minutes (add 10 rows to CSV or run `generate_synthetic_orders_csv`) |
| **Risk of Copy-Paste Bugs** | High (forgetting to update an assertion value after pasting) | Low (single shared assertion block) |

---

## 5. Conclusion: When to Use Each Approach

### Use Data-Driven Testing When:
- Testing business rules, calculators, pricing engines, tax/shipping formulas, and input validators with dozens of equivalence partitions and boundary values.
- The execution workflow and assertions are identical across cases, varying only in input data and expected outputs.
- Regression suites need to scale to 50–500+ scenarios or incorporate synthetic data generation (`Faker`).

### Use Traditional Testing When:
- Testing unique behavioral flows, exception paths, or mocking interactions where each test has a distinct setup, action sequence, or assertion structure.
- Writing a small number (1–3) of smoke or architectural tests where creating an external CSV/JSON file would add unnecessary indirection.
