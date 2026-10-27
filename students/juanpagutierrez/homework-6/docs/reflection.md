# TDD Reflection

## Design Impact

The biggest effect TDD had was on what my classes depend on. To write a late-fee test, I needed to say "26 days have
passed" without waiting 26 days. So `Library` takes a `clock`, and the tests pass in a `Mock` whose return value they
move forward. Reservations needed a way to notify people, and I didn't want tests sending emails, so `Library` also takes
a `notifier`. Neither choice was planned: in both cases the test asked for something I could only provide by
injecting it.

TDD also changed how classes appeared. `Loan`, `ReservationDesk`, `SearchQuery` and `BookDetails` were never planned.
Each one appeared during a REFACTOR step, when `Library` started knowing too much about something else. Because the
tests check behavior through `Library`, I could pull the reservation logic out into a new class without changing a
single test.

## Challenges

The hardest part was writing deliberately silly code in the GREEN step. Writing `return True` for `is_available()` felt
wrong, even though I knew the next test would force the real check.

A second challenge was tests that passed on the first run. For example, ISBN-13 already worked, because the length check
accepted both 10 and 13 digits. A test that never fails cannot prove anything new, so I didn't commit those as RED. I
gave them a separate `TEST:` label. That made me think harder about whether each new test described new behavior or
only documented existing behavior.

Finally, the linter (pylint 4.1) flagged constructors with too many arguments after the features were done. Fixing that
meant changing `Book`'s constructor and a few tests that used it. It reminded me that the tests are code too, and they
need maintenance when an interface changes.

## Benefits

The clearest benefit was a bug caught before it shipped. My first `borrow_book` took a copy off the shelf and only then
asked the member to accept it. When the member was at their limit, the error was raised but the copy was already gone.
I found this by writing a test that checked the book *after* a failed borrow. It failed with `assert 1 == 2`.

The second benefit was confidence. I did 12 refactors, including pulling a whole class out of `Library`. Each one took a
few minutes, because 70+ tests in under half a second told me right away whether I had broken anything. Coverage reached
100% of statements and branches without me ever looking for gaps, because every line was written to pass a test that
already existed.

## Comparison with Test-After

In earlier homework, I wrote tests after the code. Those tests followed the implementation: I read the code and
checked what it already did. Here the tests came from the requirements, and the code had to fit them. Test-after also
made it easy to skip awkward cases, while in TDD every rule had to be stated as a test before it could exist. TDD was
slower at the start, but by the advanced features it was faster, because I was never debugging.

## Future Use

I would use TDD for business rules: fees, limits, queues, validation, anything with clear inputs and outputs and edge
cases. I would not start with TDD for exploratory work, like a UI layout or trying out a new library. There I don't yet
know what "correct" means, and the tests would just repeat whatever I guessed. In those cases I would explore first,
throw the prototype away, and then write the real version test-first.

## Learning

What surprised me most was how much the order of tests affected the design. Writing the "fee stops growing after return"
test before the category-rate test gave me the `Loan.late_fee` method naturally. I also learned that a RED test should
fail for the *right reason*. An `ImportError` is a valid failure, but an assertion failure says much more about the
behavior. If I did this again, I would decide the order of the advanced features earlier. I would also introduce the
clock in the first `Library` test, instead of adding it partway through, which made one GREEN commit bigger than I
wanted.
