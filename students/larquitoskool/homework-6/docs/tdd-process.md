# TDD Process Documentation

## Cycle #1: Book Availability Check
**RED**: Wrote `test_book_not_available()` checking if available_copies is 0. Failed (method missing).
**GREEN**: Added `is_available()` returning `available_copies > 0`.
**REFACTOR**: None needed.

## Cycle #2: Member Borrow Limit
**RED**: Wrote `test_borrow_limit_reached()` adding 3 books to a Public member. Failed (no exception).
**GREEN**: Added `can_borrow()` and raised ValueError in `add_borrowed_book()`.
**REFACTOR**: Extracted limit values into a class-level dictionary `LIMITS`.

## Cycle #3: Library Borrow Integration
**RED**: Wrote `test_borrow_book_success()`. Failed because catalog was empty.
**GREEN**: Implemented `borrow_book()` orchestrating Member and Book methods.
**REFACTOR**: Added `get()` dictionary methods to prevent KeyErrors.

## Cycle #4: Late Fee Calculation (Advanced)
**RED**: Wrote `test_late_fee_calculation()` for 16 days. Failed (no late_fees attribute).
**GREEN**: Added `calculate_late_fee()` charging $1 per day after 14 days.
**REFACTOR**: Connected the method to `return_book()` in Library.

## Cycle #5: Search Filters (Advanced)
**RED**: Wrote `test_search_books()` filtering by partial title. Failed.
**GREEN**: Added list comprehensions checking substrings in titles and authors.
**REFACTOR**: Handled lowercase conversions for case-insensitive searching.