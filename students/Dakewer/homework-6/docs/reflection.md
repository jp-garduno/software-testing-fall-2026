# TDD Reflection

## Design Impact

Writing the test first forced me to decide how a class would be *used* before deciding how it
would be built. The clearest example is dates. When I wrote the first late-fee test, I had to
type something like `library.borrow_book("M001", isbn, borrow_date=...)` and
`calculate_late_fee("M001", as_of=...)`. Calling `date.today()` inside the library would have made
that test impossible to write, so the test pushed me to inject the dates. The result is code that
is deterministic and needs no mocks. The same thing happened with `get_member` and `get_book`:
they started as helpers to make tests readable and ended up being the single place where
"unknown member" and "unknown book" are validated.

## Challenges

The hardest part was discipline, not syntax. It is tempting to write the whole `Book` class
because you already know what it should look like. Keeping to "only enough code to pass this one
test" felt slow, especially with a constant like `return True` for `is_available()`. A second
difficulty was writing tests that fail for the *right* reason. Three times I wrote a test that
passed immediately, for example returning a book the member never borrowed, because the
existing design already handled it. My workflow refuses to commit a RED that does not fail, so I
had to stop and ask whether the test was redundant or whether it should assert something sharper,
like the error message. Sometimes I deleted the test; other times I tightened it.

## Benefits

The biggest benefit was catching a real bug early. My first `borrow_book` took a copy from the book
and then asked the member to record the loan. A test for a member at their borrow limit showed the
book had already lost a copy, so a failed borrow left the library in an inconsistent state. I would
not have thought to check that if I had been writing tests afterwards to confirm code I already
believed was correct. Other benefits were confidence while refactoring (I extracted validation
helpers and the `_search` and `_loan_fee` methods with the suite green each time) and a suite of
64 tests that runs in a fraction of a second.

## Comparison with Test-After

With test-after, I think I would have written tests that mirror the implementation: they pass,
coverage looks good, and they prove very little. Test-first tests describe behaviour and have been
seen to fail, which is the only evidence that a test can detect anything. Test-after is faster for
the first hour, but test-first made the later features cheap. Adding member categories only
required a few small failing tests because the limit and fee rules each lived in one place.

## Future Use

I would use TDD for business logic with clear rules, such as validation, fees, limits and state
transitions, and for bug fixes, where the first step is a test that reproduces the bug. I would be
more selective for exploratory work such as a UI prototype or an unfamiliar library, where I do not
yet know what to assert. There I would explore first and then add tests, or write a throwaway
spike and rebuild it test-first.

## Learning

What surprised me most was how often a "fake it" implementation was enough to move forward, and
how a second test naturally forced the real rule out of it. I also did not expect the test to
tell me about *ordering* decisions, like which object to change first when a borrow can fail in two
ways. What I would do differently: add the 13-digit ISBN test and the non-digit test in separate
commits, because adding two tests at once blurred one RED step, and I would refactor more often
instead of waiting until a file had several repeated checks. Next time I would also keep a short
note of each failure message while working, because writing the process documentation was much
easier with real output to copy.
