# Part 1: Application Selection & Analysis

**Option chosen**: Option A — an existing application I use regularly.

**Application under analysis**: **Kadu Care** — an AI-powered clinical records SaaS platform.

**Comparison baseline used throughout this homework**: **Instagram**.

## Why two applications appear in this document

The analysis in Parts 2–5 targets **one** application: Kadu Care. Instagram appears only as a
*contrast reference*. The two products are built from almost identical technical parts — a web
client and a native mobile client, media capture and upload, a real-time stream pushed to the UI,
machine-learning inference over user content, and full internationalization — but the cost of a
failure is not remotely comparable.

If Instagram drops a story upload, the user retries and is mildly annoyed. If Kadu Care drops a
vitals reading, or writes a hallucinated medication dosage into a patient's chart, a clinician can
make a decision on wrong data and a patient can be harmed. Holding the architecture roughly
constant and changing only the domain makes the ISTQB principle *"testing is context dependent"*
concrete rather than abstract, and it is the reason my priorities in Part 2 and my risk ranking in
Part 5 look nothing like what the same feature list would produce for a social network.

## Application: Kadu Care — AI Clinical Records Platform

### Purpose

Kadu Care replaces manual clinical documentation. During a live consultation the platform captures
the conversation audio, runs it through a speech-to-text and LLM summarization pipeline, and
produces a structured **SOAP note** (Subjective, Objective, Assessment, Plan) that the physician
reviews, edits, and signs into the patient record. Alongside documentation, the platform runs a
hospital monitoring dashboard that streams patient vitals in real time, computes NEWS 2 early-warning
deterioration scores, and flags medication risk. The product goal is to give clinicians back the
time they currently spend typing — measured at up to 40% less documentation time — without
degrading the accuracy or the legal integrity of the medical record.

### Target Users

- **Physicians / specialists** — the primary users. They run consultations, review and sign the
  AI-generated SOAP notes, and are legally accountable for what the record says.
- **Nurses and hospital monitoring staff** — consume the real-time vitals dashboard and act on
  NEWS 2 deterioration alerts.
- **Clinic and hospital administrators** — manage users, roles, templates, and organization-level
  configuration.
- **Patients** — indirect users. They never log in, but their protected health information (PHI)
  is the data the whole system handles, which makes them the party that carries the risk.

### Key Features

1. **Authentication and role-based access control** — physician, nurse, and administrator roles,
   each with a different slice of patient data.
2. **Patient record management and EMR data-consolidation layer** — normalizes and stores clinical
   records coming from multiple upstream sources.
3. **AI SOAP-note pipeline** — live consultation audio → speech-to-text → LLM summarization →
   structured, clinician-editable note. This is the product's core differentiator.
4. **Customizable form and template engine** — each clinic defines its own note structures and
   required fields.
5. **Real-time hospital monitoring dashboard** — patient vitals streamed over WebSockets with
   low-latency updates.
6. **NEWS 2 deterioration scoring** — a standardized clinical early-warning score computed from
   the incoming vitals.
7. **Clinical medication-risk classifier** — flags dangerous drug combinations and dosages.
8. **Cross-platform audio capture** — a shared, platform-agnostic `recorder-core` npm package
   powering both the Next.js web app and the React Native / Expo iOS app.
9. **Full EN/ES internationalization** — including clinical terminology, not just UI chrome.

### Technology Stack

- **Frontend (web)**: TypeScript, React, Next.js, Tailwind CSS, shadcn/ui
- **Frontend (mobile)**: React Native / Expo (iOS)
- **Shared**: private-scope npm package `recorder-core` for audio capture
- **Backend**: Node.js, REST APIs, WebSockets for real-time streaming
- **Database**: MongoDB
- **AI layer**: LLM speech-to-text and summarization pipeline
- **Infrastructure**: Vercel, Google Cloud
- **i18n**: next-i18next

### Critical Functions

Ranked by what happens when they fail:

1. **Clinical accuracy of the AI SOAP note** — a hallucinated symptom, dosage, or negation
   ("no chest pain" transcribed as "chest pain") that a rushed clinician signs off becomes part of
   a legal medical record and can drive a wrong treatment decision.
2. **Authentication, authorization, and PHI confidentiality** — a doctor from Clinic A must never
   retrieve a patient from Clinic B. A breach here is a regulatory and legal event, not a bug.
3. **Real-time vitals delivery and NEWS 2 scoring** — a stale, dropped, or misattributed reading
   means a deteriorating patient is not escalated in time.
4. **Medication-risk classifier correctness** — a missed interaction warning is a silent failure
   nobody notices until harm occurs.
5. **Audio capture reliability** — a consultation is unrepeatable. If the recorder fails mid-visit,
   that clinical encounter is lost and cannot be re-created.
6. **Record integrity and attribution** — every note must be traceable to the correct patient, the
   correct author, and the correct timestamp.

### Contrast with the baseline

Instagram's equivalent critical functions are the feed, upload, and messaging paths, and their
failure mode is churn: users leave. Every Kadu Care critical function above has a failure mode that
ends in *patient harm* or *regulatory exposure*. That difference is what drives the priorities,
levels, and risk rankings in the rest of this submission.
