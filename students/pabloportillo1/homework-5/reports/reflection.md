# Reflection — Homework 5

**What was most challenging about achieving high coverage?** Not the percentage itself. Reaching
98% was mostly mechanical once the database and the notification gateways were injected and could
be mocked. The hard part was the realisation that followed: `task.py` was at 100% after the first
round of unit tests, yet a mutation check showed that six small bugs in it would have gone
unnoticed. Deciding which of the remaining tests were worth writing, when the coverage report no
longer pointed anywhere, took more thought than everything before it.

**How does white box testing differ from black box testing?** In homework 4 I designed tests from
the specification without looking at the code, and the techniques (partitions, boundaries, decision
tables) told me which inputs mattered. Here the code itself told me where to look: every `if` needs
both outcomes, every `except` needs a failure to trigger it, and a compound condition hides cases
that branch coverage does not count. White box testing is good at finding code nobody exercised;
black box testing is better at choosing the values that break it. The edge case file in this
homework is really black box thinking applied after a white box measurement.

**Will I use code coverage in future projects?** Yes, branch coverage specifically, as a CI check
with a threshold, because it reliably finds forgotten error paths. I will not treat it as the
definition of done. A green report means every line ran; it says nothing about whether the
assertions would catch a wrong comparison, so I will pair it with boundary tests and the occasional
mutation check.
