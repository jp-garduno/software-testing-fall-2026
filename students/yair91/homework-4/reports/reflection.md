# Reflection — Homework 4

## What was most challenging

Writing the decision tables, and not for the reason I expected. Filling DT1 was
easy until I got to the rules where several conditions fail at once. If an
account is frozen, short of funds and over the daily limit, the customer sees
exactly one error message, and the brief never says which. I had already written
the code by then, so it had an order, but the order was an accident rather than
a decision. Going back and making it explicit — state, then amount, then limit,
then funds, with a reason for each step — was the part that took longest and the
part I actually learned from.

## What I learned about black box testing

That coverage and risk are not the same thing, and measuring one tells you very
little about the other. I ran each technique on its own against the source:
equivalence partitioning reached 76% by itself, boundary value analysis only
47%. But BVA is the technique holding the tests that would catch a `<=` written
where `<` belongs, which is the most likely defect in a system made of
thresholds. If I had optimised for the coverage number I would have deleted the
most valuable tests in the suite.

## How confident I am

Confident about the rules that are written down, much less about the ones that
are not. All 87 tests pass and every line runs, but nothing here proves the
daily limit actually resets at midnight, or that the monthly fee fires on the
1st, because the system has no clock. I tested what the code does. Whether the
code does it at the right moment is still an open question.
