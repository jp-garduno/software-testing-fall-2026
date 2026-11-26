# Comparison Report: Traditional vs. Data-Driven Testing

## Executive Summary

This report compares two implementations of the exact same 10 order calculation test scenarios:
1. **Traditional Approach (`tests/test_order_traditional.py`)**: 10 separate test functions with hardcoded inputs and assertions.
2. **Data-Driven Approach (`tests/test_order_data_driven.py`)**: A single parameterized test function (`@pytest.mark.parametrize`) driven by external records in `test_data/order_calculations.csv`.

---

## 1. Lines of Code (LOC) Analysis

| Metric | Traditional (`test_order_traditional.py`) | Data-Driven (`test_order_data_driven.py`) | Reduction / Impact |
| :--- | :---: | :---: | :--- |
| **Total Lines (including blanks/docstrings)** | 139 lines | 51 lines | **63.3% reduction** |
| **Non-empty Code Lines (SLOC)** | 118 lines | 42 lines | **64.4% reduction** |
| **Test Functions Defined** | 10 functions | 1 function (+1 loader) | **90.0% fewer test functions** |
| **Assertion Statements Written** | 50 assertions (`5 × 10`) | 5 assertions (`5 × 1`) | **90.0% fewer assertions** |
| **Marginal LOC per Additional Test Case** | +12 lines of Python code | +1 row in CSV (0 Python lines) | **100% code growth elimination** |

### Scaling Projection

If the test suite scales from 10 scenarios to 100 scenarios (as demonstrated in our Bonus Option A `generated_orders.csv`):
- **Traditional Suite**: Would require `~1,300` lines of repetitive Python boilerplate and `500` individual `assert` statements.
- **Data-Driven Suite**: Still requires only **51 lines of Python test code** plus 100 rows in the CSV file.

---

## 2. Maintainability

### Adding New Test Cases
- **Traditional**: Requires copying and pasting a 12-line function, inventing a unique function name, editing Python dictionary literals, and manually writing 5 `assert` lines.
- **Data-Driven**: Requires adding a single comma-separated row to `test_data/order_calculations.csv`. Non-programmers (QA analysts, product managers) can contribute test cases directly without touching Python code.

### Updating Existing Tests when Business Rules Change
Suppose `Order.calculate_total()` adds a new key to its returned dictionary (e.g., `"handling_fee"`) or renames `"shipping"` to `"shipping_cost"`:
- **Traditional**: Every single test function (`10` functions, or `100` in a larger suite) must be manually edited in code.
- **Data-Driven**: Only the single parameterized test body in `test_order_data_driven.py` (1 place) and the CSV column need updating.

---

## 3. Readability and Organization

- **Traditional Approach**:
  - **Pros**: Each test function is self-contained; a reader can see the exact setup and expected values on consecutive lines without opening a second file.
  - **Cons**: Structural repetition obscures differences between test cases. Scanning 10 nearly identical functions makes it difficult to spot which parameter actually changed between `test_03` and `test_04`.
- **Data-Driven Approach**:
  - **Pros**: Clean separation of **test logic** (how to exercise `Order`) from **test data** (what inputs and expected outputs to verify). In tabular CSV form, boundary pairs like `discount_save10_at_threshold` (`$50.00`) and `discount_save10_below_min` (`$49.99`) sit on adjacent rows, making boundary value coverage immediately visible.
  - **Cons**: Requires descriptive test IDs (`ids=...`) so failure tracebacks clearly identify which row failed.

---

## 4. Coverage and Execution Efficiency

| Dimension | Traditional (`10` tests) | Data-Driven (`30` CSV cases + `100` generated) |
| :--- | :--- | :--- |
| **Scenarios Tested** | 10 scenarios | 130 order scenarios + 34 customer JSON cases + 4 E2E workflows |
| **Statement Coverage (`src/`)** | 95.8% (`order_calculator.py` core paths) | **100.0%** across all modules |
| **Time to Add 10 More Cases** | ~8–10 minutes (coding + formatting + linting) | **~1–2 minutes** (adding 10 CSV rows or running generator) |

---

## 5. Conclusion: When to Use Each Approach

### Use Data-Driven Testing When:
1. **Same workflow, many input combinations**: Tax brackets, discount thresholds, shipping matrices, and input validation rules (emails, phones, credit cards).
2. **Boundary Value Analysis & Equivalence Partitioning**: Tabular formats (CSV/JSON) naturally express equivalence partitions and boundary pairs.
3. **Regression suites with large datasets**: Running 100+ cases generated programmatically or exported from production logs.

### Use Traditional Testing When:
1. **Unique control flow or mocking per test**: Testing distinct exception paths, state transitions, or complex behavioral mocks where each test has a fundamentally different setup/assertion structure.
2. **Single-purpose smoke or architectural tests**: Verifying a one-off contract or state mutation (such as `test_order_discount_state_changes`).
