# Homework 2: Testing Concepts Analysis

**Student**: Pablo Portillo Madera
**GitHub**: [@pabloportillo1](https://github.com/pabloportillo1)
**Course**: Software Testing — Fall 2026 · ITESO
**Module**: 2 — Software Testing Concepts
**Application**: Kadu Care (AI Clinical Records SaaS), with Instagram as a comparison baseline
**Date**: 2026-09-07

## Summary

I analysed **Kadu Care**, the AI-powered clinical records platform I work on, where live consultation
audio is turned into structured SOAP notes by an LLM pipeline and patient vitals are streamed to a
hospital dashboard in real time. My strategy prioritises security, AI output quality, and reliability
above raw throughput, and keeps a licensed clinician as the final acceptance authority — because
every critical failure in this system ends in patient harm or regulatory exposure rather than churn.
Throughout, I use **Instagram** as a contrast reference: it is built from nearly the same technical
parts (web and native clients, media capture, real-time streaming, ML inference, i18n), which makes
it a clean way to show that the same architecture demands a completely different test strategy once
the domain changes.

## Files

| File | Part | Contents |
| --- | --- | --- |
| [part1-application-analysis.md](part1-application-analysis.md) | 1 | Application purpose, users, nine key features, tech stack, and critical functions ranked by failure consequence |
| [part2-testing-types.md](part2-testing-types.md) | 2 | 12 test types with examples, priorities, and justifications |
| [part3-testing-levels.md](part3-testing-levels.md) | 3 | Unit, Integration, System, and Acceptance strategies with tools, coverage goals, and test-count estimates |
| [part4-testing-principles.md](part4-testing-principles.md) | 4 | All seven ISTQB principles applied to this system |
| [part5-risk-analysis.md](part5-risk-analysis.md) | 5 | 17-risk matrix and a 13-step prioritised testing order |

## Key Takeaways

1. **Non-deterministic output breaks classic assertions.** The LLM pipeline cannot be tested with
   assert-equals, so it is evaluated statistically against a curated set of clinician-approved
   reference notes, with hallucination and negation metrics gated in CI.
2. **The test pyramid is deliberately deformed.** Integration and acceptance layers are heavier than
   textbook shape, because the AI pipeline and the EMR consolidation layer only exist as
   integrations, and only a clinician can judge clinical acceptability.
3. **Impact outranks likelihood.** Several low-likelihood risks sit at P0 — a ranking no consumer
   social product would justify, and the clearest evidence that testing is context dependent.
4. **Partial failure must degrade into less automation, never into lost data.** A consultation is
   unrepeatable, so a failed summarization still has to persist the transcript.
