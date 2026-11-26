# Part 4: Testing Principles Application

The seven principles applied to Aula. Each one is stated, applied to this system, and translated into a concrete decision in the strategy.

---

## 1. Testing Shows Presence of Defects (Not Absence)

**Application to Aula**:
A green suite only means the bugs we thought of are not there. It says nothing about the transfer student whose credits were validated in a different format, or the professor who edits a grade during the exact minute the registrar publishes it. Aula processes thousands of academic paths and no suite enumerates them all.

**Impact on Strategy**:

- Coverage is treated as a floor, never as evidence of correctness. Passing tests are not accepted as an argument that a release is safe.
- Production monitoring on the invariants that must always hold: enrollments never exceeding capacity, GPAs recomputable from raw data, payments always matched to a receipt.
- A visible reporting channel for students and professors, on the assumption that they will find defects we did not.

---

## 2. Exhaustive Testing is Impossible

**Application to Aula**:
Course registration alone combines student, academic history, catalog, prerequisites, capacity, schedule and the moment of the request. The full combination is astronomically large and only a fraction of it is reachable in practice.

**Impact on Strategy**:

- Equivalence partitioning and boundary value analysis in place of enumeration: for credit limits we test the minimum, the maximum, one below, one above, and one typical value.
- Risk-based allocation of effort, following the matrix in Part 5, rather than uniform coverage of every screen.
- 100% branch coverage demanded only in the calculation modules, where the input space is small enough for the goal to be meaningful.

---

## 3. Early Testing

**Application to Aula**:
The most expensive defects in an academic system are specification defects. A misunderstood grade-rounding rule discovered after transcripts are issued means reissuing official documents; the same misunderstanding caught while reading the regulation costs a conversation.

**Impact on Strategy**:

- Institutional regulations reviewed with the registrar's office before implementation, with ambiguities written down as questions rather than assumed.
- Acceptance criteria in Gherkin agreed before development starts, so the specification is executable from day one.
- Static analysis and unit tests running on every commit; integration and end-to-end suites on every pull request.

---

## 4. Defect Clustering

**Application to Aula**:
Defects will not distribute evenly. They will concentrate where logic is dense and changes are frequent: the prerequisite engine, tuition calculation with scholarships and discounts, and concurrency around the last available seat. The catalog listing screen will be comparatively quiet.

**Impact on Strategy**:

- Defect density tracked per module, and testing effort redirected toward the modules that report the most.
- The three dense modules receive mandatory code review plus mutation testing, not only line coverage.
- After each term, the incidents reported by the registrar's office are analyzed to confirm or correct where the clusters actually are.

---

## 5. Pesticide Paradox

**Application to Aula**:
The regression suite for registration will stop finding defects once it has found the ones it was designed to find. Running it every term afterwards gives confidence that costs nothing and proves nothing new.

**Impact on Strategy**:

- The suite is reviewed each term: cases that have never failed and cover stable code are candidates for removal or consolidation.
- Every production defect becomes a new test case, so the suite grows from real evidence rather than from imagination.
- Exploratory sessions with rotating charters and rotating testers, precisely because they are not repeatable.
- Mutation testing on the calculation modules to measure whether the tests actually detect changes, rather than merely executing the lines.

---

## 6. Testing is Context Dependent

**Application to Aula**:
This is not a social network, where a display defect is a bad afternoon. It is a system of record whose output is a legal document, operating under privacy obligations, with one extreme load peak per term and a user base that cannot be trained.

**Impact on Strategy**:

- Grades and payments receive the treatment usually reserved for financial software: high branch coverage, mandatory review, immutable audit trail.
- Notifications and reporting receive proportionate treatment: functional coverage without the same depth.
- Accessibility is a release blocker rather than a nice-to-have, because the institution has a legal obligation and enrollment is mandatory.
- Load testing is scheduled against the academic calendar, not against a generic notion of peak traffic.

---

## 7. Absence-of-Errors Fallacy

**Application to Aula**:
A system with zero known defects that requires three attempts to register for a course, or whose error messages do not explain what to do next, has failed even though every test passes. Being correct is not the same as being good.

**Impact on Strategy**:

- Usability testing with real students on their own devices, treated as a first-class activity rather than a final check.
- Acceptance validated by the registrar's office and by student volunteers, not only by the development team.
- Support-ticket volume per flow tracked as a quality metric alongside defect count: a flow that is technically correct and generates hundreds of tickets is a defect in the specification.
- A beta pilot with one faculty for a full term before institution-wide rollout, because some problems only appear at real scale with real people.
