# TDD Reflection

## Design Impact

Writing the test first made me design every class from the outside. Before writing `Library`, I had
to decide what a caller would type: `library.borrow_book("m1", ISBN)`, `library.late_fee(...)`,
`library.reservation_queue(isbn)`. The API came out small and readable because each method existed
only after a test asked for it. The late fee tests also pushed me to inject a clock into `Library`
(`Library(clock=...)`). Without a test that needed to say "17 days later", I probably would have
called `date.today()` directly and ended up with code that could not be tested without waiting.

## Challenges

The hardest part was discipline. It is tempting to write the whole `Book` class when the first test
only needs a title. Writing the smallest possible code, such as `is_available` returning `True`,
felt silly until the next test failed and showed why. It was also hard to choose the next test.
Picking a test that is small enough to pass with a few lines but large enough to teach the design
something took practice. Keeping commits tiny, with a separate RED and GREEN commit every time, slowed
me down at first.

## Benefits

The biggest benefit was confidence. When I extracted `_require_member` or `_days_overdue`, I ran the
suite and knew immediately that nothing had broken. I also found a real bug by writing a test first:
borrowing over the member's limit consumed a copy before the error was raised. A happy-path test would
never have exposed that ordering problem. Finally, the suite finished with high coverage almost for
free, because every line of code exists to make a failing test pass.

## Comparison with Test-After

When I test after writing the code, I tend to test what the code does, including its accidents. With
TDD I tested what the code should do. Test-after also makes me skip awkward cases, like unknown
members or returning a book twice, because the code already "works". In TDD those cases were written
as requirements before the implementation could hide them. The cost is speed in the first hour: TDD is
slower at the start, but I spent almost no time debugging, which evened it out.

## Future Use

I would use TDD for business logic with clear rules, such as fees, limits, queues and validation,
where examples are easy to write and mistakes are expensive. I would also use it when fixing a bug:
first a failing test that reproduces it, then the fix. I would use it less for throwaway scripts,
exploratory spikes where I do not yet know what I am building, and visual user-interface work where
judging the result needs human eyes. In those cases I would explore first and add tests once the
shape is clear.

## Learning

What surprised me most was how often the refactor step changed the design in a good way. The
`_require_book` and `_require_member` helpers only appeared once duplication was visible, and
`_notify_next_in_queue` made `return_book` read like a checklist. I also did not expect a
deliberately fake implementation to be so useful: returning a hard-coded value forced me to write the
second test that defined the real rule.

Next time I would write the test list on paper before starting, so I do not stop between cycles to
think about what comes next. I would also set up a file watcher that runs the tests on every save, to
shorten the RED and GREEN feedback loop even more. Overall, TDD did not feel like extra work; it felt
like having a conversation with the code, where the failing test asks the question and the
implementation answers it.
