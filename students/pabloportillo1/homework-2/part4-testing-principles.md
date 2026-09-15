# Part 4: Testing Principles Application

**Application**: Kadu Care — AI Clinical Records Platform
**Comparison baseline**: Instagram

---

## 1. Testing Shows Presence of Defects (Not Absence)

**Application to Kadu Care**:
This principle is unusually literal for us, because the AI pipeline is non-deterministic. A green
build proves that the model produced acceptable notes *for the 200 consultations in our evaluation
set*. It says nothing about the 201st, which may contain an accent, a drug name, or a phrasing the
set never covered. We can never demonstrate that the pipeline will not hallucinate — only that it
did not hallucinate on the inputs we tried. Every test result is evidence, never proof.

The same holds for the deterministic parts. Passing NEWS 2 unit tests means our implementation
matches our reading of the specification; it does not prove our reading is correct.

**Impact on Strategy**:

- Treat the clinician's review-and-sign step as a **required safety control**, not as a UI
  convenience. The system is designed around the assumption that the AI is wrong sometimes, so a
  human must always be in the loop before a note becomes part of the record.
- Instrument production: log every clinician edit to an AI-generated note. A section that gets
  heavily rewritten is a defect signal the test suite never produced.
- Maintain a low-friction path for clinicians to flag a bad note, and feed those cases straight into
  the evaluation set.
- Communicate honestly. Never market the pipeline as "accurate"; describe it as a draft requiring
  review — an overstated claim would encourage exactly the rubber-stamping we most need to avoid.

**Instagram contrast**: Instagram absorbs unknown defects through scale and telemetry — ship, watch
dashboards, roll back. We cannot roll back a signed clinical note, so our compensating control is a
human, not a deploy pipeline.

---

## 2. Exhaustive Testing is Impossible

**Application to Kadu Care**:
The input space is unbounded in a way a form-based app's is not. A consultation is arbitrary-length
audio in two languages, spoken by any number of people, with any accent, in any acoustic
environment, about any of thousands of conditions and medications. Enumerating that space is not
merely expensive — it is not a finite set. Even the deterministic parts are large: NEWS 2 takes
several continuous physiological variables, and the medication classifier operates over a
combinatorial space of drug pairs.

**Impact on Strategy**:

- Replace exhaustiveness with **risk-based sampling**, driven by the Part 5 matrix. Test where
  failure is most likely and most costly.
- Apply equivalence partitioning and boundary value analysis to the deterministic units: for NEWS 2
  we test each documented band boundary rather than the whole continuous range.
- Curate the evaluation set for **diversity** rather than volume — accents, both languages,
  code-switching, background noise, long and short consultations, and the specialties our pilot
  clinics actually practice.
- Prioritize the drug interactions that appear in real prescribing data over the long tail of
  theoretically possible pairs.
- Accept explicitly, in writing, which areas are under-tested, so the gap is a known decision rather
  than an unexamined assumption.

**Instagram contrast**: Instagram also cannot test exhaustively, but it can substitute production
experimentation — a 1% rollout is a legitimate test. We cannot run a 1% experiment on patient
safety, so our sampling must be deliberate up front.

---

## 3. Early Testing

**Application to Kadu Care**:
In healthcare, the most expensive defects are requirement defects, not code defects. If we
misunderstand the NEWS 2 specification or the legal requirements for record attribution, no amount
of downstream testing finds it — every layer faithfully implements the wrong thing. That class of
error surfaces during a regulatory review or a clinical incident, which is the worst and most
expensive possible place to find it.

**Impact on Strategy**:

- Review requirements **with clinicians** before implementation. A physician reading the acceptance
  criteria for the medication classifier is the cheapest test we can run.
- Write the acceptance criteria for a feature before writing the feature, in language a clinician
  can validate — this is the practical justification for BDD-style `behave` scenarios.
- Static testing as a first line of defence: TypeScript's type system, ESLint, and code review catch
  whole defect classes before execution, which is exactly the Module 3 material applied here.
- Build the model-evaluation harness *before* tuning prompts, so every prompt change is measured
  from the first iteration rather than judged by impression.
- Shift-left on security: threat-model the PHI data flows at design time, because retrofitting
  authorization onto an existing data model is far more expensive than designing it in.

**Instagram contrast**: A misunderstood requirement at Instagram produces a feature users ignore.
Here it produces a clinically incorrect system that passes all its own tests.

---

## 4. Defect Clustering

**Application to Kadu Care**:
Defects are not uniformly distributed across this codebase, and the clusters are predictable:

1. **The AI pipeline** — the newest code, the most complex, and the only non-deterministic
   component. It also has the most seams: audio → storage → STT → LLM → parser → persistence.
2. **The shared `recorder-core` package** — a single codebase running in two very different
   runtimes (browser and React Native). Platform-specific audio behaviour is a classic defect nest,
   and a bug here breaks two products simultaneously.
3. **The EMR consolidation layer** — multi-source ingestion with inconsistent upstream data quality
   and a schemaless database. Patient-matching logic is where duplicates and merge errors live.
4. **Real-time WebSocket delivery** — reconnection, ordering, and backfill are notoriously
   error-prone, and failures are intermittent and hard to reproduce.

**Impact on Strategy**:

- Concentrate testing effort proportionally to these clusters rather than spreading it evenly.
- Hold the highest branch-coverage bar on the clustered modules; mandate a second reviewer on
  `recorder-core` changes.
- Track defect density per module and let real data update this list — today's clusters are a
  hypothesis, and production evidence should override my intuition.
- Treat any bug found in a cluster as a signal to add tests *around* it, not just a test *for* it,
  since neighbouring code is likely to hide the same class of error.

**Instagram contrast**: Same 80/20 dynamic, different clusters — theirs concentrate in the ranking
algorithm and the media-processing pipeline. The principle transfers; the map does not.

---

## 5. Pesticide Paradox

**Application to Kadu Care**:
This principle bites hardest on the AI evaluation set. If we freeze 200 consultations and tune
prompts against them for six months, we will engineer a pipeline that excels on those 200 recordings
and quietly degrades everywhere else. That is overfitting wearing a test suite's clothes, and it is
especially dangerous because the metric keeps improving while real-world quality falls.

The deterministic suites age in the same way: a regression suite written against last year's clinic
templates stops resembling how clinics use the product today.

**Impact on Strategy**:

- **Rotate and grow the evaluation set continuously**, seeding it with real (de-identified,
  consented) consultations that clinicians flagged as poorly transcribed. Maintain a held-out
  portion that is never used for prompt tuning, only for final evaluation.
- Run periodic **exploratory testing** sessions where a clinician deliberately tries to break the
  pipeline — heavy accents, interruptions, overlapping speakers, deliberately ambiguous phrasing.
- Add a regression test for every production defect, which grows the suite along the axes reality
  chose rather than the axes we imagined.
- Review and prune the regression suite each semester: delete tests that no longer reflect real
  usage, since a stale suite costs time and buys false confidence.
- Vary the load profiles in performance tests rather than replaying one recorded scenario forever.

**Instagram contrast**: Instagram counters the paradox with continuous A/B experimentation on live
traffic. Our substitute is deliberate exploratory testing plus a rotating held-out evaluation set,
because live experimentation on clinical output is not available to us.

---

## 6. Testing is Context Dependent

**Application to Kadu Care**:
This is the principle the whole submission is built to demonstrate, which is why Instagram runs
through it as a baseline. The two systems share an architecture — web plus native mobile clients,
media capture and upload, real-time streaming to the UI, ML inference over user content, and full
internationalization — yet almost every testing decision differs, because the *consequence of
failure* differs.

| Dimension | Instagram | Kadu Care |
| --- | --- | --- |
| Dominant risk | Scale, engagement, churn | Patient harm, regulatory exposure |
| Cost of a wrong ML output | A boring recommendation | A wrong clinical decision |
| Recovery from a failed capture | Retry from the gallery | The consultation is gone forever |
| Test pyramid shape | Classic wide-base pyramid | Heavier integration and acceptance layers |
| Release strategy | Continuous, 1% experiments | Staged pilots with clinician sign-off |
| Acceptance authority | Product metrics | A licensed clinician |
| Privacy failure | Serious privacy incident | Regulatory event, life-altering for the patient |

**Impact on Strategy**:

- Adopt a safety-critical mindset: no clinical decision path is fully automated without human
  review.
- Weight security, reliability, and AI-output quality above raw throughput — the opposite of a
  social network's ordering.
- Make a licensed clinician, not an engagement dashboard, the final acceptance authority.
- Resist importing "best practices" wholesale from consumer tech. Ship-fast-and-iterate is correct
  for a feed; applied unchanged to a medication-risk classifier it is negligent.

**Instagram contrast**: This entire principle *is* the contrast — same building blocks, different
context, therefore a different strategy.

---

## 7. Absence-of-Errors Fallacy

**Application to Kadu Care**:
We could build a system with zero defects that nobody uses. If the AI produces technically accurate
notes that do not match how a physician actually documents, or if reviewing the draft takes longer
than typing the note from scratch, the product has failed completely — while every test passes. The
value proposition is a *time saving*; a bug-free system that saves no time solves no problem.

There is a subtler version specific to this product. If the interface makes the AI draft look
authoritative and finished, clinicians will stop reading it carefully. The software would be working
exactly as specified while actively causing harm, because the specification was wrong about human
behaviour.

**Impact on Strategy**:

- Measure the outcome, not just correctness: track real documentation time before and after
  adoption, and treat a shortfall against the 40% target as a defect in the product even if no test
  fails.
- Include usability and clinical-workflow fit in the acceptance criteria, with clinician
  satisfaction as a release gate alongside defect counts.
- Test for **appropriate distrust**: verify that the UI visually distinguishes AI-generated text
  from clinician-reviewed text, so review remains an active step rather than a reflex.
- Validate the problem, not just the solution — keep talking to pilot clinics about whether
  documentation time is genuinely their bottleneck.
- Remember that a passing pipeline is a necessary condition for shipping, never a sufficient one.

**Instagram contrast**: Instagram's version of this fallacy is a flawless app nobody opens. Ours is
a flawless app that clinicians abandon after a week — or worse, one they trust more than they
should.
