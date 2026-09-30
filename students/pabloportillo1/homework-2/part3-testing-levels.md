# Part 3: Testing Levels Strategy

**Application**: Kadu Care — AI Clinical Records Platform
**Comparison baseline**: Instagram

A note on shape before the detail. For Instagram, the classic test pyramid holds cleanly: a very
wide unit base, a narrower integration band, and a thin end-to-end tip, because their dominant risk
is *scale*. Kadu Care's dominant risk is *correctness of a small number of irreversible decisions*,
so the pyramid is deliberately deformed: a heavier integration layer (the AI pipeline and the EMR
consolidation layer only exist as integrations), and a genuinely expensive acceptance layer, because
only a licensed clinician can judge whether a generated note is clinically acceptable. No amount of
unit testing can substitute for that judgement.

---

## Unit Testing

**Scope**: Individual pure functions, React components in isolation, and single backend modules,
with every external dependency (database, LLM provider, WebSocket transport) mocked.

**What to Test**:

- **NEWS 2 scoring function** — the highest-value unit in the codebase. It is pure, deterministic,
  has a published clinical specification, and directly drives escalation. Every boundary between
  score bands gets a test.
- **Medication-risk classifier rules** — deterministic rule evaluation for known interaction pairs,
  dosage ceilings, and contraindications.
- **`recorder-core` package internals** — chunking, buffering, and local-persistence logic, tested
  independently of any real microphone.
- **Template engine validation** — required-field enforcement, conditional field visibility, and
  rejection of malformed template definitions.
- **Transcript post-processing helpers** — the deterministic pieces around the model, such as
  entity extraction, unit normalization, and PHI redaction.
- **React components** — vitals cards, alert banners, and note editors, rendered with fixture props.
- **i18n formatters** — locale-aware date, decimal, and unit rendering.

**Tools**: Jest (or Vitest) with TypeScript, React Testing Library for components,
`mongodb-memory-server` for repository-level tests that need a real driver, `msw` for network mocks.

**Coverage Goal**: 80% line coverage overall, enforced in CI. Two areas are held to a stricter bar
of ~95% branch coverage: the NEWS 2 scorer and the medication-risk classifier. Coverage is treated
as a floor and a smell detector, not as a goal in itself — 80% coverage of trivial getters proves
nothing.

**Example Test Cases**:

1. `calculateNews2()` returns the correct score and escalation band for each documented boundary
   value of respiratory rate, oxygen saturation, temperature, and blood pressure — including the
   exact threshold values, one below, and one above.
2. `calculateNews2()` handles a **missing** vital sign by returning an explicit "incomplete" state
   rather than treating the absent value as zero, which would understate deterioration.
3. `classifyMedicationRisk()` flags a known dangerous interaction pair and returns the expected
   severity, and returns no flag for a documented safe pair.
4. `recorderCore.flush()` preserves already-buffered audio chunks when the network handler throws.
5. The template engine rejects signing a note whose required "Allergies" field is empty.
6. The Spanish locale formatter renders `1.5 mg` unambiguously and never as a value that could be
   read as `15 mg`.

**Estimated Number of Tests**: ~350–400 unit tests.

---

## Integration Testing

**Scope**: Two or more real components working together — API routes against a real database, the
AI pipeline against a real (or recorded) model provider, the WebSocket layer end to end, and the
shared `recorder-core` package against both host runtimes.

**What to Test**:

- **The AI SOAP pipeline as a chain**: audio upload → storage → speech-to-text → LLM summarization →
  structured note persisted against the correct patient. Most realistic failures live in the seams
  between these stages, not inside them.
- **REST API + MongoDB**: authorization enforced at the data layer, not just in route handlers.
- **WebSocket vitals streaming**: device ingest → server → subscribed dashboard clients, including
  reconnection and backfill.
- **EMR consolidation layer**: multi-source ingestion, patient matching, and de-duplication.
- **`recorder-core` in both hosts**: the same package version exercised inside the Next.js web app
  and the Expo iOS app.
- **i18n resolution across the client/server boundary**, so server-rendered content matches the
  user's locale.

**Tools**: Jest + Supertest for API integration, Testcontainers or `mongodb-memory-server` for
MongoDB, recorded/stubbed LLM responses via `msw` for deterministic CI plus a nightly job against
the live provider, `ws` client harnesses for WebSocket tests, `pytest` for the model-evaluation
harness described in Part 2.

**Coverage Goal**: 100% of critical user journeys and 100% of authorization boundaries covered by at
least one integration test. Measured by journey checklist rather than line percentage — line
coverage is the wrong instrument at this level.

**Example Test Cases**:

1. Posting a consultation recording for patient X results in a note persisted against patient X and
   *no* write to any other patient document — verified by querying the database directly.
2. When the LLM provider returns a 500, the raw transcript is still persisted, the note is marked
   `summary_failed`, and the API returns a clear error — no clinical data is dropped.
3. A vitals frame published for a patient in Clinic A is delivered only to sockets subscribed by
   Clinic A staff, and never to a Clinic B subscriber on the same server.
4. A dashboard client that disconnects for 30 seconds and reconnects receives the readings from the
   gap, in order, rather than resuming silently from the present moment.
5. Importing the same patient from two upstream EMR sources yields one consolidated record with the
   merged history intact.
6. A nurse-role JWT calling the admin user-management endpoint receives `403`, verified against the
   real route and the real database rather than a mocked guard.

**Estimated Number of Tests**: ~120–150 integration tests, plus a model-evaluation suite of 200
labelled consultations run on every model or prompt change.

---

## System Testing

**Scope**: The fully deployed, integrated system in a staging environment with production-like
configuration, exercised through the real user interfaces — the browser and the iOS app — with no
mocks in the application under test.

**What to Test**:

- Complete clinical workflows end to end, on both the web and iOS clients.
- Non-functional characteristics in a realistic environment: load, latency, WebSocket fan-out, and
  recovery from induced network failure.
- Security testing against the deployed surface, including authorization probing and session
  handling.
- Cross-browser and cross-device compatibility.
- Both locales exercised as full journeys, not just as string checks.

**Tools**: Playwright for web end-to-end (it handles WebSockets, network interception, and
multi-context tests cleanly), Detox or Maestro for the Expo iOS app, `behave` with Playwright for
BDD-style clinical scenarios readable by non-engineers, k6 or JMeter for load and WebSocket
soak tests, OWASP ZAP for an automated security baseline.

**Coverage Goal**: Every P0 and P1 risk from Part 5 has at least one system-level scenario. Roughly
40 automated end-to-end scenarios — deliberately few, because they are slow and brittle, and their
job is to cover journeys rather than to re-cover logic already proven by unit tests.

**Example Test Cases**:

1. **Full consultation journey (web)**: log in → select patient → record a scripted 10-minute
   consultation → generate note → edit the Assessment section → sign → verify the signed note
   appears in the patient's history with the correct author and timestamp.
2. **Full consultation journey (iOS)**: the same flow on the Expo app, confirming the shared
   `recorder-core` package behaves identically on both platforms.
3. **Network-loss recovery**: start a recording, disable the network for 60 seconds mid-consultation,
   restore it, and confirm the complete audio uploads and the note generates with nothing missing.
4. **Deterioration escalation**: feed a simulated vitals stream that crosses the NEWS 2 escalation
   threshold and assert the dashboard raises the alert within the agreed latency budget.
5. **Load soak**: 500 concurrent clinicians and 200 monitored patients for one hour, asserting no
   dropped WebSocket frames and stable p95 latency.
6. **Cross-tenant isolation**: log in as a Clinic A physician and attempt, through the real UI and
   through direct API calls, to reach a Clinic B patient — every path denied.

**Estimated Number of Tests**: ~40 automated end-to-end scenarios, ~15 performance and soak
scenarios, plus a scheduled security scan.

---

## Acceptance Testing

**Scope**: Validation by real users against real clinical needs — does the system solve the problem
it was bought to solve? This level answers the *absence-of-errors fallacy*: a technically flawless
system that clinicians will not adopt has failed.

**What to Test**:

- **Clinical acceptance**: licensed physicians review AI-generated notes for clinical accuracy,
  completeness, and safety. This cannot be automated and is the single most important gate.
- **User Acceptance Testing (UAT)**: pilot clinics run real (consented) consultations in a
  controlled rollout.
- **Business acceptance**: does the measured documentation-time reduction actually approach the 40%
  the product claims?
- **Regulatory and operational acceptance**: audit trails, data-retention behaviour, and consent
  capture reviewed against the obligations for handling PHI.
- **Alpha/beta**: internal dogfooding with synthetic patients, then a limited pilot with partner
  clinics.

**Tools**: Structured clinician review rubric with inter-rater agreement across at least two
reviewers per note; `behave` feature files written in clinical language so domain experts can read
and approve the scenarios themselves; analytics instrumentation for documentation-time measurement;
a formal defect-triage channel for pilot feedback.

**Coverage Goal**: A statistically meaningful sample — at least 100 real consultations per pilot
clinic reviewed by a clinician — with defined exit criteria: zero critical clinical-safety defects
(hallucinated medication, inverted negation, misattributed record), and a documented
clinician-satisfaction threshold before general rollout.

**Example Test Cases**:

1. A physician reviews 20 AI-generated notes from their own consultations and rates each for
   clinical accuracy; any note containing a fabricated or inverted clinical fact is logged as a
   critical defect and blocks release.
2. A nurse confirms the monitoring dashboard surfaces a deteriorating patient early enough to be
   clinically actionable under their ward's escalation protocol.
3. A clinic administrator configures a custom note template for their specialty end to end, without
   engineering assistance.
4. Documentation time per consultation is measured before and after adoption at a pilot clinic and
   compared against the 40% target.
5. A Spanish-speaking physician completes a full consultation entirely in Spanish and judges the
   resulting note clinically usable without reverting to English.
6. An administrator retrieves a complete audit trail for a given patient record — who accessed it,
   who edited it, and when.

**Estimated Number of Tests**: ~100 clinician-reviewed consultations per pilot clinic, ~25 scripted
UAT scenarios, plus continuous feedback capture through the pilot period.

---

## How the Levels Reinforce Each Other

The same clinical risk is deliberately attacked at several levels, at decreasing speed and
increasing realism. Take an incorrect NEWS 2 escalation: the scoring maths is proven at **unit**
level in milliseconds; that the score reaches the dashboard from a real device is proven at
**integration** level; that the alert is raised within its latency budget under realistic load is
proven at **system** level; and that the alert is early enough to be clinically useful is confirmed
by a nurse at **acceptance** level. Each level catches a class of defect the level below it
structurally cannot see, which is the whole argument for maintaining four of them rather than
over-investing in one.
