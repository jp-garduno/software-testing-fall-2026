# Part 1: Application Selection and Analysis

## Application: Aula — Student Management System

**Option B**: hypothetical application.

### Purpose

Aula is a student management system for a mid-sized university. It is the single place where the academic life of a student is recorded: enrollment, schedules, attendance, grades, transcripts and tuition. Students use it to register for courses, follow their schedule, submit assignments and pay tuition. Professors use it to publish materials, record attendance and capture grades. The registrar's office manages the course catalog, opens and closes registration windows, validates prerequisites and issues official transcripts. The finance office reconciles tuition payments and scholarships.

Aula is not a learning platform in the sense of hosting video lectures or interactive content. It is a system of record. Its value comes from being right and being up, not from being pleasant to use. A wrong grade in a transcript or a registration window that goes down for two hours during peak enrollment causes real damage to real people, and that damage is expensive to undo.

### Target Users

- **Students**: register for courses, check schedules and grades, submit assignments, pay tuition. The largest group by volume and the least predictable in behavior.
- **Professors**: manage course rosters, record attendance, enter and adjust grades, publish materials.
- **Registrar staff**: build the catalog each term, define prerequisites and capacity, open registration windows, resolve conflicts, issue transcripts.
- **Finance staff**: track tuition charges, payments, scholarships and refunds.
- **Administrators**: manage roles and permissions, audit access, produce institutional reports.
- **Integration consumers**: the institutional identity provider, the payment gateway, and the reporting warehouse.

Users vary widely in technical skill, device, connection quality and accessibility needs. A first-semester student on an old Android phone over mobile data is as much a target user as an administrator on a desktop.

### Key Features

1. **Authentication and role-based access control** through institutional single sign-on, with distinct permissions for students, professors, registrar, finance and administrators.
2. **Course catalog and registration**, including capacity limits, prerequisite validation, schedule-conflict detection, waitlists and time-boxed registration windows.
3. **Grade management**: professors capture grades per assessment, the system computes final grades according to each course's weighting scheme, and the registrar publishes them.
4. **Transcript generation**: official academic history, GPA calculation and PDF export.
5. **Tuition billing and payments**: charge generation, payment through an external gateway, scholarship and discount application, receipts and payment plans.
6. **Attendance tracking**, with per-session records and automatic alerts when a student passes an absence threshold.
7. **Assignment submission**, with deadlines, file upload and late-submission rules.
8. **Notifications** by email and push for deadlines, grade publication, payment reminders and registration openings.
9. **Administrative reporting**: enrollment by program, pass rates, payment status, with CSV and PDF export.

### Technology Stack

- **Web frontend**: React with TypeScript, consumed on desktop and mobile browsers.
- **Mobile**: React Native application for students, focused on schedule, grades and payments.
- **Backend**: NestJS REST API, organized by bounded context (enrollment, academics, finance, identity).
- **Database**: PostgreSQL as the system of record, with Redis for sessions and job queues.
- **Storage**: object storage for submitted files and generated PDF documents.
- **Integrations**: institutional SSO through SAML, an external payment gateway, and a nightly export to the reporting warehouse.

### Critical Functions

Not everything in Aula carries the same weight. Four areas are mission-critical:

1. **Grade accuracy and transcript integrity.** A transcript is a legal document. An incorrect GPA or a grade attributed to the wrong student can cost a scholarship or a job offer, and errors may surface months later.
2. **Access control.** A student must never see another student's grades, and a professor must never edit a course they do not teach. This is both a privacy obligation and a matter of institutional trust.
3. **Course registration under load.** Registration opens at a fixed hour and thousands of students hit the system in the same few minutes. Capacity limits must be enforced exactly: two students cannot take the last seat in a course.
4. **Payment processing.** Charging twice, charging the wrong amount, or losing the record of a completed payment all create financial disputes and block a student's registration for the following term.

Everything else — notifications, reporting, how pretty the catalog looks — still matters, but a bug there is annoying, not a crisis. That split is what drives the priorities in the rest of this analysis.
