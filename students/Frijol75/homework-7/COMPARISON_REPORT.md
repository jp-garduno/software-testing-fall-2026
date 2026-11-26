# Comparison Report: Traditional vs. Data-Driven Testing

**Course**: Software Testing - Fall 2026  
**Assignment**: Homework 7 - Data-Driven Test Suite  
**Student**: Frijol75  

---

## 1. Executive Summary

This report evaluates and compares two core automated testing paradigms implemented for the E-Commerce Order Processing System:
1. **Traditional Testing** (`tests/test_order_traditional.py`): Test logic and test inputs/expected outputs are coupled together in separate, hardcoded test functions.
2. **Data-Driven Testing (DDT)** (`tests/test_order_data_driven.py` & `tests/test_order_calculator.py`): Test logic is decoupled from test inputs, loading datasets dynamically from external files (`test_data/comparison_10_cases.csv` and `test_data/order_calculations.csv`) via `@pytest.mark.parametrize`.

---

## 2. Quantitative Metric Comparison

### 2.1 Lines of Code (LOC)

Analyzing the exact 10 core test cases implemented across both paradigms:

| Metric | Traditional (`test_order_traditional.py`) | Data-Driven (`test_order_data_driven.py`) | Difference |
| :--- | :---: | :---: | :---: |
| **Total Lines of Code** | 128 | 48 | **-62.5% LOC** |
| **Test Function Definitions** | 10 | 1 | **-90.0% functions** |
| **Setup & Assertion Duplication** | 10 repeated blocks | 1 parameterized block | **-90.0% duplication** |
| **Data Storage** | Inline Python dictionaries | External CSV (`comparison_10_cases.csv`) | Structured & independent |

> **Key Takeaway**: Data-Driven Testing reduced test code by **62.5%** for just 10 test cases. As the test suite scales to 30, 50, or 100 cases, the traditional suite grows linearly ($\mathcal{O}(N)$ code growth), whereas the DDT test suite remains constant ($\mathcal{O}(1)$ code size).

---

## 3. Qualitative Evaluation

### 3.1 Maintainability
- **Traditional Approach**:
  - Updating a single business rule (e.g., changing tax rate from 8% to 10% or modifying the return dictionary format) requires editing every single test function manually.
  - Adding a new test scenario involves copying and pasting an entire 12-line test function, increasing boilerplate and risks of copy-paste bugs.
- **Data-Driven Approach**:
  - Updating test assertions or calculation logic requires modifying **only one assertion block** in the parameterized test function.
  - Adding new test cases requires only adding a single row to the CSV dataset without modifying Python code.

### 3.2 Readability & Separation of Concerns
- **Traditional Approach**:
  - Test intent is buried under verbose dictionary definitions and repetitive assertion statements.
  - Non-technical stakeholders (QA analysts, product managers) cannot easily review or audit test coverage without reading Python code.
- **Data-Driven Approach**:
  - Pure separation of concerns: The test file contains pure verification logic; the CSV/JSON contains pure business scenarios.
  - Domain experts can view, edit, or contribute test cases in spreadsheets (Excel/Google Sheets) without touching Git codebases or Python scripts.

### 3.3 Extensibility & Scalability
- **Time to add 10 new test scenarios**:
  - *Traditional*: ~10–15 minutes (creating 10 functions, formatting dicts, naming functions, duplicating assertions).
  - *Data-Driven*: ~1–2 minutes (typing 10 rows into CSV).

---

## 4. Performance & Execution Benchmark (Bonus Option B)

Benchmarking 50 repeated iterations of the 10 test cases (500 test executions total):

```text
[Benchmark Results]
- Traditional (500 executions): ~0.0035s
- Data-Driven (500 executions): ~0.0042s
```

- **Analysis**:
  - The traditional approach is marginally faster per execution because inputs are already memory-resident Python literals, avoiding CSV parsing overhead during parameter collection.
  - However, in pytest, dataset loading happens once during the collection phase. The subsequent test execution time difference is negligible (< 1ms per suite run), while DDT provides vastly superior scalability and organization.

---

## 5. Summary Table: Pros & Cons

| Aspect | Traditional Testing | Data-Driven Testing (DDT) |
| :--- | :--- | :--- |
| **Code Footprint** | Large, grows with every case | Small, constant size |
| **New Test Addition** | High effort (write new Python function) | Minimal effort (append CSV row) |
| **Maintenance Cost** | High (refactoring affects $N$ functions) | Very low (refactoring affects 1 function) |
| **Debugging** | Clear stack trace directly in function | Clear test ID reported by `@pytest.mark.parametrize` |
| **Collaboration** | Developers only | QA, Business Analysts, Domain Experts |

---

## 6. Conclusion & Recommendations

1. **Use Data-Driven Testing when**:
   - Testing business logic algorithms with diverse inputs (e.g., pricing, taxes, shipping, discounts, discounts thresholds).
   - Validating forms with boundary conditions, combinatorial inputs, and equivalence partitioning.
   - Non-technical stakeholders participate in reviewing or creating test scenarios.
2. **Use Traditional Testing when**:
   - Tests require completely unique, non-uniform setup fixtures or complex mocking strategies for each case.
   - Validating unique architectural components where inputs and workflow logic vary wildly between tests.

