# Reflection — Homework 4

**What was most challenging.** The decision tables. Writing one is easy; making it *consistent* is
not. The example table in the brief marks two actions for the same rule — a frozen account with
insufficient funds — which an API returning a single error can never satisfy. Resolving that meant
stopping and deciding an explicit precedence (state → amount → limit → funds), writing it down as
an assumption, and only then testing it. Roughly half my design time went into the ten
assumptions in section 0 of the design document, and most of them exist because two techniques
disagreed about what should happen.

**What I learned about black box testing.** That the techniques answer different questions about
the same line of code. Equivalence partitioning asks whether a rule exists, boundary value analysis
asks whether its comparison operator is right, decision tables ask which rule wins when several
apply, and state transition testing asks what happens across a sequence of calls. Measuring
coverage per technique made that concrete: individually they reach 60–74% of the implementation,
and only together do they reach 100%. It also taught me not to rank techniques by coverage: BVA
had the lowest of the four and found the most real defects.

**How confident I am in the quality of the system.** Confident about the rules that are written
down, much less so about time and concurrency. Every documented rule has at least one test, all 116
pass in both languages, and coverage is complete. But the daily-limit reset is tested by calling a
hook directly rather than by crossing midnight, and nothing checks two simultaneous transfers
against the same limit. Those are the two places I would expect a real SecureBank to break first,
and neither is reachable with black box unit tests alone.
