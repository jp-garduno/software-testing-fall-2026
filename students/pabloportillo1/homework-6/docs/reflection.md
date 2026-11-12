# TDD Reflection — Homework 6

## Design Impact

The clearest effect was on how objects get what they depend on. The first late fee test needed a book to be
fourteen days overdue, and I was not going to wait two weeks, so `Library` got a `clock` parameter on the
spot. The reservation notifier came in the same way. In homework 5 I added dependency injection afterwards
so I could mock things; here the tests asked for it before the code existed, which felt more natural.

TDD also changed the shape of `borrow_book`. Two tests, "an unavailable book leaves the member unchanged" and
"a member at the limit leaves the copies unchanged", cannot both pass with either order of the two updates.
They forced "check everything, then change anything", a rule I would probably have broken writing the code
first, because the first version looked fine.

## Challenges

Writing the dumbest code that passes was harder than writing good code. `return True` for `is_available()`
felt like cheating until the next test failed for exactly the reason it should, and I understood that the
fake implementation was there to prove the test could fail. The other challenge was choosing the next
test. When the next test is too big, GREEN turns into an hour of coding; when it is too small, the commit
log fills with noise. The dozen small validation commits for `Book` are probably too fine-grained.

I also made real mistakes. Once I wrote a RED test that already passed, because two books sorted the same way
by year and by title. Another time a JavaScript test expected the wrong year order. Without a rule that
every RED must fail, the first one would have slipped in as a test that proves nothing.

## Benefits

The suite runs in about a fifth of a second in Python and half a second in Jest, so I ran it after every
change, almost 300 times in total. Refactoring stopped being risky: when I replaced three `if` branches
in `search` with a table of sort keys, the 69 tests that already passed told me in a moment that nothing had
changed. Coverage was 100% for statements and nearly 100% for branches without my aiming for it. The one
JavaScript branch it missed turned out to be dead code, which was a nicer discovery than a gap.

## Comparison with Test-After

In homework 5 I wrote the code, measured coverage and added tests where the report was red. That finds code
nobody executed, but my mutation check there showed it misses wrong comparisons. With TDD each comparison was
added because a specific test failed without it, so the boundary tests exist from the start. The trade-off
is speed at the beginning: the first hour of TDD produced less code than test-after would have, and it only
caught up once refactoring started.

## Future Use

I would use TDD for business rules with clear inputs and outputs: fees, limits, state changes, validation,
and anything I expect to refactor. I would not use it for exploratory work where I do not yet know what the
API should be, such as a UI prototype, a quick script, or learning a new library, because there the tests
would be rewritten as fast as the code. A middle ground I want to try is a spike to learn, then deleting it
and rebuilding test-first.

## Learning

What surprised me most was how often GREEN went further than the test. In JavaScript, a regular expression and
a `shift()` each solved the next test before I wrote it, so those tests were green on arrival. That is not
wrong, but it means the cycle did not prove those tests could fail. Next time I would keep GREEN even more
literal, and I would group related validations into one parameterised test per rule, so the history shows
behaviours rather than single values. Implementing the system twice also showed that the tests, not the
code, are the real specification: the JavaScript version went much faster because the Python test names
already described every behaviour it needed.
