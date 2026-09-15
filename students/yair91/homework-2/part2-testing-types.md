# Part 2: Testing Types Classification

Ten test types are proposed for Aula. Priorities follow the critical functions identified in Part 1: grade integrity, access control, registration under load and payments.

---

## Test Type: Functional Testing

**Category**: Functional

**Purpose**: Verify that each feature behaves according to the academic rules it implements. In Aula the rules are not generic CRUD: prerequisites, credit limits, grade weighting and registration windows are institutional policy expressed in code, and a deviation is not a cosmetic bug but a wrong academic decision.

**Examples**:

1. A student who has not passed Calculus I cannot register for Calculus II, and the rejection message names the missing prerequisite.
2. A final grade is computed as the weighted sum of its assessments and matches a manual calculation to two decimal places.
3. Registering for a course that overlaps an already-enrolled course is rejected with the conflicting time slot shown.

**Priority**: Critical

**Justification**: These rules are the reason the system exists. If prerequisites or grade calculations are wrong, everything built on top of them — transcript, GPA, graduation eligibility — is wrong too.

---

## Test Type: Security Testing

**Category**: Non-Functional

**Purpose**: Confirm that academic and financial data is only reachable by those entitled to it, and that the system resists common attacks. Aula holds grades, personal data and payment records for thousands of people under privacy obligations.

**Examples**:

1. A student requesting `/api/students/{other_id}/grades` receives 403, regardless of a valid session.
2. A professor cannot modify grades for a course they are not assigned to, even by crafting the request directly against the API.
3. Session tokens are invalidated on logout and cannot be replayed afterwards.

**Priority**: Critical

**Justification**: A single authorization defect exposes the records of the whole student body at once. Unlike a normal bug, you cannot fix this one away: the data has already been seen.

---

## Test Type: Performance Testing

**Category**: Non-Functional

**Purpose**: Ensure the system survives the registration window, which is the only moment of the term when load is extreme and concentrated. Traffic is not spread across the day; it arrives in a five-minute spike.

**Examples**:

1. The system sustains 5,000 concurrent students during the first ten minutes of registration with the 95th percentile response time under two seconds.
2. Course search returns results in under one second with the full catalog loaded.
3. Transcript PDF generation completes in under five seconds under normal load and degrades gracefully, not catastrophically, at three times that load.

**Priority**: High

**Justification**: An outage during the registration window is highly visible, affects everyone simultaneously, and cannot be retried later because course capacity is finite. It is the closest thing Aula has to a business-critical event.

---

## Test Type: Regression Testing

**Category**: Functional

**Purpose**: Confirm that changes made between terms do not break rules that already worked. Aula evolves continuously — new payment plans, adjusted grading schemes, catalog changes — and the academic rules it touches are interdependent.

**Examples**:

1. After adding a new scholarship type, existing tuition calculations for students without scholarships remain unchanged.
2. After refactoring the prerequisite engine, all previously validated registration scenarios still produce the same outcome.
3. After a grade-weighting change for one program, final grades in unaffected programs are byte-for-byte identical.

**Priority**: High

**Justification**: The cost of a regression here is asymmetric. Nobody notices when it works, and when it fails it corrupts records that were already correct, which is much harder to detect than a new feature failing outright.

---

## Test Type: Data Integrity Testing

**Category**: Non-Functional

**Purpose**: Verify that stored academic and financial data stays consistent across operations, concurrent access and failures. Aula is a system of record, so a transient inconsistency becomes a permanent wrong answer.

**Examples**:

1. Two students submitting a registration request for the last available seat at the same instant result in exactly one enrollment and one rejection.
2. A payment interrupted mid-transaction leaves either a complete payment record or none, never a charge without a receipt.
3. Recalculating a GPA from raw assessment data reproduces the stored GPA for every historical student record.

**Priority**: Critical

**Justification**: Corrupted records are frequently discovered long after the fact, often by the affected student, and correcting them requires manual administrative work plus an explanation to the person harmed.

---

## Test Type: Usability Testing

**Category**: Non-Functional

**Purpose**: Confirm that users complete their tasks without help. Aula's users are not trained operators; a first-semester student registers for courses roughly twice a year and has no opportunity to build expertise.

**Examples**:

1. A first-time student completes registration for five courses without external assistance in under ten minutes.
2. A professor locates and corrects an already-submitted grade without contacting support.
3. Error messages during registration state the reason and the next action, rather than only that the operation failed.

**Priority**: High

**Justification**: Usability defects convert directly into support tickets for the registrar's office. When thousands of students hit the same confusing screen in the same week, the cost is measured in staff hours.

---

## Test Type: Accessibility Testing

**Category**: Non-Functional

**Purpose**: Verify that students with disabilities can complete every essential task. A university has a legal and ethical obligation to make enrollment, grades and payments reachable by all its students.

**Examples**:

1. The full registration flow can be completed with keyboard only, with a visible focus indicator at every step.
2. A screen reader announces grade tables with correct row and column headers.
3. All text meets WCAG 2.1 AA contrast ratios, and no information is conveyed by color alone — an unpaid balance is not marked only in red.

**Priority**: High

**Justification**: An inaccessible registration screen does not degrade the experience for affected students; it blocks them entirely from an obligatory process, with legal consequences for the institution.

---

## Test Type: Compatibility Testing

**Category**: Non-Functional

**Purpose**: Confirm that Aula works across the browsers, operating systems and devices the student body actually owns, which is a much wider and older range than the development team's machines.

**Examples**:

1. Registration completes successfully on Chrome, Safari and Firefox at their two most recent versions.
2. The mobile application behaves correctly on Android 10 and above and iOS 15 and above.
3. The schedule view remains readable and operable at 360px width without horizontal scrolling.

**Priority**: Medium

**Justification**: Important but bounded. A compatibility defect affects a specific segment rather than everyone, and is usually reported quickly and worked around by switching device.

---

## Test Type: Localization Testing

**Category**: Non-Functional

**Purpose**: Verify that the interface is correct in Spanish and English, including dates, currency and text that expands or contracts on translation.

**Examples**:

1. Tuition amounts display in Mexican pesos with the correct separators and symbol placement in both locales.
2. Dates render as day/month/year in Spanish and month/day/year in English, with no ambiguous cases.
3. Translated labels do not overflow their containers on the narrowest supported screen.

**Priority**: Medium

**Justification**: A mistranslation is embarrassing rather than dangerous, with one exception: an ambiguous date on a payment deadline or an exam can cause a student to miss it, so date and currency formatting deserves more attention than the rest.

---

## Test Type: Exploratory Testing

**Category**: Functional

**Purpose**: Find defects that scripted tests cannot anticipate, by having testers work through realistic academic scenarios without a predefined script. Scripted suites only verify the cases someone already thought of.

**Examples**:

1. A timeboxed session following a student who drops a course, re-enrolls, and then requests a transcript.
2. A session on the boundaries of the registration window: submitting a request in the final second before it closes.
3. A session on an atypical academic path, such as a transfer student with credits validated from another institution.

**Priority**: Medium

**Justification**: It does not replace automated testing, but it consistently uncovers the edge cases that specifications leave undefined — and in an academic system, undefined behavior tends to surface as the strangest support tickets of the term.
