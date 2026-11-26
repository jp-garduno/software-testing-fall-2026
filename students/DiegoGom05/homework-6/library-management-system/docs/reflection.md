# TDD Reflection

## Design Impact

TDD changed my design more than I expected. The clearest example was the late
fee feature. I wanted to test that a book returned 20 days after borrowing
would cost five dollars, but `date.today()` made that impossible to test
deterministically. Writing the test first forced me to add optional
`borrow_date` and `today` parameters, which made the code both testable and
more flexible. The same happened with member categories: writing one test per
limit pushed me toward a single lookup table instead of scattered if
statements. The tests acted as the first user of my API.

## Challenges

The hardest part was discipline. In the GREEN phase I constantly wanted to
write the full solution. For example, after the first test for
`is_available`, I had to deliberately write `return True` and wait for the
next test to force the real comparison. It felt silly at first. It was also
hard to choose the next test, because picking a poor order produced big jumps
in code. Keeping commits small and labeled RED, GREEN or REFACTOR also
required a habit change, since I normally commit only when a whole feature is
finished.

## Benefits

The biggest benefit was confidence. Every refactor, such as extracting
`_find_member` and `_find_book` or merging the category rules into one table,
took minutes because the suite told me immediately if something broke. TDD
also found a real bug: the test for a member at their borrow limit showed that
the library decremented a book's copies before checking the member, leaving
inconsistent state. Coverage came almost for free, since every line exists
because a test demanded it, and I never had to wonder what a function was
supposed to do.

## Comparison with Test-After

Compared with writing tests after the code, test-first was slower at the
beginning but produced fewer surprises. When I write tests afterwards, I tend
to confirm what the code already does, and I skip edge cases I did not think
of while coding. With TDD, I saw each test fail for the right reason, so I
knew the test could actually detect a problem. Test-after is faster for quick
scripts, but the tests it produces are often coupled to the implementation,
which makes later changes more painful.

## Future Use

I would use TDD for business logic with clear rules, such as fees, limits and
validations, and for bug fixes, where I first write a test that reproduces the
bug. I would be less strict for throwaway prototypes, exploratory work where I
do not yet know what I am building, or user interface layout, where visual
feedback matters more than assertions. Even then, I would add tests once the
design stabilizes. TDD is a tool, not a religion, but for core logic I will
keep using it.

## Learning

What surprised me most was how much the tests shaped the design without any
upfront planning; the structure of `Library` emerged from the tests. I was
also surprised by how satisfying the rhythm became after the first few
cycles. Next time I would plan a list of tests before starting, write fewer
overly broad tests, and use parameterized tests earlier, since I only
discovered them midway. I would also record the real pytest failure output as
I go, rather than reconstructing it at the end.
