# Part 5: Risk Analysis & Test Prioritization

**Application**: Kadu Care — AI Clinical Records Platform
**Comparison baseline**: Instagram

## 5.1 Risk Matrix

Priorities below are assigned from the pair (likelihood × impact), with one domain-specific
adjustment: in a clinical system, **impact dominates likelihood**. A rare event that harms a patient
outranks a frequent event that annoys one. This is exactly where the ranking diverges from what the
same matrix would produce for Instagram — the first two rows are low-likelihood risks that still sit
at P0, which no consumer social product would justify.

| **Risk** | **Likelihood** | **Impact** | **Priority** | **Mitigation Strategy** |
| --- | --- | --- | --- | --- |
| AI hallucinates a medication, dosage, or diagnosis not present in the consultation | Medium | Critical | P0 | Traceability check asserting every clinical entity in the note maps to a transcript span; hallucination metrics gated in CI on every prompt/model change; mandatory clinician review before signing |
| AI inverts a negation ("denies chest pain" → "chest pain") | Medium | Critical | P0 | Dedicated negation test set in the evaluation harness; negation-specific recall metric tracked separately and treated as a release blocker |
| Cross-tenant PHI leak — a clinician retrieves another clinic's patient | Low | Critical | P0 | Server-side authorization asserted at the data layer; integration tests on every endpoint for the cross-tenant case; automated OWASP ZAP baseline; penetration test before general rollout |
| A note is attached to the wrong patient | Low | Critical | P0 | End-to-end integration tests verifying the database write target directly; explicit patient re-confirmation in the UI before signing; audit trail on every record write |
| Consultation audio lost due to network failure mid-recording | High | Critical | P0 | Local buffering and persistence in `recorder-core`; resumable upload; system-level network-loss recovery scenario; never discard a transcript because a downstream stage failed |
| Medication-risk classifier misses a dangerous interaction (silent failure) | Medium | Critical | P0 | ~95% branch coverage on classifier rules; unit tests per documented interaction pair; clinician review of the rule set; explicit "unknown pair" state rather than silent pass |
| NEWS 2 score computed incorrectly, delaying escalation | Low | Critical | P0 | Boundary value analysis on every documented band threshold; explicit "incomplete" state for missing vitals; clinician acceptance test on a simulated deterioration case |
| Vitals stream stale or silently disconnected while dashboard appears live | Medium | High | P1 | WebSocket reconnection with gap backfill; visible connection-state and data-freshness indicator in the UI; load and soak tests asserting no dropped frames |
| `recorder-core` regression breaks audio capture on one platform only | Medium | High | P1 | Regression suite executed against both the Next.js web app and the Expo iOS app on every package change; mandatory second reviewer on that package |
| EMR consolidation creates a duplicate patient chart, splitting clinical history | Medium | High | P1 | Integration tests on multi-source patient matching; quarantine malformed upstream records instead of writing partial state; pre/post migration record counts and checksums |
| Performance degradation during morning shift-change peak | Medium | High | P1 | k6/JMeter load tests at 500 concurrent clinicians and 200 monitored patients; p95 latency budget enforced in CI; one-hour soak test |
| Clinicians rubber-stamp AI drafts without reviewing them | Medium | High | P1 | Clear visual distinction between AI-generated and clinician-edited text; usability testing of the review step; production telemetry on edit rates per section |
| Audio capture fails on a specific hospital device or iOS version | Medium | High | P1 | Compatibility matrix across supported iPhone generations and iOS versions; Bluetooth headset connect/disconnect scenarios with fallback to the built-in microphone |
| Spanish-language consultations produce lower-quality notes than English | Medium | High | P1 | Locale-segmented metrics in the evaluation harness; code-switching test cases; Spanish-speaking clinician in the acceptance panel |
| Session left open on a shared ward workstation | High | Medium | P2 | Session timeout and invalidation on logout tested at integration level; automatic lock after inactivity |
| Deterioration alert conveyed by colour alone | Low | Medium | P2 | Accessibility tests asserting text and iconography accompany colour; colour-contrast checks in CI |
| Localized strings missing, clipped, or overflowing | High | Low | P3 | Automated missing-key detection in CI; visual regression checks on both locales |

**Legend** — Likelihood: Low / Medium / High · Impact: Low / Medium / High / Critical ·
Priority: P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low)

## 5.2 Testing Priority Order

Ordered by risk exposure, and shaped so that the fastest and cheapest checks run first — an
expensive clinician review should never be spent discovering a defect a unit test could have caught.

1. **Security and authorization testing** on every endpoint — cross-tenant isolation, role
   enforcement, session handling. Ranked first because it is the only category whose failures are
   *irreversible*: a patched bug is fixed, a leaked medical history is not.
2. **AI output quality evaluation** — hallucination and negation suites against the curated
   evaluation set, gated on every model or prompt change. The product's core differentiator and its
   largest risk surface.
3. **Unit testing of deterministic clinical logic** — NEWS 2 scoring and the medication-risk
   classifier, with boundary value analysis. Highest value per second of runtime in the entire
   strategy: pure functions, published specifications, direct clinical consequences.
4. **Integration testing of the AI pipeline and data layer** — the seams between audio, storage,
   STT, LLM, and persistence, plus correct patient attribution verified against the database.
5. **Reliability and recovery testing** — network loss mid-recording, LLM provider timeout,
   WebSocket reconnection with backfill. Governed by the rule that partial failure must degrade into
   less automation, never into lost clinical data.
6. **Regression suite across both platforms** — the full clinical journey on web and iOS, run on
   every pull request, with particular attention to `recorder-core`.
7. **Real-time and performance testing** — WebSocket fan-out, latency budgets, shift-change load,
   and a one-hour soak.
8. **Data integrity and migration testing** — patient matching, de-duplication, and schema
   migrations verified with counts and checksums.
9. **Compatibility testing** — the browser and device matrix that hospitals actually run.
10. **Usability testing with clinicians** — including the "appropriate distrust" check that the
    review step stays an active decision.
11. **Localization testing** — with the caveat from Part 2 that Spanish AI-output quality is not a
    localization concern at all; it belongs in step 2.
12. **Accessibility testing** — with the deterioration-alert colour dependency treated as a safety
    issue rather than a compliance item.
13. **Clinical acceptance testing** — a licensed clinician reviewing at least 100 real consultations
    per pilot clinic. Last in sequence but the final authority: nothing ships to a hospital without
    it, and it can veto a release that passed every preceding step.

## 5.3 Why this ordering differs from Instagram's

Running the same exercise for Instagram would produce a recognisably different list. Performance and
scalability would rise to the top, because their dominant risk is load and their dominant failure
mode is churn. ML output quality would be measured by engagement rather than by correctness, and
would be validated through live 1% experiments rather than gated pre-release. There would be no
equivalent of step 13 at all — no licensed professional holds veto power over a feed release.

Conversely, Instagram carries risks that barely register for us: coordinated abuse, content
moderation at scale, and viral load spikes. We have roughly two orders of magnitude fewer users and
a fraction of their traffic, but a single wrong sentence in a single note can end a patient's life.
That asymmetry — low volume, extreme per-event consequence — is what justifies every priority
decision above, and it is the clearest illustration of the principle that testing is context
dependent.
