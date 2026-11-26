# Comparison Report: Traditional vs Data-Driven Testing

## 1. Lines of Code (LOC)
* **Traditional Approach**: The `test_order_traditional.py` file requires approximately **65 lines of code** to test 10 scenarios. Each new scenario adds 5-6 lines of repetitive setup code.
* **Data-Driven Approach**: The `test_order_data_driven.py` file requires only **18 lines of code**. The test logic is written once, and the data is imported from an external JSON file.
* **Reduction**: The Data-Driven approach achieved an approximate **72% reduction** in Python codebase size for the test execution logic.

## 2. Maintainability
* **Adding New Cases**: It is significantly easier in the Data-Driven approach. A QA engineer or Business Analyst only needs to append a JSON object to the external file without touching the Python code. In the traditional approach, a developer must write a new Python function for every case.
* **Updating Existing Tests**: If the API of the `Order` class changes (e.g., `set_shipping` requires a new parameter), the Traditional suite requires modifying 10 individual functions. The Data-Driven suite only requires updating 1 line of code in the parameterized test.

## 3. Readability
* **Traditional**: Easier to understand at a glance for a *single, isolated test* because all variables and actions are explicitly written in one block. However, as a suite of 10+ tests, it becomes cluttered with boilerplate code, making it hard to spot the actual differences between tests.
* **Data-Driven**: Offers much better test organization. The Python script stays clean and focuses strictly on the *behavior* of the system, while the JSON/CSV files act as a clear, tabular specification of the *business rules*.

## 4. Coverage
* **Scenarios Tested**: Both approaches successfully cover the exact same 10 scenarios (100% parity in coverage).
* **Time to Scale**: Adding 10 more test cases takes ~2 minutes in a Data-Driven environment (just copy-pasting JSON blocks or CSV rows). Doing the same in a Traditional approach takes considerably longer due to manual code duplication and variable renaming.

## 5. Conclusion
* **Traditional Testing**: Best used for testing highly specific edge cases, structural logic, or complex integrations where each test follows a completely different execution path.
* **Data-Driven Testing (DDT)**: Highly superior for testing business rules, calculators, pricing engines, and validation logic where the *execution path is the same* but the *inputs and expected outputs vary widely*. 
* **Pros of DDT**: High scalability, separates data from logic, reduces code duplication, and allows non-programmers to contribute to test data.
* **Cons of DDT**: Can obscure the cause of a failure if the external data file becomes too complex or poorly structured.