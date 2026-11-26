# TDD Reflection

## 1. Design Impact: How TDD Influenced My Design Decisions

Developing the Library Management System using strict Test-Driven Development (TDD) fundamentally shaped the architecture of `Book`, `Member`, and `Library`. Because every feature began with a test, I had to think as a consumer of the API before writing a single line of implementation. This led to clear separation of responsibilities: `Book` encapsulates copy counts, ISBN/title validation, and availability checks; `Member` owns personal borrowing limits, active loans, and category rates; and `Library` acts as the coordinator for catalog search, borrowing workflows, late fee calculations, FIFO reservations, and borrowing history. Furthermore, writing tests first encouraged me to pass explicit `date` objects into `calculate_late_fee(borrow_date, return_date)` instead of coupling the method to `date.today()`, making the design deterministic and effortless to test.

## 2. Challenges: What Was Difficult About Test-First Development

The biggest challenge during test-first development was resisting the urge to write complete implementations all at once. When implementing `Library.borrow_book()`, my natural instinct was to immediately code member lookup, book lookup, limit validation, and history tracking in one step. Forcing myself to write one failing test at a time—first for a valid borrow, then for an unavailable book, then for exceeding a member's limit, and finally for unknown IDs—felt slower initially. Another challenge was designing state-preservation assertions for negative paths: when an operation raises a `ValueError` (for example, when a member at their limit attempts to borrow a book), the test must also verify that `book.available_copies` was not decremented prior to the failure.

## 3. Benefits: Advantages Observed During Development

Practicing the RED-GREEN-REFACTOR rhythm provided immediate, concrete feedback at every step. Whenever a test failed in the RED phase, I knew the test was genuinely exercising the target behavior. Once in the GREEN phase, having a comprehensive suite of fast tests gave me complete confidence to refactor. For instance, when I introduced member categories (`student`, `faculty`, and `public`) and advanced catalog filtering in Part 3, the existing 45 core tests acted as a safety net. Within less than half a second, `pytest` confirmed that extending `Member.__init__` and `Book.__init__` with optional parameters did not break any existing behavior. Achieving 100% statement and 100% branch coverage happened naturally as a byproduct of writing tests for every requirement rather than hunting for uncovered lines at the end.

## 4. Comparison: How TDD Compares to Test-After Development

In traditional test-after development, tests are often written to conform to the code that already exists, which leads to confirmation bias and tightly coupled interfaces. When writing tests after the fact, it is easy to skip edge cases—such as whitespace-only titles, duplicate reservations, or returning a book when all copies are already in the library—because the developer assumes the happy path works. With TDD, edge cases are treated as first-class specifications. In addition, debugging time dropped dramatically: whenever a test failed, the bug was guaranteed to be in the 5 to 15 lines of code written during the last two minutes.

## 5. Future Use: When to Use (and Not Use) TDD

I would strongly choose TDD for domain models, business rules, financial or fee calculations, data validation, and stateful workflows like queues and inventory management. In these areas, requirements can be expressed as clear inputs, state transitions, and outputs. Conversely, strict TDD is less practical during initial exploratory prototyping (spikes), UI layout experimentation, or when learning an unfamiliar third-party API whose behavior is not yet understood. In those scenarios, building a quick prototype to clarify the design and then applying TDD to the production implementation is a pragmatic balance.

## 6. Learning: What Surprised Me and What I Would Do Differently

What surprised me most was how small, incremental commits (`RED`, `GREEN`, `REFACTOR`) create a living narrative of the system's evolution. Reviewing the git log reads like documentation of every design decision. If I were to start this project again, I would define helper fixtures for common `Book` and `Member` setups earlier in the refactoring phases to reduce test setup repetition, while still keeping each test self-contained and readable. Overall, TDD transformed testing from a final verification chore into an active design tool.
