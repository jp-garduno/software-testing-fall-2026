# TDD Reflection

## Design Impact

The biggest effect was on the shape of the API. Because every test had to construct its own objects,
dependencies became constructor arguments almost by accident. The late fee tests needed to move time,
so `Library` takes a `clock`. The reservation tests needed to observe a notification, so it takes a
`notifier` callable that a `Mock` can stand in for. Neither was planned; each came from the test
that could not be written otherwise. The same thing happened with `MemberCategory`: it started as
three integers, became a tuple when a fee rate was needed, and ended as a `NamedTuple`, each step
pulled in by the next failing test instead of designed in advance.

## Challenges

The hard part was restraint, not syntax. After writing a test, the correct implementation is usually
obvious, and the discipline is to write less than that. `is_available` started as `return True`.
`calculate_late_fee` started as `return 0`. It feels silly, but the next test failed for a real
reason (`assert True is False`, `assert 0 == 3`) and that second example is what produced the actual
logic. The other challenge was choosing a test that fails for the right reason. Some RED steps
failed with `AttributeError`, which only proves the method is missing. The more useful ones failed on
an assertion about behavior.

## Benefits

Two bugs showed up that I would probably have written without TDD, because they come from the order of
operations rather than any single line. `Library.borrow_book` originally took the copy and then asked
the member to record the loan, so when the member was at their limit the error was raised but a copy
had already disappeared (`assert 1 == 2`). `return_book` had the mirror problem: a member who never
borrowed a book could still push the stock up before the error was raised (`assert 2 == 1`). Writing
the failure path as a test made me look at what state is left behind, not only at the exception. The
second benefit is speed of feedback: 64 tests run in about 0.1 seconds, so running them after every
change is free, and refactoring such as pulling out `_search`, `_holds` and the `CategoryPolicy` felt
safe.

## Comparison with Test-After

When I write tests after the code, I tend to test what the code does. Here the tests described what I
wanted, and the code had to catch up. Test-after would likely have given the same coverage number,
since this suite is at 100% for lines and branches, but with weaker assertions: I would not have
thought of the "returned book keeps accruing fees" case (`assert 5 == 0`) until a loan was never
cleared. The trade-off is that TDD is slower per feature. It also produced many more commits
than I would normally make (over 100), because each test and each fix is its own commit.

## Future Use

I would use TDD for logic with clear rules and edge cases: validation, state transitions, money,
dates, anything with business rules. I would be less strict for exploratory work, where the shape of
the problem is not known yet, and for glue code such as wiring a framework or a UI, where a test
mostly restates the configuration. Some tests are still written after the fact, like the characterization tests that pin behavior which
already passed; those are not strict TDD.

## Learning

What surprised me was how often a RED test passed or failed for a reason other than the one I
expected. One test I expected to fail with "no error raised" failed because Python had already raised
its own `ValueError` (`list.remove(x): x not in list`), just without a useful message. That led to
the domain-specific error. What I would do differently is keep the commits smaller: a few of them
(the first test of a new file, and some characterization commits) change more than 20 lines because
I grouped fixtures or several tests together. I would also add property-based tests for the date logic.

Finally, 100% coverage is a by-product here, not a goal: it shows every line ran, not that every
behavior is right. Nothing here would reveal two threads reserving at once.
