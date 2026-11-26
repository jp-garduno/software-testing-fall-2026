# Part 2: Testing Types Classification

**Application**: Kadu Care — AI Clinical Records Platform
**Comparison baseline**: Instagram

Each type below closes with a short *Instagram contrast* line. The point is not to test Instagram —
it is to show that the same test type earns a completely different priority once the domain changes.

---

## Test Type: Functional Testing

**Category**: Functional

**Purpose**: Verify that every feature behaves according to its clinical specification. A physician
must be able to run a consultation, generate a SOAP note, correct it, and sign it into the patient
record without the system losing, reordering, or misattributing any of that data.

**Examples**:

1. Recording a consultation produces a SOAP note whose four sections (Subjective, Objective,
   Assessment, Plan) are all populated and attached to the patient the clinician selected.
2. Editing the Assessment section and signing the note persists the *edited* text, not the original
   AI draft, and stores both versions for audit.
3. A clinic-specific template with a required "Allergies" field blocks signing until that field is
   completed.

**Priority**: Critical

**Justification**: These are the core workflows. If a note attaches to the wrong patient or an edit
silently reverts, the product is not merely broken — it is actively dangerous and legally
indefensible.

**Instagram contrast**: Also critical there, but a failed post is retried in five seconds. Here the
consultation cannot be replayed.

---

## Test Type: Security Testing

**Category**: Non-Functional

**Purpose**: Protect protected health information (PHI). Kadu Care stores identifiable medical data,
which places it under strict regulatory obligations. Access control must be enforced server-side on
every request, not just hidden in the UI.

**Examples**:

1. A physician from Clinic A calls the patient-record API directly with a patient ID belonging to
   Clinic B and receives `403`, not the record (broken object-level authorization).
2. A nurse-role token cannot reach administrator-only endpoints such as user management, even by
   crafting the request manually.
3. Consultation audio and transcripts are encrypted at rest and in transit, and audio URLs are not
   guessable or publicly reachable without a signed, expiring token.
4. Session tokens expire and are invalidated on logout, so a shared hospital workstation does not
   leak the previous clinician's session.

**Priority**: Critical

**Justification**: A single authorization flaw exposes medical histories. The damage is
irreversible — unlike a bug, a leak cannot be patched retroactively — and carries regulatory and
legal consequences well beyond the product itself.

**Instagram contrast**: A leaked private story is a serious privacy incident; a leaked psychiatric
history is a life-altering one. Same test type, higher stakes.

---

## Test Type: AI Output Quality Testing (Model Evaluation)

**Category**: Non-Functional

**Purpose**: The LLM transcription and summarization pipeline is **non-deterministic** — the same
audio can produce different text on two runs. Classic assert-equals testing does not apply. This
type verifies output quality statistically, against a curated gold-standard dataset of consultation
recordings with clinician-approved reference notes.

**Examples**:

1. Against a fixed evaluation set of 200 labelled consultations, clinical-entity recall (symptoms,
   medications, dosages, allergies) stays above an agreed threshold, and any regression between
   model versions fails the build.
2. **Negation handling**: audio containing "the patient denies chest pain" never yields a note
   asserting chest pain. Inverting a negation is the highest-severity failure this pipeline has.
3. **Hallucination check**: no medication, dosage, or diagnosis appears in the generated note that
   is not traceable to a span in the transcript.
4. Spanish-language consultations achieve comparable entity recall to English ones, so the quality
   bar does not silently drop for half the user base.

**Priority**: Critical

**Justification**: This is the product's core differentiator and its largest risk surface. A
plausible-sounding hallucination is worse than a crash: a crash is visible and stops the workflow,
while a fluent wrong sentence gets signed by a busy clinician and becomes the official record.

**Instagram contrast**: Instagram's ML — feed ranking, recommendations, alt-text generation — is
tuned for engagement, and a bad prediction shows a boring reel. There is no engagement metric that
justifies an incorrect dosage.

---

## Test Type: Performance Testing

**Category**: Non-Functional

**Purpose**: Confirm the system stays responsive under realistic hospital load, particularly the
WebSocket fan-out for the monitoring dashboard and the latency of the transcription pipeline.

**Examples**:

1. A ward dashboard subscribed to 200 concurrent patients renders new vitals within 2 seconds of
   the device reading, sustained over a full shift.
2. SOAP-note generation for a 15-minute consultation completes within an agreed ceiling (e.g. 90
   seconds), so the clinician is not left waiting between patients.
3. The system holds 500 concurrent clinicians during a morning shift-change spike without WebSocket
   disconnections or dropped vitals frames.
4. Long consultations (60+ minutes of audio) do not exhaust memory in the `recorder-core` package
   on a mid-range iPhone.

**Priority**: High

**Justification**: Latency here is a clinical safety property, not a comfort metric — a vitals
dashboard that lags by 30 seconds is worse than no dashboard, because staff trust it and act on it.

**Instagram contrast**: Instagram's scale is orders of magnitude larger, but its latency budget is
about retention. Ours is about escalation time on a deteriorating patient.

---

## Test Type: Reliability and Recovery Testing

**Category**: Non-Functional

**Purpose**: Verify graceful behaviour when the network, device, or backend fails mid-operation.
Hospital Wi-Fi is genuinely unreliable, and a consultation is a one-shot, unrepeatable event.

**Examples**:

1. Wi-Fi drops at minute 8 of a 20-minute recording: audio continues buffering locally, and the
   full recording uploads once connectivity returns — nothing is lost.
2. The iOS app is backgrounded by an incoming phone call mid-recording and resumes capture without
   truncating the audio.
3. The WebSocket connection to the vitals stream drops and reconnects automatically, backfilling
   the readings missed during the gap rather than silently resuming from "now".
4. If the LLM provider times out, the raw transcript is still saved and the clinician is told the
   summary failed — the encounter data is never discarded because a downstream step failed.

**Priority**: Critical

**Justification**: Point 4 is the design rule that matters most: partial failure must degrade into
*less automation*, never into *lost clinical data*.

**Instagram contrast**: A failed upload can simply be retried from the gallery, because the source
photo still exists on the phone. Our source event — the consultation — is gone forever.

---

## Test Type: Regression Testing

**Category**: Functional

**Purpose**: Ensure that shipping fast in an early-stage startup does not quietly break clinical
workflows that were already working, especially across the shared `recorder-core` package used by
both the web and iOS clients.

**Examples**:

1. An automated suite covering login, patient selection, record, generate, edit, and sign runs on
   every pull request.
2. A change to `recorder-core` triggers the regression suite on **both** the Next.js web app and
   the Expo iOS app, since one package version serves two very different runtimes.
3. Template-engine changes are replayed against a library of existing clinic templates to prove
   previously valid templates still render and still validate.

**Priority**: Critical

**Justification**: A shared cross-platform package is a natural defect cluster: one changed line
can break two products at once, and the second breakage is usually discovered by a user rather than
by the developer.

**Instagram contrast**: Same mechanism, and Instagram invests heavily here too — but their
regression escape gets hotfixed in hours with an apology, not with an incident report to a hospital.

---

## Test Type: Usability Testing

**Category**: Non-Functional

**Purpose**: Validate that clinicians can complete documentation faster *with* Kadu Care than
without it. The product's entire value proposition is a time saving, so a confusing interface does
not just annoy users — it deletes the reason to buy.

**Examples**:

1. Timed task: a physician completes a full consultation-to-signed-note flow measurably faster than
   their current manual process, with the delta recorded.
2. The AI-generated draft is visually distinguishable from clinician-edited text, so nobody signs a
   machine draft believing they already reviewed it.
3. Correcting a wrong AI sentence takes a small, bounded number of interactions rather than
   requiring the clinician to retype the section.

**Priority**: High

**Justification**: Directly tied to adoption and to the 40% documentation-time claim. It also has a
safety dimension: an interface that makes review feel optional encourages rubber-stamping.

**Instagram contrast**: Instagram optimizes usability for time *spent*. We optimize for time
*saved*. Opposite directions, same discipline.

---

## Test Type: Compatibility Testing

**Category**: Non-Functional

**Purpose**: Hospitals run whatever hardware they bought years ago. Verify the web app works on the
browsers actually deployed on ward workstations, and that audio capture works across real iOS
devices, OS versions, and microphone configurations.

**Examples**:

1. The monitoring dashboard renders and streams correctly on the last two major versions of Chrome,
   Safari, Edge, and Firefox.
2. Audio capture works on iPhone models spanning several generations and on the current and previous
   major iOS versions.
3. Recording behaves correctly with a Bluetooth headset connected, and when the headset disconnects
   mid-consultation the capture falls back to the built-in microphone instead of stopping.

**Priority**: High

**Justification**: A clinician cannot choose different hardware. If capture fails on the hospital's
standard device, the product is simply unusable at that site, regardless of how good the AI is.

**Instagram contrast**: Instagram can degrade gracefully on old devices and still be usable. Our
audio path either works on the device in the room or the feature does not exist for that customer.

---

## Test Type: Localization and Internationalization Testing

**Category**: Non-Functional

**Purpose**: Kadu Care ships full EN/ES support. Beyond translated UI strings, this covers clinical
terminology, date and number formats, and — critically — the AI pipeline's behaviour on Spanish
audio and on code-switched consultations.

**Examples**:

1. Every user-facing string resolves in both locales, with no missing keys and no raw keys leaking
   into the UI.
2. Dates, decimal separators, and units render per locale, so `1,5` and `1.5` never mean different
   doses to different users.
3. A consultation conducted mostly in Spanish with English drug names produces a correct note
   rather than mistranscribing the drug names.
4. Longer Spanish translations do not overflow or clip clinical labels in the dashboard.

**Priority**: Medium

**Justification**: Medium as an aggregate, but example 3 is genuinely Critical — it belongs to the
AI-quality suite. Pure string-level localization is lower risk because failures are visible and
cosmetic.

**Instagram contrast**: Instagram supports far more locales, but a clipped label is cosmetic there.
An ambiguous decimal separator on a dosage field is not cosmetic here.

---

## Test Type: Accessibility Testing

**Category**: Non-Functional

**Purpose**: Ensure the interface is operable by clinicians with visual impairments or colour-vision
deficiency, and that alerts never depend on colour alone.

**Examples**:

1. NEWS 2 severity is conveyed by text and iconography as well as colour, so a red/green
   colour-blind nurse reads the same urgency as everyone else.
2. The full consultation flow is completable by keyboard, since ward workstations are often used
   without a reliable mouse.
3. Screen-reader labels are present and meaningful on vitals values and alert banners.

**Priority**: Medium

**Justification**: Medium by user volume, but example 1 is a safety issue rather than a compliance
checkbox — a deterioration alert that only a colour-sighted user can interpret is a broken alert.

**Instagram contrast**: Comparable technical work; here it intersects directly with clinical
escalation.

---

## Test Type: Smoke Testing

**Category**: Functional

**Purpose**: A fast build-verification gate that answers one question before anyone spends time on
deeper testing: is this build fundamentally alive?

**Examples**:

1. The application boots, a user can log in, and the patient list loads.
2. A short scripted audio sample flows end to end and returns a non-empty note.
3. The WebSocket vitals channel connects and receives at least one frame.

**Priority**: High

**Justification**: Cheap and fast. Its value is protecting reviewer and QA time, and catching
catastrophic breakage before it reaches a staging environment clinicians are demoing on.

**Instagram contrast**: Identical practice — smoke testing is context-independent by design.

---

## Test Type: Data Integrity and Migration Testing

**Category**: Functional

**Purpose**: The EMR consolidation layer ingests records from multiple upstream systems into
MongoDB. Because the schema is flexible, integrity has to be enforced and verified explicitly
rather than assumed from the database.

**Examples**:

1. Importing the same patient from two upstream sources produces one merged record, not a duplicate
   chart that splits the clinical history in half.
2. A schema migration preserves every historical note, its author, its signature, and its
   timestamp, verified by record counts and checksums before and after.
3. Records with missing or malformed upstream fields are quarantined and reported rather than
   written into the database in a partial state.

**Priority**: High

**Justification**: Silent data corruption is the hardest failure class to detect and the most
expensive to reverse. A split patient chart means a clinician reads half a history and believes it
is the whole one.

**Instagram contrast**: A duplicated Instagram account is a support ticket. A duplicated patient
chart is a missed allergy.
